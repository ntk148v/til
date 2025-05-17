# Citus

Source: <https://docs.citusdata.com/en/v12.1/portals/getting_started.html>

## 1. What is Citus?

- Citus is a PostgreSQL extension (not a fork) that transforms Postgres into a distributed database - so you can achieve high performance at any scale.
  - **Distributed tables** are shared across a cluster of PostgreSQL nodes to combine their CPU, memory, storage and I/O capacity.
  - **References tables** are replicated to all nodes for joins and foreign keys from distributed tables and maximum read performance.
  - **Distributed query engine** routes and parallelizes SELECT, DML, and other operations on distributed tables across the cluster.
  - **Columnar storage** compresses data, speeds up scans, and supports fast projections, both on regular and distributed tables.
  - **Query from any node** enables you to utilize the full capacity of your cluster for distributed queries.
- You use Citus, you are also using Postgres. You can leverage the latest Pos
  tgres features, tooling, and ecosystem.

## 2. Architecture

- A Citus database cluster grows from a single PostgreSQL node into a cluster by adding worker nodes. In a Citus cluster, the original node to which the application connects is referred to as the coordinator node. The Citus coordinator contains both the metadata of distributed tables and reference tables, as well as regular (local) tables, sequences, and other database objects (e.g.foreign tables).
- Data in distributed tables is stored in "shards", which are actually just regular PostgreSQL tables on the worker nodes. When querying a distributed table on the coordinator node, Citus will send regular SQL queries to the worker nodes. That way, all the usual PostgreSQL optimizations and extensions can automatically be used with Citus.

![](https://github.com/citusdata/citus/raw/main/images/citus-architecture.png)

## 3. Distributed data

### 3.1. Table types

- **Type 1: Distributed tables**:

  - Normal tables to SQL statements, but are horizontally partitions across worker nodes.

  ![](https://docs.citusdata.com/en/v12.1/_images/diagram-parallel-select.png)

  - Here the rows of `table` are stored in tables `table_1001`, `table_1002` etc on the workers. The component worker tables are called _shards_.

- **Type 2: Reference tables**:
  - A type of distributed table whose entire contents are concentrated into a single shard which is replicated on every worker. Thus queries on any worker can access the reference information locally, without the network overhead of requesting rows from another node. Reference tables have no distribution column because there is no need to distinguish separate shards per row.
  - Reference tables are typically small, and are used to store data that is relevant to queries running on any worker node. For example, enumerated values like order statuses, or product categories.
  - Two-phae commits (2PC) on transactions.
- **Type 3: Local tables**:
  - The coordinator node you connect to and interact with is a regular PostgreSQL database with the Citus extension installed. Thus you can create ordinary tables and choose not to shard them. This is useful for small administrative tables that don't participate in join queries. An example would be users table for application login and authentication.
- **Type 4: Local managed tables**:
  - `citus.enable_local_reference_table_foreign_keys (boolean)` is enabled.
  - Citus may automatically add local tables to metadata if a foreign key reference exists between a local table and a reference table.
  - Tables present in metadata are considered managed tables and can be queried from any node, Citus will know to route to the coordinator to obtain data from the local managed table.
- **Type 5: Schema tables**:
  - Distributed schemas are automatically associated with individual colocation groups such that the tables created in those schemas are automatically converted to colocated distributed tables without a shard key.

### 3.2. Shards
