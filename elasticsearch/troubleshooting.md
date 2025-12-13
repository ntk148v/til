# Troubleshooting

Source: <https://www.elastic.co/docs/troubleshoot/elasticsearch>

Table of contents:

- [1. Clusters](#1-clusters)
  - [1.1. High CPU Usage](#11-high-cpu-usage)

## 1. Clusters

### 1.1. High CPU Usage

- Elasticsearch uses thread pools to manage CPU resources for concurrent operations. High CPU usage typically means one or more thread pools are running low. If a thread pool is depleted, Elasticsearch will reject requests related to the thread pool. For example, if the search thread pool is depleted, Elasticsearch will reject search requests until more threads are available.
- Diagnose:
  - Check CPU usage.
  - Check hot threads. High CPU usage frequently correlates to a long-running task, or a backlog of tasks.
- Reduce:
  - Check JVM garbage collection: high CPU usage is often caused by excessive JVM GC activity.
    - For optimal JVM performance, garbage collection should meet these criteria:

    | GC type  | Completion time | Frequency             |
    | -------- | --------------- | --------------------- |
    | Young GC | <50ms           | ~once per 10 seconds  |
    | Old GC   | <1s             | <=once per 10 minutes |

  - You might experience high CPU usage on specific data nodes or an entire data tier if traffic isn’t evenly distributed. This is known as hot spotting.
  - Oversharding occurs when a cluster has too many shards, often times caused by shards being smaller than optimal. While Elasticsearch doesn’t have a strict minimum shard size, an excessive number of small shards can negatively impact performance. Each shard consumes cluster resources because Elasticsearch must maintain metadata and manage shard states across all nodes.
    - Aim for shard sizes between 10GB and 50GB
    - Keep the number of documents on each shard below 200 million

- To further reduce CPU load or mitigate temporary spikes in resource usage:
  - Scale your cluster.
  - Spread out bulk requests.
  - Cancel long-running searches.

### 1.2. High JVM memory pressure

- High JVM memory usage can degrade cluster performance and trigger circuit breaker errors. To prevent this, we recommend taking steps to reduce memory pressure if a node’s JVM memory usage consistently exceeds 85%.
- Check:
  - Check JVM memory pressure.
  - Check GC logs: As memory usage increases, GC becomes more frequent and takes longer.

  ```log
  [timestamp_short_interval_from_last][INFO ][o.e.m.j.JvmGcMonitorService] [node_id] [gc][number] overhead, spent [21s] collecting in the last [40s]
  ```

  - Capture a JVM heap dump: capture a heap dump of the JVM while its memory usage is high, and also capture the garbage collector logs covering the same time period.

- Reduce:
  - Reduce your shard count: Every shard uses memory. In most cases, a small set of large shards uses fewer resources than many small shards.
  - Avoid expensive searches: Expensive searches can use large amounts of memory. To better track expensive searches on your cluster, enable slow logs.
  - Prevent mapping explosions: Defining too many fields or nesting fields too deeply can lead to mapping explosions that use large amounts of memory. To prevent mapping explosions, use the mapping limit settings to limit the number of field mappings.
  - Spread out bulk requests: SWhile more efficient than individual requests, large bulk indexing or multi-search requests can still create high JVM memory pressure. If possible, submit smaller requests and allow more time between them.
  - Upgrade node memory!
