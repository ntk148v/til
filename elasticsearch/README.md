# Elasticsearch

## Limiting Memory Usage

* Once analyzed strings have been loaded into fielddata -> sit there until evicted (or node crashed) -> **Check memory usage**
* Query, return 100 hits, but fielddata will be loaded for **all** documents.
* Load all fielddata structure values once, keep in memory.
* The JVM heap - choose a Heap Size - $ES\_HEAP\_SIZE
    * Check JVM heap:

    ```
    GET /_nodes/stats/jvm?pretty
    ```

    * **No more than 50% of available RAM**: Lucense makes good use of the filesystem cache, which are managed by the kernel. Without enough filesystem cache space, performance will suffer.
    * **No more than 32GB**: If the heap < 32 GB, the JVM can use compressed pointers which saves a lot of memory: 4 bytes per pointers instead of 8 bytes.
    * **Swapping is the Death of Performance**: An in-memory operation is one that needs to execute quickly. If memory swaps to disk, 100-microsecond operation becomes one that take 10 milliseconds. The best thing to do is disable swap completely.
* Fielddata Size: the `indices.fielddata.cache.size` controls how much heap space is allocated to fielddata.
* Monitoring fielddata:
    * per-index using the `indices-stats API`:
    
    ```
    GET /_stats/fielddata?fields=*
    ```

    * per-node using the `nodes-stats API`:
    
    ```
    GET /_nodes/stats/indices/fielddata?fields=*
    ```

    * Or even per-index per-node:
    
    ```
    GET /_nodes/stats/indices/fielddata?level=indices&fields=*
    ```

* Circuit Breaker
* Refs:
    * [Limiting Memory Usage](http://www.elastic.co/guide/en/elasticsearch/guide/current/_limiting_memory_usage.html)

## Tracking in-sync shard copies

* Elasticsearch provides failover capabilities by keep multiple copies of your data in the cluster.

## Monitoring Individual Nodes

* [Source](https://www.elastic.co/guide/en/elasticsearch/guide/current/_monitoring_individual_nodes.html)
* `node-stats` API:

```
GET _nodes/stats
```

### indices Section

```json
"indices": {
        "docs": {   # docs show how many documents reside on this node, as well as the number deleted docs that haven't been purged from segment yet.
           "count": 6163666,
           "deleted": 0
        },
        "store": { # How much physical storage is consumed by the node.
           "size_in_bytes": 2301398179,
           "throttle_time_in_millis": 122850
        },
        "indexing": { # Show the number of docs that have been indexed.
           "index_total": 803441,
           "index_time_in_millis": 367654,
           "index_current": 99,
           "delete_total": 0,
           "delete_time_in_millis": 0,
           "delete_current": 0
        },
        "get": {
           "total": 6,
           "time_in_millis": 2,
           "exists_total": 5,
           "exists_time_in_millis": 2,
           "missing_total": 1,
           "missing_time_in_millis": 0,
           "current": 0
        },
        "search": {
           "open_contexts": 0,
           "query_total": 123,
           "query_time_in_millis": 531,
           "query_current": 0,
           "fetch_total": 3,
           "fetch_time_in_millis": 55,
           "fetch_current": 0
        },
        "merges": {
           "current": 0,
           "current_docs": 0,
           "current_size_in_bytes": 0,
           "total": 1128,
           "total_time_in_millis": 21338523,
           "total_docs": 7241313,
           "total_size_in_bytes": 5724869463
        },
```

### OS and process sections

### JVM Section

```
"jvm": {
    "timestamp": 1408556438203,
    "uptime_in_millis": 14457,
    "mem": { # General stas about heap memory usage
       "heap_used_in_bytes": 457252160,
       "heap_used_percent": 44, # Elasticsearch is configured to initiate GCs when the heap reachs 75% full. If heap_used_percent >=75%, memory pressure. if heap_used_percent >- 85%, trouble. if heap_used_percent >= 90-95%, very bad.
       "heap_committed_in_bytes": 1038876672,
       "heap_max_in_bytes": 1038876672,
       "non_heap_used_in_bytes": 38680680,
       "non_heap_committed_in_bytes": 38993920,
    ...
    "pools": { # Memory usage of each generation in the GC.
        "young": {
            "used_in_bytes": 138467752,
            "max_in_bytes": 279183360,
            "peak_used_in_bytes": 279183360,
            "peak_max_in_bytes": 279183360
        },
        "survivor": {
            "used_in_bytes": 34865152,
            "max_in_bytes": 34865152,
            "peak_used_in_bytes": 34865152,
            "peak_max_in_bytes": 34865152
        },
        "old": {
            "used_in_bytes": 283919256,
            "max_in_bytes": 724828160,
            "peak_used_in_bytes": 283919256,
            "peak_max_in_bytes": 724828160
        } 
    }
    ...
    "gc": { # Show the garbage collection counts and cumulative time for both young & old generations.
        "collectors": {
           "young": {
              "collection_count": 13,
              "collection_time_in_millis": 923
           },
           "old": {
              "collection_count": 0,
              "collection_time_in_millis": 0
           }
        }
    }
},
```

### Threadpool Section

* Maintains threadpools internally.

```
"index": {
    "threads": 1, # number of threads
    "queue": 0, # How many work untils are sitting in a queue
    "active": 0, # How many of those threads are actively processing somw work
    "rejected": 0,
    "largest": 1,
    "completed": 1
}
```

* Keep an eye on:
    * "indexing": Threadpool for normal indexing requests
    * "bulk": Bulk requests, which are distinct from the nonbuilk indexing requests
    * "get": Get-by-ID operations
    * "search": All search and query requests
    * "merging": Threadpool dedicated to manager Lucene merges

### FS and Network Sections (WIP)

### Circuit Breaker (WIP)

## How to monitor Elasticsearch performance

* Refs:
    * [How to monitor Elasticsearch performance](https://www.datadoghq.com/blog/monitor-elasticsearch-performance-metrics/)
