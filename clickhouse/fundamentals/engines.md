# Engines

Source: <https://youtu.be/jBJgGjhu6TA>

Engines define the ClickHouse data architecture.

- Storage: parts layout, indexes, marks, etc.
- Lifecycle: merges, deduplication, replication, etc.
- Query behavior: skip unnecessary data, merge newer parts/states, etc.

```text
+--------------------+        +--------------------+        +-----------------------+
|        TABLE       |  uses  |        ENGINE      | defines|        STORAGE        |
|  (logical schema)  | -----> |   (behavior/sem)   | -----> | (on-disk layout/index)|
+--------------------+        +--------------------+        +-----------------------+
        |                              |                              |
        | columns, types               | merges, dedup,               | parts, marks, columns/*.bin
        | settings, constraints        | replication, TTL             | primary.idx, *.mrk3

```

Engine families

- MergeTree: OLAP general purpose - append & merge for logs, events, time-series. All MergeTree engines share the same physical layer, data parts, marks, indexes, but differ in how they merge those parts.

| Engine               | Purpose                       | Best for                  |
| -------------------- | ----------------------------- | ------------------------- |
| MergeTree            | Append & merge                | Logs, events, time-series |
| ReplacingMergeTree   | Deduplication                 | Upserts, dimensions table |
| AggregatingMergeTree | Pre-aggregated data           | Materialized views        |
| SummingMergeTree     | Sums numeric columns on merge | Metrics aggregation       |

- Integration: connect to external systems - MySQL, PostgreSQL, Kafka, S3.
- Others: Specialized engines - Log, URL, Dictionary, Null, Distributed.

```sql
SELECT partition, name, rows, active, level FROM system.parts
-- then Insert
-- level 0
OPTIMIZE TABLE <...>
-- level 1 - active
```

Partitions group the data parts of a table into organized, logical units, which is a way of organizing data that is conceptually meaningful and aligned with specific criteria,

- Whenever a set of rows is inserted into the table, instead of creating (at least) one single data part containing all the inserted rows, ClickHouse creates one new data part for each unique partition key value among the inserted rows.
- With partitioning enabled, ClickHouse only merges data parts within, but not across partitions.
- Partition size: Good size for single partition is something like 100-300Gb. For Summing/Replacing a bit smaller (400Mb-40Gb)
- Query performance: better to avoid touching more than few dozens of partitions with typical SELECT query.
- Partition count: the number of partitions in table - dozen or hundreds, not thousands. Single insert should bring data to one or few partitions.

Insert data:

| Concept        | Description                             |
| -------------- | --------------------------------------- |
| Insert         | Create a temporary part                 |
| Part           | Directory of compressed column files    |
| Merge          | Combines smaller parts into bigger ones |
| Compression    | Per-column encoding (ZSTD, LZ4, etc.)   |
| Marks / Index  | Allow skipping and fast reads           |
| TTLs & Indexes | Applied during merges                   |

ClickHouse uses a heuristic based on part sizes and levels:

```text
Merge candidates = adjacent parts where:
   size_sum <= max_bytes_to_merge_at_min_space_in_pool
   number_of_parts <= max_merge_at_once
   ...
Sorted by “score” (favoring small+close)
```

If no such candidate exists, background merge does not start.
