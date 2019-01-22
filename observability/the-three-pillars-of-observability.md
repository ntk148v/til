# The Three Pillars of Observability

Logs, metrics, and traces are often known as the three pillars of observability.

> Distributed Systems Observability by Cindy Sridharan (Chapter 4)

## Event logs

* An event log is an immutable, timestamped record of discrete events that happened over time. Event logs in general come in three forms but are fundamentally the same: a timestamp and a payload of some context. The three forms are:
    * Plaintext: A log record might be free-form text. This is also the most common format of logs.
    * Structured: Much evangelized and advocated for in recent days. Typically, these logs are emitted in the JSON format.
    * Binary: Think logs in the Protobuf format, MySQL binlogs used for replication and point-in-time recovery, systemd journal logs, the pflog format used by the BSD firewall pf that often serves as a frontend to tcpdump.

* Traces and metrics are an abstraction built on top of logs that pre-process and encode information along two orthogonal axes, one being request-centric (trace), the other being system-centric (metric).

### The Pros and Cons of Logs

> Pros

* The easiest to generate. The fact that a log is just a string or a blob of JSON or typed key-value pairs makes it easy to represent any data in the form of a log line.
* Logs perform really well in terms of surfacing highly granular information pregnant with rich local context.

> Cons

* The performance: the default logging libraries of many languages and frameworks are not the cream of the crop, which means the application as a whole becomes susceptible to suboptimal performance due to the overhead of logging.
* Log messages can also be lost unless one uses a protocol like [RELP](https://en.wikipedia.org/wiki/Reliable_Event_Logging_Protocol) to guarantee reliable delivery of messages.
* Logging excessively has the capability to adversely affect application performance as a whole. This is exacerbated when the logging isn't asynchronous and request processing is blocked while writing a log line to disk or stdout.

## Metrics

* Metrics are a numeric representation of data measured over intervals of time.
* Since numbers are optimized for storage, processing, compression and retrieval, metrics enable longer retention of data as well as easier quering.

### The anatomy of modern metric

* One of the biggest drawbacks of historical time-series databases has been the *identification* of metrics that didn't lend itself very well to exploratory analysis or filtering.
* A metric is identified using both the metric name and the labels (additional key-value pairs).

### Advantages of metrics over event logs

* Metric transfer and storage has a constant overhead. Unlike logs, the cost of metrics doesn't increase in lockstep with user traffic or any other system activity that could result in a sharp uptick in data.
* Metrics, once collected, are more malleable to mathematical, probabilistic, and statistical transformations such as sampling, aggregation, summarization, and correlation.
* Metrics are also better suited to trigger alerts, since running queries against an in-memory, time-series database is far more efficient, not to mention more reliable, than running a query against a distributed system like Elasticsearch and then aggregating the results before deciding if an alert needs to be triggered

### The drawbacks of metrics

* System scoped, making it hard to understand anything else other than what's happening inside a particular system.
* With logs without fancy joins, a single line doesn’t give much information about what happened to a request across all components of a system. While it’s possible to construct a system that correlates metrics and logs across the address space or RPC boundaries, such systems require a metric to carry a UID as a label. -> overwhelm time-series databases.

## Tracing

* A trace is representation of a series of causally related distributed events that encode the end-to-end request flow through distributed system.
* The basic idea behind tracing is identify specific points (function calls or RPC boundatries or segments of concurrency such as threads, continuations, or queues) in an application, proxy, framework, library, runtime, middleware, and anything else in the path of a request that represents the following:
    * Forks in execution flow (OS thread or a green thread)
    * A hop or a fan out across network or process boundaries
* Having an understanding of the entire request lifecycle makes it possible to debug requests spanning multiple services to pinpoint the source of increased latency or resource utilization. 
* The use cases of distributed tracing are myriad. While used primarily for inter service dependency analysis, distributed profiling, and debugging steady-state problems, tracing can also help with chargeback and capacity planning.

### The Challenges of Tracing

* Tracing is, by far, the hardest to retrofit into an existing infrastructure, because for tracing to be truly effective, every component in the path of a request needs to be modified to propagate tracing information.
* The second problem with tracing instrumentation is that it’s not sufficient for developers to instrument their code alone.
* The cost of tracing isn’t quite as catastrophic as that of logging, mainly because traces are almost always sampled heavily to reduce runtime overhead as well as storage costs. 

### Service Meshes: A new hop for the future

While tracing has been difficult to implement, the rise of [service meshes](https://blog.buoyant.io/2017/04/25/whats-a-service-mesh-and-why-do-i-need-one/) make integrating tracing functionality almost effortless. [Data planes](https://blog.envoyproxy.io/service-mesh-data-plane-vs-control-plane-2774e720f7fc) of service meshes implement tracing and stats collections at the proxy level, which allows one to treat individual services as blackboxes but still get uniform and thorough observability into the mesh as a whole. Applications that are a part of the mesh will still need to forward headers to the next hop in the mesh, but no additional instrumentation is necessary.

## Conclusion

* Logs, metrics, and traces serve their own unique purpose and are complementary. In unison, they provide maximum visibility into the behavior of distributed systems. For example, it makes sense to have the following:
    * A counter and log at every major entry and exit point of a request
    * A log and trace at every decision point of a request

* It also makes sense to have all three semantically linked such that it becomes possible at the time of debugging:
    * To reconstruct the codepath taken by reading a trace
    * To dervive request or error ratios from any single point in the codepath
