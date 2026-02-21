# Skipping Indices

Source:

- <https://clickhouse.com/docs/optimize/skipping-indexes>
- <https://altinity.com/blog/clickhouse-black-magic-skipping-indices>

## 1. Introduction

ClickHouse indices are different from traditional relational database management systems (RDMS) in that:

- Primary keys are not unique.
- There are no foreign keys and traditional B-tree indices.
Instead, ClickHouse uses secondary `skipping` indices. Those are often confusing and hard to tune even for experienced ClickHouse users.

The data in MergeTree is organized as parts.

- Every part is a folder on the storage device that contains files for every column and a few additional files with metadata.
- The column is stored as an array of values, where position is mapped to a row number.
- The data in columns is sorted using the ORDER BY key of the table.
- Every 8192 rows in a part are called a **granule**.

The granule size is defined by the `index_granularity` parameter of the MergeTree table definition, but ClickHouse sometimes may adjust it through adaptive granularity. Every granule is referenced by the `main` table index aka the PRIMARY KEY that is typically the same as ORDER BY. Since the granule is 8192 rows, the index is sparse. The index also references the special `mark` files, per column, that contain pointers to the data in the column files themselves.

If we look for a real world analogy, the use of a PRIMARY KEY is similar to the search in an Oxford dictionary, for example. Since all words in the dictionary are sorted alphabetically, we quickly find a page (granule) with a word we are looking for using a `sparse index` – a single word printed in the page header:

![](https://web.archive.org/web/20220703053043im_/https://lh3.googleusercontent.com/B1VjCg3JVytkCkrIMX1SZKimHQv-iUdwydmD2y79ea9Hq5nRnFu8ztPbUCHLfv-S3p7dZH5UcXS6MNttc_tAB9HR_IKjrSDibgk1loH86livMJ66dJYcalHki9e62VxL4nr8mMwN)

… and then scan the page for the word itself.

However, if we need to find something that is not based on a sort order then the alphabetical index can not be used. Say we need to find all articles about Antique culture. In this case we have to do a full scan, or use a special topic index, that sometimes can be found at the end of books. Such an index references multiple pages where the topic can be found. It is not as effective as an alphabetical one but still allows us to avoid the full scan.

Getting back to the dictionary analogy — what if we put some extra information to the top or bottom of every page, that would quickly annotate the content? For example, if the page contains an article about Antique culture we could add a small icon of an Antique temple. When looking for Antique culture articles, we still have to list all the pages, but we can quickly skip those without an icon. This is much faster than a full scan.

ClickHouse skipping indices utilize a very similar idea — they encapsulate some sort of “condensed knowledge” about the content of the granule. This knowledge allows quickly finding pages/granules that need to be scanned and skip everything else.

## 2. Basic

You can only employ Data Skipping Indexes on the MergeTree family of tables. Each data skipping has four primary arguments:

- Index name. The index name is used to create the index file in each partition. Also, it is required as a parameter when dropping or materializing the index.
- Index expression. The index expression is used to calculate the set of values stored in the index. It can be a combination of columns, simple operators, and/or a subset of functions determined by the index type.
- TYPE. The type of index controls the calculation that determines if it is possible to skip reading and evaluating each index block.
- GRANULARITY. Each indexed block consists of GRANULARITY granules. For example, if the granularity of the primary table index is 8192 rows, and the index granularity is 4, each indexed "block" will be 32768 rows.

```sql
INDEX index_name expr TYPE type(...) GRANULARITY granularity_value
```

## 3. Index types

- **Minmax**: It stores minimum and maximum values of the column (or expression) for a particular granula. During query execution ClickHouse can quickly check if column values are out of range without scanning the column. It works the best when the value of a column changes slowly over the sort order.
- **Set(N)**: It stores all distinct values of a column or an expression in a granule. When an indexed column is used in a WHERE clause, ClickHouse can read a small set instead of a full column. It works well if a column contains a small number of distinct values in a granule but values change over table order. The parameter of a Set index limits the maximum number of distinct values stored in an index. ‘0’ means unlimited. The index size needs to be significantly smaller than a column itself, otherwise it does not give any benefit.
- **Bloom filter types**: There are three Data Skipping Index types based on Bloom filters:
  - `bloom_filter([false_positive])`: This is the most generic case.  Input strings are stored in a bloom filter “as is”. That works for exact matches in strings and also in arrays.
  - `tokenbf_v1(size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)`: An input string is split into alphanumeric tokens, and then tokens are stored in a bloom filter (see below). It works for the cases when an exact match on a string is searched. For example, if we have a 'url' column and are looking for a specific part of the URL or a query parameter.
  - `ngrambf_v1(n, size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)`: In this case an input string is split into n-grams (first parameter – n-gram size, usually 3 or 4), and then stored in a bloom filter. That can work for full text search.

## 4. When NOT TO use Skipping indices

- Apply only if there is a benefit in a query time.
- The index is different if it is significantly smaller than the column itself,  otherwise it may slow down the query execution.  Remember, that ClickHouse can just load the full column, apply a filter and decide what granules to read for the remaining columns. It is called the PREWHERE step in the query processing. If you want to confirm the skipping index size, check the `system.data_skipping_indices` table and compare it with an indexed column.
- Using skipped indices for columns that are already in the PRIMARY KEY is also useless. It is always faster to use the PRIMARY KEY when it can be applied for a query.
