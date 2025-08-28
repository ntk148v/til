# Clickhouse

## 1. Clickhouse's structure explained

Source: <https://posthog.com/blog/clickhouse-vs-elasticsearch>

ClickHouse is engineered to process data in a massive, consolidated place. Unlike Elasticsearch, ClickHouse’s optimizations don’t happen through distributing data, but by efficiently pre-processing it in anticipation of queries.

There are three major components that enable ClickHouse to return aggregations, such as averages, sums, and standard deviations, in millisecond times over petabytes of data.

### 1.1. Component 1: Columnar layout

ClickHouse’s columnar layout – which flips rows and columns in storage relative to a MySQL database – makes aggregations efficient.

When databases physically access data, they scan data row-by-row. By extension, if an analyst is trying to calculate the average value of bank account balances in a PostgreSQL database, they would need to access every bank account row. Alone, that would probably blow out memory. But in ClickHouse, the same analyst would only need to access one (physical) row of data – the bank balance one – and collapse it into an average.

Again, this is a physical row of data. As far as ClickHouse’s interface goes, data is still stored in a traditional format. ClickHouse’s syntax still treats individual entries as rows and attributes as columns. But under the hood, ClickHouse stores the data in an inverted arrangement, optimized for merging attribute data into single values.

### 1.2. Component 2: Materialized views

ClickHouse’s second superpower is dynamic materialized views.

Materialized views are not a new concept – in MySQL or PostgreSQL, a materialized view is a new table that can be queried from, rendered by a SQL query accessing other tables. However, once new data is added to the core tables, that materialized view goes out-of-date. Because creating materialized views is often expensive in traditional databases given their non-columnar layout, refreshing materialized views can only happen occasionally.

But ClickHouse truly makes materialized views dynamic. ClickHouse doesn’t only accomplish this because of the columnar layout of its data. It also leverages incremental data structures that merges data strategically.

### 1.3. Component 3: Specialized engines

ClickHouse has a series of specialized engines that enable developers to take advantage of multiple CPUs in parallel on the same machine. For instance, there is an engine for summing data (`SummingMergeTree`) and removing duplicates (`ReplacingMergeTree`). This technique has some resemblance to Elasticsearch’s parallelization across multiple machines to expedite search; ClickHouse does it at a more granular, per-machine level.

### 1.4. Sharding

ClickHouse has some overlap with Elasticsearch’s sharding features. ClickHouse extends Apache Zookeeper to manage multiple instances of ClickHouse should data need to be split across machines. However, this concept of sharding is closer to Elasticsearch’s support for multiple clusters – it is more a big data distribution problem, not a smaller optimization for speeding up queries.
