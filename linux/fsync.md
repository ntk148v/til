# `fsync` in Linux

## Overview

`fsync()` is a POSIX system call used to ensure that all modified data and metadata associated with a file descriptor are flushed from volatile memory (page cache) to stable storage (e.g., disk). It is commonly used in durability-critical software such as databases, filesystems, and transactional systems.

```c
int fsync(int fd);
```

On success, `fsync()` returns `0`. On failure, it returns `-1` and sets `errno`.

## What `fsync()` Guarantees

When `fsync(fd)` returns successfully:

- All dirty **file data** for `fd` is written to disk
- All necessary **metadata** (e.g., file size, timestamps, allocation info) is committed
- Data is guaranteed to survive a **power loss or system crash**

This guarantee applies only to the specific file referenced by the file descriptor.

## What `fsync()` Does _Not_ Guarantee

- It does **not** guarantee persistence of directory entries unless the directory itself is also synced
- It does **not** guarantee ordering between multiple file descriptors unless explicitly controlled
- It does **not** ensure durability of memory-mapped (`mmap`) writes unless paired with `msync()`

## Common Usage Pattern

```c
int fd = open("data.log", O_WRONLY | O_CREAT | O_TRUNC, 0644);
write(fd, buffer, len);
fsync(fd);
close(fd);
```

To ensure the file **name and existence** are durable:

```c
int dfd = open(".", O_DIRECTORY | O_RDONLY);
fsync(dfd);
close(dfd);
```

## `fsync()` vs Related Calls

### `fdatasync()`

- Flushes **data** only
- May skip some metadata (e.g., timestamps)
- Often faster than `fsync()`

```c
fdatasync(fd);
```

### `sync()`

- Flushes **all** dirty buffers system-wide
- Asynchronous on many systems
- Not suitable for per-file durability guarantees

### `msync()`

- Used for `mmap()`-based I/O
- Required to flush memory-mapped changes

## Filesystem-Specific Behavior

- **ext4**
  - Honors `fsync()` fully
  - Behavior affected by mount options (`data=ordered`, `data=journal`)

- **XFS**
  - Strong `fsync()` guarantees
  - Directory `fsync()` often required for durability

- **btrfs**
  - Copy-on-write semantics
  - `fsync()` may trigger more extensive metadata writes

## Performance Characteristics

- `fsync()` is expensive:
  - Forces cache flushes
  - Often triggers disk barriers or cache flush commands (e.g., `FLUSH CACHE`)

- High-frequency `fsync()` calls can dominate latency
- Common optimizations:
  - Group commit
  - Batched writes
  - Asynchronous I/O with explicit durability boundaries

## Error Handling

Common `errno` values:

- `EBADF` – Invalid file descriptor
- `EIO` – I/O error during writeback
- `EINVAL` – Descriptor does not support syncing

Errors may indicate **data loss risk** and should be treated as fatal in durability-sensitive applications.

## Best Practices

- Call `fsync()` only at well-defined durability points
- Sync directories when creating, deleting, or renaming files
- Prefer `fdatasync()` when metadata durability is unnecessary
- Avoid relying on `close()` for durability guarantees
- Test behavior under crash/power-failure scenarios
