# Prometheus tips

1. Make use of the query function `avg_over_time` to discover for what percentage of time a given service was up or down for. Using `avg_over_time` in our alerting rules allows us to negate the issues described above by tracking how a particular time series appears over time rather than just the last known value of that time series. This way gaps in our data resulting from failed scrapes and flaky time series will no longer result in false positives or negatives in our alerting.

For example, rather than having the alerting rule:

```
up{job="jobname"} < 1
```

which would trigger an alert as soon as one scrape failed, we could have:

```
avg_over_time(up{job="jobname"} [5m]) < 0.9
```

which would trigger an alert if the average of `up` was below 0.9 for the last 5 minutes of scrapes.
