# Prometheus Histogram

Source: https://www.robustperception.io/how-does-a-prometheus-histogram-work

## First look

- The histogram is a combination of various counters.
- Histogram ~ Summary: used to track the size of events, same utilities.
- Histogram != Summary: their handling of quantiles.

## Gotchas through example

```
# HELP prometheus_http_request_duration_seconds Histogram of latencies for HTTP requests.
# TYPE prometheus_http_request_duration_seconds histogram
prometheus_http_request_duration_seconds_bucket{handler="/",le="0.1"} 25547
prometheus_http_request_duration_seconds_bucket{handler="/",le="0.2"} 26688
prometheus_http_request_duration_seconds_bucket{handler="/",le="0.4"} 27760
prometheus_http_request_duration_seconds_bucket{handler="/",le="1"} 28641
prometheus_http_request_duration_seconds_bucket{handler="/",le="3"} 28782
prometheus_http_request_duration_seconds_bucket{handler="/",le="8"} 28844
prometheus_http_request_duration_seconds_bucket{handler="/",le="20"} 28855
prometheus_http_request_duration_seconds_bucket{handler="/",le="60"} 28860
prometheus_http_request_duration_seconds_bucket{handler="/",le="120"} 28860
prometheus_http_request_duration_seconds_bucket{handler="/",le="+Inf"} 28860
prometheus_http_request_duration_seconds_sum{handler="/"} 1863.80491025699
prometheus_http_request_duration_seconds_count{handler="/"} 28860
```

- `_bucket` time series: counters which form a cumulative histogram, `le` stands for **less than or equal to**. 26688 requests took less than or equal to 200ms.
- The `+Inf` bucket must always be present and will match the value of the `_count`.
- Calculate the X quantile (the X \* 100th percentile):

```
histogram_quantile(X,
  rate(prometheus_http_request_duration_seconds_bucket[5m])
)
```

- Aggregate the buckets before calculating the quantile.

```
histogram_quantile(0.9,
  sum without (handler)(
    rate(prometheus_http_request_duration_seconds_bucket[5m])
  )
)
```

- Why not always use histograms?

  - With histograms you have to pre-choose your buckets.
  - The cost moves from the client to Prometheus itself due to bucket cardinality. Cardinality is always something to consider with labels, and a histogram by default will have a cardinality of 10 for its buckets. If additional labels are added to the histogram, or more buckets are added, then histograms can get rather expensive.

- You can drop some buckets at ingestion time -> reduce the cost to Prometheus. Not that, you can drop as many as few buckets as you like, however the +Inf bucket is required for `histogram_quantile`. For example:

```
scrape_configs:
 - job_name: 'my_job'
   static_configs:
     - targets:
       - my_target:1234
   metric_relabel_configs:
   - source_labels: [ __name__, le ]
     regex: 'example_latency_seconds_bucket;(0\.0.*)'
     action: drop
```

- The potential high cardinality of histograms is also one reason a histogram has a `_sum` and `_count`. Even if you drop all the bucket time series, you can still calculate an average latency with just those two time series.
