# Pushgateway

The Pushgateway is an intermediary service which allows you to push metrics from jobs which cannot be scraped.

## Should I be using the Pushgateway?

**Only using the Pushgateway in certain limited cases**. There are several pitfalls when blindly using the Pushgateway instead of Prometheus's usual pull model for general metrics collection:
* When monitoring multiple instances through a single Pushgateway, the Pushgateway becomes both a single point of failure and a potential bottleneck.
* You lose Prometheus's automatic instance health monitoring via the `up` metric.
* The Pushgateway never forgets series pushed to it and will expose them to Prometheus forever unless those series are manually deleted via the Pushgateway API.


The latter point is especially relevant when multiple instances of a job differentiate their metrics in the Pushgateway via an `instance` label or similar. Metrics for an instance will then remain in the Pushgateway even if the originating instance is renamed or removed. When using the Pushgateway, you would now have to delete any stale metrics manually or automate lifecycle synchronization yourself.

**The only valid use case for the Pushgateway is for capturing the outcome of a service-level batch**.

## Alternative strategies

If an inbound firewall or NAT is preventing you from pulling metrics from targets, consider moving the Prometheus server behind the network barrier as well. We generally recommend running Prometheus servers on the same network as the monitored instances.

For batch jobs that are related to a machine (such as automatic security update cronjobs or configuration management client runs), expose the resulting metrics using the Node Exporter's textfile module instead of the Pushgateway.

