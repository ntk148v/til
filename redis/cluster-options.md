# Redis Clustering options

Source:

- <https://redis.com/blog/why-migrate-dynomite-database-to-redis-enterprise-active-active-database/>
- <https://segmentfault.com/a/1190000040083625/en>
- <https://www.alibabacloud.com/forum/read-822>
- <https://groups.google.com/g/redis-db/c/f39An0E5XUs>
- <https://redis.com/redis-enterprise/technology/active-active-geo-distribution/>
- <https://www.slideshare.net/cihangirb/cross-data-center-replication-with-redis-using-redis-enterprise>

Table of contents:

- [Redis Clustering options](#redis-clustering-options)
  - [0. Scenario \& Requirement](#0-scenario--requirement)
  - [1. Redis Cluster](#1-redis-cluster)
  - [2. Dynomite](#2-dynomite)
  - [3. Codis](#3-codis)
  - [4. Twemproxy](#4-twemproxy)
  - [5. Roshi](#5-roshi)
  - [6. Redis Enterprise](#6-redis-enterprise)

## 0. Scenario & Requirement

- We have two datacenters which run concurrently (both serve traffic) -> Active/Active.
- We want to deploy Redis cluster solution to cross datacenters replication.
- Assume network conditions allow for cross datacenters replication.
- Key considerations:
  - Consistency guarantees.
  - Performance.
  - Redis's features supported.
  - Automatically failover.
  - High availability.
  - Scalability.
  - Manageability.

## 1. Redis Cluster

- Redis cluster provides a way to run a Redis installation where data is automatically sharded across multiple Redis nodes. Redis cluster also provides some degree of _availability_ during partitions.
- However, _the cluster will become unavailable in the event of large failures (for example, when the majority of masters are unavailable)_.
- Take a look at [cluster note](./cluster.md).
- Redis cluster master-replica model:
  - We can leverage this model to deploy cross datacenter cluster.
  - For example, we have a cluster with 3 master nodes A, B, C. Each one has two replicas: A1, A2; and so on.
  - Master and its replicas have to be placed in the different datacenter. So, if one goes down, the replica can be promoted to master.
- To use a client library with Redis Cluster, the client libraries need to be cluster-aware. Clients that support Redis Cluster typically feature a special connection module for managing connections to the cluster.
- _Consistency_ guarantees:
  - Does not guarantee strong consistency.
  - Asynchronous replication.
  - Client writes to master B -> B (OK).
  - B propagates the write to its replicas B1, B2 and B3.
  - _Trade-off between performance and consistency_.
- Undirectional replication.
- _Scalability_:
  - We can scale in/scale out.
  - Add/Remove nodes -> reshard -> rebalance.
  - The cluster continues serving incoming requests.
  - Check out [Linear Scaling](https://redis.com/redis-enterprise/technology/linear-scaling-redis-enterprise/).
- Simple to deploy.

## 2. Dynomite

- Dynomite was developed by a team of engineers at Netflix and released as open source.
- A typical Dynomite cluster can be described as follows:
  - It spans across multiple data centers
  - A single datacenter is a group of racks
  - A rack is a group of nodes: each rack holds the entire dataset, which is partitioned across multiple nodes in that rack.

![](https://redis.com/wp-content/uploads/2022/03/image1-3.png)

- Dynomite is a peer-to-peer distribution layer, therefore a client can send write traffic to any node in a Dynomite cluster.
  - If the node is the one responsible for the data, then the data is written to its local Redis OSS server process, then asynchronously replicated to other racks in the cluster across all data centers.
  - If the node does not own the data, it acts as a coordinator and sends the write to the node owning the data in the same rack. It also replicates the writes to the corresponding nodes in other racks and DCs.
- Some of Redis commands and data types are rendered unavailable or limited by Dynomite:

![](https://redis.com/wp-content/uploads/2022/03/image3-2-1024x483.png)

- You can find a complete list of supported and unsupported commands with Dynomite [here](https://github.com/Netflix/dynomite/blob/dev/notes/redis.md).
- _High availability_:
  - When a node fails within a Dynomite rack, writing and reading to the rack becomes impossible. This means that an application writing locally needs to andle the failover to another rack by itself ([Dyno](https://github.com/Netflix/dyno) client can handle failovers to remote racks when a local Dynomite node fails).
  - When the node comes back up, any data that has been written on remote racks during the failure will be missing from the failed node.
- _Scalability_:
  - Dynomite allows you to scale Redis while maintaining good performance in terms of latency.
  - [Benchmark](http://netflix.github.io/dynomite/3.2%20Dynomite-with-Redis-on-AWS---Benchmarks/).
- Manageability:
  - Dynomite-manager.

## 3. Codis

- Codis is a proxy based high performance Redis cluster solution written in Go.

![](https://raw.githubusercontent.com/CodisLabs/codis/master/doc/pictures/architecture.png)

- _Mangeability_:
  - GUI website dashboard & admin tools.
- Codis has a lot of component -> Complex deployment.
  - codis-proxy: mainly responsible for forwarding the read and write requests
  - codis-dashbaord: a unified control center that integrates functions such as data forwarding rules, automatic fault recovery, online data migration, node expansion and contraction, and automated operation and maintenance APIs
  - codis-group: Redis Server based on the secondary development of Redis 3.2.8 version, adding asynchronous data migration function
  - codis-fe: UI interface for managing multiple clusters
- At this time, Codis has been no longer maintained, so [Redis version 3.2.8](https://github.com/CodisLabs/codis/blob/master/doc/tutorial_en.md) can only be used when using Codis, which is a pain point.
- _Support online node expansion_.
- Some commands [are not supported](https://github.com/CodisLabs/codis/blob/master/doc/unsupported_cmds.md), for example: Pub/Sub.

## 4. Twemproxy

## 5. Roshi

## 6. Redis Enterprise

- After all, these above solutions are opensource. There is no guarantee that something won't be broken.
- Redis Enterprise Cluster:
  - [Shared nothing architecture](https://redis.com/redis-enterprise/technology/redis-enterprise-cluster-architecture/)
  - Fully compatible with open source commands & data structures: Simply change your connection string to Redis enterprise.
- Distribution:
  - [Active-Passive Database Geo-Distribution](https://redis.com/redis-enterprise/technology/active-passive-geo-distribution/):
    - Replica Of - Source DB to Destination DB across WAN.
  - [Active-Active Database Geo-Distribution](https://redis.com/redis-enterprise/technology/active-active-geo-distribution/):
    - Multi-Master Database with Concurrent Active-Active Writes using CRDTs.
    - Consistency model: local CRDB -> near strong consistentcy. global CRDB -> strong eventual consitency.
