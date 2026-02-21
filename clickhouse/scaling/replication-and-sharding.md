# Replication and Sharding

Sources:

- <https://posthog.com/handbook/engineering/clickhouse/replication>
- <https://altinity.com/wp-content/uploads/2024/05/Deep-Dive-on-ClickHouse-Sharding-and-Replication-2024-1-1.pdf>
- <https://chistadata.com/how-to-setup-6-nodes-clickhouse-horizontal-scaling/>

Table of contents:

- [Replication and Sharding](#replication-and-sharding)
  - [1. Sharding](#1-sharding)
  - [2. Replication](#2-replication)
  - [3. Distributed table engine](#3-distributed-table-engine)
  - [4. Parallel replicas with dynamic sharding](#4-parallel-replicas-with-dynamic-sharding)
  - [5. Best practices](#5-best-practices)

## 1. Sharding

Sharding splits a large table horizontally (row-wise) and stores it across multiple servers.

### Pros and cons

| Pros | Cons |
|------|------|
| High availability | Added complexity |
| Faster query response time | Possibility of unbalanced data |
| Increased write bandwidth | |
| Easy to scale out | |

### How it works

ClickHouse uses **hash-based sharding**:

1. A column is chosen as the sharding key
2. Values are hashed
3. Remainder of hash divided by number of shards determines target shard
   - Example: `1234 % 3 = 1` → stored on shard 2

### When to shard

**Shard:**

- Table could become too large for single server
- Need to distribute read/write load

**Don't shard:**

- Table often JOINed in queries (where whole dataset needed)
- Examples: persons, groups, cohorts tables

### Implementation

When creating a replicated table, configure sharding via ReplicatedMergeTree engine parameters:

```sql
-- Sharded table
ENGINE = ReplicatedMergeTree('/zk/some/path/{shard}/tablename', '{replica}')

-- Unsharded (replicated) table
ENGINE = ReplicatedMergeTree('/zk/some/path/tablename', '{replica}-{shard}')
```

## 2. Replication

### Requirements

- ClickHouse replication works table-by-table
- Tables need to be created on all shards (use `ON CLUSTER`)
- Requires running ZooKeeper or ClickHouse Keeper

### Replicated tables

Replication uses a multi-master coordination scheme based on Raft consensus to guarantee configurable number of replicas per shard.

**Key points:**

- All replicas are writable
- Data synchronization is multi-directional
- Uses eventual consistency by default (can be sequential)
- Coordinated by Keeper (lightweight ZooKeeper alternative)

### Monitoring replication

```sql
-- Check replication queue
SELECT * FROM system.replication_queue;

-- Check ongoing fetches
SELECT * FROM system.replicated_fetches;
```

### Replication log operations

Nodes advance table state using 3 operations:

1. **Inserts**: Add new part to state
2. **Merges**: Add new part, delete existing parts  
3. **Mutations/DDL**: Add/delete parts, change metadata

Operations are performed locally and recorded as state transitions in global replication log.

## 3. Distributed table engine

`Distributed` tables don't store data - they fan out to `ReplicatedMergeTree` tables on the cluster.

### How writes work

When INSERTing data against Distributed tables:

1. ClickHouse decides which shard each row belongs to
2. Forwards data to relevant shard(s) based on `sharding_key`

**Tip:** If underlying table has ALIAS/MATERIALIZED columns, set up two Distributed tables:

- One for writes (minimum columns)
- One for reads (all columns)

### How queries work

When querying Distributed table:

1. Query sent to any node (becomes coordinator)
2. Coordinator figures out queries for individual shards
3. Queues sub-queries
4. Aggregates results and returns answer

**Optimization:** ClickHouse usually performs one query locally instead of sending to another replica of its shard.

```
┌─────────────────────────────────────────────────────────────┐
│                      Coordinator Node                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Distributed Table                     ││
│  └─────────────────────────────────────────────────────────┘│
│                           │                                  │
│              ┌────────────┼────────────┐                     │
│              ▼            ▼            ▼                     │
│        ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│        │ Shard 1 │  │ Shard 2 │  │ Shard 3 │                │
│        │  (Rep1) │  │  (Rep1) │  │  (Rep1) │                │
│        └─────────┘  └─────────┘  └─────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### clusterAllReplicas table function

Access all shards without creating Distributed table:

```sql
-- Query one replica per shard
cluster('cluster_name', db.table, sharding_key)

-- Query all replicas
clusterAllReplicas('cluster_name', db.table, sharding_key)
```

## 4. Parallel replicas with dynamic sharding

> Released with ClickHouse 23.3

In a replicated cluster, normal SELECT queries are sent to the primary server. With parallel replicas:

1. Request is automatically distributed among all replicas
2. Data is read from all replicas simultaneously
3. Results arrive faster (like reading from sharded cluster, but with replicated data)

This enables horizontal scaling of query throughput without actual sharding.

## 5. Best practices

### General guidelines

```
- Replicas improve read QPS and concurrency.
- Shards add throughput and IOPS.
```

### Vertical scaling first

ClickHouse was designed to utilize full machine resources:

- Hundreds of cores
- Terabytes of RAM
- Petabytes of disk

**Benefits:**

- Cost efficiency
- Lower operational complexity
- Better query performance (minimized network data for JOINs)

Two machines should be sufficient for all but the largest use cases.

### When to scale horizontally

Consider horizontal scaling when:

- Single node disk capacity exceeded
- Need higher write throughput than single node can provide
- Query parallelization across nodes required

### Configuration checklist

1. Use `ON CLUSTER` for DDL operations
2. Ensure Keeper/ZooKeeper has adequate resources
3. Monitor `system.replication_queue` and `system.replicated_fetches`
4. Configure appropriate `sharding_key` for data distribution
5. Consider read vs write patterns when designing schema
