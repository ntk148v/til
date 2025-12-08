# Inverted index

Source: <https://www.cockroachlabs.com/blog/inverted-indexes/>

An inverted index is a type of index that stores a record of where search terms – such as words or numbers – are located in a table.

| id  | content         |
| --- | --------------- |
| 101 | ‘Multi cloud’   |
| 102 | ‘Elastic scale’ |
| 103 | ‘Multi region’  |
| 104 | ‘Cloud native’  |

Below is an inverted index for that table.

| token   | id       |
| ------- | -------- |
| multi   | 101, 103 |
| cloud   | 101, 104 |
| elastic | 102      |
| scale   | 102      |
| region  | 103      |
| native  | 104      |

## Why use inverted indexes?

Inverted indexes are used to facilitate more efficient full-text searches in a database.

For example, search our database for entries that include the word “multi.”

```sql
SELECT * FROM table WHERE content LIKE '%multi%';
```

If our table does not have an inverted index, this query will execute a _full table scan_. In other words, the database will read every single row to check whether the word “multi” appears in it. If that database had 10,000 rows, or a million rows -> **bottleneck database performance**.

**Inverted indexes allow text search to run much more efficiently.** With an inverted index created, the database does not need to perform a full table scan. Instead, it can simply refer to the index entry for multi and immediately find that it appears in rows 101 and 103.

## What are the downsides of inverted indexes?

The only real downside to creating an inverted index is that, like any type of SQL index, it will slightly slow down writes. This is because when (for example) a row is committed to the database table, those new values also have to be copied to the index and sorted accordingly.
