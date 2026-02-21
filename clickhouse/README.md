# ClickHouse Learning Notes

A comprehensive guide to learning ClickHouse, organized by topic.

## Table of Contents

### Fundamentals

Core concepts and architecture of ClickHouse.

| Topic | Description |
|-------|-------------|
| [Architecture](fundamentals/architecture.md) | System architecture, storage layer, query processing |
| [Why ClickHouse is Fast](fundamentals/why-is-clickhouse-so-fast.md) | Performance factors: columnar storage, vectorization, merge-time computation |
| [Storage](fundamentals/storage.md) | MergeTree storage, parts, granules, query execution |
| [Table Engines](fundamentals/engines.md) | MergeTree family, special-purpose, integration engines |
| [Table Parts](fundamentals/table-parts.md) | Data parts lifecycle, active/inactive parts, merges |
| [Skipping Indices](fundamentals/skipping-indices.md) | Secondary indices for data pruning |

### Guides

Practical how-to guides for working with ClickHouse.

| Topic | Description |
|-------|-------------|
| [Getting Started Issues](guides/getting-started-issues.md) | 13 common pitfalls and how to avoid them |
| [Common Issues & Monitoring](guides/common-issues-monitoring.md) | Using advanced dashboards, identifying problems |
| [Data Ingestion](guides/data-ingestion.md) | INSERTs, Kafka tables, materialized views |
| [Operations](guides/operations.md) | System tables, settings, mutations, merges |
| [TTL](guides/ttl.md) | Time-to-live for data management, hot/warm/cold storage |
| [Materialized Views](guides/materialized-views.md) | Pre-aggregation, data transformation, best practices |
| [JSON Type](guides/json.md) | When to use JSON vs structured types |
| [LowCardinality](guides/lowcardinality.md) | Dictionary encoding for low-cardinality columns |

### Scaling

Horizontal and vertical scaling strategies.

| Topic | Description |
|-------|-------------|
| [Replication & Sharding](scaling/replication-and-sharding.md) | Distributed architecture, multi-master replication |

### Comparisons

Comparisons with other data systems.

| Topic | Description |
|-------|-------------|
| [ClickHouse vs Elasticsearch](comparisons/clickhouse-vs-elasticsearch.md) | Architecture, storage, query differences |

### Use Cases

Real-world applications and patterns.

| Topic | Description |
|-------|-------------|
| [Observability](use-cases/observability.md) | Logging, monitoring, ClickHouse Cloud architecture |

### Resources

External links and references.

| Topic | Description |
|-------|-------------|
| [Links & References](resources/links.md) | Documentation, videos, blog posts, papers |

## Quick Start

### When to use ClickHouse

- **Analytics on large datasets** - Petabyte-scale with millisecond queries
- **Time-series data** - Logs, metrics, events
- **Real-time analytics** - INSERTs at millions of rows/second
- **Column-oriented workloads** - Aggregations, filtering, GROUP BY

### When NOT to use ClickHouse

- **OLTP workloads** - High-frequency point updates/deletes
- **Transaction-heavy applications** - Limited ACID guarantees
- **Complex JOINs** - Better suited for normalized OLTP databases

### Key concepts at a glance

```
┌─────────────────────────────────────────────────────────────┐
│                    ClickHouse Concepts                       │
├─────────────────────────────────────────────────────────────┤
│  Storage          │ Parts, Granules, MergeTree              │
│  Indexing         │ Sparse primary key, Skipping indices    │
│  Compression      │ Per-column codecs (ZSTD, LZ4, etc.)     │
│  Query Engine     │ Vectorized, parallel execution          │
│  Scaling          │ Vertical-first, then horizontal         │
│  Data Lifecycle   │ TTL, materialized views, merges         │
└─────────────────────────────────────────────────────────────┘
```

## Learning Path

### Beginner

1. Read [Architecture](fundamentals/architecture.md) for system overview
2. Learn [Why ClickHouse is Fast](fundamentals/why-is-clickhouse-so-fast.md)
3. Review [Getting Started Issues](guides/getting-started-issues.md) to avoid common mistakes

### Intermediate

4. Study [Storage](fundamentals/storage.md) and [Table Engines](fundamentals/engines.md)
5. Practice [Data Ingestion](guides/data-ingestion.md) patterns
6. Implement [Materialized Views](guides/materialized-views.md)

### Advanced

7. Optimize with [Skipping Indices](fundamentals/skipping-indices.md)
8. Scale with [Replication & Sharding](scaling/replication-and-sharding.md)
9. Monitor using [Operations](guides/operations.md) and [Common Issues](guides/common-issues-monitoring.md)
