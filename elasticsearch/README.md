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

## How to monitor Elasticsearch performance

* Refs:
    * [How to monitor Elasticsearch performance](https://www.datadoghq.com/blog/monitor-elasticsearch-performance-metrics/)
