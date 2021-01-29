# Container runtime metrics

https://docs.docker.com/config/containers/runmetrics

## Brief

Linux Containers rely on control groups - `cgroups`:

- Track groups of processes.
- Expose metrics about CPU, memory and block I/O usage.

Cgroups are exposed through a pseudo-filesystem: `/sys/fs/cgroup`.

`/proc/cgroups`: The different control group subsystems known to the system, the hierarchy they belong to, and how many groups they contain.

To look at the memory metrics for a Docker container, take a loot at: `/sys/fs/cgroup/memory/docker/<longid>`

## Memory

Check `/sys/fs/cgroup/memory/memory.stat`:

- The first half (without the `total` prefix) contains statistics relevant to the processes within the cgroup, excluding sub-cgroups.
- The second half (with the `total` prefix) includes sub-cgroups as well.

Explain metrics:

- `cache`: The amount of memory used by the processes of this control group that can be associated precisely with a block on a block device (page cache). When you read from and write to files on disk, this amount increases. This is the case if you use "conventional" I/O (open, read, write syscalls) as well as mapped files (with `mmap`). It also accounts for the memory used by `tmpfs` mounts. through the reasons are unclear.
- `rss`: The amount of memory that _doesn't correspond_ to anything on disk: stacks, heaps, and anonymous memory maps.
- `mapped_file`: The amount of memory mapped by the processes in the control group. It doesn't give you information about _how much_ memory is used; it rather tells you _how_ it is used.
- `swap`: The amount of swap currently used by the processes in this cgroup.
- `active_anon,inactive_anon`: The amount of _anonymous_ memory that has been identified has respectively _active_ and _inactive_ by the kernel. "Anonymous" memory is the memory that is _not_ linked to disk pages. In other words, that's equivalent of the rss counter described above without `tmpfs`: `active_anon + inactive_anon - tmpfs`. Pages are intially "active", and at regular intervals, the kernel sweeps over the memory, and tags some pages as "inactive". Whenever they are accessed again, they are immediately retagged “active". When the kernel is almost out of memory, and time comes to swap out to disk, the kernel swaps “inactive" pages (Further reading: _Least-recently-used LRU_).
- `active_file,inactive_file`: Cache memory, with _active_ and _inactive_ similar to the _anon_ memory above: `cache = active_file + inactive_file + tmpfs`.
- `unevictable`: The amount of memory that cannot be reclaimed; generally, it accounts for memory that has "locked" with `mlock`.
- `memory_limit,memsw_limit`: These are not really metrics, but a reminder of the limits applied to this cgroup. The first one indicates the maximum amount of physical memory that can be used by the processes of this control group; the second one indicates the maximum amount of RAM+swap.
- `pgfault, pgmajfault`: Indicate the number of times that a process of the cgroup triggered a “page fault" and a “major fault", respectively. A page fault happens when a process accesses a part of its virtual memory space which is nonexistent or protected. The former can happen if the process is buggy and tries to access an invalid address (it is sent a SIGSEGV signal, typically killing it with the famous Segmentation fault message). The latter can happen when the process reads from a memory zone which has been swapped out, or which corresponds to a mapped file: in that case, the kernel loads the page from disk, and let the CPU complete the memory access. It can also happen when the process writes to a copy-on-write memory zone: likewise, the kernel preempts the process, duplicate the memory page, and resume the write operation on the process own copy of the page. “Major" faults happen when the kernel actually needs to read the data from disk. When it just duplicates an existing page, or allocate an empty page, it’s a regular (or “minor") fault.

**NOTE**: Accounting for memory in the page cache is very complex. If two processes in different control groups both read the same file (ultimately relying on the same blocks on disk), the corresponding memory charge is split between the control groups. It’s nice, but it also means that when a cgroup is terminated, it could increase the memory usage of another cgroup, because they are not splitting the cost anymore for those memory pages.
