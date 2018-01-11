# Monitoring Distributed Systems

## Definitions

- Monitoring: Collecting, processing, aggregating, and displaying real-time
  *quantitative* data about a system, such as query counts and types, error
  counts and types, processing times, and server lifetimes.
- White-box monitoring: Monitoring based on metrics exposed by the internals
  of the system, including logs, interfaces or HTTP handler that emits
  internal statistics.
- Black-box monitoring: Testing externally visible behavior as a user would
  see it.
- Dashboard: An application (usually web-based) that provides a summary view
  of a service's core metrics.
- Alert: A notification intended to be read by a human and that is pushed to a
  system such as a bug or ticket queue, an email alias...
- Root cause: A defect in a software or human system that, if repaired,
  instills confidence that this event won't happen again in the same way.

## The four Golden Signals

- Latency: The time it takes to service a request. It's important to
  distinguish between the latency of successful requests and the latency of
  failed requests.
- Traffic: A measure of how much demand is being placed on your systemi,
  measured in a high-level system-specific metric (For e.x: a web service -
  HTTP requests/second,audio streaming system - network I/O rate or concurrent
  sessions.)
- Errors: The rate of requests that fail, either explicitly (HTTP 500s),
  implicity (HTTP 200 success response, but coupled with the wrong content),
  or by policy (Ex: If you committed to 1s response, any request over 1s is an
  error.)
- Saturation: How "full" your service is. A measure of your system fraction,
  emphasizing the resources that are most constrained (E.x: in a
  memory-constrained system, show memory; in an I/O-constrained system, show
  I/O.)

## Options

- [Graylog](https://www.graylog.org/)
- [Icinga](https://www.icinga.com/)(https://github.com/Icinga/icinga2)
- [Prometheus](https://prometheus.io/)(https://github.com/prometheus/prometheus)
- [LibreNMS](http://www.librenms.org/)(https://github.com/librenms/librenms)
- [Rackspace Cloud Monitoring](https://github.com/rcbops/rpc-maas)
- [OpenNMS](https://www.opennms.org/en)
...

## Comprasion

- [Comprasioni to alternatives](https://prometheus.io/docs/introduction/comparison/)

## Requirements

- Physical (SNMP), Virtualization (agent/agent less), Container (CoE
integration)
- Metric store/query, event, alert (SMS, Mail, Slack, Telegram,...)
- 2 Part: Log - Monitor

-> Define stack, ref/performance and features.
-> Test benchmark?

## Benchmark

1. Benchmark tools.

- [wrk](https://github.com/wg/wrk)
- [Aweome-http-benchmark](https://github.com/denji/awesome-http-benchmark)

## Refs

- [Monitoring Distributed Systems](https://landing.google.com/sre/book/chapters/monitoring-distributed-systems.html)
- [24/7 OpenStack Monitoring: Architecture and Tools](https://platform9.com/blog/24-7-openstack-monitoring-architecture-tools/)
- [Comprasion](https://www.loomsystems.com/blog/single-post/2017/06/07/prometheus-vs-grafana-vs-graphite-a-feature-comparison)
