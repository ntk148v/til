# Common Getting Started Issues

Source: <https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse>

This guide covers the 13 "Deadly Sins" of getting started with ClickHouse and how to avoid them.

## 1. Too many parts

A common ClickHouse error usually pointing to incorrect usage. When data is inserted, separate data parts are created, each lexicographically sorted by primary key. Background merges combine parts for efficiency. Too many parts results in:

- Slower queries (more indices to evaluate, more files to read)
- Slow startup times
- Pressure on ClickHouse Keeper in replicated configurations

### Causes and solutions

**Poorly chosen partitioning key:**

- Parts belonging to different partitions are never merged
- Choose a partition key with cardinality < 1000
- Avoid high-cardinality keys like `date_time_ms`

**Many small inserts:**

- Each INSERT creates a new part
- Buffer data client-side and insert as batches (ideally 1000+ rows)
- Use [async inserts](https://clickhouse.com/docs/en/operations/settings/settings/#async-insert) if client-side buffering isn't possible

**Excessive materialized views:**

- Each MV creates parts on insert
- Consolidate views where possible

## 2. Going horizontal too early

ClickHouse was designed to utilize full machine resources. Unlike databases limited by JVM heap size, ClickHouse can run on servers with:

- Hundreds of cores
- Terabytes of RAM
- Petabytes of disk space

**Benefits of vertical scaling first:**

- Cost efficiency
- Lower operational complexity
- Better query performance (minimized network data transfer for JOINs)

Two machines should be sufficient for all but the largest use cases. Go vertical before going horizontal.

## 3. Mutation pain

ClickHouse performs best on immutable data. [Mutations](https://clickhouse.com/docs/en/sql-reference/statements/alter/#mutations) rewrite whole data parts using the same thread pool as merges.

**Issues:**

- CPU and IO-intensive
- Can cause "too many parts" errors
- May cause replication delays

**Alternatives:**

- Deduplicate upstream before insertion
- Use `ReplacingMergeTree` for deduplication
- Use [lightweight deletes](https://clickhouse.com/docs/en/sql-reference/statements/delete/) for deletions (experimental)
- Monitor via `system.mutations` table

## 4. Unnecessary use of complex types

ClickHouse supports complex types (Nested, Tuple, Map, JSON), but primitive types offer best performance.

**JSON type limitations:**

- Increased insert cost (dynamic column creation)
- Sub-optimal type usage (no codecs, unnecessary Nullable)
- Cannot use JSON columns in primary key

**Nullable type:**

- Requires extra byte per value
- Adds query time overhead
- Only use if really needed

**Recommendation:** If you know your schema, specify it explicitly.

## 5. Deduplication at insert time

Identical inserts may appear to have no effect. This is due to [`replicated_deduplication_window`](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#replicated-deduplication-window):

- Hash of inserted blocks is stored in ClickHouse Keeper
- Subsequent identical blocks are ignored
- Allows safe retry of inserts after network interruptions
- Default window: 100 blocks

This behavior can be enabled for non-replicated instances via [`non_replicated_deduplication_window`](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#replicated-deduplication-window).

## 6. Poor primary key selection

ClickHouse uses a sparse index designed for millions of inserts per second and petabyte-scale datasets.

**Guidelines:**

- Select columns often used in WHERE clauses
- 2-3 columns rarely required
- Order columns by cardinality (ascending)
- Order affects compression and filtering efficiency

**Example:** `ORDER BY (tenant_id, site_id, timestamp)` - lower cardinality first.

## 7. Overuse of data skipping indices

Data skipping indices can accelerate queries but are often overused.

**Issues:**

- Slow insert performance
- Rarely improve query performance
- Complicate table design

**Recommendations:**

- Only consider after investigating alternatives (modify primary key, projections, materialized views)
- Works best with strong correlation between primary key and targeted column
- Check index size in `system.data_skipping_indices`

## 8. LIMIT doesn't always short circuit

**OLTP intuition doesn't always apply:**

- `SELECT * FROM table LIMIT 10` - scans only few granules (streaming)
- `SELECT a FROM table ORDER BY b LIMIT N` - may require full table scan if table ordered by `a` not `b`
- Aggregations with LIMIT may need full scan

**Optimization:**

- Use `optimize_aggregation_in_order=1` for GROUP BY primary key
- Point lookups require careful index design

## 9. IP Filtering in Cloud

When creating a ClickHouse Cloud cluster, you must specify allowed IP addresses.

**Recommendation:**

- Be restrictive by default
- Obtain IPs of external services (e.g., Grafana Cloud) early
- Modify allow list as needed

## 10. Read-only tables

Occurs in replicated environments when a node loses connection to ZooKeeper.

**Causes:**

- Under-resourced ZooKeeper
- Hosting keeper on same host as ClickHouse in production
- Poorly tuned ZooKeeper JVM resources

**Solution:** Separate keeper on dedicated hardware with adequate resources.

## 11. Memory limit exceeded for query

Common causes: large JOINs or high-cardinality aggregations.

### Aggregations

Use settings for spilling to disk:

- `max_bytes_before_external_group_by`
- `max_bytes_before_external_sort`

### JOINs

Different algorithms for different scenarios:

- **Hash join** (default) - best performance, most memory
- **Partial merge** - less memory, slower
- **Full sorting merge** - for very large tables
- **Auto** - adaptive approach

**Recommendation:** Place smaller table on right side of JOIN.

### Rogue queries

- Set [quotas](https://clickhouse.com/docs/en/operations/quotas/)
- Use [query complexity restrictions](https://clickhouse.com/docs/en/operations/settings/query-complexity/)
- Consider [memory overcommit](https://clickhouse.com/docs/en/operations/settings/memory-overcommit/)

## 12. Issues with materialized views

Common misunderstandings:

- MVs are insert triggers only - no knowledge of source table data
- No visibility of merges, partition drops, or mutations
- Changes to source table require updating attached MVs

**Best practices:**

- Limit to < 50 MVs per table (more slows inserts)
- Use `parallel_view_processing` for parallelization
- Ensure target table ORDER BY matches MV GROUP BY
- Column names in MV SELECT must match target table (use aliases)

**Example:**

```sql
CREATE MATERIALIZED VIEW test.mv1 (timestamp Date, id Int64, counter Int64)
ENGINE = SummingMergeTree
ORDER BY (timestamp, id)
AS
SELECT timestamp, id, count() as counter
FROM source
GROUP BY timestamp, id;
```

## 13. Experimental features in production

Experimental features are marked in docs and require explicit enabling.

**Risks:**

- May change or be deprecated
- Not suitable for core functionality
- Require understanding of caveats

**Recommendation:** Don't build critical functionality around experimental features.
