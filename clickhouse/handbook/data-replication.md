# Data replication and distributed queries

Source: <https://posthog.com/handbook/engineering/clickhouse/replication>

## 1. Replicated tables

- ClickHouse replication works on a table-by-table level, tables need to be created on all shards (preferably via using `ON CLUSTER`).
- Replication requires a running ZooKeeper/clickhouse-keeper setup.
- Sharding helps scale a dataset by having each node only store part of the data. To decide whether to shard a table, consider how it's queried and what data it stores:
  - Shard: table that could become too large for a single server.
  - Don't shard: table often JOINed in queries (e.g. persons, groups, cohorts) where the whole dataset is needed.
- Sharding requires care given in the schema - queries touching data should ideally only need to load data from a given shard.
- When creating a replicated table, configuring whether a table is sharded or not is done via varying the parameters to a ReplicatedMergeTree engine:
  - Example sharded engine: `ReplicatedMergeTree('/zk/some/path/{shard}/tablename', '{replica}')`
  - Example unsharded table engine: `ReplicatedMergeTree('/zk/some/path/tablename', '{replica}-{shard}')`
- Monitoring replication: `system.replication_queue` and `system.replicated_fetches`.

## 2. `Distributed` table engine

- `Distributed` table engine tables are used to query and write to sharded tables. Note that Distributed engine tables do not store any data on their own but rather always fan out to `ReplicatedMergeTree` tables on the cluster.
- How writes againts `Distributed` tables work.
  - When INSERTing data against Distributed tables, ClickHouse decides which shard each row belongs to and forwards data to relevant shard(s) based on the sharding_key.
  - Note that if your underlying table has columns that ClickHouse populates (e.g. ALIAS, MATERIALIZED), it's often necessary to set up two Distributed tables:
    - One for writes containing a minimum set of columns
    - Another for reads which contain all columns

![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*C_NL7jIIQGHh3aKkYDqKGQ.png)

- How queries against `Distributed` tables work.
  - When querying Distributed table, you can send the query to any node in the ClickHouse cluster. That node becomes the `coordinator`, which:
    - Figures out what queries individual shards need to execute and queues these queries.
    - Once results are in, aggregates the results together and returns an answer.
  - Given local execution is faster than reading data over the network, ClickHouse will usually perform one of the queries locally instead of sending it to another replica of its shard.
  - Depending on the query, sub-queries executed on other shards might either return already aggregated data or stream entire datasets across the network.

## 2. `clusterAllReplicas` table function

- Allows accessing all shards (configured in the remote_servers section) of a cluster without creating a Distributed table. Only one replica of each shard is queried. `clusterAllReplicas` function — same as cluster, but all replicas are queried. Each replica in a cluster is used as a separate shard/connection.

```sql
cluster(['cluster_name', db.table, sharding_key])
cluster(['cluster_name', db, table, sharding_key])
clusterAllReplicas(['cluster_name', db.table, sharding_key])
clusterAllReplicas(['cluster_name', db, table, sharding_key])
```
