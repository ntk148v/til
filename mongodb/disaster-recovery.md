# Disaster Recovery

Source:

- <http://s3.amazonaws.com/info-mongodb-com/MongoDB_Multi_Data_Center.pdf>
- <https://www.mongodb.com/developer/products/mongodb/active-active-application-architectures/>

Table of contents:

- [Disaster Recovery](#disaster-recovery)
  - [1. Backup and Restore](#1-backup-and-restore)
  - [2. mongosync](#2-mongosync)
  - [3. Replication](#3-replication)
  - [3. Sharding](#3-sharding)

MongoDB provides several options for Disaster Recovery.

## 1. Backup and Restore

- MongoDB built-in tools `mongodump` and `mongorestore` work with BSON data dumps, and are useful for [creating a point-in-time backup of your data and restoring it in case of a disaster](https://www.mongodb.com/docs/manual/tutorial/backup-and-restore-tools/).
- Performance considerations: `mongodump` and `mongorestore` operate by interracting with a running `mongod` instance, they can impact the performance of your running database. Not only do the tools create traffic for a running database instance, they also force the data to read all data through memory.
- You can also use third-party backup tools like [MongoDB Ops Manager](https://www.mongodb.com/docs/ops-manager/current/tutorial/nav/backup-use/) to automate the backup and restore process.
- Best practices:
  - It's better to use BSON when backing up and restoring.
  - You don't need to explicitly create a MongoDB database, as it will be automatically created when you specify a database to import from.
  - Use secondary servers for backup as this helps avoid degrading the performance of the primary node.
  - Time the backup of data sets around periods of low bandwidth/traffic. Backups can take a long time, especially if the data sets are quite large.
  - Use a [replica set connection string](https://docs.mongodb.com/manual/reference/connection-string/) when using unsupervised scripts.
  - Use `--oplog` to capture incoming write operations during the {{out_tool}} operation to ensure that the backups reflect a consistent data state.
  - Ensure that your backups are usable by restoring them to a test MongoDB deployment.
- We can automate backup process using crontab.
- Pros:
  - Simple
- Cons:
  - Performance impact.
  - Potential data loss.
  - Require manual actions.

## 2. mongosync

- We can use [mongosync for Disaster Recovery](https://www.mongodb.com/docs/cluster-to-cluster-sync/current/reference/disaster-recovery/).
- Setting up Cluster-to-Cluster Sync to prepare for disaster recovery follows thesame procedure as other [connections](https://www.mongodb.com/docs/cluster-to-cluster-sync/current/connecting/#std-label-c2c-connecting) between clusters.

![](https://webimages.mongodb.com/_com_assets/cms/l3vrj3vkdvt6vwze2-Screen%20Shot%202022-06-01%20at%209.47.40%20AM.png?auto=format%252Ccompress)

- Synchronization keeps the destination cluster up to date with the source clulster and ready as backup. In the event that the source cluster fails or becomes otherwise unavailable, the destination cluster can replace it as the primary cluster.
- Cluster-to-Cluster Sync is now Generally Available as part of MongoDB 6.0. Currently, Cluster-to-Cluster Sync is compatible only with source and destination clusters that are running on MongoDB 6+.
- Pros:
  - Simple.
  - Full control of Synchronization process by deciding when to start, stop, pause, resume,or reverse the direction of synchronization.
- Cons:
  - MongoDB 6+.
  - Potential data loss.
  - Questionable: Performance impact?
  - Require manual actions: switch between clusters.

## 3. Replication

- [Distributing replica set members across geographically distinct data centers](https://www.mongodb.com/docs/manual/core/replica-set-architecture-geographically-distributed/) adds redundancy and provides fault tolerance if one of the data centers is unavailable.
- Keep at least one member in an alternative data center. If possible, use an odd number of data centers, and choose a distribution of members that maximizes thelikehood that even with a loss of a data center, the remaining replica set members can form a majority or at minimum, provide a copy of your data.
- In a two data center distribution:
  - If one of the data centers goes down, the data is still available for reads unlike a single data center distribution.
  - If the data center with a minority of the members goes down, the replica set can still serve write operations as well as read operations.
  - However, if the data center with the majority of the members goes down, the replica set becomes read-only.

- If possible, _distribute members across at least three data centers_. If the cost of thrid data center is prohibitive, one distribution possibility is to evenly distribute the data bearing members across the two data centers and store the remaining member in the cloud if your company policy allows.

![](https://www.mongodb.com/docs/manual/images/replica-set-three-data-centers.bakedsvg.svg)

- Example:
  - _Three-member replica set_:
    - Two data centers: two members to Data Center 1 and one member to Data Center 2. If one of the members of the replica set is an arbiter, distribute the arbiter to Data Center 1 with a data-bearing member.
      - If one of the data centers goes down, the data is still available for reads unlike a single data center distribution.
      - If Data Center 1 goes down, the replica set becomes read-only.
      - If Data Center 2 goes down, the replica set remains writeable as the members in Data Center 1 can create a majority.
    - Three data centers: two member to Data Center 1, two members to Data Center 2, and one member to site Data Center 3.
      - If any Data Center goes down, the replica set remains writable as the remaining members can hold an election.
  - _Five-member replica set_:
    - Two data centers: Three members to Data Center 1 and two members to Data Center 2.
    - Three data centers: two member to Data Center 1, two members to Data Center 2, and one member to site Data Center 3.
- Pros:
  - Data is replicated across data centers.
  - Replica sets are self-healing as failover and recovery is fully automated.
- Cons:
  - You may have only 2 data centers, so you have to bring up the primary node as soon as possible.

## 3. Sharding

- MongoDB provides horizontal scaling for databases using a technique called [sharding](https://docs.mongodb.org/manual/core/sharding-introduction/), allowing MongoDB deployment to scale beyond the hardware limitations of a single server.
- Sharding distributes data across multiple physical partitions called shards. Shards can be located within a single data center or distributed across multiple data centers -> _Sharding is another option for disaster recovery in MongoDB_.
- A MongoDB sharded cluster consists of the following components:
  - `shard`: Each shard contains a subset of the sharded data. Each shard can be deployed as a `replica set`.
  - `mongos`: The `mongos` acts as a query router, providing an interface between client applications and the sharded cluster. Starting in MongoDB 4.4, mongos can support hedged reads to minimize latencies.
  - `config servers`: Config servers store metadata and configuration settings for the cluster.

![](https://www.mongodb.com/docs/manual/images/sharded-cluster-production-architecture.bakedsvg.svg)

- Configure Shards across data centers:
  - Range-based sharding:
    - Ranged sharding involves dividing data into ranges based on the shard key values. Each chunk is then assigned a range based on the shard key values.

    ![](https://www.mongodb.com/docs/manual/images/sharding-range-based.bakedsvg.svg)

  - Hash-based sharding:
    - Hashed Sharding involves computing a hash of the shard key field's value. Each chunk is then assigned a range based on the hashed shard key values.

    ![](https://www.mongodb.com/docs/manual/images/sharding-hash-based.bakedsvg.svg)

  - Zones sharding:
    - Zones can help improve the locality of data for sharded clusters that span multiple data centers.
    - In sharded clusters, you can create [zones](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-zone) of sharded data based on the shard key. You can associate each zone with one or more shards in the cluster.

    ![](https://www.mongodb.com/docs/manual/images/sharded-cluster-zones.bakedsvg.svg)

- Pros:
  - Performance: low latency reads and writes (reads and writes on nodes in a data center local to the application) (Active-Active).
  - High Availability.
  - Eventually consistent
  - Minimal data loss and down time.
- Cons:
