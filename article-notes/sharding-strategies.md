# Four Data Sharding Strategies

Source:
- <https://blog.yugabyte.com/four-data-sharding-strategies-we-analyzed-in-building-a-distributed-sql-database/>
- <https://medium.com/@jeeyoungk/how-sharding-works-b4dec46b3f6>

- Data sharing helps in scalability and geo-distribution by horizontally partitioning data.
- For SQL database, a SQL table is decomposed into multiple set of rows according to a specific sharding strategy. Each of these sets of rows is called a shard. These shards are distributed across multiple server nodes.
- High availability is achieved by replicating each shard across multiple nodes.

## 1. Memcached and Redis - Algorithmic Sharding

- Each key consistently maps to the same node. This is achieved by computing a numetric hash value out of the key and computing a modulo of that hash using the total number of nodes to compute which node owns the key.

![](https://blog.yugabyte.com/wp-content/uploads/2020/01/image2.png)

- Pros:
  - Client can determine a given partition's database without any help
- Cons:
  - When a new node is added or removed, the ownership of almost all keys would be affected, resulting in a massive redistribution of all the data across nodes of the cluster.

## 2. Initial implementation in Cassandra - Linear Hash Sharding

- Linear hash sharding is a hybrid between hash and range sharding that preserves the sort order of the rows by utilizing a linear hash function instead of a regular random hash function to compute how to shard the rows.
  - A linear hash function is a hash function that maintains the relative ordering of input values while changing distribution spacing.

![](https://blog.yugabyte.com/wp-content/uploads/2020/01/image5.png)

- Pros:
  -  The type of sharding allows efficiently querying a range of rows by the primary key values while enabling pre-splitting of the table into multiple shards.
- Cons:
  - This sharding strategy was problematic because it was impossible to pick good shard split boundaries ahead of time.

> WIP: Dang doc thi tu nhien luoi qua
