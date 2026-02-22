# Benchmarking and sizing your Elasticsearch cluster for logs and metrics

Source: <https://www.elastic.co/blog/benchmarking-and-sizing-your-elasticsearch-cluster-for-logs-and-metrics>

Table of contents:

- [Benchmarking and sizing your Elasticsearch cluster for logs and metrics](#benchmarking-and-sizing-your-elasticsearch-cluster-for-logs-and-metrics)
  - [1. Computing resource basics](#1-computing-resource-basics)
  - [2. Sizing by data volume](#2-sizing-by-data-volume)
  - [3. Benchmarking](#3-benchmarking)
    - [3.1. Index benchmark](#31-index-benchmark)
    - [3.2. Search benchmark](#32-search-benchmark)

## 1. Computing resource basics

- **Storage**: Where data persists
  - SSDs are recommended whenever possible, in particular for nodes running search and index operations. Due to the higher cost of SSD storage, a hot-warm architecture is recommended to reduce expenses.
  - When operating on bare metal, local disk is king!
  - Elasticsearch does not need redundant storage (RAID 1/5/10 is not necessary), logging and metrics use cases typically have at least one replica shard, which is the minimum to ensure fault tolerance while minimizing the number of writes.
- **Memory**: Where data is buffered
  - JVM heap: stores metadata about the cluster, indices, shards, segments, and fielddata. This is ideally set to 50% of available RAM.
  - OS cache: Elasticsearch will use the remainder of available memory to cache data, improving performance dramatically by avoiding disk reads during full-text search, aggregations on doc values, and sorts.
- **Compute**: Where data is processed
  - Elasticsearch nodes have thread pools and thread queues that use the available compute resources. The quantity and performance of CPU cores governs the average speed and peak throughput of data operations in Elasticsearch.
- **Network**: Where data is transfered
  - The network performance — both bandwidth and latency — can have an impact on the inter-node communication and inter-cluster features like cross-cluster search and cross-cluster replication.

## 2. Sizing by data volume

For metrics and logging use cases, we typically manage a huge amount of data, so it makes sense to use the data volume to initially size our Elasticsearch cluster.

- How much raw data (GB) we will index per day?
- How many days we will retain the data?
- How many days in the hot zone?
- How many days in the warm zone?
- How many replica shards will you enforce?

> [!important]
>
> - **Total Data (GB)** = Raw data (GB) per day \* Number of days retained \* (Number of replicas + 1) \* Indexing/Compression Factor
> - **Total Storage (GB)** = Total data (GB) \* (1 + 0.15 disk Watermark threshold + 0.1 Margin of error)
> - **Total Data Nodes** = ROUNDUP(Total storage (GB) / Memory per data node / Memory:Data ratio)
>
>   In case of large deployment it's safer to add a node for failover capacity.
>
>   1.2 is an average ratio we have observed with throughout deployments.To get the value that relates to your data, index logs and metrics and divide the index size (without replica) by the raw volume size.

## 3. Benchmarking

Now that we have our cluster(s) sized appropriately, we need to confirm that our math holds up in real world conditions. To be more confident before moving to production, we will want to do benchmark testing to confirm the expected performance, and the targeted SLA.

For this benchmark, we will use the same tool our Elasticsearch engineers use Rally. This tool is simple to deploy and execute, and completely configurable so you can test multiple scenarios.

### 3.1. Index benchmark

For the indexing benchmarks we are trying to answers the following questions:

- What is the maximum indexing throughput for my clusters?
- What is the data volume that I can index per day?
- Is my cluster oversized or undersized ?

### 3.2. Search benchmark

For the search, we will execute three benchmarks:

- Service time for queries.
- Service time for parallel queries.
- Index rate and service time with parallel indexing.
