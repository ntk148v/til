# Data storage

Source: <https://posthog.com/handbook/engineering/clickhouse/data-storage>

## 1. MergeTree

```sql
CREATE TABLE sensor_values (
    timestamp DateTime,
    site_id UInt32,
    event VARCHAR,
    uuid UUID,
    metric_value Int32
)
ENGINE = MergeTree()
ORDER BY (site_id, toStartOfDay(timestamp), event, uuid)
SETTINGS index_granularity = 8192;

INSERT INTO sensor_values
SELECT *
FROM generateRandom('timestamp DateTime, site_id UInt8, event VARCHAR, uuid UUID, metric_value Int32', NULL, 10)
LIMIT 200000000;
```

- Every INSERT creates a new directory containing data files - `part`. If you send 1,000 individual inserts per second, ClickHouse creates 1,000 folders and files on your disk every second. As having a lot of small files would be disadvantageous for many reasons from query performance to storage, ClickHouse regularly **merges** small parts together until they reach a maximum size. That's what the Merge stand for.
  - Data would be stored in **parts**, each part a separate directory on disk. Data for a given part is always sorted by the order set in `ORDER BY` statement and compressed.
  - Parts can be `Wide` or `Compact` depending on its size.
  - Merges can be monitored using the `system.merges` table.
  - `system.parts` table contain a lot of metadata about every part.

