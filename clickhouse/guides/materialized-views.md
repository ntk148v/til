# Materialized Views

Source: <https://den-crane.github.io/Everything_you_should_know_about_materialized_views_commented.pdf>

A materialized view is a special trigger that stores the result of a SELECT query on data, as it is inserted, into a target table.

![Materialized View](https://clickhouse.com/uploads/materialized_view_5a321dc56d.png)

## 1. How materialized views work

### Key concepts

- An MV is an **insert trigger**
- An MV **never reads** its source table
- MV processes data from the INSERT block, not from the stored table

### Processing flow

1. INSERT arrives with 3 million rows
2. Data is processed in streaming manner, separated into blocks (based on `max_insert_blocks_size`)
3. Blocks written to table (may form multiple parts due to partitioning)
4. Each block triggers the MV's SELECT
5. MV results stored in target table (may also form multiple parts)

## 2. Use cases

### Pre-aggregation

Accelerate queries by precomputing aggregations at INSERT time:

```sql
CREATE TABLE visits (
    CounterID UInt32,
    StartDate Date,
    Sign Int32,
    UserID UInt64
)
ENGINE = MergeTree()
ORDER BY (CounterID, StartDate);

CREATE TABLE visits_agg (
    CounterID UInt32,
    StartDate Date,
    Visits AggregateFunction(sum, Int32),
    Users AggregateFunction(uniq, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (CounterID, StartDate);

CREATE MATERIALIZED VIEW visits_mv
TO visits_agg
AS SELECT
    CounterID,
    StartDate,
    sumState(Sign) AS Visits,
    uniqState(UserID) AS Users
FROM visits
GROUP BY CounterID, StartDate;
```

### Data transformation

Transform and route data to different tables:

```sql
CREATE MATERIALIZED VIEW errors_mv
TO error_logs
AS SELECT *
FROM all_logs
WHERE level = 'ERROR';
```

### Multiple primary indexes

Create alternative sort orders for different query patterns:

```sql
-- Main table ordered by user
CREATE TABLE events (
    user_id UInt32,
    timestamp DateTime,
    event_type String
)
ENGINE = MergeTree()
ORDER BY (user_id, timestamp);

-- MV for time-based queries
CREATE MATERIALIZED VIEW events_by_time
TO events_time_ordered
AS SELECT * FROM events;

-- Target table with different order
CREATE TABLE events_time_ordered (
    user_id UInt32,
    timestamp DateTime,
    event_type String
)
ENGINE = MergeTree()
ORDER BY (timestamp, user_id);
```

## 3. Best practices

### Column matching

- MV SELECT column names must match target table column names
- Use aliases to ensure names match
- Target table can have default values for omitted columns

```sql
CREATE MATERIALIZED VIEW mv1 (timestamp Date, id Int64, counter Int64)
ENGINE = SummingMergeTree
ORDER BY (timestamp, id)
AS
SELECT timestamp, id, count() as counter  -- alias required
FROM source
GROUP BY timestamp, id;
```

### ORDER BY consistency

Target table ORDER BY must match MV SELECT's GROUP BY:

```sql
-- Correct
CREATE MATERIALIZED VIEW test.basic
ENGINE = AggregatingMergeTree()
ORDER BY (CounterID, StartDate)  -- matches GROUP BY
AS SELECT
   CounterID,
   StartDate,
   sumState(Sign) AS Visits
FROM test.visits
GROUP BY CounterID, StartDate;
```

### Limit views per table

- Each MV runs on every INSERT
- More than 50 MVs typically slows inserts significantly
- Each MV creates parts, contributing to "too many parts"
- Use `parallel_view_processing` setting for parallelization

## 4. Common issues

### MV doesn't see table changes

MVs only process INSERT blocks, not:

- Merges
- Partition drops
- Mutations
- Manual data modifications

If source table changes, update attached MVs manually.

### State functions are CPU-intensive

MV with many state functions (especially quantiles) can slow inserts:

```sql
-- CPU intensive
SELECT
    quantileState(0.5)(value),
    quantileState(0.95)(value),
    quantileState(0.99)(value)
```

### Target table mismatch

Common errors when target table doesn't match MV:

- Different column names → silent data loss
- Different ORDER BY → incorrect aggregation
- Missing columns → errors (unless defaults exist)

## 5. Managing materialized views

### Create MV

```sql
CREATE MATERIALIZED VIEW [IF NOT EXISTS] [db.]table_name
[TO [db.]name]  -- target table
AS SELECT ...
FROM source_table
[WHERE ...]
[GROUP BY ...]
[ORDER BY ...];
```

### Drop MV

```sql
DROP VIEW [IF EXISTS] [db.]view_name;
```

### Check MV status

```sql
SELECT *
FROM system.tables
WHERE engine = 'MaterializedView';

SELECT *
FROM system.views
WHERE database = 'your_db';
```

## 6. Performance considerations

| Factor | Impact | Mitigation |
|--------|--------|------------|
| Number of MVs | More MVs = slower inserts | Consolidate where possible |
| Complexity of SELECT | Complex queries = more CPU | Simplify transformations |
| State functions | Quantiles, uniq = expensive | Use approximate versions |
| Target table parts | Each MV creates parts | Monitor part count |
| Parallel processing | Reduces latency | Enable `parallel_view_processing` |
