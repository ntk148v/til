# Operations

Source: <https://posthog.com/handbook/engineering/clickhouse/operations>

Table of contents:

- [Operations](#operations)
  - [1. System tables](#1-system-tables)
    - [1.1. Overview](#11-overview)
    - [1.2. Hot tips for querying system tables](#12-hot-tips-for-querying-system-tables)
      - [1.2.1. What settings were changed from the default value?](#121-what-settings-were-changed-from-the-default-value)
      - [1.2.2. What are the long-running queries? Which queries took up the most memory?](#122-what-are-the-long-running-queries-which-queries-took-up-the-most-memory)
      - [1.2.3. Which queries have failed?](#123-which-queries-have-failed)
      - [1.2.4. Are parts being created when the rows are inserted?](#124-are-parts-being-created-when-the-rows-are-inserted)
      - [1.2.5. What is the status of the in-progress merges?](#125-what-is-the-status-of-the-in-progress-merges)
      - [1.2.6. Are there parts with errors?](#126-are-there-parts-with-errors)
      - [1.2.7. Are there long-running mutations that are stuck?](#127-are-there-long-running-mutations-that-are-stuck)
      - [1.2.8. How much disk space are the tables using?](#128-how-much-disk-space-are-the-tables-using)
      - [1.2.9. What is the status of the parts that are moving?](#129-what-is-the-status-of-the-parts-that-are-moving)
      - [1.2.10. Querying system tables from all nodes in a cluster?](#1210-querying-system-tables-from-all-nodes-in-a-cluster)

## 1. System tables

### 1.1. Overview

- ClickHouse exposes a lot of information about its internals in [system tables](https://clickhouse.com/docs/operations/system-tables).
  - System tables are virtual tables.
  - Read-only.
  - Cannot be dropped or altered, but their partition can be detached and old records can be removed using TTL.
- Some stand-out tables:
  - `system.query_log` and `system.processes` contain information on queries executed on the server
  - `system.tables` and `system.columns` contain metadata about tables and columns
  - `system.merges` and `system.mutations` contain information about ongoing operations
  - `system.replicated_fetches` and `system.replication_queue` contain information about data replication.
  - `system.errors` and `system.crash_log` contain information about errors and crashes respectively.
  - `system.distributed_ddl_queue` shows information to help diagnose progress of ON CLUSTER commands.
  - `system.settings`, `system.users`, and `systems.roles` provide information on the current configuration and user privileges.
  - `system.metrics`, `system.events`: show real-time information, provide a snapshot view of the current system events.
- Most system tables store their data in memory, but system log tables such (`metric_log`, `query_log`, `part_log`) use the MergeTree table engine and store their data in the filesystem by default.
- Explore:

```sql
SELECT *
FROM system.databases
LIMIT 2
FORMAT vertical

Query id: b0723853-414d-4d94-bfde-e1313f7128fa

Row 1:
──────
name:          INFORMATION_SCHEMA
engine:        Memory
data_path:     /var/lib/clickhouse/
metadata_path:
uuid:          00000000-0000-0000-0000-000000000000
engine_full:   Memory
comment:
is_external:   0

Row 2:
──────
name:          default
engine:        Atomic
data_path:     /var/lib/clickhouse/store/
metadata_path: store/56f/56fdce48-167d-4902-8e24-a04a86cb782f/
uuid:          56fdce48-167d-4902-8e24-a04a86cb782f
engine_full:   Atomic
comment:
is_external:   0

2 rows in set. Elapsed: 0.005 sec.

SELECT
    engine,
    count() AS count
FROM system.databases
GROUP BY engine;

Query id: f4803531-78fe-4928-9871-7e1d54153942

   ┌─engine─┬─count─┐
1. │ Memory │     2 │
2. │ Atomic │     3 │
   └────────┴───────┘

2 rows in set. Elapsed: 0.008 sec.
```

### 1.2. Hot tips for querying system tables

#### 1.2.1. What settings were changed from the default value?

During troubleshooting, we should begin by reviewing the list of settings that were changed from the default value.

```sql
SELECT *
FROM system.settings
WHERE changed
LIMIT 2
FORMAT Vertical
```

#### 1.2.2. What are the long-running queries? Which queries took up the most memory?

Next, we dive into the query log table (system.query_log) that holds a wealth of information about executed queries. It is often the go-to table for identifying long-running, memory-intensive, or failed queries.

```sql
-- resource utilized: memory_usage, userCPU, systemCPU
-- normalizedQueryHash hashes similar queries into identical 64-bit hash values, allowing us to further aggrgate the value and monitor performance for similar queries.
SELECT
    type,
    event_time,
    query_duration_ms,
    initial_query_id,
    formatReadableSize(memory_usage) AS memory,
    `ProfileEvents.Values`[indexOf(`ProfileEvents.Names`, 'UserTimeMicroseconds')] AS userCPU,
    `ProfileEvents.Values`[indexOf(`ProfileEvents.Names`, 'SystemTimeMicroseconds')] AS systemCPU,
    normalizedQueryHash(query) AS normalized_query_hash,
    substring(normalizeQuery(query) AS query, 1, 100)
FROM system.query_log
ORDER BY query_duration_ms DESC
LIMIT 2
FORMAT Vertical
```

#### 1.2.3. Which queries have failed?

Next, we explore the `system.errors` table. This table contains error codes and the number of times each error has been triggered. Furthermore, we can see when the error last occurred coupled with the exact error message. The `last_error_trace` column also contains a stack trace for debugging and is helpful for introspecting the server state.

- The list of [error codes](https://github.com/ClickHouse/ClickHouse/blob/master/src/Common/ErrorCodes.cpp).
- [The most common errors and how to deal with them](https://www.tinybird.co/docs/sql-reference/clickhouse-errors).

```sql
SELECT
    name,
    code,
    value,
    last_error_time,
    last_error_message,
    last_error_trace AS remote
FROM system.errors
LIMIT 1
FORMAT Vertical
```

#### 1.2.4. Are parts being created when the rows are inserted?

To confirm that the rows inserted are successfully written into the disk as parts, we can review the `system.part_log` and check that new parts are created in a timely manner.

```sql
SELECT
    event_time,
    event_time_microseconds,
    rows
FROM system.part_log
ORDER BY event_time ASC
LIMIT 5
```

#### 1.2.5. What is the status of the in-progress merges?

As newly created parts are constantly merged in the background, we can watch for long-running merges using the `system.merges` table. Merges that take a long time to complete could mean that certain system resources (e.g. CPU, disk IO) have reached a saturation point.

```sql
SELECT
    hostName(),
    database,
    table,
    round(elapsed, 0) AS time,
    round(progress, 4) AS percent,
    formatReadableTimeDelta((elapsed / progress) - elapsed) AS ETA,
    num_parts,
    formatReadableSize(memory_usage) AS memory_usage,
    result_part_name
FROM system.merges
ORDER BY (elapsed / percent) - elapsed ASC
FORMAT Vertical
```

#### 1.2.6. Are there parts with errors?

To identify errors during part merges, we can again examine the `system.part_log` table to reveal the number of times a data part error occurred for a particular event type.

```sql
SELECT
    event_date,
    event_type,
    table,
    error AS error_code,
    errorCodeToName(error) AS error_code_name,
    count() as c
FROM system.part_log
WHERE (error_code != 0) AND (event_date > (now() - toIntervalMonth(1)))
GROUP BY
    event_date,
    event_type,
    error,
    table
ORDER BY
    event_date DESC,
    event_type ASC,
    table ASC,
    error ASC
```

#### 1.2.7. Are there long-running mutations that are stuck?

`ALTER` queries that are intended to manipulate table data are implemented with a mechanism called [mutations](https://clickhouse.com/docs/sql-reference/statements/alter#mutations). They are asynchronous background processes similar to merges in MergeTree tables that to produce new "mutated" versions of parts.

- For `*MergeTree` tables mutations execute by **rewriting whole data parts**. There is no atomicity — parts are substituted for mutated parts as soon as they are ready and a `SELECT` query that started executing during a mutation will see data from parts that have already been mutated along with data from parts that have not been mutated yet.
- Mutations are totally ordered.

![](https://clickhouse.com/uploads/sins_06_mutations_647f7d67d9.png)

- The query below lists the in-progress mutations and displays the reason of failure, if any.

```sql
SELECT
    database,
    table,
    mutation_id,
    command,
    create_time,
    parts_to_do_names,
    parts_to_do,
    is_done,
    latest_failed_part,
    latest_fail_time,
    latest_fail_reason
FROM system.mutations
WHERE NOT is_done
ORDER BY create_time DESC
```

#### 1.2.8. How much disk space are the tables using?

ClickHouse compresses data really well with the use of LZ4 compression codec by default. To find out how much disk space each table is using.

```sql
SELECT
    hostName(),
    database,
    table,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS total_bytes_on_disk,
    formatReadableSize(sum(data_compressed_bytes)) AS total_data_compressed_bytes,
    formatReadableSize(sum(data_uncompressed_bytes)) AS total_data_uncompressed_bytes,
    round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 3) AS compression_ratio
FROM system.parts
WHERE database != 'system'
GROUP BY
    hostName(),
    database,
    table
ORDER BY sum(bytes_on_disk) DESC FORMAT Vertical
```

#### 1.2.9. What is the status of the parts that are moving?

Other than parts merging in the background, parts and partitions can also be moved between disks and volumes. For example, it is common to first store the recently written parts on a hot volume (SSD) and then move them automatically to a cold volume (HDD) when they have passed a certain age. This operation can be done using the TTL clause or be triggered with the ALTER statement.

```sql
SELECT *
FROM system.moves FORMAT Vertical
```

#### 1.2.10. Querying system tables from all nodes in a cluster?

When querying for system tables in a cluster, take note that the query is only executed on the local node where the query is issued. To retrieve rows from all nodes in a cluster with shards and replicas, we need to use the `clusterAllReplicas` table function.

```sql
SELECT
    hostName(),
    is_initial_query,
    query_id,
    initial_query_id,
    query
FROM clusterAllReplicas('default', system.processes)
FORMAT Vertical
```
