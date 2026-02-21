# TTL

Source: <https://clickhouse.com/docs/guides/developer/ttl>

## Overview

TTL refers to the capability of having rows or columns moved, deleted, or rolled up after a certain interval of time has passed.
Use cases:

- Removing old data: no surprise, you can delete rows or columns after a specified time interval.
- Moving data between disks: after a certain amount of time, you can move data between storage volumes - useful for deploying a hot/warm/cold architecture.
- Data rollup: rollup your older data into various useful aggregations and computations before deleting it.

For example:

```sql
CREATE TABLE example1 (
   timestamp DateTime,
   x UInt32 TTL timestamp + INTERVAL 1 MONTH,
   y String TTL timestamp + INTERVAL 1 DAY,
   z String
)
ENGINE = MergeTree
ORDER BY tuple()
```

When the interval lapses, the column expires. ClickHouse replaces the column with the default value of its data types. If all the column values in the data part expire, ClickHouse deletes this column from the data part in the system.

## Removing rows

```sql
CREATE TABLE customers (
timestamp DateTime,
name String,
balance Int32,
address String
)
ENGINE = MergeTree
ORDER BY timestamp
TTL timestamp + INTERVAL 12 HOUR -- <-- TTL rule at the table level
-- TTL time + INTERVAL 1 MONTH DELETE WHERE event != 'error',
--     time + INTERVAL 6 MONTH DELETE WHERE event = 'error'
```

## Removing columns

```sql
ALTER TABLE customers
MODIFY COLUMN balance Int32 TTL timestamp + INTERVAL 2 HOUR,
MODIFY COLUMN address String TTL timestamp + INTERVAL 2 HOUR
```

## Implementing a rollup

## Implementing a hot/warm/cold architecture

To move the data around as it gets older.

1. The `TO DISK` and `TO VOLUME` options refer to the names of disks or volumes defined in your ClickHouse configuration files.

```xml
<!-- /etc/clickhouse-server/config.d/ -->
<clickhouse>
    <storage_configuration>
        <disks>
            <default>
            </default>
           <hot_disk>
              <path>./hot/</path>
           </hot_disk>
           <warm_disk>
              <path>./warm/</path>
           </warm_disk>
           <cold_disk>
              <path>./cold/</path>
           </cold_disk>
        </disks>
        <policies>
            <default>
                <volumes>
                    <default>
                        <disk>default</disk>
                    </default>
                    <hot_volume>
                        <disk>hot_disk</disk>
                    </hot_volume>
                    <warm_volume>
                        <disk>warm_disk</disk>
                    </warm_volume>
                    <cold_volume>
                        <disk>cold_disk</disk>
                    </cold_volume>
                </volumes>
            </default>
        </policies>
    </storage_configuration>
</clickhouse>
```

2. Checkout the disks:

```sql
SELECT name, path, free_space, total_space
FROM system.disks
```

```text
┌─name────────┬─path───────────┬───free_space─┬──total_space─┐
│ cold_disk   │ ./data/cold/   │ 179143311360 │ 494384795648 │
│ default     │ ./             │ 179143311360 │ 494384795648 │
│ hot_disk    │ ./data/hot/    │ 179143311360 │ 494384795648 │
│ warm_disk   │ ./data/warm/   │ 179143311360 │ 494384795648 │
└─────────────┴────────────────┴──────────────┴──────────────┘
```

3. Verify the volumes:

```sql
SELECT
    volume_name,
    disks
FROM system.storage_policies
```

```text
┌─volume_name─┬─disks─────────┐
│ default     │ ['default']   │
│ hot_volume  │ ['hot_disk']  │
│ warm_volume │ ['warm_disk'] │
│ cold_volume │ ['cold_disk'] │
└─────────────┴───────────────┘
```

4. Add a `TTL` rule that moves the data between the hot, warm and cold volumes:

```sql
ALTER TABLE my_table
   MODIFY TTL
      trade_date TO VOLUME 'hot_volume',
      trade_date + INTERVAL 2 YEAR TO VOLUME 'warm_volume',
      trade_date + INTERVAL 4 YEAR TO VOLUME 'cold_volume';
```

5. The new `TTL` rule should materialize, but you can force it to make sure:

```sql
ALTER TABLE my_table
    MATERIALIZE TTL
```

6. Verify your data has moved.

```sql
Using the system.parts table, view which disks the parts are on for the crypto_prices table:

SELECT
    name,
    disk_name
FROM system.parts
WHERE (table = 'my_table') AND (active = 1)
```

```text
┌─name────────┬─disk_name─┐
│ all_1_3_1_5 │ warm_disk │
│ all_2_2_0   │ hot_disk  │
└─────────────┴───────────┘
```
