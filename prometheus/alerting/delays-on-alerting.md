# Prometheus: Understanding the delays on alerting

[Source](https://pracucci.com/prometheus-understanding-the-delays-on-alerting.html)

## Scraping, Evaluation and Alerting

- `scrape_interval` [1m]: Prometheus scrape metrics from monitored targets at regular intervals.
- `evaluation_interval` [1m]: Prometheus has another loop, whose clock is independent from the scraping one, that evaluates alerting rules at a regular interval.
- Alert's state:

```
inactive -> pending -> firing
```

- An alert transitions from a state to another only during the evaluation cycle.
  - W/O **FOR**: inactive -> firing (1 x evaluation_interval).
  - W/ **FOR**: inactive -> pending -> firing (>= 2 x evaluation_interval).

## The Alert Lifecycle

- Example:

```yaml
# Alert rules
  rules:
  - alert: node_load_1m
    expr: node_load1 > 20
    for: 1m
# Prometheus config
global:
  scrape_interval: 20s
  evaluation_interval: 1m
```

- How much time does it take to fire `node_load_1m`?
- Expected: `1m` - Reality: `1m` -> `20s + 1m + 1m`

![](https://pracucci.com/assets/2016-11-16-prometheus-alert-lifecycle-612f4a8f0171d3e56c2cc2ed4bcfb90232bfbdd2d1273d11d97f52a0e3cd121d.png)

## The Alertmanager

- Alertmanager groups similar alerts together into a single notifcation.

```yaml
# Alertmanager config
group_by: ["a-label", "another-label"]
group_wait: 30s
group_interval: 5m
```

- A new alert is fired, it waits for `group_wait` time to eventually group further upcoming alerts that matchthe same `group_by` condition.
- The `group_interval` setting controls how long to wait before dispatching further notifications of the same group, and the time interval is calculated starting from the last notification sent.
