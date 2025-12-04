# Victoriametrics storage, compare to Prometheus

Source:

- <https://victoriametrics.com/blog/tsdb-performance-techniques-strings-interning/>
- <https://victoriametrics.com/blog/vmstorage-retention-merging-deduplication/>
- <https://github.com/VictoriaMetrics/VictoriaMetrics/issues/3268>
- <https://docs.google.com/presentation/d/13kZ3W4CMz5WOuziNMGJ8okzPU6OHisqD4_pKXIcF5Z8/edit?slide=id.geadb6e000c_0_1134#slide=id.geadb6e000c_0_1134>
- <https://valyala.medium.com/wal-usage-looks-broken-in-modern-time-series-databases-b62a627ab704>
- <https://valyala.medium.com/mmap-in-go-considered-harmful-d92a25cb161d>
- <https://faun.pub/victoriametrics-achieving-better-compression-for-time-series-data-than-gorilla-317bc1f95932>

VictoriaMetrics follows a few important principles in its design:

- Log Structured Merge (LSM) data structure - LSMs are data structures that take into account the storage medium they are implemented on. They can help prevent write amplification, which could easily saturate even the fastest storage mediums.
- Column-oriented storage - Storing each column of your data separately allows you to sort and compress your data separately, both of which enable optimizations that aren’t available with row-oriented storage.
- Append-only writes - In general, the data that TSDBs store has already happened in time, and it’s likely that it will never change. For example, the weather forecast is unlikely to be updated in the past. This principle allows you to use data structures that are append-only. Append-only data structures trade flexibility for extra write speed.

### 1. Victoriametrics columnar storage

VictoriaMetrics stores time-series data in a column-oriented layout, where key components are separated into independent, compressed streams. This is similar in principle to Parquet/ORC, but optimized for time-series (append-only, fixed schema).

- The data are organized into blocks. Each block contains many rows (up to 8,192 rows) of the same TSID.

![](https://victoriametrics.com/blog/vmstorage-how-it-handles-data-ingestion/tsid-rows-to-lsm-part.webp)

- Within a partition, you’ll find in-memory parts, small parts, and big parts. All of them are stored the same way: in a columnar format. That means Victoriamertrics doesn’t store a block in a single record. Instead, the value, the timestamp, and the TSID are split into different files.

![](https://victoriametrics.com/blog/vmstorage-how-it-handles-data-ingestion/vmstorage-inmemory-part-structure.webp)

- Specifically, each cell of `values.bin` and `timestamps.bin` represents data for one block, and each block contains many rows of the same TSID. It turns out each block has a header that describes the block, including the `TSID` of the block, how many rows are in the block, and the boundary of the block in `values.bin` and `timestamps.bin`. These headers are stored in `index.bin`. One row in `index.bin` corresponds to many blocks.

![](https://victoriametrics.com/blog/vmstorage-how-it-handles-data-ingestion/vmstorage-file-block-header.webp)

- But again, how do we know the boundary of each row (array of blocks) in `index.bin`? This is where `metaindex.bin` comes in. It contains information about how many blocks are in each row of `index.bin`, the offset of each row in `index.bin`, and the TSID of the first block in each row. When vmstorage opens a part, it only loads the `metaindex.bin` into memory and then uses it to find the correct metrics it needs.

Prometheus, by contrast, stores data in per-chunk row groups inside per-2h blocks, not globally columnar. Labels and samples are tied to each block and chunk file rather than globally managed.

## 2. No WAL

Write-ahead logging (WAL) is a common practice among modern time series databases — Prometheus uses WAL, InfluxDB uses WAL, TimescaleDB transiently uses WAL from PostgreSQL, Cassandra also uses WAL.

OS doesn't write data to persistent storage on every write syscall. The data is just written into page cache residing in RAM unless direct IO is used. So data successfully written into WAL file may disappear on power loss. How to deal with this? Either to use cumbersome direct IO or to explicitly tell the OS to flush recently written data from page cache to persistent storage via fsync syscall. But fsync has a major downside — it is very slow on SSD (1K-10K rps) and extremely slooow on HDD (100 rps). For instance, 1M inserts per second may be easily slowed down to 100 inserts per second with fsync-after-each-inserted-row strategy. To deal with that, Prometheus calls fsync only after big chunk of data (aka segment) is written into WAL, so all the segment data may be lost / corrupted on power loss before fsync. The data may be corrupted if the OS flushes a few pages with the written data to disk, but doesn't flush the remaining pages. Prometheus fscync's segments every 2 hours by default, so a lot of data may be corrupted on hardware reset.

Victoriametrics chooses the different approach - [SSTable](https://stackoverflow.com/questions/2576012/what-is-an-sstable). The idea is simple — just buffer data in memory and atomically flush it into SSTable-like data structure on disk without the need of WAL. The flush may be triggered either by timeout (i.e. every N seconds) or by reaching the maximum buffer size. This gives similar data safety guarantees as the "optimized WAL usage" described in the previous chapter — recently inserted data may be lost on power loss / process crash.

## 3. Efficiency

- Better compression: Columnar formats store one type of data per stream, enabling compression that is highly optimized for that specific data type.
- Queries scan only the columns they need:
  - Prometheus often need only Label/metric index, Timestamps, Value. But Prometheus’ row-group-in-chunk structure often forces decompression of:
    - Entire chunks even if only some values are needed
    - Index files per block
  - VictoriaMetrics can selectively load only:
    - Index columns to find series
    - Timestamps+values for relevant series only
- Columnar + [global indexing](https://docs.victoriametrics.com/victoriametrics/?utm_source=chatgpt.com#indexdb) eliminates block-level duplication
  - Prometheus stores:
    - Index tables in each 2-hour block
    - Posting lists repeated many times
    - Label-value mapping per block
  - VictoriaMetrics stores:
    - One global index
    - One dictionary for labels
    - One postings set per label-value
  - This only works efficiently because columnar layout allows global compression and merge operations.

| Benefit                 | How Columnar Format Enables It                      |
| ----------------------- | --------------------------------------------------- |
| Much better compression | Homogeneous streams → optimized encoding            |
| Faster lookups          | Global postings + direct column offset reading      |
| Lower CPU               | No repeated index decoding, fewer decompress cycles |
| Lower disk              | No repeated symbol tables or block metadata         |
| Lower RAM               | mmap-based column pages, selective column loading   |
| Faster merges           | Segment-by-segment LSM merging                      |
