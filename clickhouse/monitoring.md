# Monitoring

Source:

- <https://clickhouse.com/docs/operations/monitoring>
- <https://sematext.com/clickhouse-monitoring-key-metrics/>

## 1. Event metrics

- Total query count – clickhouse.query.count. This number represents the total number of queries in your ClickHouse integration. It’s a key metric for assessing the overall level of activity in your ClickHouse system.
- Inserted rows – clickhouse.insert.rows. This metric represents the number of rows inserted in all tables and reflects the level of activity within your database, as well as database size.
- Inserted bytes – clickhouse.insert.bytes. The number of uncompressed bytes inserted in all tables. Also a reflection of activity level and database size.
- Merged rows – clickhouse.merge.rows. Rows read for background merges. This is the number of rows before a merge. This metric represents the number of rows before a merge.
- Uncompressed bytes merged – clickhouse.merge.bytes.uncompressed. Uncompressed bytes that were read for background merges. This is the number before a merge.

## 2. Network metrics

- TCP Connections – clickhouse.connection.tcp.count. The total number of connections to TCP server. Helps measure the load of your ClickHouse installation.
- HTTP Connections – clickhouse.connection.http.count (long gauge). Number of connections to the HTTP server. Also a reflection of load.
- Interserver Connections – clickhouse.connection.interserver.count. This metric represents the number of connections from other replicas to fetch parts. It’s not directly tied to overall system load, but it is useful for assessing and optimizing the performance of your ClickHouse installation.

## 3. Zookeeper metrics

- ZooKeeper watches – clickhouse.zk.watches. The number of watches (e.g., event subscriptions) in ZooKeeper.
- ZooKeeper wait – clickhouse.zk.wait.time. Time spent waiting for ZooKeeper operations
- ZooKeeper requests – clickhouse.zk.requests. Number of requests to ZooKeeper in progress.

## 4. Asynchronous metrics

- Max active part count – clickhouse.part.count.max. This metric represents the maximum number of active parts in ClickHouse partitions. If a part is active, it is used in a table; otherwise, it will be deleted. Inactive data parts remain after merging.

## 5. Data part metrics

- Active part count – clickhouse.mergetree.table.parts. The number of active parts in MergeTree tables.
- Row count – clickhouse.mergetree.table.rows. The number of row counts in MergeTree tables.

## 6. Replica status

- Replica queue size – clickhouse.replica.queue.size. This metric represents the size of the queue for operations waiting to be performed. In this case, operations include inserting blocks of data, merges, and certain other actions.
