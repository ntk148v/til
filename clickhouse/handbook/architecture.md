# Archiecture

Source:

- <https://clickhouse.com/docs/academic_overview>
- <https://blog.dataengineerthings.org/i-spent-8-hours-learning-the-clickhouse-mergetree-table-engine-511093777daa>
- <https://www.alibabacloud.com/blog/clickhouse-kernel-analysis-storage-structure-and-query-acceleration-of-mergetree_597727>

## 1. Architecture

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_0.141fdff.2048.png)

ClickHouse is split into 3 main layers:

- The **query processing layer** follows the traditional paradigm of parsing incoming queries, building and optimizing logical and physical query plans, and execution.
- The **storage layer** consists of different table engines that encapsulate the format and location of table data. Table engines fall into 3 categories:
  - The MergeTree family: based on the idea of LSM trees.
  - Special-purpose table engines which are used to speed up or distribute query execution. For example, in-memory key-value table engines called dictionaries; pure in-memory engine used for temporary tables and Distributed table engine for transparent data sharding.
  - Virtual table engines is used for bidirectional data exchange with external systems such as relational databases, publish/subscribe systems, or key/value stores.
- The integration layer.

ClickHouse supports sharding and replication of tables across multiple cluster nodes for scalability and availability.

- Sharding partitions a table into a set of table shards according to a sharding expression.
  - The main purpose: to process data sets which exceed the capacity of individual nodes. And distribute the read-write load for a table over multiple nodes.
  - The individual shards are mutually independent tables and typically located on different nodes.
  - Clients can read/write shards directly, or use Distributed special table engine.
- Table can be replicated across multiple nodes. To that end, each Merge-Tree table engine has a corresponding ReplicatedMergeTree engine which uses a multi-master coordination scheme based on Raft consensus to guarantee that every shard has, at all times, a configurable number of replicas.

## 2. Storage layer

### 2.1. On-disk format

Each table in the MergeTree table engine is organized as a collection of immutable table **parts**.

- A part is created whenever a set of rows is inserted into the table.
- A background merge job periodically combines multiple smaller parts into a larger part until a configurable part size is reached (150GB by default).
- The source parts are marked as inactive and eventually deleted as soon as their reference count drops to zero, i.e. no further queries read from them.
- Rows can be inserted in two modes:
  - In synchronous insert mode, each INSERT statement creates a new part and appends it to the table -> should insert tuples in bulk (e.g. 20,000 rows at once)
  - In asynchronous insert mode, ClickHouse buffers rows from multiple incoming INSERTs into the same table and creates a new part only after the buffer size exceeds a configurable threshold or a timeout expires.

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_5.8af62c4.2048.png)

Note that, ClickHouse treats all parts as equal instead of arranging them in a hierarchy. It also writes inserts directly to disk while other LSM-treebased stores typically use WAL.

A part corresponds to a directory on disk, with one file per column (small parts can pack all columns into a single file for better locality).

- Rows in a part are grouped into fixed-size **granules** (8192 rows by default) - that's the smallest unit the scan/index operators reason about.
- Physical I/O happens in **blocks** which combine multiple granules within a column, not per granule: a block is ~1MB of adjacent granules from a single column, and the number of granules per block varies by data type and distribution.
- Blocks are compressed on disk (LZ4 by default).
- Blocks are decompressed on the fly when they are loaded from disk into memory, and ClickHouse keeps, for each column, a mapping from granule id to:
  - the offset of its compressed block in the column file.
  - the offset of the granule inside the uncompressed block, which enables fast random access to specific granules despite compression.
- Tables can be range, hash, or round-robin partitioned using arbitrary partition expressions.

### 2.2. Data pruning

> Skip the majority of rows during searches and therefore speed up queries significantly.

#### 2.2.1. Primary key index

The primary key columns determine the sort order of the rows within each part, i.e. the index is locally clustered. ClickHouse additionally stores, for every part, a mapping from the primary key column values of each granule's first row to the granule's id, i.e. the index is sparse. Granules that match the range predicate in the query can be found by binary searching the primary key index instead of scanning EventTime sequentially.

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_3_Figure_7.2d47cac.2048.png)

#### 2.2.2. Table projections

Projections allow to speed up queries that filter on columns different than the main table's primary key at the cost of an increased overhead for inserts, merges, an space consumption.

- By default, projections are populated lazily only from parts newly inserted into the main table.
- The query optimizer chooses between reading from the main table or a projection based on estimated I/O costs.

#### 2.2.3. Skipping indices

