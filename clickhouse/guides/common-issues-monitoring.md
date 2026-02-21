# Common Issues and Monitoring

Source: <https://clickhouse.com/blog/common-issues-you-can-solve-using-advanced-monitoring-dashboards>

Monitoring your database in production is mandatory. ClickHouse provides built-in advanced dashboards for deep insights into system health and performance.

## 1. Getting started with advanced dashboard

The advanced dashboard is available at `<your_clickhouse_url>/dashboard`.

### Enable metric logs (self-managed)

Edit `/etc/clickhouse-server/config.d/metric_log.xml`:

```xml
<clickhouse>
    <metric_log>
        <database>system</database>
        <table>metric_log</table>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
        <collect_interval_milliseconds>1000</collect_interval_milliseconds>
    </metric_log>
    <asynchronous_metric_log>
        <database>system</database>
        <table>asynchronous_metric_log</table>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
        <collect_interval_milliseconds>1000</collect_interval_milliseconds>
    </asynchronous_metric_log>
</clickhouse>
```

### Create dashboard user

```sql
CREATE USER dashboard_user IDENTIFIED BY 'your_password';
CREATE ROLE dashboard;
GRANT dashboard TO dashboard_user;
GRANT REMOTE ON *.* to dashboard;
GRANT CREATE TEMPORARY TABLE on *.* to dashboard;
GRANT SELECT ON system.metric_log to dashboard;
GRANT SELECT ON system.asynchronous_metric_log to dashboard;
GRANT SELECT ON system.dashboards to dashboard;
```

## 2. Out-of-box visualizations

### ClickHouse-specific metrics

| Metric                    | Description                      |
| ------------------------- | -------------------------------- |
| Queries Per Second        | Rate of queries being processed  |
| Selected Rows/Sec         | Rows being read by queries       |
| Inserted Rows/Sec         | Data ingestion rate              |
| Total MergeTree Parts     | Active parts in MergeTree tables |
| Max Parts for Partition   | Maximum parts in any partition   |
| Queries Running           | Currently executing queries      |
| Selected Bytes Per Second | Volume of data being read        |

### System health metrics

| Metric                   | Description                                     |
| ------------------------ | ----------------------------------------------- |
| IO Wait                  | I/O wait times                                  |
| CPU Wait                 | Delays from CPU resource contention             |
| Read From Disk           | Bytes read from disks/block devices             |
| Read From Filesystem     | Bytes read from filesystem including page cache |
| Memory (tracked)         | Memory usage for tracked processes              |
| Load Average (15 min)    | System load average                             |
| OS CPU Usage (Userspace) | CPU running userspace code                      |
| OS CPU Usage (Kernel)    | CPU running kernel code                         |

### ClickHouse Cloud-specific metrics

| Metric                         | Description                      |
| ------------------------------ | -------------------------------- |
| S3 Read wait                   | Latency of S3 read requests      |
| S3 read errors/sec             | Read error rate                  |
| Read From S3                   | Rate of data read from S3        |
| Disk S3 write req/sec          | Write operation frequency to S3  |
| Disk S3 read req/sec           | Read operation frequency from S3 |
| Page cache hit rate            | Page cache effectiveness         |
| Filesystem cache hit rate      | Filesystem cache effectiveness   |
| Network send/receive bytes/sec | Network throughput               |

## 3. Identifying common issues

### 3.1. Unbatched inserts

**Indicators:**

- Spike in **Max Parts for Partition** with slow **Inserted Rows/sec**
- Many small parts being created

**Solution:** Use bulk inserts with reasonable batch sizes.

### 3.2. Resource-intensive queries

**Indicators:**

- CPU usage spikes without change in query throughput
- Sudden increase in memory usage

**Detection:** Check `system.query_log` for queries during peak times:

```sql
SELECT
    type,
    event_time,
    query_duration_ms,
    query,
    read_rows,
    memory_usage,
    tables
FROM system.query_log
WHERE event_time >= '2024-12-23 11:20:00'
  AND event_time <= '2024-12-23 11:30:00'
  AND type = 'QueryFinish'
ORDER BY query_duration_ms DESC
LIMIT 10
FORMAT VERTICAL
```

### 3.3. Bad primary key design

**Indicators:**

- Sudden peak in **Selected Rows per second**
- Queries reading many rows for small result sets

**Detection:** Compare queries against tables with different primary keys to identify optimization opportunities.

## 4. Custom visualizations

### Add custom charts

Click "Add chart" in the dashboard and provide a SQL query:

```sql
SELECT
    toStartOfInterval(event_time, INTERVAL {rounding:UInt32} SECOND)::INT AS t,
    avg(value)
FROM merge('system', '^asynchronous_metric_log')
WHERE event_date >= toDate(now() - {seconds:UInt32})
  AND event_time >= now() - {seconds:UInt32}
  AND metric = 'TotalPrimaryKeyBytesInMemory'
GROUP BY t
ORDER BY t
WITH FILL STEP {rounding:UInt32}
```

### Store custom dashboards

```sql
CREATE DATABASE custom;

CREATE TABLE custom.dashboards
(
    `dashboard` String,
    `title` String,
    `query` String
) ORDER BY ();

INSERT INTO custom.dashboards (dashboard, title, query)
VALUES (
    'Overview',
    'Total primary keys size',
    'SELECT toStartOfInterval(event_time, INTERVAL {rounding:UInt32} SECOND)::INT AS t, avg(value) FROM merge(\'system\', \'^asynchronous_metric_log\') WHERE event_date >= toDate(now() - {seconds:UInt32}) AND event_time >= now() - {seconds:UInt32} AND metric = \'TotalPrimaryKeyBytesInMemory\' GROUP BY t ORDER BY t WITH FILL STEP {rounding:UInt32}'
);
```

Query merged dashboards:

```sql
SELECT title, query
FROM merge(REGEXP('custom|system'),'dashboards')
WHERE dashboard = 'Overview'
```

## 5. Key monitoring queries

### Long-running queries

```sql
SELECT
    type,
    event_time,
    query_duration_ms,
    formatReadableSize(memory_usage) AS memory,
    normalizedQueryHash(query) AS normalized_query_hash,
    substring(normalizeQuery(query), 1, 100) AS query
FROM system.query_log
ORDER BY query_duration_ms DESC
LIMIT 10
FORMAT VERTICAL
```

### Failed queries

```sql
SELECT
    name,
    code,
    value,
    last_error_time,
    last_error_message
FROM system.errors
LIMIT 10
FORMAT VERTICAL
```

### Merge status

```sql
SELECT
    database,
    table,
    round(elapsed, 0) AS time,
    round(progress, 4) AS percent,
    formatReadableTimeDelta((elapsed / progress) - elapsed) AS ETA,
    num_parts,
    formatReadableSize(memory_usage) AS memory_usage
FROM system.merges
ORDER BY (elapsed / percent) - elapsed ASC
FORMAT VERTICAL
```

### Stuck mutations

```sql
SELECT
    database,
    table,
    mutation_id,
    command,
    create_time,
    parts_to_do,
    is_done,
    latest_fail_reason
FROM system.mutations
WHERE NOT is_done
ORDER BY create_time DESC
```

### Disk space by table

```sql
SELECT
    database,
    table,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS total_bytes,
    round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 3) AS compression_ratio
FROM system.parts
WHERE database != 'system'
GROUP BY database, table
ORDER BY sum(bytes_on_disk) DESC
FORMAT VERTICAL
```

## 6. Integration with other tools

ClickHouse integrates with monitoring tools like [Prometheus](https://clickhouse.com/docs/en/integrations/prometheus) for more comprehensive observability.
