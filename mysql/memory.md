# How MySQL uses memory

Source:

- <https://dev.mysql.com/doc/refman/8.0/en/memory-use.html>
- <https://cloud.google.com/mysql/memory-usage>

Table of contents:

- [How MySQL uses memory](#how-mysql-uses-memory)
  - [1. Global buffers](#1-global-buffers)
    - [1.1. InnoDB buffer pool](#11-innodb-buffer-pool)
    - [1.2. InnoDB log buffer](#12-innodb-log-buffer)
    - [1.3. Key buffer size](#13-key-buffer-size)
  - [2. Global caches](#2-global-caches)
    - [2.1. Table cache](#21-table-cache)
    - [2.2. Thread cache](#22-thread-cache)
    - [2.3. InnoDB data dictionary cache](#23-innodb-data-dictionary-cache)
  - [3. Session buffers](#3-session-buffers)
    - [3.1. Binary log cache](#31-binary-log-cache)
    - [3.2. Temporary tables](#32-temporary-tables)
  - [4. Per connection memory](#4-per-connection-memory)
  - [5. Performance schema](#5-performance-schema)

MySQL allocates buffers and caches to improve performance of database operations. The default configuration is designed to permit a MySQL server to start on a virtual machine that has approximately 512MB of RAM.

Therefore, MySQL instances conusming lot of memory or running OOM issues is a common problem, often causes performance issues, staling, or even application downtime. Before start allocating memory for MySQL instances it is important to understand how MySQL uses memory.

## 1. Global buffers

MySQL allocates global buffers at the server startup and these are shared among all the connections. The majority of MySQL's memory is consumed by the global buffers.

### 1.1. InnoDB buffer pool

- InnoDB buffer pool is a memory area that holds cached `InnoDB` data for tables, indexes, and other auxilliary buffers.
- For efficiency of high-volume read operations, the buffer pool is divided into pages that can potentially hold multiple rows. For efficiency of cache management, the buffer pool is implemented as a linked list of pages; data that is rarely used is aged out of the cache, using a variation of the LRU algorithm.
- Typically the largest consumer of memory in a MySQL instance.
- Configured using [innodb_buffer_pool_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_buffer_pool_size) parameter.
  - Recommend value: **50-75% of system memory**.

- On systems with a large amount of memory, you can improve concurrency by diving the buffer pool into [multiple buffer pool instances](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_buffer_pool_instance), using [innodb_buffer_pool_instances](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_buffer_pool_instances).
- Check:

  ```sql
  mysql> show engine innodb status\G
  ```

### 1.2. InnoDB log buffer

- InnoDB log buffer is used to hold the changes to be written to the InnoDB redo log files on the disk.
- Configured using [innodb_log_buffer_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_buffer_size).
- Default value: 16 MB.

### 1.3. Key buffer size

- The key buffer is used by MySQL to cache the [MyISAM](https://dev.mysql.com/doc/refman/8.0/en/myisam-storage-engine.html) indexes in memory.
- Configured using [key_buffer_size](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_key_buffer_size).

## 2. Global caches

MySQL allocates global caches that are shared among all the connections, these are allocated dynamically and the configuration variables define the maximum limit for them.

### 2.1. Table cache

- MySQL uses table cache to speed up the opening of tables.
- It is separated into 2 parts:
  - A cache of open tables, configured by [table_open_cache](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_table_open_cache): a memory cache to store the file descriptor of the open tables by all the connected threads -> increase to increase the number of file descriptors that MySQL requires. Please make sure that your operating system can handle the number of open file descriptors implied by the `table_open_cache` setting.
  - A cache of table definitions, configured by [table_definition_cache](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_table_definition_cache): a memory cache to store the table definitions. It is global and shared among all connections. If you use a large number of tables, you can create a large table definition cache to speed up the opening of tables. The table definition cache takes less space and does not use file descriptors, unlike the table cache.

### 2.2. Thread cache

- For each client connection, MySQL assigns a dedicated thread which executes all the queries and returns the result back to the client until the client disconnects.

![](https://dev.mysql.com/blog-archive/mysqlserverteam/wp-content/uploads/2019/03/Connect-768x320.png)

- MySQL cahces the thread so that it doesn't have to create and detroy threads for each connection.
- Configured using [thread_cache_size](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_thread_cache_size).

### 2.3. InnoDB data dictionary cache

- InnoDB has its own cache for storing table definitions, this is different from the table open cache and table definition cache.
  - Check:

    ```sql
    mysql> show engine innodb status\G

    ----------------------

    BUFFER POOL AND MEMORY

    ----------------------

    …

    Dictionary memory allocated 65816817
    ```

- The [table_definition_cache](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_table_definition_cache) setting sets a soft limit on the number of table instances in the InnoDB data dictionary cache, if the number of table instances in InnoDB data dictionary cache exceeds the `table_definition_cache` limit, LRU mechanism begins marking table instances for eviction and eventually removes them from this cache.
- If MySQL instance has a large number of tables with foreign key relationships, InnoDB data dictionary cache may consume multiple GBs of memory. It is often overlooked while configuring MySQL buffers/caches and could be one of the reasons for unanticipated high memory usage or out-of-memory (OOM) issues.

## 3. Session buffers

Another feature which consumes memory is the session buffers. These buffers are allocated on the per-session basis and in some cases multiple instances of them can be allocated for a single query.

- `sort_buffer_size`
- `join_buffer_size`
- `read_buffer_size`
- `read_rnd_buffer_size`

These buffers are allocated only when a query needs them, but when these are needed, they are allocated to their full size even if a very small portion is required. Setting these buffers to a high value may result in wasted memory.

As per-session buffers and in-memory temporary tables allocate memory separately for each connection -> large number of connections -> high overall memory usage.

### 3.1. Binary log cache

- MySQL uses binary log cache to hold the changes made to binary log while a transaction is running.
- Configured using [binary_cache_size](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_cache_size).

### 3.2. Temporary tables

- MySQL creates internal temporary tables to store the intermediate result while processing some types of queries such as GROUP BY, ORDER BY, DISTINCT, and UNION.
- Created in memory first and converted to on-disk tables when the maximum size is reached.
  - [tmp_table_size](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_tmp_table_size).
  - [max_heap_table_size](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_heap_table_size)

## 4. Per connection memory

- Each thread requires little memory to manage the client connection.
  - [thread_stack](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_thread_stack): the stack size for each thread, default is 256 KB.
  - [net_buffer_length](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_net_buffer_length): Each client is associated with a connection buffer and result buffer of `net_buffer_length`. This can further grow up to [max_allowed_packet](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_allowed_packet) size.

## 5. Performance schema

- [Performance schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html) is a feature for monitoring MySQL server execution at a low level.
- It dynamically allocates memory incrementally, scaling its memory use to actual server load, instead of allocating required memory during server startup. It is freed only at MySQL shutdown/restart.
- Disabled by default.
