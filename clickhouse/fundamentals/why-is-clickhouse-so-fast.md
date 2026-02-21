# Why is ClickHouse so fast?

Source: <https://clickhouse.com/docs/concepts/why-clickhouse-is-so-fast>

Many factors contribute to a database's performance besides its data orientation. ClickHouse provides innovations in both the storage layer and query processing layer that enable extremely fast inserts and SELECT queries.

## 1. Storage layer: Concurrent inserts are isolated

In ClickHouse, each table consists of multiple "table parts". A part is created whenever a user inserts data into the table (INSERT statement). A query is always executed against all table parts that exist at the time the query starts.

To avoid too many parts accumulating, ClickHouse runs a merge operation in the background which continuously combines multiple smaller parts into a single bigger part.

This approach has several advantages:

- All data processing can be offloaded to background part merges
- Data writes remain lightweight and highly efficient
- Individual inserts are "local" - they don't need to update global per-table data structures
- Multiple simultaneous inserts need no mutual synchronization
- Inserts can be performed almost at the speed of disk I/O

## 2. Storage layer: Concurrent inserts and selects are isolated

Inserts are fully isolated from SELECT queries. Merging inserted data parts happens in the background without affecting concurrent queries.

## 3. Storage layer: Merge-time computation

Unlike other databases, ClickHouse keeps data writes lightweight and efficient by performing all additional data transformations during the merge background process.

Examples include:

- **Replacing merges** - retain only the most recent version of a row, discard all other versions
- **Aggregating merges** - combine intermediate aggregation states to new aggregation state (incremental aggregation)
- **TTL merges** - compress, move, or delete rows based on time-based rules

This shifts work from query time to merge time, making queries significantly faster (sometimes 1000x or more) while not significantly impacting merge runtime.

## 4. Storage layer: Data pruning

ClickHouse provides three techniques for data pruning:

### 4.1. Primary key indexes

Define the sort order of table data. A well-chosen primary key allows evaluating filters using fast binary searches instead of full-column scans. Runtime becomes logarithmic instead of linear in data size.

### 4.2. Table projections

Alternative, internal versions of a table storing the same data but sorted by a different primary key. Useful when there's more than one frequent filter condition.

### 4.3. Skipping indexes

Embed additional data statistics into columns (min/max, unique values, etc.). Orthogonal to primary keys and projections, they can greatly speed up filter evaluation.

All three techniques aim to skip as many rows during reads as possible - the fastest way to read data is to not read it at all.

## 5. Storage layer: Data compression

ClickHouse's storage layer optionally compresses raw table data using different codecs:

- Generic compression algorithms (ZSTD, LZ4)
- Specialized codecs: Gorilla and FPC for floating-point, Delta and GCD for integers
- AES as an encrypting codec

Column-stores are particularly well suited for compression as values of the same type and distribution are located together. Data compression reduces storage size and often improves query performance by reducing I/O constraints.

## 6. State-of-the-art query processing layer

ClickHouse uses a vectorized query processing layer that parallelizes query execution to utilize all resources.

### Vectorization

Query plan operators pass intermediate result rows in batches instead of single rows:

- Better CPU cache utilization
- Operators can apply SIMD instructions to process multiple values at once
- Many operators come in multiple versions - one per SIMD instruction set generation
- ClickHouse automatically selects the fastest version based on hardware capabilities

### Parallelization

- Modern systems have dozens of CPU cores
- ClickHouse unfolds the query plan into multiple lanes (typically one per core)
- Each lane processes a disjoint range of table data
- Performance scales "vertically" with available cores
- For horizontal scaling, tables can be sharded across nodes

## 7. Meticulous attention to detail

> "ClickHouse is a freak system - you guys have 20 versions of a hash table. You guys have all these amazing things where most systems will have one hash table... ClickHouse has this amazing performance because it has all these specialized components" - Andy Pavlo, Database Professor at CMU

### Hash Tables

Hash tables are central to joins and aggregations. Design decisions include:

- Hash function choice
- Collision resolution: open addressing or chaining
- Memory layout: one array for keys/values or separate arrays
- Fill factor and resize behavior
- Deletion handling

ClickHouse chooses from **30+ precompiled hash table variants** based on query and data specifics.

### Algorithms

Sorting algorithms consider:

- What's being sorted: numbers, tuples, strings, structures?
- Is data in RAM?
- Is stable sort required?
- Partial or full sort needed?

Algorithms that rely on data characteristics often outperform generic counterparts. When characteristics aren't known, the system can try implementations and choose the best at runtime.

## 8. Key performance factors summary

| Factor | Benefit |
|--------|---------|
| Columnar storage | Only read needed columns |
| Sparse primary index | Skip irrelevant data granules |
| Merge-time computation | Shift work from query to insert time |
| Vectorized execution | SIMD instructions, better cache utilization |
| Parallel processing | Utilize all CPU cores |
| Specialized data structures | Optimal algorithms for specific cases |
| Efficient compression | Reduced I/O, better cache efficiency |

## References

- [VLDB 2024 Paper](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) - ClickHouse architectural overview
- [Hash Tables in ClickHouse](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions)
- [LZ4 Decompression Implementation](https://habr.com/en/company/yandex/blog/457612/)
