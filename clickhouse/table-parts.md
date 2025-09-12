# Table parts

Source:

- <https://clickhouse.com/docs/parts>
- <https://altinity.com/blog/understanding-detached-parts-in-clickhouse>

The data from each table in the ClickHouse MergeTree engine family is organized on disk as a collection of immutable `data parts`. A data part is created whenever a set of rows is inserted into the table, each part is an immutable chunk of data, organized in a columnar format.

The following diagram sketches this:

![](https://clickhouse.com/docs/assets/ideal-img/part.d9b96ef.2048.png)

When a ClickHouse server processes the example insert with 4 rows (e.g., via an INSERT INTO statement) sketched in the diagram above, it performs several steps:

1. Sorting: The rows are sorted by the table's sorting key (town, street), and a sparse primary index is generated for the sorted rows.
2. Splitting: The sorted data is split into columns.
3. Compression: Each column is compressed.
4. Writing to Disk: The compressed columns are saved as binary column files within a new directory representing the insert's data part. The sparse primary index is also compressed and stored in the same directory.

Data parts are self-contained, including all metadata needed to interpret their contents without requiring a central catalog. Beyond the sparse primary index, parts contain additional metadata, such as secondary data skipping indexes, column statistics, checksums, min-max indexes (if partitioning is used), and more.

To manage the number of parts per table, a background **merge** job periodically combines smaller parts into larger ones until they reach a configurable compressed size (typically ~150 GB). Merged parts are marked as inactive and deleted after a configurable time interval. Over time, this process creates a hierarchical structure of merged parts, which is why it's called a MergeTree table:

![](https://clickhouse.com/docs/assets/ideal-img/merges.285da65.2048.png)

- Active data parts:
  - Current Data: Active parts represent the current, valid data that is used when querying the table.
  - MergeTree Operations: When data is inserted, updated (via mutations), or merged, new active parts are created to reflect the latest state.
  - Queryable: Only active parts are considered by SELECT queries.
- Inactive Data Parts:
  - Historical or Superseded Data: Inactive parts are older versions of data that are no longer considered part of the active dataset. This typically occurs in scenarios such as:
  - Merges: When smaller data parts are merged into a larger, consolidated part, the original smaller parts become inactive.
  - Mutations: When rows are updated or deleted, new active parts are created with the changes, and the old parts containing the superseded data become inactive.
  - Pending Deletion: Inactive parts are essentially marked for eventual removal by ClickHouse's background cleanup processes. They are kept for a certain period to ensure data consistency during merges and mutations, but are not used for queries.
  - Not Queryable: Inactive parts are not accessed by SELECT queries.

Over time, the system automatically merges these parts based on certain rules and heuristics (like size and age) to keep the number of parts manageable and maintain optimal read efficiency. While merges improve performance in the long run, they consume CPU, disk I/O, and memory, so their behavior can be fine-tuned or throttled for low-resource environments.

But what happens when data changes? Since, ClickHouse doesn’t modify existing parts directly, (they are immutable, remember?), merges also handle data cleanup for deleted or updated rows. These type of merges are called mutations. If a part needs to be mutated, ClickHouse will create a new part with the changes, mark the old one as inactive and the new one as active, so the cleaning background process can delete those and reclaim space.

Inactive parts are essentially data segments that are no longer part of the active dataset but still exist on disk. They’re like old snapshots of your data, waiting to be cleaned up.

Ok, so what is the difference between inactive parts and detached parts? Think of **detached parts** as data chunks that are still physically present on your disk but are intentionally excluded from the table’s active data set. They can be explicitly detached by a ClickHouse command or can be automatically detached by Clickhouse, which is the most common case.

In contrast to detached parts, inactive parts are not explicitly put aside by an administrator. Instead, they represent an internal, transient state of data parts that are no longer considered the “current” version and are slated for eventual removal.

// WIP
