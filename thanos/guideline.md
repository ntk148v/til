# Thanos Guideline

## 1. Sizing

Source: <https://krisztianfekete.org/sizing-thanos-receive-and-prometheus-storage/>

## 2. Operation note

Source: <https://blog.devops.dev/streamlining-long-term-storage-query-performance-for-metrics-with-thanos-b44419c70cc4>

> Do one component at a time

### 2.1. Thanos query

- Query is responsible to take care of queries to all Store API.
- By default, it relies on **Prometheus Query API**, which by definition, from the moment the query starts, begins by defining a series of operations in a tree-like structure to assemble the data to be returned.
- But just recently was introduced the [**Thanos Query PromQL Engine**](https://github.com/thanos-community/promql-engine), which retrieves the data in a distributed way and thus speeds up the process of query execution.
- In my case, after use Thanos PromQL Engine, the resource usage is significantly reduced. If you have trouble with the resource usage, it is worth a try here.

```shell
--query.promql-engine=thanos
```

### 2.2. Thanos compact

- Compact is about to compact and downsample metrics, but instead of doing in from memory, will do it from your Object storage of choice.
- This is necessary to allow for querying longer periods of time since it reduces the amount of retrieved data. It will also be the component where you can define the retention of the metrics in storage.

```shell
--retention.resolution-raw=90d
--retention.resolution-5m=180d
--retention.resolution-1h=1y
```

- Also if the Compact runs out of blocks to work on it it will exit. For that either define the `--wait` flag in order to keep it running and waiting for more metrics tohandle, or `--wait-interval` if you prefer to specify a specific interval.
- Always keep only **one instance running** to handle the metrics compacting and downsampling for one specific Prometheus/Object storage for that matter.
- Always ensure it has enough disk space to avoid any [halting](https://thanos.io/tip/components/compact.md/#halting) due to lack of space.
- Check the amount of resources:
  - The CPU number has to be in pair with `--compact.concurrency` flag.
  - Memory will be related to the amount of blocks.

### 2.3. Thanos store

- Store will be responsible to retrieve all data from storage based on the query's time range.
- To better handle your querying distributions you could define Sharding for Store, `--min-time`, `--max-time` flags, to have dedicated Stores for each time window.

```shell
# From now to ago to 30 days:
- min-time=30d
# From 30 days ago to 90 days:
- min-time=90d
- max-time=30d
# From 90 days ago to 1 year:
- min-time=1y
- max-time=90d
```

- You can shard in a similar way as you can do with Prometheus, with relabelings, and using hashmod or just keep or drop relabels.

```shell
  --selector.relabel-config=
    - action: hashmod
    source_labels: ["__block_id"]
    target_label: shard
    modulus: 2
    - action: keep
    source_labels: ["shard"]
    regex: 0
```

- By default, Store has in memory caching -> you can configure Memcached or Redis to handle cache instead.

### 2.4. Thanos query frontend

- Query Frontend breaks you queries into multiple short queries, also has caching built in or supported by Memcached or Redis.

```yaml
type: MEMCACHED
config:
  addresses: [memcache-host:port]
  timeout: 3s
  max_idle_connections: 1024
  max_async_concurrency: 20
  max_item_size: 30MB
  max_async_buffer_size: 10000
  max_get_multi_concurrency: 200
  max_get_multi_batch_size: 0
  dns_provider_update_interval: 10s
  expiration: 24h
```

### 2.5. Thanos receiver

- Hashring!
