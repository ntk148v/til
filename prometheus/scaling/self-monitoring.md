# Who watches the watchmen?

[Source](https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusSelfMonitoring)

Monitor Prometheus itself.

A lot of how we're monitoring for problems is probably basically standard in Prometheus deployments. The 1st level of monitoring and alerts is things inside Prometheus:

- Alert on unresponsive host agents as part of our general checking for and alerting on down hosts; this will catch when a configured machine doesn't have the agent installed or it hasn't been started. The one thing it won't catch is a production machine that hasn't been added to our Prometheus configuration. (This alert uses the Prometheus `up` metric)
- Alert if Prometheus can't talk to a number of other metric sources it's specifically configured to pull from, such as Grafana, Pushgateway, the Blackbox agent itself, Alertmanager...This is also based on the `up` metric, excluding the ones for host agents and for all of our Blackbox checks (which generate `up` metrics themeselves, which can be distinguished from regular `up` metrics because the Blackbox check ones have a non-empty `probe` label).
- Publish some system-wide information for temperature sensor readings and global disk space, so we have checks to make sure this information is both present at all and not too old.
- Publish various per-host information through the host agent's `textfile` collector, where you put files of metrics you want to publish in a specific directory, so we check to make sure that these files aren't too stale through the `node_textfile_mtime_seconds` metric.
- A useful check on Alertmanager because if Alertmanager is down, Prometheus can't send out the alert it detects.
