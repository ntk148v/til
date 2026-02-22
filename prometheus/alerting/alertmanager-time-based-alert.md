# Alertmanager Time of day based routing/notification

- [Alertmanager Time of day based routing/notification](#alertmanager-time-of-day-based-routingnotification)
  - [1. Upstream Issue](#1-upstream-issue)
  - [2. Solutions](#2-solutions)
    - [2.1. Prometheus record rules and Alertmanager inhibit rules](#21-prometheus-record-rules-and-alertmanager-inhibit-rules)
    - [2.2. External exporters](#22-external-exporters)
    - [2.3. Alertmanager time-based muting](#23-alertmanager-time-based-muting)

## 1. Upstream Issue

<https://github.com/prometheus/alertmanager/issues/876>

## 2. Solutions

### 2.1. Prometheus record rules and Alertmanager inhibit rules

- Create record rules to define the holidays (timezone aware), then create inhibit rules based on them or just provide them in alert rules.

```yaml
# Use record -> vector + on()
- record: business_day
  expr: |
    vector(1) and day_of_week(belgium_localtime) > 0
    and day_of_week(belgium_localtime) < 6
    unless count(public_holiday)
```

- <https://gist.github.com/roidelapluie/8c67e9c8fb18b310a4a90cb92a23056b>
- <https://github.com/roidelapluie/prometheus-timezone-holidays/blob/master/alertmanager.yml>
- <https://promcon.io/2019-munich/slides/improved-alerting-with-prometheus-and-alertmanager.pdf>

### 2.2. External exporters

- Use external exporters to calculate holidays/desired times..., expose them as metrics. Then we can use them in the alert rules.
- <https://github.com/OneMainF/time-range-exporter>
- <https://github.com/allangood/holiday_exporter>

### 2.3. Alertmanager time-based muting

- Design: <https://docs.google.com/document/d/1pf-rPDQUGJUHazyr5vanTO6ft3loNZO9UoVpvhShFtA/edit>
- Goal: for Alertmanager to support user-defined time intervals and integrate them into the routing tree, allowing users to model their time-based requirements.
- Implementation: <https://github.com/prometheus/alertmanager/pull/2393>
