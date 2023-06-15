# Redis cluster

Source:

- <https://redis.io/topics/cluster-tutorial>
- <https://redis.io/topics/cluster-spec>
- <http://intro2libsys.info/introduction-to-redis/clustering-and-ha>
- <https://aws.amazon.com/blogs/database/work-with-cluster-mode-on-amazon-elasticache-for-redis/>
- <https://developer.redis.com/operate/redis-at-scale/scalability/redis-cluster-and-client-libraries/>

Table of contents:

- [Redis cluster](#redis-cluster)
  - [1. Overview](#1-overview)
  - [2. Communication](#2-communication)
  - [3. Docker](#3-docker)
  - [4. Data sharding](#4-data-sharding)
  - [5. Master-slave model](#5-master-slave-model)
  - [6. Consistency guarantees](#6-consistency-guarantees)
  - [7. Client](#7-client)

## 1. Overview

- Redis cluster provides a way to run a Redis installation where data is **automatically shared across multiple Redis nodes**.
- Advantages:
  - Horizontally scalable.
  - Auto data sharding.
  - Fault tolerant.
  - Decentralized cluster management system.

## 2. Communication

- Redis cluster node requires 2 TCP connections open:
  - Port used to serve client (`6379`) + all the other cluster nodes (that use the client port for key migrations).
  - Cluster bus port (`<client port> + 10000`): node-to-node communcation channel using a binary protocol.

## 3. Docker

- In order to make Docker compatible with Redis cluster, need to use **host networking mode** of Docker (`--net=host`).

## 4. Data sharding

- Redis cluster uses **hash slot**.
- There are **16,384** hash slots available. Those slots are divided amongst the total number of shards in the cluster.

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2019/07/26/ClusterModeElasticache2.png)

- The client calculates which hash slot to use via:

```
HASH_SLOT = CRC16(key) mod 16384
```

- Moving hash slots from a node to another doesn't require to stop operations, adding and removing nodes, or changing percentage of hash slots hold by notes, doesn't require any downtime.
- The client can force multiple keys to be part of the same hash slot by using a concept called **hash tags**.

## 5. Master-slave model

- Every hash slot has from 1 (the master itself) to N replicas (N-1 additional slave nodes).
  - Master One (M1) - Slave One (S1): S1 replicates M1, is promoted if a quorum of nodes cannot reach M1.
  - If M1 and S2 fail at the same time, Redis cluster is not able to continue to operate.

![](http://intro2libsys.info/introduction-to-redis/static/img/six-node-redis-cluster.png)

## 6. Consistency guarantees

- Not able to guarantee **strong consistency**, may lose writes.
- During writes the following happens:
  - Client writes to the master A.
  - The master A replies OK to client.
  - The master A propagates the write to its slave A1, A2, A3. A doesn't wait for an ACK from A1, A2, A3 before replying to the client.
- There is a trade-off to be made between performance and consistency.

## 7. Client

- To use a client library with Redis Cluster, the client libraries need to be cluster-aware. Clients that support Redis Cluster typically feature a special connection module for managing connections to the cluster. The process that some of the better client libraries follow usually goes like this:

  - The client connects to any shard in the cluster and gets the addresses of the rest of the shards. The client also fetches a mapping of hash slots to shards so it can know where to look for a key in a specific hash slot.

  ![](https://s3.us-east-2.amazonaws.com/assets-university.redislabs.com/ru301/4.4/image1.png)

  - When the client needs to read/write a key, it first runs the hashing function (crc16) on the key name and then modulo divides by 16384, which results in the key’s hash slot number.
  - In the example below the hash slot number for the key “foo” is 12182. Then the client checks the hash slot number against the hash slot map to determine which shard it should connect to. In our example, the hash slot number 12182 lives on shard 127.0.0.1:7002.
  - Finally, the client connects to the shard and finds the key it needs to work with.

  ![](https://s3.us-east-2.amazonaws.com/assets-university.redislabs.com/ru301/4.4/image2.png)
