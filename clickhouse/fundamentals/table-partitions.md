# Table partitions

Source: <https://clickhouse.com/docs/partitions>

## 1. Introduction

- Partitions group the data parts of a table in the MergeTree engine family into organized, logical units, which is a way of organizing data that is conceptually meaningful and aligned with specific criteria, such as time ranges, categories, or other key attributes. These logical units make data easier to manage, query, and optimize.

- Partitioning can be enabled when a table is initially defined via the PARTITION BY clause.

```sql
CREATE TABLE uk.uk_price_paid_simple_partitioned
(
    date Date,
    town LowCardinality(String),
    street LowCardinality(String),
    price UInt32
)
ENGINE = MergeTree
ORDER BY (town, street)
PARTITION BY toStartOfMonth(date);
```

- **Structure on disk**: Whenever a set of rows is inserted into the table, instead of creating >= 1 one single data part containing all the inserted rows, ClickHouse creates one new data part for each unique partition key value among the inserted data.

```text
0. Split the rows by partition key.
1. Sorting.
2. Splitting into columns.
3. Compression.
4. Writing to disk.
```

![](https://clickhouse.com/docs/assets/ideal-img/partitions.4c07acd.2048.png)

- ClickHouse automatically creates MinMax indexes for each data aprt.
- **Per partition merges**: With partitioning enabled, ClickHouse only merges data parts within, but not across partitions. If a partition key with high cardinality is chosen -> `Too many parts` -> Addressing this problem is simple: choose a sensible partition key with cardinality under 1000..10000.

## 2. Monitoring partitions

```sql
-- virtual column _partition_value
SELECT DISTINCT _partition_value AS partition
FROM uk.uk_price_paid_simple_partitioned
ORDER BY partition ASC;

--  The list of all partitions, plus the current number of active parts and the sum of rows in these parts per partition
SELECT
    partition,
    count() AS parts,
    sum(rows) AS rows
FROM system.parts
WHERE (database = 'uk') AND (`table` = 'uk_price_paid_simple_partitioned') AND active
GROUP BY partition
ORDER BY partition ASC;
```

## 3. Use cases

### 3.1. Data management

- In ClickHouse, partitioning is primarily a data management feature. By organizing data logically based on a partition expression, each partition can be managed independently.
- For example, auto remove older than 12 months data using a TTL rule. Since the table is partitioned by `toStartOfMonth(date)`, entire partitions (sets of table parts) that meet the TTL condition will be dropped, making the cleanup operation more efficient, without having to rewrite parts.

```sql
CREATE TABLE uk.uk_price_paid_simple_partitioned
(
    date Date,
    town LowCardinality(String),
    street LowCardinality(String),
    price UInt32
)
ENGINE = MergeTree
PARTITION BY toStartOfMonth(date)
ORDER BY (town, street)
TTL date + INTERVAL 12 MONTH DELETE;

-- or move to a more cost-effective storage tier
CREATE TABLE uk.uk_price_paid_simple_partitioned
(
    date Date,
    town LowCardinality(String),
    street LowCardinality(String),
    price UInt32
)
ENGINE = MergeTree
PARTITION BY toStartOfMonth(date)
ORDER BY (town, street)
TTL date + INTERVAL 12 MONTH TO VOLUME 'slow_but_cheap';
```

### 3.2. Query optimization

- Partitions can assist with query performance, but this depends heavily on the access patterns. If queries target only a few partitions (ideally one), performance can potentially improve. This is only typically useful if the partitioning key isn't in the primary key and you're filtering by it, as shown in the example query below.

```sql
SELECT MAX(price) AS highest_price
FROM uk.uk_price_paid_simple_partitioned
WHERE date >= '2020-12-01'
  AND date <= '2020-12-31'
  AND town = 'LONDON';
```

- ClickHouse processes that query by applying a sequence of pruning techniques to avoid evaluating irrelevant data:
  - ① Partition pruning: MinMax indexes are used to ignore whole partitions (sets of parts) that logically can't match the query's filter on columns used in the table's partition key.
  - ② Granule pruning: For the remaining data parts after step ①, their primary index is used to ignore all granules (blocks of rows) that logically can't match the query's filter on columns used in the table's primary key.

![](https://clickhouse.com/docs/assets/ideal-img/partition-pruning.87dc016.2048.png)

### 3.3. Partitioning is primarily a data management feature

Be aware that querying across all partitions is typically slower than running the same query on a non-partitioned table.
