# Prometheus Federation

## Use cases

Federation helps to perform global aggregations (allows your to have a global Prometheus that pulls aggregated metrics from your datacenter Prometheus servers).

Commonly, federation is used to either scalable Prometheus monitoring setups or pull related metrics from one service's Prometheus into another.

- Hierarchical federation
- Cross-service federation

Federation is not for copying the content of entire Prometheus servers.

Federation is not a way to have one Prometheus proxy another Prometheus.

You should not use federation to pull metrics with an `instance` label.

## Why should not use federation beyond its intended use case?

Pulling all metrics over the internet to a global Prometheus from where you can then graph and alert on them means that internet connectivity to another datacenter is now a hard dependency on your per-datacenter monitoring working.

Each Prometheus is standalone and running on one machine and thus limited by machine size in terms of how much it can handle. If the global Prometheus was pulling in all metrics from each datacenter Prometheus, the global Prometheus would become the bottleneck and greatly limit your ability to scale.

Prometheus is designed to scrape many thousands of small to medium size targets. By spreading the scrapes over the scrape interval, Prometheus can keep up with the data volumes with even load. If you instead have it scrape a handful of targets with massive numbers of time series, such as massive federation endpoints, this can cause load spikes and it may not even be possible for Prometheus to complete processing of one massive scrape worth of data in time to start the next scrape.
