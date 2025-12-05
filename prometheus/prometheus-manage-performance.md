# Manage Performance

## Detecting a problem

The useful metrics:

- `prometheus_rule_group_iterations_missed_total` can indicate that some rule groups are taking too long to evaluate.
- Comparing `prometheus_rule_group_lats_duration_second` against `prometheus_rule_group_interval_seconds` can tell you which group is at fault and if it is a recent change in behaviour.
- `prometheus_notifications_dropped_total` indicates issues talking to the Alertmanger.
- If `prometheus_notifications_queue_length` is approaching `prometheus_notifications_queue_capacity`, you may start losing alerts.
- Each service discovery mechanism tends to have a metric such as `prometheus_sd_file_read_errors_total`...
- `prometheus_rule_evaluation_failures_total`, `prometheus_tsdb_compaction_failed_total` and `prometheus_tsdb_wal_corruptions_total` indicate that something has gone wrong in the storage layer.

## Finding expensive metrics and targets

- Find metrics with high cardinality:

```
topk(10, count by(__name__)({__name__=~".+"}))
```

- In addition to `up`, Prometheus adds 3 other samples for every target scrape. `scrape_samples_scraped` is the number of samples that were on the /metrics.
- `sample_samples_post_metric_relableling` is similar, but it excludes samples that were dropped by `metric_relabel_configs`.
- The final special sample added is `scrape_duration_seconds`, which is how long that scrape took.

## Reducing load

- Drop the metric at ingestion time using `metric_label_configs`. This still transfers the metric over the network and parses it, but it's still cheaper than ingesting it into the storage layer.

```yaml
scrape_configs:
  - job_name: some_application
    static_configs:
      - targets:
          - localhost:1234
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: expensive_metric_name
        action: drop
```

- Increase `scrape_interval` and `evaluation_interval` (<= 2 minutes)
- If the number of samples after `metric_relabel_configs` is higher than `sample_limit`, then the scrape will fail and the samples will not be ingested. This is disabled by default but can act as an emergency relief vavle!

## Horizontal sharding

The approach to horizontal sharding is to have a master Prometheus and several scraping Prometheus servers.

```yaml
global:
  external_labels:
    env: prod
    scraper: 2
scrape_configs:
  - job_name: my_job
    # Service discovery etc. goes here.
    relabel_configs:
      - source_labels: [__address__]
        modulus: 4
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: 2 # This is the 3rd scraper.
        action: keep
```

Here you can see there are 4 scrapers from the `modulus` setting. Each scraper should have a unique external label + the external labels of the master Prometheus. The master Prometheus can then use the remote read endpoint of Prometheus itself to transparently pull in data from the scrapers:

```yaml
global:
  external_labels:
    env: prod
remote_read:
  - url: http://scraper0:9090/api/v1/read
    read_recent: true
  - url: http://scraper1:9090/api/v1/read
    read_recent: true
  - url: http://scraper2:9090/api/v1/read
    read_recent: true
  - url: http://scraper3:9090/api/v1/read
    read_recent: true
```

The disadvantages:

1. Operational

Hashmod sharding is static. Adding or removing Prometheus instances changes the modulus value and forces a full redistribution of scrape targets. This causes:

- Large-scale target churn
- Increased scrape failures during transitions
- Potential dual-scraping or gaps while the fleet stabilizes

2. Uneven Load Distribution With Heterogeneous Targets

Hashmod sharding provides uniform distribution by count, not by cost or cardinality. If some jobs are heavier (high cardinality, expensive exporters, long scrape durations), shards become imbalanced even if target counts are equal.

3. Difficulties With Global Querying and Federation

Because each shard stores only a portion of the metrics:

- Federation layers or external query engines must aggregate across shards.
- Debugging becomes harder because a target’s data lives on only one shard.
- Global alerting requires a separate aggregator or Thanos Ruler; local rules cannot be global.