Skipping indices are lightweight metadata structures that helps ClickHouse skip whole chunks of data (multiple granules) that definitely cannot match your query.

- Granularity: They work on groups of granules called an index block. For each block, the index stores a small summary of the indexed expression (e.g. min/max, a small set of values, or a Bloom filter).
- How they speed things up:
  - When you run a query with a WHERE condition that matches the index expression, ClickHouse checks the skipping index first.
  - If the metadata shows the block cannot possibly contain matches, that whole block is skipped without reading it from disk.
- Trade-off vs. projections:
  - Skipping indices are much cheaper in storage and write overhead, but they don't serve queries directly.
  - Projections are heavier but can actually serve the query from their own layout.

### 2.3. Merge-time data transformation

ClickHouse allows a continuous incremental transformation of existing data using different merge strategies. If necessary, all merge-time transformations can be applied at query time by specifying the keyword FINAL in SELECT statements.

- **Replacing merges** retains only the most recently inserted version of a tuple based on the creation timestamp of its containing part, older versions are deleted. Tuples are considered equivalent if they have the same primary key column values
- **Aggregating merges** collapse rows with equal primary key column values into an aggregated row. Non-primary key columns must be of partial aggregation state that holds the summary values. Aggregating merges are typically used in materialized views instead of normal tables. Materialized views are populated based on a transformation query against a source table.

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_4_Figure_6.61f6fda.2048.png)

- **TTL merges** provide aging for historical data. Unlike deleting and aggregating merges, TTL merges process only one part at a time. TTL merges are defined in terms of rules with triggers and actions. A trigger is an expression computing a timestamp for every row, which is compared against the time at which the TTL merge runs. While this allows users to control actions at row granularity, we found it sufficient to check whether all rows satisfy a given condition and run the action on the entire part. Possible actions include 1. move the part to another volume (e.g. cheaper and slower storage), 2. re-compress the part (e.g. with a more heavy-weight codec), 3. delete the part, and 4. roll-up, i.e. aggregate the rows using a grouping key and aggregate functions.

### 2.4. Updates and deletes

**Mutations** rewrite all parts of a table in-place.

- This operation is non-atomic, i.e. parallel SELECT statements may read mutated and non-mutated parts.
- Mutations guarantee that the data is physically changed at the end of the operation. Delete mutations are still expensive as they rewrite all columns in all parts.

**Lightweight delete** only update the internal bitmap column, indicating if a row is deleted or not.

- ClickHouse amends SELECT queries with an additional filter on the bitmap column to exclude deleted rows from the result.
- Deleted rows are physically removed only by regular merges at an unspecified time in future. Depending on the column count, lightweight deletes can be much faster than mutations, at the cost of slower SELECTs.

### 2.5. Idempotent inserts

A problem that frequently occurs in practice is how clients should handle connection timeouts after sending data to the server for insertion into a table. In this situation, it is difficult for clients to distinguish between whether the data was successfully inserted or not. ClickHouse solves it by maintaining hashes of the N last inserted parts (in Keeper) and ignores re-inserts of parts with a known hash.

### 2.6. Data replication

In ClickHouse, replication is based of the notion of table states which consist of a set of table parts and table metadata.

Nodes advance the state of table using 3 operations (are performed locally on a single node and recorded as a sequence of state transition in a global replication log):

- Inserts add a new part to the state.
- Merges add a new part and delete existing parts to/from the state.
- Mutations and DDL statements add parts, and/or delete parts, and/or change table metadata, depending on the concrete operation.

Initially empty replicated table:

- Node 1 first receives 2 inset statements and records them (1 2) in the replication log.
- Node 2 replays the first log entry by fetching it (3) and download the new part from Node 1 (4), whereas Node 3 replay both logs entries (3 4 5 6).
- Node 3 merges both parts to a new part, deletes the input parts and records a merge entry in the replication log (7).

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_5_Figure_8.074743d.2048.png)

Three optimizations to speed up synchronization exist:

- New nodes added to the cluster do replay the replication log from scratch.
- Merges are replayed by repeating them locally or by fetching the result part from the another node.
- Nodes replay mutually independent replication log entries in parallel.

### 2.7. ACID compliance

Source: <https://clickhouse.com/docs/guides/developer/transactional>

ClickHouse is generally not considered a fully ACID-compliant database in the traditional sense of OLTP systems like PostgreSQL or MySQL. It prioritizes high-speed analytical performance (OLAP) over strict transactional guarantees.

