# Archiecture

Source:

- <https://clickhouse.com/docs/academic_overview>
- <https://blog.dataengineerthings.org/i-spent-8-hours-learning-the-clickhouse-mergetree-table-engine-511093777daa>

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
