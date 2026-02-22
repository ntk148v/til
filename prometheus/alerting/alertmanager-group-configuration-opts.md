# 3 Alertmanager configuration options

> NOTE: [source](https://www.robustperception.io/whats-the-difference-between-group_interval-group_wait-and-repeat_interval)

## Recap on some Prometheus alerting basics

- `evaluation_interval`: the time between each evaluation of Prometheus's alerting rules.
- `scrape_interval`: the time between each Prometheus scrape.
- When a rule is evaluated, its state can be alerted to be either inactive, pending or firing. Follow evaluation, this state is sent to the connected Alertmanager to potentially start/stop the sending of alert notifications.

## `group_by`

- In order to avoid continuosly sending notifications for similar alerts, the Alertmanager may be configured to group these related alerts into one alert:

```
group_by: ['alert_name', 'job']
```

## `group_interval`

- How long to wait before sending an alert that has been added to a group which contains already fired alerts.

## `group_wait`

- How long to wait to buffer alerts of the same group before sending initially.

```
group_by: ['alertname', 'job']
group_wait: 45s # Usually set between ~0s to a few minutes.
```

## `repeat_interval`

- How long to wait before re-sending a given alert that has already been sent.k
