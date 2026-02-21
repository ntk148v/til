# Observability Use Cases

Sources:

- <https://blog.cloudflare.com/log-analytics-using-clickhouse/>
- <https://www.uber.com/en-VN/blog/logging/>
- <https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year>
- <https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog>
- <https://clickhouse.com/blog/scaling-observability-beyond-100pb-wide-events-replacing-otel>

Table of contents:

- [Observability Use Cases](#observability-use-cases)
  - [1. ClickHouse Cloud Architecture](#1-clickhouse-cloud-architecture)
  - [2. LogHouse: Building a logging platform](#2-loghouse-building-a-logging-platform)
  - [3. Scaling to 100 PB](#3-scaling-to-100-pb)
  - [4. Monitoring with ClickHouse](#4-monitoring-with-clickhouse)

## 1. ClickHouse Cloud Architecture

### Architectural decisions

**Separation of Storage and Compute:**

- Moved away from "shared-nothing" model
- Uses Amazon S3/GCS as primary storage layer
- Local NVMe for caching
- Solves "rebalancing" problem - new node simply points to same object store

**Cellular Infrastructure:**

- Organized into Cells to avoid "blast radius" issues
- Each cell is self-contained infrastructure unit
- Prevents single failure from impacting global fleet

**Control vs. Data Plane:**

- **Control Plane (AWS):** User accounts, billing, global orchestration
- **Data Plane (Multi-cloud):** Kubernetes (EKS/GKE) with custom ClickHouse Operator

### Scaling and idling

- Custom Idler and Scaler for cost optimization
- Envoy-based proxy intercepts requests to paused services
- Activator pattern spins up compute pods on demand

## 2. LogHouse: Building a logging platform

### Economic drivers

| Solution | Cost for 10T rows/month, 30-day retention |
|----------|-------------------------------------------|
| Datadog | ~$26M/month |
| ClickHouse | <1% of Datadog cost + 6 months retention |

### Technical implementation

**Schema optimization:**

```sql
CREATE TABLE logs (
    timestamp DateTime64(6, 'UTC'),
    message String CODEC(ZSTD(3)),
    level LowCardinality(String),
    source LowCardinality(String),
    metadata Map(String, String)  -- High-cardinality metadata
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (source, timestamp)
```

**Ingestion pipeline:**

- OTel Agents as DaemonSets on every Kubernetes node
- OTel Gateways for heavy processing (tagging, routing)
- Native protocol for maximum speed
- **No Kafka needed** - ClickHouse fast enough to ingest millions of rows/sec

### Key learnings

1. Use `Map(String, String)` for flexible log attributes
2. Skip Kafka - ClickHouse handles direct ingestion efficiently
3. OTel internal memory buffering sufficient for short bursts

## 3. Scaling to 100 PB

### The death of OTel at extreme scale

At 20 million rows/second:

- OTel pipeline would require 8,000 CPU cores just for JSON parsing/marshalling
- "Text logs via stdout" approach was too expensive
- Lost data during spikes

### The SysEx innovation

**System Tables Exporter (SysEx):**

- Custom Go-based tool
- Byte-for-byte copy from source ClickHouse system tables to central LogHouse
- **Zero-marshalling:** Stream data in ClickHouse Native Format without decoding to Go objects
- **90% CPU reduction** compared to OTel

**Dynamic schema generation:**

- Auto-detects when ClickHouse adds new columns to system tables
- Updates LogHouse schema to match
- No telemetry lost during upgrades

### Transition to Observability 2.0

**Wide Events over Metrics:**

- Instead of pre-aggregating into Prometheus metrics (causes cardinality explosion)
- Log **Wide Events**: every event as rich row with 100+ dimensions
- Unified UI (HyperDX + ClickStack) replacing "three pillars" (logs, metrics, traces)

**Scale statistics:**

| Metric | Value |
|--------|-------|
| Uncompressed data | 100+ Petabytes |
| Total rows | ~500 Trillion |
| Data managed through | column-oriented compression |

## 4. Monitoring with ClickHouse

### Event metrics

| Metric | Description |
|--------|-------------|
| `clickhouse.query.count` | Total number of queries |
| `clickhouse.insert.rows` | Rows inserted in all tables |
| `clickhouse.insert.bytes` | Uncompressed bytes inserted |
| `clickhouse.merge.rows` | Rows read for background merges |
| `clickhouse.merge.bytes.uncompressed` | Uncompressed bytes for merges |

### Network metrics

| Metric | Description |
|--------|-------------|
| `metrics.TCPConnection` | Connections to TCP server |
| `metrics.HTTPConnection` | Connections to HTTP server |
| `metrics.InterserverConnection` | Connections from replicas to fetch parts |

### ZooKeeper metrics

| Metric | Description |
|--------|-------------|
| `clickhouse.zk.watches` | Event subscriptions in ZooKeeper |
| `clickhouse.zk.wait.time` | Time spent waiting for ZooKeeper |
| `clickhouse.zk.requests` | Requests to ZooKeeper in progress |

### Data part metrics

| Metric | Description |
|--------|-------------|
| `clickhouse.part.count.max` | Maximum active parts in partitions |
| `clickhouse.mergetree.table.parts` | Active parts in MergeTree tables |
| `clickhouse.mergetree.table.rows` | Row count in MergeTree tables |

### Replica status

| Metric | Description |
|--------|-------------|
| `asynchronous_metrics.ReplicasSumQueueSize` | Queue size for pending operations |

### Useful monitoring queries

```sql
-- Query performance
SELECT
    type,
    event_time,
    query_duration_ms,
    memory_usage,
    query
FROM system.query_log
ORDER BY query_duration_ms DESC
LIMIT 10;

-- Merge status
SELECT
    database,
    table,
    round(elapsed, 0) AS time,
    round(progress, 4) AS percent,
    num_parts
FROM system.merges;

-- Disk space by table
SELECT
    database,
    table,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS size
FROM system.parts
WHERE database != 'system'
GROUP BY database, table
ORDER BY sum(bytes_on_disk) DESC;
```

## References

- [Cloudflare: Log Analytics with ClickHouse](https://blog.cloudflare.com/log-analytics-using-clickhouse/)
- [Uber: Logging Architecture](https://www.uber.com/en-VN/blog/logging/)
- [ClickHouse Cloud Architecture](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year)
- [LogHouse Platform](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog)
- [Scaling to 100PB](https://clickhouse.com/blog/scaling-observability-beyond-100pb-wide-events-replacing-otel)