- **Atomicity**: inserts into a single table are atomic for single-partition/single-block. This means either an entire batch of rows is written, or none are.
- **Consistency**: ClickHouse offers eventual consistency by default. While data is eventually merged and made consistent, updates and deletes (mutations) are asynchronous and may not be immediately visible to all queries.
- **Isolation**: It uses MVCC (Multi-Version Concurrency Control) with snapshot isolation internally. However, because many operations are asynchronous, true isolation for complex, concurrent read-write workloads is limited.
- **Durability**: a successful INSERT is written to the filesystem before answering to the client, on a single replica or multiple replicas (controlled by the `insert_quorum` setting), and ClickHouse can ask the OS to sync the filesystem data on the storage media (controlled by the `fsync_after_insert setting`).

## 3. Query processing layer

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_6_Figure_0.0d157e1.2048.png)

## Gotchas

### ClickHouse writes

In synchronous insert mode, each INSERT statement creates a new part and appends it to the table. It means ClickHouse writes data directly to the file system for every INSERT operation (unless using specific buffering settings), whereas standard LSM-tree stores (like RocksDB, Cassandra, or HBase) write to an in-memory MemTable and a sequential WAL (Write-Ahead Log) first.

If you insert data into ClickHouse frequently in small chunks (e.g., 1 row at a time), performance degrades catastrophically. Here is the technical breakdown of why:

1. The "Too Many Parts" problem (Read & Write Amplification)

- How it works: In ClickHouse, every INSERT creates a new directory containing data files (a "Part").
- The Problem: If you send 1,000 individual inserts per second, ClickHouse creates 1,000 folders and files on your disk every second.
- The Impact: The background merger (compaction process) cannot keep up. It has to merge these thousands of small files into larger ones. This causes massive Write Amplification (data is rewritten to disk multiple times) and chokes the CPU and Disk I/O. Eventually, ClickHouse will throw a [Too many parts](https://www.tinybird.co/docs/sql-reference/clickhouse-errors/TOO_MANY_PARTS) error and reject writes to protect itself.

2. Random I/O vs. Sequential I/1. first

- Standard LSM: Writes go to a WAL (append-only file). This is a purely sequential operation, which is extremely fast on both HDDs and SSDs.
- ClickHouse: Creating a new "Part" involves creating a directory, creating multiple files (one for each column + indexes), and writing metadata. This involves significantly more file system inode operations and random I/O overhead than simply appending to a single log file.

3. Read Latency Degradation
   The Impact: Queries in LSM trees must check all "Parts" (SSTables) to find data. If you have thousands of small unmerged parts, a SELECT query has to open and read from thousands of files simultaneously. This destroys query latency.

**How ClickHouse handles this**: Basically, the client must essentially build the "MemTable" yourself on its side (or use buffering layer).

- _To minimize the overhead of merges, database clients are encouraged to insert tuples in bulk, e.g. 20,000 rows at once_.
- ClickHouse buffers rows from multiple incoming INSERTs into the same table and creates a new part only after the buffer size exceeds a configurable threshold or a timeout expires. This is _async insert_, basically now we have a pseudo-MemTable.

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_5.8af62c4.2048.png)

ClickHouse buffers (Async Inserts or Buffer Engine) act exactly like an LSM "MemTable" (in-memory storage), but without the WAL (Write-Ahead Log). This means if the server pulls the plug (crash, power loss, OOM kill) while data is in that buffer, that data is gone forever.

We don't talk about [Buffer Engine](https://clickhouse.com/docs/engines/table-engines/special/buffer), because it is the legacy and not recommended. Let's just talk about how [async insert handle this](https://clickhouse.com/docs/optimize/asynchronous-inserts). There is a `wait_for_async_insert` settings.

- When set to 1 (the default), ClickHouse only acknowledges the insert after the data is successfully flushed to disk. This ensures strong durability guarantees and makes error handling straightforward: if something goes wrong during the flush, the error is returned to the client. This mode is recommended for most production scenarios, especially when insert failures must be tracked reliably -> _The client has to handle the retry logic_.
- Setting `wait_for_async_insert = 0` enables "fire-and-forget" mode. Here, the server acknowledges the insert as soon as the data is buffered, without waiting for it to reach storage.

**Why does ClickHouse do this?**

Sheer speed. Writing a WAL requires a sequential disk write (fsync) for every batch. Even though sequential writes are fast, they are strictly slower than writing to RAM. ClickHouse is designed for analytics where ingesting 100 million rows/sec is sometimes more important than losing the last 0.5 seconds of data during a catastrophic crash.
