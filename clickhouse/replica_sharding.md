# Replication and Sharding

Source:

- <https://altinity.com/wp-content/uploads/2024/05/Deep-Dive-on-ClickHouse-Sharding-and-Replication-2024-1-1.pdf>
- <https://chistadata.com/how-to-setup-6-nodes-clickhouse-horizontal-scaling/>

## Sharding

Sharding is splitting a large table horizontally (row-wise) and storing it in multiple servers. ClickHouse uses distributed table engine for processing the sharded tables. Shards can be internally replicated or non-replicated in ClickHouse. Sharding allows storing huge amounts of data that may otherwise not fit in a single server.

Pros:

- High availability
- Faster query response time
- Increased write bandwidth
- Easy to scale out

Cons:

- Added complexity
- Possibility of unbalanced data in a shard

ClickHouse uses hash-based sharding, where a column is chosen as the sharding key from the table, and the values are hashed. Storing the data in appropriate shards is based on the hash value. For example, if there are 3 shards for a table, the remainder (modulo operation) of the hashed value, when divided by the number of shards, will determine the shard on which the particular row is stored (e.g 1234 % 3 = 1, so the data is stored on shard 2 and if the hash value is 12345 the data will be stored on shard 1 (12345 % 3 = 0))

Distributed table engines can perform parallel and distributed query processing in a ClickHouse cluster. This table engine can not store the data independently and depends on other table engines (MergeTree family) to store the underlying data. It is possible to insert the data directly into the distributed table (and ClickHouse determines the shards based on the shard key) or insert it into the underlying storage table in every cluster manually. It is possible to read the data directly by querying the distributed engine table.

```
- Replias improve read QPS and concurrency.
- Shards add throughput and IOPS.
```

## Parallel replicas with dynamic sharding

Source:

- <https://clickhouse.com/docs/deployment-guides/parallel-replicas>
- <https://chistadata.com/parallel-replicas-with-dynamic-shards-horizontal-scaling-clickhouse/>

> It is released with 23.3 version of ClickHouse.

Imagine that you want to build a ClickHouse cluster with 10 replicas. Normally, when you run a Select query, your database server send a request your primary server and bring the result to you.

With paralel replicas, when you run a Select query for example, Your request is automatically distributed among all replicas and data is read from all replicas so that your transaction result can reach you faster. It is like your data is reading from sharded cluster but it is actually just replicated cluster.
