# Operations

Source: <https://posthog.com/handbook/engineering/clickhouse/operations>

## 1. System tables

- ClickHouse exposes a lot of information about its internals in system tables.
- Some stand-out tables:

  - `system.query_log` and `system.processes` contain information on queries executed on the server
  - `system.tables` and `system.columns` contain metadata about tables and columns
  - `system.merges` and `system.mutations` contain information about ongoing operations
  - `system.replicated_fetches` and `system.replication_queue` contain information about data replication
  - `system.errors` and `system.crash_log` contain information about errors and crashes respectively
  - `system.distributed_ddl_queue` shows information to help diagnose progress of ON CLUSTER commands

- [ClickHouse system tables](https://clickhouse.com/blog/clickhouse-debugging-issues-with-system-tables)