![](https://clickhouse.com/docs/assets/ideal-img/_vldb2024_2_Figure_5.8af62c4.2048.png)

- ClickHouse stores a sparse index for the part. A collection of rows with size equal to the `index_granularity` setting (8,192 by default) is called a **granule**. For every granule, the primary index stores a mark containing the value of the `ORDER BY` statement as well as a pointer to where that mark is located in each data file.
  - Check [primary indexes docs](https://clickhouse.com/docs/primary-indexes).

- Look at part data.

```sql
SELECT
    name,
    part_type,
    rows,
    marks,
    formatReadableSize(bytes_on_disk),
    formatReadableSize(data_compressed_bytes),
    formatReadableSize(data_uncompressed_bytes),
    formatReadableSize(marks_bytes),
    path
FROM system.parts
WHERE active and table = 'sensor_values'
FORMAT Vertical;

Row 1:
──────
name:                     all_1_186_3
part_type:                Wide
rows:                     198969780 -- 198.97 million
marks:                    24290
formatReadab⋯es_on_disk): 5.30 GiB
formatReadab⋯ssed_bytes): 5.30 GiB
formatReadab⋯ssed_bytes): 7.60 GiB
formatReadab⋯arks_bytes): 373.17 KiB
path:                     /var/lib/clickhouse/store/953/9535a226-b720-4ede-a3c0-8c460e3b3cac/all_1_186_3/

Row 2:
──────
name:                     all_187_187_0
part_type:                Wide
rows:                     1030220 -- 1.03 million
marks:                    127
formatReadab⋯es_on_disk): 28.44 MiB
formatReadab⋯ssed_bytes): 28.43 MiB
formatReadab⋯ssed_bytes): 40.28 MiB
formatReadab⋯arks_bytes): 2.41 KiB
path:                     /var/lib/clickhouse/store/953/9535a226-b720-4ede-a3c0-8c460e3b3cac/all_187_187_0/

2 rows in set. Elapsed: 0.003 sec.
```

- Inspect data on disk.
  - For every column, `{column_name}.bin` file, contains the compressed (LZ4 compression by default) data for that column.
  - For every column, `{column_name}.cmrk2` file, contains an index with data to locate each granule in `{column_name}.bin` file.
  - `primary.cidx` contains information on ORDER BY column values for each granule. This is loaded into memory during queries.
  - `checksums.txt, columns.txt, default_compression_codec.txt and count.txt` contain metadata about this part.
  - Note, the `c` in file extension stands for compression. Checkout [issue](https://github.com/ClickHouse/ClickHouse/issues/34437).
  - [ClickHouse index design](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#clickhouse-index-design).

```shell
ls -la /var/lib/clickhouse/store/953/9535a226-b720-4ede-a3c0-8c460e3b3cac/all_187_187_0/
total 29196
drwxr-x--- 2 clickhouse clickhouse     4096 Feb 13 02:42 .
drwxr-x--- 5 clickhouse clickhouse    12288 Feb 13 02:52 ..
-rw-r----- 1 clickhouse clickhouse      721 Feb 13 02:42 checksums.txt
-rw-r----- 1 clickhouse clickhouse      277 Feb 13 02:42 columns_substreams.txt
-rw-r----- 1 clickhouse clickhouse      123 Feb 13 02:42 columns.txt
-rw-r----- 1 clickhouse clickhouse        7 Feb 13 02:42 count.txt
-rw-r----- 1 clickhouse clickhouse       15 Feb 13 02:42 default_compression_codec.txt
-rw-r----- 1 clickhouse clickhouse  4281345 Feb 13 02:42 event.bin
-rw-r----- 1 clickhouse clickhouse      513 Feb 13 02:42 event.cmrk2
-rw-r----- 1 clickhouse clickhouse   792761 Feb 13 02:42 event.size.bin
-rw-r----- 1 clickhouse clickhouse      356 Feb 13 02:42 event.size.cmrk2
-rw-r----- 1 clickhouse clickhouse        1 Feb 13 02:42 metadata_version.txt
-rw-r----- 1 clickhouse clickhouse  4123085 Feb 13 02:42 metric_value.bin
-rw-r----- 1 clickhouse clickhouse      420 Feb 13 02:42 metric_value.cmrk2
-rw-r----- 1 clickhouse clickhouse     3592 Feb 13 02:42 primary.cidx
-rw-r----- 1 clickhouse clickhouse      438 Feb 13 02:42 serialization.json
-rw-r----- 1 clickhouse clickhouse     4083 Feb 13 02:42 site_id.bin
-rw-r----- 1 clickhouse clickhouse      295 Feb 13 02:42 site_id.cmrk2
-rw-r----- 1 clickhouse clickhouse  4123085 Feb 13 02:42 timestamp.bin
-rw-r----- 1 clickhouse clickhouse      420 Feb 13 02:42 timestamp.cmrk2
-rw-r----- 1 clickhouse clickhouse 16488182 Feb 13 02:42 uuid.bin
-rw-r----- 1 clickhouse clickhouse      459 Feb 13 02:42 uuid.cmrk2
```

## 2. Query execution

### 2.1. Aggregation supported by `ORDER BY`

- ClickHouse leverages the table `ORDER BY` clause (`ORDER BY (site_id, toStartOfDay(timestamp), event, uuid)`) to skip reading a lot of data.

```sql
SELECT
    toStartOfDay(timestamp),
    event,
    sum(metric_value) as total_metric_value
FROM sensor_values
WHERE site_id = 233 AND timestamp > '2010-01-01' and timestamp < '2023-01-01'
GROUP BY toStartOfDay(timestamp), event
ORDER BY total_metric_value DESC
LIMIT 20

20 rows in set. Elapsed: 0.039 sec. Processed 90.11 thousand rows, 1.80 MB (2.29 million rows/s., 45.89 MB/s.)
Peak memory usage: 15.59 MiB.
```

- Use EXPLAIN to dig into how primary index for this query is used.
  - ClickHouse loaded the primary index for each part into memory. From this output, we know that query first used the primary key to filter based on `site_id` and `timestamp` values stored in the index.
  - This allowed it to know that only 11 out of 24415 granules (0.05%) contained any relevant data.
  - From there it read those 11 granules (11 \* 8192 rows) worth of data from `timestamp`, `site_id`, `event` and `metric_value` columns and did the rest of filtering and aggregation on that data alone.

```sql
EXPLAIN indexes = 1, header = 1
SELECT
    toStartOfDay(timestamp),
    event,
    sum(metric_value) AS total_metric_value
FROM sensor_values
WHERE (site_id = 233) AND (timestamp > '2010-01-01') AND (timestamp < '2023-01-01')
GROUP BY
    toStartOfDay(timestamp),
    event
ORDER BY total_metric_value DESC
LIMIT 20
FORMAT LineAsString

Query id: d374bc07-5bb6-48fe-b5a1-08ef29d0b557

Expression (Project names)
Header: toStartOfDay(timestamp) DateTime
        event String
        total_metric_value Int64
  Limit (preliminary LIMIT)
  Header: sum(__table1.metric_value) Int64
          toStartOfDay(__table1.timestamp) DateTime
          __table1.event String
    Sorting (Sorting for ORDER BY)
    Header: sum(__table1.metric_value) Int64
            toStartOfDay(__table1.timestamp) DateTime
            __table1.event String
      Expression ((Before ORDER BY + Projection))
      Header: sum(__table1.metric_value) Int64
              toStartOfDay(__table1.timestamp) DateTime
              __table1.event String
        Aggregating
        Header: toStartOfDay(__table1.timestamp) DateTime
                __table1.event String
                sum(__table1.metric_value) Int64
          Expression (Before GROUP BY)
          Header: toStartOfDay(__table1.timestamp) DateTime
                  __table1.event String
                  __table1.metric_value Int32
            Expression ((WHERE + Change column names to column identifiers))
            Header: __table1.timestamp DateTime
                    __table1.event String
                    __table1.metric_value Int32
              ReadFromMergeTree (default.sensor_values)
              Header: timestamp DateTime
                      site_id UInt32
                      event String
                      metric_value Int32
              Indexes:
                PrimaryKey
                  Keys:
                    site_id
                    toStartOfDay(timestamp)
                  Condition: and((toStartOfDay(timestamp) in (-Inf, 1672506000]), and((toStartOfDay(timestamp) in [1262278800, +Inf)), (site_id in [233, 233])))
                  Parts: 2/2
                  Granules: 11/24415
                  Search Algorithm: binary search
                Ranges: 2

43 rows in set. Elapsed: 0.003 sec.
```

- How to pick an `ORDER BY` (The primary key): The goal is to align the physical data storage with your most common filter patterns.
  - Columns: Pick 3–5 columns used most frequently in WHERE clauses.
  - Cardinality: Order them from lowest cardinality (left) to highest cardinality (right). Example: (`tenant_id`, `site_id`, `timestamp`).
  - Hierarchy: Put "root" elements before "leaves" (e.g., `continent`, `country`, `city`).
  - Timestamps: Usually go last. If you often query small ranges (e.g., specific days in a monthly partition), use (`toStartOfHour(timestamp), timestamp`).

### 2.2. "Point queries" not supported by `ORDER BY`

```sql
SELECT *
FROM sensor_values
WHERE uuid = '69028f26-768f-afef-1816-521b22d281ca'

Query id: ae5d90b7-2558-472a-850c-59dfa3ac5bb5

Ok.

0 rows in set. Elapsed: 2.563 sec. Processed 200.00 million rows, 3.20 GB (78.03 million rows/s., 1.25 GB/s.)
Peak memory usage: 6.97 MiB.
```

While the overall execution time of this query is not bad thanks to fast I/O, it needed to read 2200x the amount of data from disk. As the dataset size or column sizes increase, this performance would get dramatically worse. Why is this query slower? Because our `ORDER BY` does not support fast filtering by uuid and ClickHouse needs to read the whole table to find a single record and read all columns.

## 3. `PARTITION BY`

Another tool to make queries faster is `PARTITION BY`. Consider the updated table definition:

```sql
DROP TABLE sensor_values;

CREATE TABLE sensor_values (
    timestamp DateTime,
    site_id UInt32,
    event VARCHAR,
    uuid UUID,
    metric_value Int32
)
ENGINE = MergeTree()
PARTITION BY intDiv(toYear(timestamp), 10)
ORDER BY (site_id, toStartOfDay(timestamp), event, uuid)
SETTINGS index_granularity = 8192;

INSERT INTO sensor_values SELECT *
FROM generateRandom('timestamp DateTime, site_id UInt8, event VARCHAR, uuid UUID, metric_value Int32', NULL, 10)
LIMIT 200000000;
```

- Here, ClickHouse would generate one partition per 10 years of data, allowing to skip reading even the primary index in some cases.
- In the underlying data, each part would belong to a single partition and only parts within a partition would get merged.
- One additional benefit of partitioning by a derivate of timestamp is that if most queries touch recent data, you can also set up rules to automatically move older parts and partitions to cheaper storage or drop them entirely.

### 3.1. Query analysis

- First leverages an internal MinMax index on `timestamp`

```sql
EXPLAIN indexes=1, header=1 SELECT
    toStartOfDay(timestamp),
    event,
    sum(metric_value) as total_metric_value
FROM sensor_values
WHERE site_id = 233 AND timestamp > '2010-01-01' and timestamp < '2023-01-01'
GROUP BY toStartOfDay(timestamp), event
ORDER BY total_metric_value DESC
LIMIT 20

    ┌─explain──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 1. │ Expression (Project names)                                                                                                                                       │
 2. │ Header: toStartOfDay(timestamp) DateTime                                                                                                                         │
 3. │         event String                                                                                                                                             │
 4. │         total_metric_value Int64                                                                                                                                 │
 5. │   Limit (preliminary LIMIT)                                                                                                                                      │
 6. │   Header: sum(__table1.metric_value) Int64                                                                                                                       │
 7. │           toStartOfDay(__table1.timestamp) DateTime                                                                                                              │
 8. │           __table1.event String                                                                                                                                  │
 9. │     Sorting (Sorting for ORDER BY)                                                                                                                               │
10. │     Header: sum(__table1.metric_value) Int64                                                                                                                     │
11. │             toStartOfDay(__table1.timestamp) DateTime                                                                                                            │
12. │             __table1.event String                                                                                                                                │
13. │       Expression ((Before ORDER BY + Projection))                                                                                                                │
14. │       Header: sum(__table1.metric_value) Int64                                                                                                                   │
15. │               toStartOfDay(__table1.timestamp) DateTime                                                                                                          │
16. │               __table1.event String                                                                                                                              │
17. │         Aggregating                                                                                                                                              │
18. │         Header: toStartOfDay(__table1.timestamp) DateTime                                                                                                        │
19. │                 __table1.event String                                                                                                                            │
20. │                 sum(__table1.metric_value) Int64                                                                                                                 │
21. │           Expression (Before GROUP BY)                                                                                                                           │
22. │           Header: toStartOfDay(__table1.timestamp) DateTime                                                                                                      │
23. │                   __table1.event String                                                                                                                          │
24. │                   __table1.metric_value Int32                                                                                                                    │
25. │             Expression ((WHERE + Change column names to column identifiers))                                                                                     │
26. │             Header: __table1.timestamp DateTime                                                                                                                  │
27. │                     __table1.event String                                                                                                                        │
28. │                     __table1.metric_value Int32                                                                                                                  │
29. │               ReadFromMergeTree (default.sensor_values)                                                                                                          │
30. │               Header: timestamp DateTime                                                                                                                         │
31. │                       site_id UInt32                                                                                                                             │
32. │                       event String                                                                                                                               │
33. │                       metric_value Int32                                                                                                                         │
34. │               Indexes:                                                                                                                                           │
35. │                 MinMax                                                                                                                                           │
36. │                   Keys:                                                                                                                                          │
37. │                     timestamp                                                                                                                                    │
38. │                   Condition: and((timestamp in (-Inf, 1672505999]), (timestamp in [1262278801, +Inf)))                                                           │
39. │                   Parts: 14/101                                                                                                                                  │
40. │                   Granules: 3594/24457                                                                                                                           │
41. │                 Partition                                                                                                                                        │
42. │                   Keys:                                                                                                                                          │
43. │                     intDiv(toYear(timestamp), 10)                                                                                                                │
44. │                   Condition: and((intDiv(toYear(timestamp), 10) in (-Inf, 202]), (intDiv(toYear(timestamp), 10) in [201, +Inf)))                                 │
45. │                   Parts: 14/14                                                                                                                                   │
46. │                   Granules: 3594/3594                                                                                                                            │
47. │                 PrimaryKey                                                                                                                                       │
48. │                   Keys:                                                                                                                                          │
49. │                     site_id                                                                                                                                      │
50. │                     toStartOfDay(timestamp)                                                                                                                      │
51. │                   Condition: and((toStartOfDay(timestamp) in (-Inf, 1672506000]), and((toStartOfDay(timestamp) in [1262278800, +Inf)), (site_id in [233, 233]))) │
52. │                   Parts: 14/14                                                                                                                                   │
53. │                   Granules: 24/3594                                                                                                                              │
54. │                   Search Algorithm: binary search                                                                                                                │
55. │                 Ranges: 14                                                                                                                                       │
    └─explain──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

55 rows in set. Elapsed: 0.010 sec.
```
