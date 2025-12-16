# Prometheus tips

- [Prometheus tips](#prometheus-tips)
  - [`avg_over_time`](#avg_over_time)
  - [Alerting on approach open file limits](#alerting-on-approach-open-file-limits)
  - [Absent alerting for Jobs](#absent-alerting-for-jobs)
  - [Absent alerting for Scraped metrics](#absent-alerting-for-scraped-metrics)
  - [Don't put the value in alert labels](#dont-put-the-value-in-alert-labels)
  - [Hardware](#hardware)
  - [--query.max-samples](#--querymax-samples)
  - [When does CPU matter?](#when-does-cpu-matter)
  - [By/Without and Ignoring/On](#bywithout-and-ignoringon)
  - [Authentication and encryption for Prometheus and its exporters](#authentication-and-encryption-for-prometheus-and-its-exporters)
  - [Prometheus and fsync](#prometheus-and-fsync)

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

## Hardware

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

## --query.max-samples

- Default value: 50000000
- Description: Maximum number of samples a single query can load into memory. Note that queries will fail if they would load more samples than this into memory, so this also limits the number of samples a query can return
- Each sample uses 16 bytes of memory, however keep in mind there's more than just active samples in memory for a query.

## When does CPU matter?

<https://giedrius.blog/2018/12/16/capacity-planning-of-prometheus-2-4-2-thanos-sidecar-0-1-0/>

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

## Authentication and encryption for Prometheus and its exporters

Source: <https://0x63.me/tls-between-prometheus-and-its-exporters/>

## Prometheus and fsync

Prometheus `fsync` refers to the crucial disk synchronization operations, especially within its Time Series Database (TSDB) and its Write-Ahead Log (WAL), ensuring recently ingested metrics data is safely written to durable storage to prevent loss during crashes, often manifesting as performance metrics like `prometheus_tsdb_wal_fsync_duration_seconds` which can indicate I/O bottlenecks if too slow.

What fsync means in Prometheus:

- Data Durability: Prometheus uses a Write-Ahead Log (WAL) to buffer incoming metrics before committing them to the main database files.
- fsync() System Call: To guarantee data isn't lost on power failure, Prometheus periodically calls fsync() to force this buffered data from the operating system's cache to the physical disk.
- Performance Impact: This disk write is a critical operation, and if the underlying storage is slow, fsync calls take longer, impacting Prometheus's ingestion rate and overall performance.

I found a link: <https://groups.google.com/g/prometheus-users/c/Oy1qI3Og9ww> but the logic seems to be changed in the current source code (v3.8.0).

## `min-block-duration` and `max-block-duration`

In Prometheus, the `--storage.tsdb.min-block-duration` and `--storage.tsdb.max-block-duration` flags control the time range of data stored in individual, on-disk data blocks
- `--storage.tsdb.min-block-duration`: This flag sets the minimum duration for which data is held in memory (the "head" block) before being persisted to disk as an initial data block. The default value is 2 hours. Lowering this value can reduce Prometheus's memory usage because data is written to disk more frequently.
- `--storage.tsdb.max-block-duration`: This flag sets the maximum duration a block of data may span before it is compacted with other adjacent blocks into a larger block. The default value is a dynamic calculation based on retention time, but often effectively 2 hours for initial blocks

**Usage and recommendations**

- Default Operation: By default, Prometheus creates 2-hour blocks which are then compacted into larger blocks in the background, spanning up to 10% of the total retention time or 31 days (whichever is smaller).
- Memory Management: If you experience high memory usage, you might consider lowering the min-block-duration, which causes Prometheus to write data to disk more often, reducing the memory footprint of the head block.

The max open files limit is a system configuration that restricts the number of file handles a single process can have open simultaneously. The block duration settings relate to this in the following ways:
- More Blocks, More Files: Each on-disk block in the Prometheus TSDB is made up of several files (index, chunks, meta.json, etc.). More blocks mean more files overall.
- Compaction and File Management:
  - Compaction operations temporarily involve opening multiple source blocks and a new destination block simultaneously, requiring more file handles during that time.
  - A setup with many small blocks (due to a low min-block-duration or an unusual max-block-duration setting) can increase the number of files the system needs to manage, potentially bumping into the max open files limit if the limit is set too low.
- Memory Mapping (mmap): Prometheus uses memory-mapping (mmap) to access older data blocks on disk efficiently. Each memory-mapped file consumes a file handle. The sheer volume of blocks, rather than the duration setting itself, is the primary concern here, which is why Prometheus instances managing terabytes of data require a high max open files limit.
