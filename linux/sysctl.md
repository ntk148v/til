# sysctl

Table of Contents:

- [sysctl](#sysctl)
  - [1. `vm.max_map_count`](#1-vmmax_map_count)
    - [1.1. Overview](#11-overview)
    - [1.2. How to check](#12-how-to-check)
    - [1.3. Does it affect server performance?](#13-does-it-affect-server-performance)
    - [1.4. Recommended values](#14-recommended-values)
  - [2. `vm.drop_caches`](#2-vmdrop_caches)
  - [4. `vm.dirty_*`](#4-vmdirty_)

## 1. `vm.max_map_count`

### 1.1. Overview

- According to `kernel-doc/Documentation/sysctl/vm.txt`:
  - This file contains the maximum number of memory map areas (VMAs) a process may have. Memory map areas are used as a side-effect of calling malloc, directly by mmap and mprotect, and also when loading shared libraries.
  - While most applications need less than a thousand maps, certain programs, particularly malloc debuggers, may consume lots of them, e.g., up to one or two maps per allocation.
  - The default value is 65530.
- Lowering the value can lead to problematic application behavior because the system will return out of memory errors when a process reaches the limit. The upside of lowering this limit is that it can free up lowmem for other kernel uses.
- Raising the limit may increase the memory consumption on the server. There is no immediate consumption of the memory, as this will be used only when the software requests, but it can allow a larger application footprint on the server.
- Applications that allocate memory in numerous small segments (e.g., Elasticsearch, OpenSearch, high-load JVM workloads, or processes using extensive memory-mapped I/O) may require higher limits.

### 1.2. How to check

The file `/proc/$PID/maps` lists all VMAs for that process. Each line represents one memory mapping.

To check the exact count of VMAs currently in use by that process:

```shell
wc -l /proc/$PID/maps
```

This count is what the kernel enforces against vm.max_map_count. If the count approaches the configured limit, the process will begin to fail memory-mapping operations, resulting in errors such as “mmap: Cannot allocate memory.”

### 1.3. Does it affect server performance?

**Direct performance impact: No** Changing the limit does not influence CPU utilization, RAM throughput, latency, or I/O performance.

**Indirect performance impact: Yes, if set too low**

If the limit is insufficient:

- Applications may fail to start.
- Memory-mapped I/O may fail.
- JVMs can throw allocation errors.

Elasticsearch and similar systems can crash or refuse to create indices.

**Indirect performance impact if set extremely high: Possible but negligible**

Only unrealistically large values (millions+) can introduce modest kernel bookkeeping overhead. Common recommended settings such as 262144 do not cause performance degradation. Some OSs (ArchLinux, Fedora, Ubuntu) already set the default value to the much larger value 1048576.

### 1.4. Recommended values

Source: <https://memgraph.com/docs/database-management/system-configuration#recommended-values-for-the-vmmax_map_count-parameter>

For optimal system performance, the vm.max_map_count value should be chosen in accordance with your system’s RAM, aiming for approximately one memory map area per 128 KB of system memory.

> [!warn]
> The recommended values below are starting points and may need to be increased depending on your workload. If you encounter `munmap` errors or crashes due to `bad_alloc` errors, you should try increasing the `vm.max_map_count` value beyond the recommended amount.

| Amount of RAM | vm.max_map_count value    |
| ------------- | ------------------------- |
| 8GB - 32GB    | vm.max_map_count=262144   |
| 32GB - 64GB   | vm.max_map_count=524288   |
| 64GB - 128GB  | vm.max_map_count=1048576  |
| 128GB - 256GB | vm.max_map_count=2097152  |
| 256GB - 512GB | vm.max_map_count=4194304  |
| 512GB - 1TB   | vm.max_map_count=8388608  |
| 1TB - 1.5TB   | vm.max_map_count=12582912 |
| 1.5TB - 2TB   | vm.max_map_count=16777216 |
| 2TB - 2.5TB   | vm.max_map_count=20971520 |
| 2.5TB - 3TB   | vm.max_map_count=25165824 |
| 3TB - 3.5TB   | vm.max_map_count=29360128 |
| 3.5TB - 4TB   | vm.max_map_count=33554432 |

## 2. `vm.drop_caches`

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

## 4. `vm.dirty_*`

Source:

- <https://lonesysadmin.net/2013/12/22/better-linux-disk-caching-performance-vm-dirty_ratio/>
- <https://www.slideshare.net/slideshow/disk-and-page-cache/72722837>

Check out [pagecache](./pagecache.md), now let's talk about the kernel options to control pagecache.

```shell
$ sysctl -a | grep dirty
vm.dirty_background_ratio = 10
vm.dirty_background_bytes = 0
vm.dirty_ratio = 20
vm.dirty_bytes = 0
vm.dirty_writeback_centisecs = 500
vm.dirty_expire_centisecs = 3000
```

- `vm.dirty_background_ratio` is the percentage of system memory that can be filled with “dirty” pages — memory pages that still need to be written to disk — before the pdflush/flush/kdmflush background processes kick in to write it to disk. My example is 10%, so if my virtual server has 32 GB of memory that’s 3.2 GB of data that can be sitting in RAM before something is done.
- `vm.dirty_ratio` is the absolute maximum amount of system memory that can be filled with dirty pages before everything must get committed to disk. When the system gets to this point all new I/O blocks until dirty pages have been written to disk. This is often the source of long I/O pauses, but is a safeguard against too much data being cached unsafely in memory.

![](https://img-blog.csdnimg.cn/20210706095814793.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcwMDg2Ng==,size_16,color_FFFFFF,t_70)

- `vm.dirty_background_bytes` and `vm.dirty_bytes` are another way to specify these parameters. If you set the \_bytes version the \_ratio version will become 0, and vice-versa.
- `vm.dirty_expire_centisecs` is how long something can be in cache before it needs to be written. In this case it’s 30 seconds. When the pdflush/flush/kdmflush processes kick in they will check to see how old a dirty page is, and if it’s older than this value it’ll be written asynchronously to disk. Since holding a dirty page in memory is unsafe this is also a safeguard against data loss.
- `vm.dirty_writeback_centisecs` is how often the pdflush/flush/kdmflush processes wake up and check to see if work needs to be done.

You can also see statistics on the page cache in /proc/vmstat.

```shell
$ cat /proc/vmstat | egrep "dirty|writeback"
nr_dirty 878
nr_writeback 0
nr_writeback_temp 0
```

In many cases we have fast disk subsystems with their own big, battery-backed NVRAM caches, so keeping things in the OS page cache is risky. In such case, it's better to decrease the cache:

```shell
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
```

There are scenarios where raising the cache dramatically has positive effects on performance. These situations are where the data contained on a Linux guest isn’t critical and can be lost, and usually where an application is writing to the same files repeatedly or in repeatable bursts. In theory, by allowing more dirty pages to exist in memory you’ll rewrite the same blocks over and over in cache, and just need to do one write every so often to the actual disk. To do this we raise the parameters:

```shell
vm.dirty_background_ratio = 50
vm.dirty_ratio = 80
```

There are also scenarios where a system has to deal with infrequent, bursty traffic to slow disk (batch jobs at the top of the hour, midnight, writing to an SD card on a Raspberry Pi, etc.). In that case an approach might be to allow all that write I/O to be deposited in the cache so that the background flush operations can deal with it asynchronously over time:

```shell
vm.dirty_background_ratio = 5
vm.dirty_ratio = 80
```

Here the background processes will start writing right away when it hits that 5% ceiling but the system won’t force synchronous I/O until it gets to 80% full.
