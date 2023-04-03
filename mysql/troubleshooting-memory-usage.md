# Troubleshooting MySQL memory usage

Source: <https://www.percona.com/blog/2012/03/21/troubleshooting-mysql-memory-usage/>

Table of contents:

- [Troubleshooting MySQL memory usage](#troubleshooting-mysql-memory-usage)
  - [1. Plot Memory Usage](#1-plot-memory-usage)
  - [2. Check Table Cache Related Allocations](#2-check-table-cache-related-allocations)
  - [3. Connection Related Allocations](#3-connection-related-allocations)
  - [4. Memory Tables](#4-memory-tables)
  - [5. Innodb Memory Usage](#5-innodb-memory-usage)
  - [6. MySQL command pager](#6-mysql-command-pager)

## 1. Plot Memory Usage

- MySQL memory consumption plotted -> VSZ columns from ps output on Linux.
- Simple script:

```shell
while true
do
  date >> ps.log
  ps aux | grep mysqld >> ps.log
  sleep 60
done
```

## 2. Check Table Cache Related Allocations

- MySQL will allocate a lot of memory of table cache.
- Run `FLUSH TABLES`;

## 3. Connection Related Allocations

## 4. Memory Tables

- Memory tables can take memory.
- Implicit MEMORY Tables size can be controlled by \*`tmp_table_size`.
- Explicit MEMORY Tables - limit size with `max_heap_table_size`.
- Commands:

```sql
mysql> select sum(data_length+index_length) from information_schema.tables where engine='memory';
+-------------------------------+
| sum(data_length+index_length) |
+-------------------------------+
|                        126984 |
+-------------------------------+
1 row in set (0.98 sec)

mysql> select sum(data_length+index_length) from information_schema.global_temporary_tables where engine='memory';
+-------------------------------+
| sum(data_length+index_length) |
+-------------------------------+
|                        126984 |
+-------------------------------+
1 row in set (0.00 sec)
```

## 5. Innodb Memory Usage

- Check how much InnoDB has allocated.
- Command:

```sql
SHOW ENGINE INNODB STATUS;

BUFFER POOL AND MEMORY
----------------------
Total memory allocated 132183490560; in additional pool allocated 0
Internal hash tables (constant factor + variable factor)
    Adaptive hash index 4422068288      (2039977928 + 2382090360)
    Page hash           127499384
    Dictionary cache    512619219       (509995888 + 2623331)
    File system         294352  (82672 + 211680)
    Lock system         318875832       (318747272 + 128560)
    Recovery system     0       (0 + 0)
    Threads             425080  (406936 + 18144)
Dictionary memory allocated 2623331
Buffer pool size        7864319
Buffer pool size, bytes 128849002496
Free buffers            1
Database pages          8252672
Old database pages      3046376
Modified db pages       23419
```

## 6. MySQL command pager

- [Source](https://www.percona.com/blog/2008/06/23/neat-tricks-for-the-mysql-command-line-pager/)
- For big result sets, it's a pretty handy way to be able to search and scroll though with `pager less`.
