# Notes

## fsync

I use [deepwiki](https://deepwiki.com/search/when-fsync-is-performed_093b7c38-943b-4285-bd4e-641a4279f5c8).

In Victoriametrics, fsync is commonly used during:

- Persistent queue operations when finalizing chunks.
- Backup operations when copying parts between filesystems.
- Storage partitions.
- MergeSet, part header.
