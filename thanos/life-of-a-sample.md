# Life of a Sample in Thanos, and How to Configure it

Source:

- <https://thanos.io/blog/2023-11-20-life-of-a-sample-part-1/>
- <https://thanos.io/blog/2023-11-20-life-of-a-sample-part-2/>

> I only note the main idea what I think worth to be noted. For detail, check out the original posts.

## 1. Sending sample to Thanos

- Thanos Receive exposes a remote-write endpoint that Prometheus servers can use to transmit metrics. The only prerequisite on the client side is to configure the remote write endpoint on each Prometheus server, a feature natively supported by Prometheus.
- The remote-write protocol is based on POST request. The payload consists of a protobuf message containing a list of time-series samples and labels. Generally, a payload contains at most one sample per time series and spans numerous time series. Metrics are typically scraped every 15 seconds, with a maximum remote write delay of 5 seconds to minimize latency, from scraping to query availability on the receiver.
- Each [remote write](https://prometheus.io/docs/practices/remote_write/) destination starts a queue which reads from the write-ahead log (WAL), writes the samples into an in memory queue owned by a shard, which then sends a request to the configured endpoint. The flow of data looks like:
  - Once samples are extracted from the WAL, they are aggregated into parallel queues (shards) as remote-write payloads.
  - When a queue reaches its limit or a maximum timeout is reached, the remote-write client stops reading the WAL and dispatches the data.
  - The cycle continues. The parallelism is defined by the number of shards, their number is dynamically optimized.

```text
      |-->  queue (shard_1)   --> remote endpoint
WAL --|-->  queue (shard_...) --> remote endpoint
      |-->  queue (shard_n)   --> remote endpoint
```

![](https://thanos.io/v0.40/blog/img/life-of-a-sample/remote-write.png)

- Key points to consider:
  - **The send deadline setting**: `batch_send_deadline` should be set to around 5s to minimize latency. This timeframe strikes a balance between minimizing latency and avoiding excessive request frequency that could burden the Receiver. While a 5-second delay might seem substantial in critical alert scenarios, it is generally acceptable considering the typical resolution time for most issues.
  - The backoff settings: The `min_backoff` should ideally be no less than 250 milliseconds, and the max_backoff should be at least 10 seconds. These settings help prevent Receiver overload, particularly in situations like system restarts, by controlling the rate of data sending.
- In scenarios where you have limited control over client configurations, it becomes essential to shield the Receive component from potential misuse or overload. The Receive component includes several configuration options designed for this purpose.

![](https://thanos.io/v0.40/blog/img/life-of-a-sample/receive-limits.png)

- Keys to consider:
  - **Series and samples limits**: Typically, with a standard target scrape interval of 15 seconds and a maximum remote write delay of 5 seconds, the `series_limit` and `samples_limit` tend to be functionally equivalent. However, in scenarios where the remote writer is recovering from downtime, the `samples_limit` may become more restrictive, as the payload might include multiple samples for the same series.
  - **Handling request limits**: If a request exceeds these limits, the system responds with a 413 (Entity Too Large) HTTP error.
  - **Active series limiting**: The limitation on active series persists as long as the count remains above the set threshold in the Receivers’ TSDBs. Active series represent the number of time series currently stored in the TSDB’s (Time Series Database) head block. The head block is the in-memory portion of the TSDB where incoming samples are temporarily stored before being compacted into persistent on-disk blocks. The head block is typically compacted every two hours. This is when stale series are removed, and the active series count decreases. Requests reaching this limit are rejected with a 429 (Too Many Requests) HTTP code, triggering retries.

## 2. Receiving samples with high availability and durability

- The need for multiple receive instances: Relying on a single instance of Thanos Receive is not sufficient for two main reasons:
  - Scalability: As your metrics grow, so does the need to scale your infrastructure.
  - Reliability: If a single Receive instance falls, it disrupts metric collection, affecting rule evaluation and alerting. Furthermore, during downtime, Prometheus servers will buffer data in their Write-Ahead Log (WAL). If the outage exceeds the WAL’s retention duration (default is 2 hours), this can lead to data loss.
- To achieve high availability, it is necessary to deploy multiple Receive replicas -> crucial to maintain consistency in sample ingestion (samples from a given time series should always be ingested by the same Receive instance) -> uses a hashring.
  - When clients send data, they connect to any Receive instance, which then routes the data to the correct instances based on the hashring. This is why the Receive component is also known as the IngestorRouter.
  - There're two possible hashrings:
    - **hashmod**: This algorithm distributes time series by hashing labels modulo the number of instances. The downside is that scaling operations on the hashring cause a high churn of time series on the nodes, requiring each node to flush its TSDB head and upload its recent blocks on the object storage. During this operation that can last a few minutes, the receivers cannot ingest data, causing a downtime. This is especially critical if you are running big Receive nodes. The more data they have, the longer the downtime.
    - **ketama**: an implementation of a consistent hashing algorithm. It means that during scaling operations, most of the time series will remain attached to the same nodes. No TSDB operation or data upload is needed before operating into the new configuration. As a result, the downtime is minimal, just the time for the nodes to agree on the new hashring. As a downside, it can be less efficient in evenly distributing the load compared to hashmod.

![](https://thanos.io/v0.40/blog/img/life-of-a-sample/ingestor-router.png)

- Keys to consider:
  - If you load is stable for the foreseeable future -> hashmod. Otherwise -> ketama.
  - The case for small Receive nodes -> hashmod.
  - Protecting the nodes after recovery: recommend using the `receive.limits-config` flag to limit the amount of data that can be received.
- For clients requiring high data durability, the `--receive.replication-factor` flag ensures data duplication across multiple receivers.
- A new deployment topology was proposed, separating the router and ingestor roles. The hashring configuration is read by the routers, which will direct each time series to the appropriate ingestor and its replicas. This role separation provides some important benefits.

![](https://thanos.io/v0.40/blog/img/life-of-a-sample/router-and-ingestor.png)

- To enhance reliability in data ingestion, Thanos Receive supports out-of-order samples. Samples are ingested into the Receiver’s TSDB, which has strict requirements for the order of timestamps:
  - Samples are expected to have increasing timestamps for a given time series.
  - A new sample cannot be more than 1 hour older than the most recent sample of any time series in the TSDB.
- Support for out-of-order samples has been implemented for the TSDB. This feature can be enabled with the `tsdb.out-of-order.time-window` flag on the Receiver. The downsides are:
  - An increase in the TSDB’s memory usage, proportional to the number of out-of-order samples.
  - The TSDB will produce blocks with overlapping time periods, which the compactor must handle. Ensure the `--compact.enable-vertical-compaction` flag is enabled on the compactor to manage these overlapping blocks. We will cover this in more detail in the next article.
- Additionally, consider setting the `tsdb.too-far-in-future.time-window` flag to a value higher than the default 0s to account for possible clock drifts between clients and the Receiver.

## 3. Preparing Samples for Object Storage: Building Chunks and Blocks

// wip
