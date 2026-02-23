# Columnar database vs. Row database

Source:

- <https://estuary.dev/blog/columnar-database-vs-row-database/>
- <https://www.fivetran.com/learn/columnar-database-vs-row-database>
- <https://clickhouse.com/resources/engineering/what-is-columnar-database>

Table of contents:

- [Columnar database vs. Row database](#columnar-database-vs-row-database)
  - [1. Row database](#1-row-database)
    - [1.1. Pros](#11-pros)
    - [1.2. Cons](#12-cons)
  - [2. Columnar database](#2-columnar-database)
    - [2.1. Pros](#21-pros)
    - [2.2. Cons](#22-cons)
  - [3. Key architectural and performance differences](#3-key-architectural-and-performance-differences)
    - [3.1. Storage layout](#31-storage-layout)
    - [3.2. Compression efficiency](#32-compression-efficiency)
    - [3.3. Scalability](#33-scalability)
  - [4. How to choose](#4-how-to-choose)
    - [4.1. When to choose row-oriented databases](#41-when-to-choose-row-oriented-databases)
    - [4.2. When to choose column-oriented databases](#42-when-to-choose-column-oriented-databases)
  - [5. Hybrid and emerging options](#5-hybrid-and-emerging-options)

Database performance relies heavily on the type of database storage you choose. Most organizations use either a row database, a column database or a combination of both.

Row-oriented databases are ideal for some access patterns, specifically transactional processing, while column-oriented databases are better suited for analytical processing.

![](https://estuary.dev/static/989e7f420ef54ac010c943bc9ec12c04/e306d/Is_your_workload_transactional_or_analytical_a3988285a2.webp)

## 1. Row database

Row-oriented databases are used in traditional database management systems that are primarily focused on storage. In a row store or row database, the data is stored row by row. Each row contains all the values associated with a single entity, such as a customer, order, or transaction. This format mirrors how users often interact with spreadsheets or form-based applications: all the details about one item grouped together.

![](https://cdn.prod.website-files.com/6130fa1501794e37c21867cf/6474849ec0b99a87ce46bb32_7712216d.png)

In a row database, this would be stored as:

```text
# Here the “|” signifies the end of the block, meaning all of the data within that block is stored together.
John Male USA 63 | Mary Female Canada 29 | James Male Australia 48 |
```

When you execute a query like `SELECT * FROM users WHERE user_id = 123`, a row-based engine can quickly locate and return the entire record. This makes row databases ideal for Online Transaction Processing (OLTP) systems that demand high-speed inserts, updates, and lookups.

### 1.1. Pros

- **Fast for transactional queries**: When applications frequently read or write entire rows, this model shines.
- **Efficient for frequent writes**: Because data for a full record is stored together, updates involve fewer disk reads or writes.
- **Ideal for OLTP**: Row-based databases are very good at processing single-row operations. They are built for fast and efficient online transaction processing in highly concurrent environments and are often heavily indexed.
- **Schema enforcement and ACID guarantees**: Row databases typically offer strong consistency and transactional integrity, which are essential for mission-critical systems.

### 1.2. Cons

- **Slower data aggregation**: Row-oriented databases struggle with aggregation since data from every row has to be loaded before relevant data can be extracted and acted upon. For example, if we wanted the average age of male customers in the “Top Customers” table and used a row store, it would load all the customer data first and then pull out the relevant data.
- **Insufficient compression**: Because data types are mixed within each row, compression algorithms are less effective, leading to larger storage requirements and potentially slower I/O performance.
- **Less efficient for read-heavy analytical workloads**: Analytical queries that scan large datasets and perform aggregations across many rows can be slower in row databases due to the need to read entire rows.

> **Ask yourself**: Do we need to insert, update, or delete many individual records per second? Are queries mostly fetching full rows rather than analyzing patterns across columns?

## 2. Columnar database

A columnar database stores all the data from each column as a single block. Think of it as vertical partitioning compared to the horizontal partitioning of a row store.

For example, a columnar database would store the ‘Top Customers’ data in the following manner:

```text
John Mary James | Male Female Male | USA Canada Australia | 63 29 48
```

![](https://cdn.prod.website-files.com/6130fa1501794e37c21867cf/6474849e928d0fc8ffab0fce_18a7e287.png)

### 2.1. Pros

- **Best for OLAP applications**: Databases using columnar storage have a major benefit over equivalent databases using row-based storage: query performance is much faster for analytical queries that crunch through lots of data. Data is only accessed if required to compute the query result.
- **High compression speeds**: Since data in each column is of the same type, compression algorithms can be more effective, leading to reduced storage requirements and improved I/O performance.
- **Optimized for aggregations and filters**: Count, sum, average, and other operations across billions of rows become faster and more efficient.

### 2.2. Cons

- **Slower for transactional queries**: Columnar databases are not optimized for transactional workloads that require frequent inserts, updates, or deletes of individual records. Modifying a single record may require updating multiple column files, leading to increased latency. Columnar databases prefer to process inserts, updates and deletes (or merges) as batch operations.
  - For example, if you wanted to add a row of data, each value from the new row has to be added to the correct block of the existing database. This can become complicated when there are many column
- **Complex schema management**: Columnar databases may require more careful schema design and management, as changes to the schema can be more involved compared to row databases.
- **Less suitable for real-time applications**: Applications that require immediate consistency and low-latency access to individual records may find columnar databases less suitable.

> **Ask yourself**: Do your queries typically analyze trends across a few fields over millions of records? Are your data volumes growing faster than your ability to query them?

## 3. Key architectural and performance differences

### 3.1. Storage layout

- **Row databases**: Store data row by row, making them efficient for transactional operations that involve reading or writing entire records.
- **Columnar databases**: Store data column by column, optimizing them for analytical queries that access specific fields across many records.

-> This fundamental difference in storage layout leads to varying performance characteristics depending on the workload.

### 3.2. Compression efficiency

- Columnar databases compress data more effectively. Similar data types stored together result in smaller storage footprints and faster scans.
- Row databases have lower compression rates due to mixed data types in each row.

### 3.3. Scalability

- Columnar systems scale horizontally for analytics, making them suitable for big data environments.
- Row databases may require more optimization and indexing as datasets grow.

## 4. How to choose

### 4.1. When to choose row-oriented databases

Ask yourself, if you answered yes to any of these, then a row-oriented database is likely the better option.

- Do your applications require real-time inserts, updates, or deletes on individual records?
- Are most queries retrieving entire rows rather than analyzing trends across specific fields?
- Is data consistency critical, with strict ACID compliance?

Use cases:

- Customer Relationship Management (CRM): Managing user profiles, preferences, and support tickets.
- Financial systems: Processing transactions, ledgers, and account updates with integrity.
- Ecommerce platforms: Handling carts, orders, inventory, and customer records.
- Operational dashboards: Displaying user activity, recent transactions, or real-time system data.

### 4.2. When to choose column-oriented databases

Ask yourself:

- Are you running complex queries over millions or billions of records?
- Do most queries only require a few columns from a large dataset?
- Is query performance more important than insert speed?

If these questions resonate, a columnar database aligns well with your needs.

Use cases:

- Business Intelligence (BI): Generating aggregated metrics, KPIs, and performance dashboards.
- Data Warehousing: Storing and querying historical data for reporting and compliance.
- Marketing Analytics: Running segmentation, attribution, and cohort analyses on behavioral data.
- IoT and Event Streams: Capturing time-series data and scanning it for patterns.

## 5. Hybrid and emerging options

- TiDB: Combines MySQL compatibility with distributed analytics capabilities.
- SingleStore: Uses a row store for transactions and a column store for analytics, automatically managing data movement between the two.
- PostgreSQL with columnar extensions: Tools like Citus and TimescaleDB allow analytics over PostgreSQL with hybrid-like performance.
- ClickHouse with materialized views: Though primarily columnar, ClickHouse can simulate row-like performance for specific use cases using secondary structures
