# Envoy performance

- Control plane performance: The CPu consumption scales with the following factors:
  - The rate of deployment changes.
  - The rate of configuration changes.
  - The numberof proxies connecting to.
- Data plane performance: depends on many factors:
  - Number of client connections.
  - Target request rate.
  - Request size and Response size.
  - Number of proxy worker threads.
  - Protocol.
  - CPU cores.
  - Number and types of proxy filters, specifically telemetry v2 related filters.
- The latency, throughput, and the proxies’ CPU and memory consumption are measured as a function of said factors.
