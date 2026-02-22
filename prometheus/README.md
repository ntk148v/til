# Prometheus

## Quick Reference

- [notes.md](./notes.md) - Practical tips, snippets, and common patterns
- [qa.md](./qa.md) - Q&A on Prometheus internals (WAL, 2-hour blocks, etc.)
- [articles.md](./articles.md) - Curated external articles
- [tools.md](./tools.md) - Prometheus ecosystem tools

## Fundamentals

- [Internal Architecture](./fundamentals/internal-architecture.md)
- [TSDB](./fundamentals/tsdb.md) - Write-Ahead Log, head block, compaction
- [Service Discovery](./fundamentals/service-discovery.md)

## PromQL

- [Cheatsheet](./promql/cheatsheet.md)
- [Gotchas](./promql/gotchas.md) - Instant vs range vectors, rate vs irate
- [Join](./promql/join.md) - Vector matching, group_left
- [Query Steps](./promql/query-steps.md)

## Metrics & Instrumentation

- [Metric Types](./metrics/types.md) - Counter, Gauge, Histogram, Summary
- [Histogram Gotchas](./metrics/histogram-gotchas.md) - Buckets, quantiles, cardinality
- [Instrumentation](./metrics/instrumentation.md)

## Alerting

- [Alertmanager HA](./alerting/alertmanager-ha.md)
- [Silence Alerts](./alerting/alertmanager-silence.md)
- [Time-based Alert](./alerting/alertmanager-time-based-alert.md)
- [Group Configuration Options](./alerting/alertmanager-group-configuration-opts.md)
- [Alert Rules](./alerting/alert-rules.md)
- [Delays on Alerting](./alerting/delays-on-alerting.md)

## Performance

- [Capacity Planning](./performance/capacity-planning.md) - Storage, RAM, CPU estimates
- [Manage Performance](./performance/manage-performance.md)
- [Analysing](./performance/analysing.md) - Memory profiling, cardinality analysis
- [Memory Monitoring](./performance/memory-monitoring.md) - Golang pprof
- [WAL](./performance/wal.md) - Write-Ahead Log internals

## Scaling

- [Federation](./scaling/federation.md)
- [Long-term Storage](./scaling/lts.md) - Solutions for durable storage
- [Remote APIs](./scaling/remote-apis.md)
- [Self Monitoring](./scaling/self-monitoring.md) - "Who watches the watchmen?"

## Operations

- [Labels & Relabel](./operations/labels-relabel.md)
- [Pushgateway](./operations/pushgateway.md)
- [Docker Metrics](./operations/docker-metrics.md)

## Security

- [Hacking Kubernetes via Prometheus](./security/hacking-kubernetes.md)

## Critiques & Comparisons

- [Prometheus Sucks?](./critiques/prometheus-sucks.md) - Honest assessment of limitations
- [Zabbix vs Prometheus](./critiques/zabbix-prometheus.md)

## References (PDFs)

See [refs/](./refs/) for conference slides and papers.

## External Resources

- [RobustPerception](https://www.robustperception.io/) - Brian Brazil's blog
- [Prometheus Official Docs](https://prometheus.io/docs/)
- [PromLabs](https://promlabs.com)
- [Awesome-prometheus](https://github.com/roaldnefs/awesome-prometheus)
