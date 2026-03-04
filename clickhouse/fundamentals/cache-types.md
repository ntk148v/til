# Cache types

When performing queries, ClickHouse uses different caches to speed up queries and reduce the need to read from or write to disk.

- `mark_cache`: Cache of marks used by table engines of the `MergeTree` family.
- `uncompressed_cache`: Cache of uncompressed data used by table engines of the `MergeTree` family.
- OS page cache (used indirectly, for files with actual data).

There are also a host of additional cache types:

- DNS cache.
- Regexp cache.
- Compiled expressions cache.
- Vector similarity index cache.
- Text index cache.
- Avro format schemas cache.
- Dictionaries data cache.
- Schema inference cache.
- Filesystem cache over S3, Azure, Local and other disks.
- Userspace page cache
- Query cache.
- Query condition cache.
- Format schema cache.

Should you wish to clear one of the caches, for performance tuning, troubleshooting, or data consistency reasons, you can use the `SYSTEM CLEAR ... CACHE` statement.
