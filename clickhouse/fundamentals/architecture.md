# Architecture

Sources:

- <https://clickhouse.com/docs/academic_overview>
- <https://posthog.com/blog/clickhouse-vs-elasticsearch>
- <https://blog.dataengineerthings.org/i-spent-8-hours-learning-the-clickhouse-mergetree-table-engine-511093777daa>
- <https://www.alibabacloud.com/blog/clickhouse-kernel-analysis-storage-structure-and-query-acceleration-of-mergetree_597727>

Table of contents:

- [Architecture](#architecture)
  - [1. Overview](#1-overview)
  - [2. Three key components](#2-three-key-components)
  - [3. Architecture layers](#3-architecture-layers)
  - [4. Storage layer](#4-storage-layer)
    - [4.1. On-disk format](#41-on-disk-format)
    - [4.2. Data pruning](#42-data-pruning)
    - [4.3. Merge-time data transformation](#43-merge-time-data-transformation)
    - [4.4. Updates and deletes](#44-updates-and-deletes)
    - [4.5. Idempotent inserts](#45-idempotent-inserts)
    - [4.6. Data replication](#46-data-replication)
    - [4.7. ACID compliance](#47-acid-compliance)
  - [5. Query processing layer](#5-query-processing-layer)
  - [6. Gotchas](#6-gotchas)

## 1. Overview

ClickHouse is engineered to process data in a massive, consolidated place. Unlike some databases, ClickHouse's optimizations don't happen through distributing data, but by efficiently pre-processing it in anticipation of queries.

ClickHouse is split into 3 main layers:

- **Query processing layer**: Parses incoming queries, builds and optimizes logical and physical query plans, and executes them
- **Storage layer**: Different table engines that encapsulate the format and location of table data
- **Integration layer**: Connects to external systems

![Architecture](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_0.141fdff.2048.png)

## 2. Three key components

Three major components enable ClickHouse to return aggregations in milliseconds over petabytes of data:

### 2.1. Columnar layout

ClickHouse's columnar layout flips rows and columns in storage relative to MySQL databases. When databases physically access data, they scan row-by-row. By extension, if calculating the average value of bank account balances in PostgreSQL, you would need to access every bank account row.

In ClickHouse, the same analyst would only need to access one (physical) row of data - the bank balance column - and collapse it into an average. ClickHouse stores data in an inverted arrangement optimized for merging attribute data into single values.

### 2.2. Materialized views

Materialized views in ClickHouse are truly dynamic. ClickHouse accomplishes this through the columnar layout and incremental data structures that merge data strategically. Unlike MySQL or PostgreSQL where materialized views go out-of-date when new data is added, ClickHouse keeps them updated incrementally.

### 2.3. Specialized engines

ClickHouse has specialized engines that enable developers to take advantage of multiple CPUs in parallel on the same machine:

- `SummingMergeTree` - for summing data
- `ReplacingMergeTree` - for removing duplicates

This has resemblance to Elasticsearch's parallelization across multiple machines, but ClickHouse does it at a more granular, per-machine level.

## 3. Architecture layers

### Storage layer components

Table engines fall into 3 categories:

1. **MergeTree family**: Based on the idea of LSM trees. All MergeTree engines share the same physical layer (data parts, marks, indexes) but differ in how they merge parts.
2. **Special-purpose engines**: Used to speed up or distribute query execution
   - Dictionaries: in-memory key-value tables
   - Temporary tables: pure in-memory engine
   - Distributed table engine: for transparent data sharding
3. **Virtual table engines**: Bidirectional data exchange with external systems (relational databases, pub/sub, key/value stores)

### Sharding and replication

ClickHouse supports sharding and replication of tables across multiple cluster nodes for scalability and availability.

**Sharding:**

- Partitions a table into shards according to a sharding expression
- Purpose: process datasets exceeding single-node capacity, distribute read-write load
- Individual shards are mutually independent tables on different nodes
- Clients can read/write shards directly or use Distributed table engine

**Replication:**

- Each MergeTree engine has a corresponding ReplicatedMergeTree engine
- Uses multi-master coordination scheme based on Raft consensus
- Guarantees configurable number of replicas per shard

## 4. Storage layer

### 4.1. On-disk format

Each table in the MergeTree family is organized as a collection of immutable table **parts**.

- A part is created whenever a set of rows is inserted into the table
- Background merge job periodically combines smaller parts into larger parts (until ~150GB by default)
- Source parts are marked inactive and deleted when reference count drops to zero

**Insert modes:**

- **Synchronous insert mode**: Each INSERT creates a new part → insert in bulk (e.g., 20,000 rows at once)
- **Asynchronous insert mode**: ClickHouse buffers rows from multiple INSERTs, creates new part only after buffer exceeds threshold or timeout expires

![Parts](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_5.8af62c4.2048.png)

**Important:** ClickHouse treats all parts as equal (no hierarchy) and writes inserts directly to disk (no WAL like other LSM-tree stores).

#### Part structure

A part corresponds to a directory on disk:

- One file per column (small parts can pack all columns into single file)
- Rows grouped into fixed-size **granules** (8192 rows by default) - smallest unit scan/index operators reason about
- Physical I/O happens in **blocks** (~1MB of adjacent granules from single column)
- Blocks are compressed on disk (LZ4 by default)

For each column, ClickHouse keeps a mapping from granule id to:

- Offset of compressed block in column file
- Offset of granule inside uncompressed block (enables fast random access)

### 4.2. Data pruning

> Skip the majority of rows during searches and speed up queries significantly.

#### 4.2.1. Primary key index

Primary key columns determine sort order within each part (locally clustered). ClickHouse stores, for every part, a mapping from primary key values of each granule's first row to granule id (sparse index).

Granules matching range predicates can be found by binary searching instead of sequential scanning.

![Primary Index](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_3_Figure_7.2d47cac.2048.png)

#### 4.2.2. Table projections

Projections allow speeding up queries that filter on columns different than the main table's primary key.

- By default, projections are populated lazily from newly inserted parts
- Query optimizer chooses between main table or projection based on estimated I/O costs
- Cost: increased overhead for inserts, merges, and space consumption

#### 4.2.3. Skipping indices

Lightweight metadata structures that help skip whole chunks of data.

- Work on groups of granules called index blocks
- For each block, stores small summary (min/max, small set of values, Bloom filter)
- When WHERE condition matches index expression, ClickHouse checks skipping index first
- Much cheaper in storage/write overhead than projections, but don't serve queries directly

### 4.3. Merge-time data transformation

ClickHouse allows continuous incremental transformation of existing data using different merge strategies.

**Replacing merges:**

- Retains only most recently inserted version of a tuple
- Older versions are deleted
- Tuples considered equivalent if same primary key column values

**Aggregating merges:**

- Collapse rows with equal primary key into aggregated row
- Non-primary key columns must be partial aggregation states
- Typically used in materialized views

![Merge Transformations](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_4_Figure_6.61f6fda.2048.png)

**TTL merges:**

- Provide aging for historical data
- Process one part at a time
- Actions include: move to another volume, re-compress, delete, roll-up (aggregate)

All merge-time transformations can be applied at query time with `FINAL` keyword.

### 4.4. Updates and deletes

**Mutations** rewrite all parts of a table in-place:

- Non-atomic: parallel SELECTs may read mutated and non-mutated parts
- Expensive: delete mutations rewrite all columns in all parts

**Lightweight delete:**

- Only updates internal bitmap column indicating deleted rows
- SELECT queries amended with filter on bitmap
- Deleted rows physically removed by regular merges later
- Faster than mutations, but slower SELECTs

### 4.5. Idempotent inserts

Problem: Clients can't distinguish between successful insert and connection timeout.

**Solution:** ClickHouse maintains hashes of N last inserted parts (in Keeper) and ignores re-inserts of parts with known hash.

### 4.6. Data replication

Replication is based on notion of table states (set of parts and metadata).

Nodes advance table state using 3 operations (performed locally, recorded as state transitions in replication log):

1. **Inserts**: add new part to state
2. **Merges**: add new part, delete existing parts
3. **Mutations/DDL**: add/delete parts, change metadata

![Replication](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_5_Figure_8.074743d.2048.png)

**Optimizations:**

- New nodes replay replication log from scratch
- Merges can be replayed locally or by fetching result from another node
- Mutually independent log entries replayed in parallel

### 4.7. ACID compliance

ClickHouse is generally not fully ACID-compliant (prioritizes OLAP performance over OLTP transactional guarantees).

| Property | ClickHouse Support |
|----------|-------------------|
| **Atomicity** | Inserts into single table are atomic for single-partition/single-block |
| **Consistency** | Eventual consistency by default; updates/deletes are asynchronous |
| **Isolation** | Uses MVCC with snapshot isolation internally; limited for complex concurrent workloads |
| **Durability** | Successful INSERT written to filesystem before responding; controlled by `insert_quorum` and `fsync_after_insert` |

## 5. Query processing layer

![Query Processing](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_6_Figure_0.0d157e1.2048.png)

ClickHouse parallelizes queries at data elements, data chunks, and table parts levels.

**Vertical parallelization:**

- Multiple data elements processed within operators using SIMD instructions
- Query plan unfolded into multiple lanes (typically one per core)
- Each lane processes disjoint range of table data
- Performance scales vertically with number of cores

![Parallel Execution](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_7_Figure_1.204b48a.2048.png)

**Horizontal parallelization:**

- If table split into shards, multiple nodes scan simultaneously
- Scales horizontally by adding nodes, vertically by adding cores

**Concurrency control:**

- Memory usage limits
- I/O scheduling
- Query isolation into workload classes
- Limits on shared resources (CPU, DRAM, disk, network)

## 6. Gotchas

### ClickHouse writes

In synchronous insert mode, each INSERT creates a new part. ClickHouse writes data directly to filesystem for every INSERT (unless using buffering settings), whereas standard LSM-tree stores write to MemTable and WAL first.

**Problem with small inserts:**

1. **"Too Many Parts" problem** - Each INSERT creates new directory with data files. 1,000 individual inserts/second = 1,000 folders/files/second. Background merger can't keep up.

2. **Random I/O vs Sequential I/O** - Creating new "Part" involves directory creation, multiple files (one per column + indexes), metadata. More overhead than appending to single log file.

3. **Read Latency Degradation** - Queries must check all parts. Thousands of small parts = thousands of files to open simultaneously.

**How ClickHouse handles this:**

- Client must buffer inserts (e.g., 20,000 rows at once)
- Use async insert mode for pseudo-MemTable behavior
- Buffer Engine (legacy, not recommended)

**Async insert durability:**

- `wait_for_async_insert = 1` (default): Acknowledges only after data flushed to disk. Recommended for production.
- `wait_for_async_insert = 0`: "Fire-and-forget" mode. Acknowledges as soon as data buffered. Data lost if crash before flush.

**Why no WAL?**

Sheer speed. Writing WAL requires sequential disk write (fsync) for every batch. ClickHouse is designed for analytics where ingesting 100 million rows/sec is more important than potentially losing last 0.5 seconds of data during catastrophic crash.
