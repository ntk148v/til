# Drop cache

> [!important]
> You should only drop caches if you are benchmarking disk performance or debugging a severe memory issue, not for general system optimization. Modern Linux kernels manage memory efficiently by using "free" RAM for disk caches, which are automatically freed when applications need more memory.
>
> Performance degration: The primary function of the disk cache is to store frequently accessed data in RAM so that future requests can be served much faster than reading from a physical disk.
>
> - Increased I/O Operations: Clearing the cache forces the system to re-read all necessary data from the slower disk storage, significantly increasing I/O operations and CPU usage.
> - Slower Application Response: Applications that rely on cached data will experience a temporary but noticeable slowdown the first time they run after the cache is cleared.
> - Wasted Resources: The entire purpose of caching is to leverage otherwise unused RAM. Manually clearing it renders that RAM temporarily useless until the cache rebuilds naturally.

The correct way to execute this command with `sudo` privileges is to use `tee`, often preceded by sync to ensure all data is written to disk first and prevent data loss:

```shell
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

- `sudo sync`: This command flushes all pending filesystem buffers from memory to the disk, which is a crucial preparatory step.
- echo 1: Clears the page cache only.
- echo 2: Clears dentries and inodes (metadata).
- echo 3: Clears all three (page cache, dentries, and inodes).

Source: <https://www.kernel.org/doc/Documentation/sysctl/vm.txt>

```text
Writing to this will cause the kernel to drop clean caches, as well as
reclaimable slab objects like dentries and inodes.  Once dropped, their
memory becomes free.

To free pagecache:
	echo 1 > /proc/sys/vm/drop_caches
To free reclaimable slab objects (includes dentries and inodes):
	echo 2 > /proc/sys/vm/drop_caches
To free slab objects and pagecache:
	echo 3 > /proc/sys/vm/drop_caches

This is a non-destructive operation and will not free any dirty objects.
To increase the number of objects freed by this operation, the user may run
`sync' prior to writing to /proc/sys/vm/drop_caches.  This will minimize the
number of dirty objects on the system and create more candidates to be
dropped.

This file is not a means to control the growth of the various kernel caches
(inodes, dentries, pagecache, etc...)  These objects are automatically
reclaimed by the kernel when memory is needed elsewhere on the system.

Use of this file can cause performance problems.  Since it discards cached
objects, it may cost a significant amount of I/O and CPU to recreate the
dropped objects, especially if they were under heavy use.  Because of this,
use outside of a testing or debugging environment is not recommended.

You may see informational messages in your kernel log when this file is
used:

	cat (1234): drop_caches: 3

These are informational only.  They do not mean that anything is wrong
with your system.  To disable them, echo 4 (bit 2) into drop_caches.
```
