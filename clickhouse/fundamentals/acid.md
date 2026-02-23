# ClickHouse ACID compliance

ClickHouse is fundamentally an **OLAP** (Online Analytical Processing) database, meaning it is optimized for high-speed reads and massive batch inserts rather than the row-level transactional integrity found in databases like PostgreSQL or MySQL.

While ClickHouse does not support traditional, multi-statement ACID transactions (e.g., `BEGIN...COMMIT`), it provides specific transactional guarantees for certain operations.

---

## 1. The ACID Breakdown

How ClickHouse handles the four pillars of ACID:

- **Atomicity:** \* **Single-Block Inserts:** Inserts are atomic at the **block** level. If you insert a batch of 100,000 rows, either the entire block is written, or none of it is.
- **Multi-Statement:** ClickHouse does **not** support atomicity across multiple separate queries or across multiple tables. There is no "rollback" for a sequence of different operations.

- **Consistency:** \* ClickHouse ensures structural consistency (data matches the schema), but it does not enforce traditional relational constraints like **Foreign Keys** or **Unique Constraints** (except via specific engines like `ReplacingMergeTree`, which handles duplicates eventually).
- **Isolation:** \* ClickHouse provides **Snapshot Isolation** for reads. A query will see a consistent snapshot of the data as it existed when the query began. However, because it is a distributed system, you may experience "eventual consistency" across different replicas unless specifically configured.
- **Durability:** \* By default, ClickHouse prioritizes performance and may not `fsync` every single write to disk immediately (relying on the OS page cache). To guarantee hardware-level durability, you must enable `fsync` settings, which can significantly slow down ingestion.

---

## 2. Experimental Transaction Support

As of 2024–2026, ClickHouse has introduced **experimental** support for multi-statement transactions. This allows for more traditional transactional behavior but comes with heavy caveats:

- **Must be enabled manually:** Set `allow_experimental_transactions = 1`.
- **Scope:** It primarily works for local (single-server) operations and does not yet fully support distributed transactions across a large cluster with the same maturity as an OLTP database.

---

## 3. ACID in Distributed Environments

When working with clusters, the "C" (Consistency) and "I" (Isolation) are managed through **ClickHouse Keeper** (or ZooKeeper).

| Feature           | Behavior                                                                                                         |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Replication**   | Asynchronous by default. A write to one node is eventually visible on others.                                    |
| **Quorum Writes** | You can configure `insert_quorum` to ensure data is written to a majority of nodes before acknowledging success. |
| **Deduplication** | ClickHouse automatically deduplicates retried inserts to ensure "Exactly-Once" semantics for data ingestion.     |

---

## 4. Summary: When to Use What

- **Use ClickHouse if:** You need to insert millions of rows per second and run complex analytical queries over billions of records. You can live with "eventual consistency" across replicas.
- **Avoid ClickHouse if:** You are building an ATM system, an e-commerce checkout, or any application where a "partial success" between two tables (like moving money from Account A to Account B) would be a disaster.
