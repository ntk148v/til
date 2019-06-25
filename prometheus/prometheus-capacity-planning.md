# Prometheus Capacity Planning

## Storage

* The best disk for time series database is SSD.

* The rough formula:

```
needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample

ingested_samples_per_second = rate(prometheus_tsdb_head_samples_appended_total[5m])
bytes_per_sample = rate(prometheus_tsdb_compaction_chunk_size_bytes_sum[1d]) / rate(prometheus_tsdb_compaction_chunk_samples_sum[1d])

needed_disk_space = retention_time_seconds * rate(prometheus_tsdb_compaction_chunk_size_bytes_sum[1d]) / rate(prometheus_tsdb_compaction_chunk_samples_sum[1d]) * rate(prometheus_tsdb_head_samples_appended_total[5m])
```

## Memory

How much RAM you will need? The storage in Prometheus 2.x works in blocks that are written out every two hours and subsequently into larger time ranges. The storage engine does no internal caching, rather it uses your kernel's page cache.

Each sample is generally 1-2 bytes in size. Let's err on side of caution and use 2 bytes. Assuming we're collecting 100,000 samples/s for 12 hours, we can work out memory usage like so:

```
100,000 * 2 bytes * 43200 seconds
~8.64GB of RAM
```

You'll also need to factor in memory use for querying and recording rules.

If you already knew number of time series, average labels per time series, number of unique label pairs,...you can fill into the [calculator](https://www.robustperception.io/how-much-ram-does-prometheus-2-x-need-for-cardinality-and-ingestion)

## CPU

Prometheus is relatively light on CPU.
