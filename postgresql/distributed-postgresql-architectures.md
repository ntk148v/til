# An Overview of Distributed PostgreSQL Architectures

Source:

- <https://www.crunchydata.com/blog/an-overview-of-distributed-postgresql-architectures>
- <https://www.postgresql.eu/events/pgconfeu2023/sessions/session/4826-postgresql-distributed-architectures-best-practices/>

Table of content:

- [An Overview of Distributed PostgreSQL Architectures](#an-overview-of-distributed-postgresql-architectures)
  - [1. Single machine PostgreSQL](#1-single-machine-postgresql)
  - [2. Goals of a Distributed Database architecture](#2-goals-of-a-distributed-database-architecture)
  - [3. The importance of latency in OLTP systems](#3-the-importance-of-latency-in-oltp-systems)
  - [4. PostgreSQL distributed architectures](#4-postgresql-distributed-architectures)
    - [4.1. Network-attached block storage](#41-network-attached-block-storage)
    - [4.2. Read replicas](#42-read-replicas)
    - [4.3. DBMS-optimized cloud storage](#43-dbms-optimized-cloud-storage)
    - [4.4. Active-active](#44-active-active)
    - [4.5. Transparent sharding](#45-transparent-sharding)
    - [4.6. Distributed key-value storage with SQL](#46-distributed-key-value-storage-with-sql)

## 1. Single machine PostgreSQL

- The simplest possible architecture: running PostgreSQL on a single machine, or "node".
- Pros: Incredibly fast, performant and cost-efficient choice.
- Cons: Operational hazards
  - If machine fails, there's inevitably some kind of downtime.
  - If the disk fails, you're likely facing some data loss.
  - An overloaded system can be difficult to scale (scale up has its limit).
- Distributed PostgreSQL architectures -> address the operational hazards of a single machine. In doing so, they do lose some of its efficiency, and especially the low latency.

## 2. Goals of a Distributed Database architecture

- The goal is to try to meet the availability, durability, performance, regulatory, and scale requirements of large organizations, subject the physics.
- Mechanisms:
  - Replication: Place copies of data on different machines.
  - Distribution: Place partitions of data on different machines.
  - Decentralization: Place different DBMS activities on different machines.

## 3. The importance of latency in OLTP systems

- PostgreSQL uses a synchronous, interactive protocol where transactions are performed step-by-step. The client waits for the database to answer before sending the next command, and the next command might depend on the answer to the previous.
- Any network latency between client and database server will already be a noticeable factor in the overall duration of a transaction.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/41566cae-dec8-4d8d-9b32-a8c23cb70200/public)

- If transactions take on average 20ms, then a single (interactive) session can only do 50 transactions per second -> need a lot concurrent sessions to actually achieve high throughput.
- Having many sessions -> each session uses significant resources like memory on the database server -> PostgreSQL set ups t limit the maximum number of sessions -> a hard limit on achievable transaction throughput when network latency is involved.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/f094a883-daa1-4a52-caa5-5590bce9fe00/public)

## 4. PostgreSQL distributed architectures

### 4.1. Network-attached block storage

- The database server typically runs in a virtual machine in a Hypervisor, which exposes a block device to the VM. Any reads and writes to the block device will result in network calls to a block storage API. The block storage service internally replicates the writes to 2-3 storage nodes.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/4cd769ee-098e-4f1e-072c-1b15dcfcb500/public)

- Pros:
  - Higher durability (replication)
  - Higher uptime (replace VM, reattach)
  - Fast backups and replica creation (snapshots)
  - Disk is resizable
- Cons:
  - High disk latency (~20μs -> ~1000μs)
  - Lower IOPS (~1M -> ~10k IOPS)
  - Crash recovery on restart takes time
  - Cost can be high
- Guideline: the durability and availability benefits of network-attached storage usually outweigh the performance downsides.

### 4.2. Read replicas

- PostgreSQL has built-in support for physical replication to read-only replicas. The most common way of using replica is to set it up as a hot standby that takes over when the primary fails in a high-availability set up.
- Another common use of read replica is to help you scale read throughput when reads are CPU or I/O bottlenecked by load balancing queries across replicas, which achieves linear scalability of reads and also offloads the primary, which speeds up write.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/67558330-e428-41c2-a876-3d6fe88ba000/public)

- Pros:
  - Read throughput scales linearly
  - Low latency state reads if read replica is closer than primary
  - Lower load on primary
- Cons:
  - Eventual read-your-writes consistency
  - No monotonic read consistency
  - Poor cache usage
- Guideline: Consider using read replicas when you need >100K reads/sec or observe a CPU bottleneck due to reads.

### 4.3. DBMS-optimized cloud storage

- A DBMS normally performs every write in two different ways: immediately to the write-ahead log (WAL),and in the background to a data page (or several pages, when indexes are involved).
- In the DBMS-optimized storage architecture the background pages writes are performed by the storage layer instead, based on the incoming WAL -> reduce the amount of write I/O on the primary node.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/8f4c2648-db97-40f8-1581-7d4a6ce0fa00/public)

- Pros:
  - Potential performance benefits by avoiding page writes from primary
  - Replicas can reuse storage, incl. hot standby
  - Can do faster reattach, branching than network-attached storage.
- Cons:
  - Write latency is high by default
  - High cost/pricing
  - PostgreSQL is not designed for it, not OSS
- Guideline: Can be beneficial for complex workloads, but important to measure whether price-performance under load is actually better than using a bigger machine.

### 4.4. Active-active

- Any node can locally accept writes without coordination with other nodes. It is typically used with replicas in multiple sites, each of which will then see low read and write latency, and can survive failure of other sites.
- Pros:
  - Very high read and write availability
  - Low read and write latency
  - Read throughput scales linearly
- Cons:
  - Eventual read-you-writes consistency
  - No monotonic read consistency
  - No linear history (update might conflicts after commit)
- Guideline: Consider only for very simple workloads (e.g. queues) and only if you really need the benefits.

### 4.5. Transparent sharding

- Distribute tables by a shard key and/or replicate tables across multiple primary nodes. Each node shows the distributed tables as if they were regular PostgreSQL tables and queries & transactions are transparently routed or parallelized across nodes.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/1cb5e4db-c901-40e3-5327-73a5c6caa500/public)

- Pros:
  - Scale throughput for reads & writes (CPU & IOPS)
  - Scale memory for large working sets
  - Parallelize analytical queries, batch operations
- Cons:
  - High read and write latency
  - Data model decisions have high impact on performance
  - Snapshot isolation concessions
- Guideline: Use for multi-tenant apps, otherwise use for large working set (>100GB) or compute heavy queries.

### 4.6. Distributed key-value storage with SQL

- Open source alternatives like CockroachDB and Yugabyte followed a similar approach with Google Spanner without the requirements of synchronized clocks, at the cost of significiantly higher latency.
- Tables are then stored in the key-value store, with the key being a combination of the table ID and the primary key. The SQL engine is adjusted accordingly, distributing queries where possible.

![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/de7bc03c-8f80-4384-383a-0d38dde0d800/public)

- Pros:
  - Good read and write availability (shard-level failover)
  - Single table, single key operations scale well
  - No additional data modeling steps or snapshot isolation concessions
- Cons:
  - Many internal operations incur high memory
  - No local joins in current implementations
  - Not actually PostgreSQL, and less mature and optimized
