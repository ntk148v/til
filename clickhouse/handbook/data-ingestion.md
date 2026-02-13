# Data ingestion

Source: <https://posthog.com/handbook/engineering/clickhouse/data-ingestion>

## 1. Using `INSET`s for ingestion

ClickHouse allows using `INSERTs` to load data. Each INSERT creates a new part in ClickHouse, which comes with a lot of overhead and, in a busy system, will lead to errors due to exceeding `parts_to_throw` MergeTree table setting (default 300).

## 2. Using Kafka tables

- Use [Kafka table engine](https://clickhouse.com/docs/engines/table-engines/integrations/kafka) to handle ingestion into ClickHouse.
- How Kafka tables work:

  - Kafka engine tables act as Kafka consumers in a given consumer group. Selecting from that table advances the consumer offsets.
  - A Kafka table on its own does nothing beyond allowing querying data from Kafka - it needs to be paired with other tables for ingestion to work.

  ```sql
  CREATE TABLE kafka_ingestion_warnings
  (
      team_id Int64,
      source LowCardinality(VARCHAR),
      type VARCHAR,
      details VARCHAR CODEC(ZSTD(3)),
      timestamp DateTime64(6, 'UTC')
  )
  ENGINE = Kafka('kafka:9092', 'clickhouse_ingestion_warnings_test', 'group1', 'JSONEachRow')
  ```

## 3. Materialized views

- Materialized views in ClickHouse can be thought of as triggers - they react to new blocks being INSERTed into source tables and allow transforming and piping that data to other tables.
- [Everything you should know about materialized views](https://den-crane.github.io/Everything_you_should_know_about_materialized_views_commented.pdf).
  - An MV is an insert trigger.
  - An MV never reads its source table.
  - When CH gets an insert into a table with MV and for example this insert has 3 mil. rows. This Insert is processed in a streamable manner and its data is separated into 3 blocks because of settings -- in particular because of `max_insert_blocks_size`.
  - Then these blocks will be written into a table and every block can form multiple parts because of a table partitioning. For example a table has a partitioning expression and if an inserted block contains multiple partitioning key values then it will be written as multiple parts.
  - If this table has an MV then MV will get this block and not FROM the table but from the insert. Then MV select will be processed over the inserted block. So our insert brought 3 mil. rows and the MV select was triggered 3 times. And for every select’s result MV stored this result into an mv storage table. If this storage table is partitioned then this result might be separated into several parts as well.
