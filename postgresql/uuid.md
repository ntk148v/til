# PostgreSQL and UUID as primary key

Source:

- <https://maciejwalkowiak.com/blog/postgres-uuid-primary-key/>
- <https://commitfest.postgresql.org/47/4388/>
- <https://www.ietf.org/archive/id/draft-peabody-dispatch-new-uuid-format-04.html#name-uuid-version-7>

UUIDs are often used as database table **primary keys**. They are easy to generate, easy to share between distributed systems and guarantee uniqueness.

## 1.1. Postgres Data Types for UUID

**Don't store UUID as `text`. Postgres has a dedicated data type for UUIDs: `uuid`, use it**. UUID is 128 bit data type, so storing single value takes 16 bytes. `text` data type has 1 or 4 bytes overhead plus storing the actual string. These differences become an issue once you start storing hundreds of thousands or millions of rows.

Larger size of tables, indexes and bigger number of tables means that Postgres must perform work to inset new rows and fetch rows - especially once index sizes are larger than available RAM memory, and Postgres must load indexes from disk.

## 1.2. UUID and B-Tree index

Random UUIDs are not a good fit for a B-tree indexes, and B-tree indexes is the only available index type for a primary key.

B-tree indexes work the best with ordered values - like auto-incremented or time sorted columns.

UUID - even though always looks similar - comes in multiple variants. Java's `UUID.randomUUID()` - returns UUID v4 - which is a pseudo-random value. For us the more interesting one is **UUID v7** - which produces time-sorted values. It means that each time UUID v7 is generated, a greater value it has. And that makes it a good fit for B-tree index.

**UUID v7 improves the performance of executing `INSERT` statements**.
