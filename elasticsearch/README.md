# Elasticsearch

[What is Elasticsearch?](https://www.elastic.co/what-is/elasticsearch)

## Quick Reference

- [articles.md](./articles.md) - Curated external articles
- [reference/old.md](./reference/old.md) - Comprehensive legacy reference document

## Fundamentals

- [Basic Concepts](./fundamentals/basic-concepts.md) - Cluster, node, index, shard, document
- [Mapping](./fundamentals/mapping.md) - Dynamic and explicit mapping
- [Search Data](./fundamentals/search-data.md) - Near real-time search, refresh
- [Use Cases](./fundamentals/use-cases.md) - Search, analytics, autocompletion, multi-tenancy

## Architecture

- [Hot-Warm Architecture](./architecture/hot-warm-architecture.md) - Tiered storage for cost optimization

## Performance

- [Benchmark & Sizing](./performance/benchmark-sizing.md) - Cluster sizing guide
- [Cache](./performance/cache.md) - Page cache, shard-level request cache, query cache
- [Capacity Planning](./performance/capacity-planning.md) - Disk, memory, traffic
- [Garbage Collector](./performance/garbage-collector.md) - CMS vs G1GC tuning
- [Increase Write Throughput](./performance/increase-write-throughput-speed.md) - Indexing optimization
- [Reduce Shard Usage](./performance/reduce-shard-usage.md) - Shard management strategies

## Operations

- [Alias](./operations/alias.md) - Index aliases for zero-downtime operations
- [Monitoring](./operations/monitoring.md) - Performance monitoring
- [Resolve Unassigned Shards](./operations/resolve-unassigned-shards.md) - Common causes and fixes
- [Rollover](./operations/rollover.md) - Rolling indices for lifecycle management

## Troubleshooting

- [Troubleshooting](./troubleshooting/troubleshooting.md) - High CPU, JVM memory pressure
- [Found Crash](./troubleshooting/found-crash.md) - Six ways to crash Elasticsearch

## Ecosystem

- [Metricbeat](./ecosystem/metricbeat.md) - Metrics collection, comparison with Prometheus
- [ElastAlert](./ecosystem/elastalert.md) - Alerting framework for Elasticsearch

## External Resources

- [Elasticsearch Official Docs](https://www.elastic.co/guide/index.html)
- [Bonsai Documentation](https://docs.bonsai.io)
