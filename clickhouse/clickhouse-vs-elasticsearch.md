# Elasticsearch vs. ClickHouse

Source: <https://clickhouse.com/docs/use-cases/observability/clickstack/migration/elastic/concepts#elasticsearch-vs-clickhouse>

Table of contents:
- [Elasticsearch vs. ClickHouse](#elasticsearch-vs-clickhouse)
  - [1. Core structural concepts](#1-core-structural-concepts)
  - [2. Data modeling and flexibility](#2-data-modeling-and-flexibility)
  - [3. Ingestion and transformation](#3-ingestion-and-transformation)
  - [4. Query languages](#4-query-languages)
  - [5. File formats and interfaces](#5-file-formats-and-interfaces)
  - [6. Indexing and storage](#6-indexing-and-storage)
  - [7. Distribution and replication](#7-distribution-and-replication)
  - [8. Deduplication and routing](#8-deduplication-and-routing)
  - [9. Data management](#9-data-management)
    - [9.1. Index lifecycle management vs native TTL](#91-index-lifecycle-management-vs-native-ttl)
    - [9.2. Storage tiers and hot-warm architectures](#92-storage-tiers-and-hot-warm-architectures)

ClickHouse and Elasticsearch organize and query data using different underlying models, but many core concepts serve similar purposes.

## 1. Core structural concepts

| Elasticsearch | ClickHouse       | Description                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Field         | Column           | The basic unit of data, holding one or more values of a specific type. Elasticsearch fields can store primitives as well as arrays and objects. Fields can have only one type. ClickHouse also supports arrays and objects (Tuples, Maps, Nested), as well as dynamic types like Variant and Dynamic which allow a column to have multiple types.                                                    |
| Document      | Row              | A collection of fields (columns). Elasticsearch documents are more flexible by default, with new fields added dynamically based on the data (type is inferred from ). ClickHouse rows are schema-bound by default, with users needing to insert all columns for a row or subset. The JSON type in ClickHouse supports equivalent semi-structured dynamic column creation based on the inserted data. |
| Index         | Table            | The unit of query execution and storage. In both systems, queries run against indices or tables, which store rows/documents.                                                                                                                                                                                                                                                                         |
| Implicit      | Schema (SQL)     | SQL schemas group tables into namespaces, often used for access control. Elasticsearch and ClickHouse don't have schemas, but both support row-and table-level security via roles and RBAC                                                                                                                                                                                                           |
| Cluser        | Cluster/Database | Elasticsearch clusters are runtime instances that manage one or more indices. In ClickHouse, databases organize tables within a logical namespace, providing the same logical grouping as a cluster in Elasticsearch. A ClickHouse cluster is a distributed set of nodes, similar to Elasticsearch, but is decoupled and independent of the data itself.                                             |

## 2. Data modeling and flexibility

- Elasticsearch is known for its schema flexibility through [dynamic mappings](https://www.elastic.co/docs/manage-data/data-store/mapping/dynamic-mapping). Fields are created as documents are ingested, and types are inferred automatically - unless a schema is specified.
- ClickHouse is stricter by default =- tables are defined and explicit schemas - but offers flexibility through `Dynamic`, `Variant` (allow mixed-type data), and `JSON` types.

## 3. Ingestion and transformation

- Elasticsearch uses ingest pipelines with processors (e.g., enrich, rename, grok) to transform documents before indexing.
- In ClickHouse, similar functionality is achieved using [incremental materialized views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view), which can filter, transform, or enrich incoming data and insert results into target tables.

## 4. Query languages

- Elasticsearch supports a [number of query languages](https://www.elastic.co/docs/explore-analyze/query-filter/languages) including DSL, ES|QL and KQL queries.
- ClickHouse supports full SQL syntax.

## 5. File formats and interfaces

- Elasticsearch supports JSON (and limited CSV) ingestion.
- ClickHouse supports over 70 file formats, including Parquet, Protobuf, Arrow, CSV, and others — for both ingestion and export. This makes it easier to integrate with external pipelines and tools.
- Both systems offer a REST API, but ClickHouse also provides a native protocol for low-latency, high-throughput interaction.

## 6. Indexing and storage

- Each ① index is broken into shards, each of which is a physical Lucene index stored as segments on disk. A shard can have one or more physical copies called replica shards for resilience. For scalability, shards and replcas can be distributed over several nodes. A single shard ② consists of one or more immutable segments. A segment is the basic indexing structure of Lucene, the Java library providing the indexing and search features on which Elasticsearch is based.
  - Elasticsearch recommends sizing shards to around [50 GB or 200 million documents](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards#general-sizing-guidelines) due to [JVM heap and metadata overhead](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards#each-shard-has-overhead).
  - Each Elasticsearch shard is a separate Lucene index, so it shares Lucene’s `MAX_DOC` limit of having at most 2,147,483,519 ((2^31)-129) documents
  - Elasticsearch indexes all fields into inverted indices for fast search, optionally using doc values for aggregations, sorting and scripted field access.
  - Importantly, Elasticsearch stores the full original document in \_source (compressed with LZ4, Deflate or ZSTD).

![](https://clickhouse.com/docs/assets/ideal-img/elasticsearch.a2755cb.1606.png)

- ClickHouse, by contrast, is column-oriented — every column is stored independently but always sorted by the table's primary/ordering key. This ordering enables sparse primary indexes, which allow ClickHouse to skip over data during query execution efficiently. When queries filter by primary key fields, ClickHouse reads only the relevant parts of each column, significantly reducing disk I/O and improving performance — even without a full index on every column.
  - Supports [skip indexes](https://clickhouse.com/docs/optimize/skipping-indexes), which accelerate filtering by precomputing index data for selected columns.
  - Lets users specify compression codecs and compression algorithms per column.
  - Support sharding, but its model is designed to favor vertical scaling. A single shard can store trillions of rows and continues to perform efficiently as long as memory, CPU, and disk permit. Shards in ClickHouse are logical — effectively individual tables — and do not require partitioning unless the dataset exceeds the capacity of a single node. This typically occurs due to disk size constraints, with sharding ① introduced only when horizontal scale-out is necessary - reducing complexity and overhead. In this case, similar to Elasticsearch, a shard will hold a subset of the data. The data within a single shard is organized as a collection of ② immutable data parts containing ③ several data structures.
  - ClickHouse does not store a separate document representation. Data is reconstructed from columns at query time, saving storage space

![](https://clickhouse.com/docs/assets/ideal-img/clickhouse.3198dfb.1608.png)

## 7. Distribution and replication

- Elasticsearch uses a **primary-secondary model** for replication.

  - When data is written to a primary shard, it is synchronously copied to one or more replicas. These replicas are themselves full shards distributed across nodes to ensure redundancy.
  - Elasticsearch acknowledges writes only after all required replicas confirm the operation — a model that provides near **sequential consistency**, although dirty reads from replicas are possible before full sync.
  - A master node coordinates the cluster, managing shard allocation, health, and leader election.

- ClickHouse employs **eventual consistency** by default, coordinated by Keeper - a lightweight alternative to ZooKeeper.

  - Writes can be sent to any replica directly or via a [distributed table](https://clickhouse.com/docs/engines/table-engines/special/distributed), which automatically selects a replica.
  - Replication is asynchronous - changes are propagated to other replicas after the write is acknowledged. For stricter guarantees, ClickHouse supports [sequential consistency](https://clickhouse.com/docs/migrations/postgresql/appendix#sequential-consistency), where writes are acknowledged only after being committed across replicas, though this mode is rarely used due to its performance impact.

- In summary:
  - Elastic: Shards are physical Lucene structures tied to JVM memory. Over-sharding introduces performance penalties. Replication is synchronous and coordinated by a master node.
  - ClickHouse: Shards are logical and vertically scalable, with highly efficient local execution. Replication is asynchronous (but can be sequential), and coordination is lightweight.

## 8. Deduplication and routing

- Elasticsearch de-duplicates documents based on their `_id`, routing them to shards accordingly
- ClickHouse supports insert-time deduplication, allowing users to retry failed inserts safely.
- Index routing in Elasticsearch ensures specific documents are always routed to specific shards.
- In ClickHouse, users can define shard keys or use Distributed tables to achieve similar data locality.

## 9. Data management

### 9.1. Index lifecycle management vs native TTL

- In Elasticsearch, long-term data management is handled through **Index Lifecycle Management (ILM)** and **Data Streams**.
  - Define policies that govern when indices are rolled over (e.g. after reaching a certain size or age), when older indices are moved to lower-cost storage, and when they're ultimately deleted.
  - To manage shards sizes and support efficient deletion, new indices must be created periodically and old ones removed - effectively rotating data at the index level.
- In ClickHouse, data is typically stored in a **single table** and managed using **TTL (time-to-live) expressions** at the column or partition level.
  - Data can be partitioned by date, allowing efficient deletion without the need to new tables or perform index rollovers.

### 9.2. Storage tiers and hot-warm architectures

- Elasticsearch supports **hot-warm-cold-frozen** storage architectures, where data is moved between storage tiers with different performance characteristics. This is typically configured through ILM and tied to node roles in the cluster.
- ClickHouse supports **tiered storage** through native table like `MergeTree`, which can automatically move older data between different volumes based on custom rules.
