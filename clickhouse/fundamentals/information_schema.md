# `information_schema`

## 1. Introduction

```sql
SHOW TABLES FROM INFORMATION_SCHEMA;
┌─name─────┐
│ columns  │
│ schemata │
│ tables   │
│ views    │
└──────────┘
```

The `information_schema` database is a virtual system database in ClickHouse that provides a set of system tables that contain metadata about the database and its objects. These tables are virtual, meaning they do not physically exist in the database but are generated dynamically by the database management system.

The `information_schema` database plays a critical role in the ClickHouse ecosystem as it enables users to access and query the system metadata in a standardized way, without requiring access to low-level system information. The virtual tables in the `information_schema` database can be queried like any other tables in ClickHouse, allowing users to gain insights into the database schema, optimize queries, and diagnose performance issues.

1. **schemata**: contains metadata about the database schema, including the schema name and the default character set.

```sql
SELECT * FROM information_schema.schemata WHERE schema_name ILIKE 'information_schema' LIMIT 1 FORMAT Vertical;

Row 1:
──────
catalog_name:                  INFORMATION_SCHEMA
schema_name:                   INFORMATION_SCHEMA
schema_owner:                  default
default_character_set_catalog: ᴺᵁᴸᴸ
default_character_set_schema:  ᴺᵁᴸᴸ
default_character_set_name:    ᴺᵁᴸᴸ
sql_path:                      ᴺᵁᴸᴸ
```

2. **tables**: contains metadata about the tables in the database schema, including the table name, type, engine, and the number of rows in the table.

```sql
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE (table_schema = currentDatabase() OR table_schema = '') AND table_name NOT LIKE '%inner%' LIMIT 1 FORMAT Vertical;

Row 1:
──────
table_catalog: default
table_schema:  default
table_name:    describe_example
table_type:    BASE TABLE
```

3. **columns**: contains metadata about the columns in the tables in the database schema, including the column name, data type, and whether the column is nullable or not.

```sql
SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE (table_schema=currentDatabase() OR table_schema='') AND table_name NOT LIKE '%inner%' LIMIT 1 FORMAT Vertical;

Row 1:
──────
table_catalog:            default
table_schema:             default
table_name:               describe_example
column_name:              id
ordinal_position:         1
column_default:
is_nullable:              0
data_type:                UInt64
character_maximum_length: ᴺᵁᴸᴸ
character_octet_length:   ᴺᵁᴸᴸ
numeric_precision:        64
numeric_precision_radix:  2
numeric_scale:            0
datetime_precision:       ᴺᵁᴸᴸ
character_set_catalog:    ᴺᵁᴸᴸ
character_set_schema:     ᴺᵁᴸᴸ
character_set_name:       ᴺᵁᴸᴸ
collation_catalog:        ᴺᵁᴸᴸ
collation_schema:         ᴺᵁᴸᴸ
collation_name:           ᴺᵁᴸᴸ
domain_catalog:           ᴺᵁᴸᴸ
domain_schema:            ᴺᵁᴸᴸ
domain_name:              ᴺᵁᴸᴸ
```

4. **views**: contains metadata about the views in the database schema, including the view name, definition, and the tables used in the view.

```sql
CREATE VIEW v (n Nullable(Int32), f Float64) AS SELECT n, f FROM t;
CREATE MATERIALIZED VIEW mv ENGINE = Null AS SELECT * FROM system.one;
SELECT * FROM information_schema.views WHERE table_schema = currentDatabase() LIMIT 1 FORMAT Vertical;

Row 1:
──────
table_catalog:              default
table_schema:               default
table_name:                 mv
view_definition:            SELECT * FROM system.one
check_option:               NONE
is_updatable:               NO
is_insertable_into:         YES
is_trigger_updatable:       NO
is_trigger_deletable:       NO
is_trigger_insertable_into: NO
```

The `information_schema` tables in ClickHouse are useful for a variety of use cases, including:

1. Data dictionary: The `information_schema` tables can be used to create a data dictionary that provides information about the database schema, tables, and columns. This information can be used by data analysts and developers to understand the data model and schema of the database.
2. Database administration: The `information_schema` tables can be used by database administrators to monitor the database and diagnose issues. For example, the processes table can be used to monitor the running queries on the server and diagnose performance issues.
3. Query optimization: The `information_schema` tables can be used to optimize queries by providing metadata about the database schema, tables, and columns. For example, the columns table can be used to determine the data type and nullability of columns, which can be used to optimize query execution.
4. Cluster management: The `information_schema` tables can be used to manage ClickHouse clusters, including monitoring the cluster status, adding or removing nodes from the cluster, and changing the replication factor.
