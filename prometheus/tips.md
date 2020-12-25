# Prometheus tips

## `avg_over_time`

Make use of the query function `avg_over_time` to discover for what percentage of time a given service was up or down for. Using `avg_over_time` in our alerting rules allows us to negate the issues described above by tracking how a particular time series appears over time rather than just the last known value of that time series. This way gaps in our data resulting from failed scrapes and flaky time series will no longer result in false positives or negatives in our alerting.

For example, rather than having the alerting rule:

```
up{job="jobname"} < 1
```

which would trigger an alert as soon as one scrape failed, we could have:

```
avg_over_time(up{job="jobname"} [5m]) < 0.9
```

which would trigger an alert if the average of `up` was below 0.9 for the last 5 minutes of scrapes.

## Alerting on approach open file limits

```
groups:
- name: example
  rules:
  - alert: ProcessNearFDLimits
    expr: process_open_fds / process_max_fds > 0.8
    for: 10m
```

## Absent alerting for Jobs

It is advised to have alerts on all the targets for a job going away, for example:

```
groups:
- name: example
  rules:
  - alert: MyJobMissing
    expr: absent(up{job="myjob"})
    for: 10m
```

## Absent alerting for Scraped metrics

It can happen that certain subsystems of a target don't always return all metrics that they should. It is possible to detect this situation by noticing that the `up` metric exists, but the metric in question does not. In addition you will want to check that `up` is 1, so that the alert doesn't spuriously fire when the target is down. If you already have down alerts for the job, there's no need to spam yourself with additional ones about missing metrics too.

```
groups:
- name: example
  rules:
  - alert: MyJobMissingMyMetric
    expr: up{job="myjob"} == 1 unless my_metric
    for: 10m
```

## Don't put the value in alert labels

Example:

```
groups:
- name: example
  rules:
  - alert: ExampleAlert
    expr: metric > 10
    for: 5m
    labels:
      severity: page
      value: "{{ $value }}"
    annotations:
      summary: "Instance {{ $labels.instance }}'s metric is too high"
```

It's likely this alert will never fire. The reason is that `labels` include a label called `value`. The effect of this is that each evaluation will see a brand new alert, and treat the previous one as no longer firing. This is the labels of an alert define its identity, and thus the `for` will never be satisfied.

If you want to have the value of the alert expression or anything else that can vary from one evaluation of an alert instance to another, you could use `annotations` instead.

```
groups:
- name: example
  rules:
  - alert: ExampleAlert
    expr: metric > 10
    for: 5m
    labels:
      severity: page
    annotations:
      summary: "Instance {{ $labels.instance }}'s metric is {{ $value }}"
```

## Running Prometheus notes

### Hardware

Storage space. To estimate how much you'll need you have to know how much data you will be ingesting. For an existing Prometheus you can run a PromQL query to report the samples ingested per second:

```
rate(prometheus_tsdb_head_samples_appended_total[5m])
```

While Prometheus can achieve compression of 1.3 bytes per sample in production -> 2 bytes per sample to be conservative. The deafault rentention for Prometheus is 15 days, so 100.000 samples per second would be around 240GB over 15 days.

How much RAM you will need? The storage in Prometheus 2.x works in blocks that are written out every two hours and subsequently into larger time ranges. The storage engine does no internal caching, rather it uses your kernel's page cache. So you will need:

```
RAM to hold a block + overheads + RAM used during queries
```

Prometheus is relatively light on CPU.

Network bandwidth is another consideration. Prometheus usually uses compression when scraping, so it uses somewhere around 20 bytes of network traffic to transfer a sample.

## Performance tunning

## --query.max-samples

- Default value: 50000000
- Description: Maximum number of samples a single query can load into memory. Note that queries will fail if they would load more samples than this into memory, so this also limits the number of samples a query can return
- Each sample uses 16 bytes of memory, however keep in mind there's more than just active samples in memory for a query.

## When does CPU matter?

https://giedrius.blog/2018/12/16/capacity-planning-of-prometheus-2-4-2-thanos-sidecar-0-1-0/

Prometheus is relatively light on CPU, the CPU usage is deeply impacted by the actual content of the PromQL queries that are being executed. To be even more exact, what matters is what kind of (if any) aggregation operators or math functions you are using in the queries --> `CPU - calculation`.

- Functions such as `time()` do not cost a lot since you only the Unix timestamp of the current time.
- Functions which use a range vector use more CPU time than those which take an instant vector.

To avoid recalculating the same thing over and over, you can use `recording rules`.

## By/Without and Ignoring/On

- `by`/`without` and `on`/`ignoring`.
- The `ignoring` keyword allows ignoring certain labels when matching, while the `on` keyword allows reducing the set of considered labels to a provided list.

```
<vector expr> <bin-op> ignoring(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) <vector expr>
```

- `without` removes the listed labels from the result vector, while all other labels are preserved the output. `by` does the opposite and drops labels that are not listed in the by clause, even if their label values are identical between all elements of the vector.

```
<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)
<aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
```
