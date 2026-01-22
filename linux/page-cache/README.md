# The page cache

Source:

- <https://notes.eddyerburgh.me/operating-systems/linux/the-page-cache-and-page-writeback>
- <https://biriukov.dev/docs/page-cache/0-linux-page-cache-for-sre/>

Table of contents:

The page cache is a disk cache used to minimize disk I/O. Instead of read requests and write operations running against a disk, they run against an in-memory cache (unused areas of the memory) that only reads data from disk when needed and writes changes to disk periodically.

The page cache contains physical pages in RAM, which correspond to physical blocks on a disk. The page cache is dynamic: “it can grow to consume any free memory and shrink to relieve memory pressure”.

“Page” in the Page Cache means that linux kernel works with memory units called pages. It would be cumbersome and hard to track and manage bites or even bits of information. So instead, Linux’s approach (and not only Linux’s, by the way) is to use pages (usually 4K in length) in almost all structures and operations. Hence the minimal unit of storage in Page Cache is a page, and it doesn’t matter how much data you want to read or write. All file IO requests are aligned to some number of pages.

The above leads to the important fact that if your write is smaller than the page size, the kernel will read the entire page before your write can be finished.

![](https://biriukov.dev/docs/page-cache/images/page-cache.png)

## 1. Approaches to caching

### 1.1. Read strategy

Generally speaking, reads are handled by the kernel in the following way:

① – When a user-space application wants to read data from disks, it asks the kernel for data using special system calls such as `read()`, `pread()`, `vread()`, `mmap()`, `sendfile()`, etc.

② – Linux kernel, in turn, checks whether the pages are present in Page Cache and immediately returns them to the caller if so. As you can see kernel has made 0 disk operations in this case.

③ – If there are no such pages in Page Cache, the kernel must load them from disks. In order to do that, it has to find a place in Page Cache for the requested pages. A memory reclaim process must be performed if there is no free memory (in the caller’s cgroup or system). Afterward, kernel schedules a read disk IO operation, stores the target pages in the memory, and finally returns the requested data from Page Cache to the target process. Starting from this moment, any future requests to read this part of the file (no matter from which process or cgroup) will be handled by Page Cache without any disk IOP until these pages have not been evicted.

### 1.2. Write strategy

Let’s repeat a step-by-step process for writes:

① – When a user-space program wants to write some data to disks, it also uses a bunch of syscalls, for instance: `write()`, `pwrite()`, `writev()`, `mmap()`, etc. The one big difference from the reads is that writes are usually faster because real disk IO operations are not performed immediately. However, this is correct only if the system or a cgroup doesn’t have memory pressure issues and there are enough free pages (we will talk about the eviction process later). So usually, the kernel just updates pages in Page Cache. it makes the write pipeline asynchronous in nature. The caller doesn’t know when the actual page flush occurs, but it does know that the subsequent reads will return the latest data. Page Cache protects data consistency across all processes and cgroups. Such pages, that contain un-flushed data have a special name: dirty pages.

② – If a process’ data is not critical, it can lean on the kernel and its flush process, which eventually persists data to a physical disk. But if you develop a database management system (for instance, for money transactions), you need write guarantees in order to protect your records from a sudden blackout. For such situations, Linux provides `fsync()`, `fdatasync()` and `msync()` syscalls which block until all dirty pages of the file get committed to disks. There are also `open()` flags: `O_SYNC` and `O_DSYNC`, which you also can use in order to make all file write operations durable by default. I’m showing some examples of this logic later.

There are three strategies for implementing write requests with caches:

- No-write—the write request updates the data on disk, and the cache is invalidated.
- Write-through—the write request updates the data on disk and in the cache.
- Write-back—the write request updates the data in the cache and updates the data on disk in the future.

Linux uses the write-back strategy. Write requests update the cached data. The updated pages are then marked as dirty, and added to the dirty list. A process then periodically updates the blocks corresponding to pages in the dirty list.

### 1.3. Cache eviction

- Removing items from the cache is known as cache eviction. This is done to either make room for more relevant data, or to shrink it in order to free memory.
- Linux cache eviction works by removing only clean pages. It uses a variation of the LRU (Least Recently Used) algorithm, the two-list strategy.
- In the two-list strategy, Linux maintains two linked lists: the active list and the inactive list. Pages on the active list are considered hot and are not available for eviction. Pages on the inactive list are available for eviction. Pages are placed on the active list if they are already residing in the inactive list [1, P. 325].
- The lists are maintained in a pseudo-LRU manner. Items are added to the tail, and are removed from the head. If the active list grows much larger than the inactive list, items are moved back from the active list to the inactive list.

## 2. The Flusher Threads

The flusher threads periodically write dirty pages to disk. There are three situations that cause writes:

- When free memory shrinks below a predefined threshold.
- When dirty data grows older than a specific threshold.
- When a user process calls the `sync()` or `fsync()` system calls.

When free memory shrinks below the threshold (defined by the `dirty_background_ratio` sysctl), the kernel invokes `wakeup_flusher_threads()` to wake up one or more flusher threads to run `bdi_writeback_all()`. `bdi_writeback_all()` takes the number of pages to write-back as a parameter. It will continue writing back pages until either the free memory is above the `dirty_background_ratio` threshold, or until the minimum number of pages has been written out.

To ensure dirty data doesn’t grow older than a specific threshold, a kernel thread periodically wakes up and writes out old dirty pages

## 3. Page cache and basic file operations

```shell
$ dd if=/dev/random of=/var/tmp/file1.db count=128 bs=1M
```

### 3.1. File reads

- Reading files with `read()` syscall.

```python
with open("/var/tmp/file1.db", "br") as f:
    print(f.read(2))
```

```shell
$ strace -s0 python3 ./read_2_bytes.py
# read syscall returned 4096 bytes (one page) even though the script asked only for 2 bytes.

# Check how much data the kernel's cached
$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 128/32768  512K/128M  0.391%
         Elapsed: 0.000698 seconds
# The kernel has cached 512KiB or 128 pages
```

- By design, the kernel can't load anything less than 4KiB or one page into Page cache, but what about the other 127 pages? It's called **read ahead** logic and preference to perform sequential IO operations over random ones. The basic idea is to **predict the subsequent reads and minimize the number of disks seeks** (`man 2 readahead` and `man 2 posix_fadvise`).
- Use `posix_fadvise()` to notify the kernel that we're reading the file randomly, and thus we don't want to have any ahead features:

```python
import os

with open("/var/tmp/file1.db", "br") as f:
    fd = f.fileno()
    os.posix_fadvise(fd, 0, os.fstat(fd).st_size, os.POSIX_FADV_RANDOM)
    print(f.read(2))
```

```shell
$ echo 3 | sudo tee /proc/sys/vm/drop_caches && python3 ./read_2_random.py
3
b'\xf5\xf2'

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 1/32768  4K/128M  0.00305%
         Elapsed: 0.000376 seconds
```

- Reading files with `mmap()` syscall: it's a "magic" tool and can be used to solve a wide range and can be used to solve a wide range of tasks.

```python
import mmap

with open("/var/tmp/file1.db", "r") as f:
    with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
        print(mm[:2])
```

```shell
$ echo 3 | sudo tee /proc/sys/vm/drop_caches && python3 ./read_2_mmap.py

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 32/32768  128K/128M  0.0977%
         Elapsed: 0.00056 seconds
```

- Let's change the readahead with `madvise()` syscall like we did with `fadvise()`.

```python
import mmap

with open("/var/tmp/file1.db", "r") as f:
    with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
        mm.madvise(mmap.MADV_RANDOM)
        print(mm[:2])
```

```shell
$ echo 3 | sudo tee /proc/sys/vm/drop_caches && python3 ./read_2_mmap_random.py

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 1/32768  4K/128M  0.00305%
         Elapsed: 0.00052 seconds
```

### 3.2. File writes

- Writing to files with `write()` syscall.

```python
with open("/var/tmp/file1.db", "br+") as f:
    print(f.write(b"ab"))
```

```shell
$ sync; echo 3 | sudo tee /proc/sys/vm/drop_caches && python3 ./write_2_bytes.py

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 130/32768  520K/128M  0.397%
         Elapsed: 0.0004 seconds
```

- Check dirty pages by reading the current cgroup memory stat file.

```shell
$ cat /proc/self/cgroup
0::/user.slice/user-1000.slice/session-c2.scope

$ grep dirty /sys/fs/cgroup/user.slice/user-1000.slice/session-c2.scope/memory.stat
file_dirty 102400
```

- File writes with `mmap()` syscall.

```python
import mmap

with open("/var/tmp/file1.db", "r+b") as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        mm[:2] = b"ab"
```

```shell
$ sync; echo 3 | sudo tee /proc/sys/vm/drop_caches && python3 ./write_mmap.py

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 120/32768  480K/128M  0.366%
         Elapsed: 0.000705 seconds
```

- If your program uses `mmap()` to write to files, you have one more option to get dirty pages stats with a per-process granularity. `procfs` has the `/proc/PID/smaps` file. It contains memory counters for the process broken down by virtual memory areas (VMA). We can get dirty pages by finding:
  - `Private_Dirty` – the amount of dirty data this process generated;
  - `Shared_Dirty` – and the amount other processes wrote. This metric shows data only for referenced pages. It means the process should access pages and keep them in its page table.

### 3.3. Synchronize file changes with `fsync()`, `fdatasync()`, and `msync()`

Linux provides several methods to force the kernel to run a sync of pages for the file in Page Cache:

- `fsync()` – blocks until all dirty pages of the target file and its metadata are synced;
- `fdatasync()` – the same as the above but excluding metadata;
- `msync()` – the same as the fsync() but for memory mapped file;
- open a file with `O_SYNC` or `O_DSYNC` flags to make all file writes synchronous by default and work as a corresponding `fsync()` and `fdatasync()` syscalls accordingly.

### 3.4. Check file presence in Page Cache with `mincore()`

`mincore()` stands for "memory in the core". Its parameters are a starting virtual memory address, a length of the address space and a resulting vector.

```go
package main

import (
	"fmt"
	"log"
	"os"
	"syscall"
	"unsafe"
)

var (
	pageSize = int64(syscall.Getpagesize())
	mode     = os.FileMode(0600)
)

func main() {
	path := "/var/tmp/file1.db"

	file, err := os.OpenFile(path, os.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NOATIME, mode)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	stat, err := os.Lstat(path)
	if err != nil {
		log.Fatal(err)
	}
	size := stat.Size()
	pages := size / pageSize

	mm, err := syscall.Mmap(int(file.Fd()), 0, int(size), syscall.PROT_READ, syscall.MAP_SHARED)
	defer syscall.Munmap(mm)

	mmPtr := uintptr(unsafe.Pointer(&mm[0]))
	cached := make([]byte, pages)

	sizePtr := uintptr(size)
	cachedPtr := uintptr(unsafe.Pointer(&cached[0]))

	ret, _, err := syscall.Syscall(syscall.SYS_MINCORE, mmPtr, sizePtr, cachedPtr)
	if ret != 0 {
		log.Fatal("syscall SYS_MINCORE failed: %v", err)
	}

	n := 0
	for _, p := range cached {
		// the least significant bit of each byte will be set if the corresponding page
		// is currently resident in memory, and be clear otherwise.
		if p%2 == 1 {
			n++
		}
	}

	fmt.Printf("Resident Pages: %d/%d  %d/%d\n", n, pages, n*int(pageSize), size)
}
```

```shell
$ go run ./main.go
Resident Pages: 120/32768  491520/134217728

$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 120/32768  480K/128M  0.366%
         Elapsed: 0.000559 seconds
```

## 4. Page cache eviction and page reclaim

### 4.1. Theory

Like any other cache, Linux Page cache continuously monitors the last used pages and makes decisions about which pages should be deleted and which should be kept in the cache.

The primary approach to control and tune Page cache is the cgroup subsystem. You can divide the server’s memory into several smaller caches (cgroups) and thus control and protect applications and services. In addition, the cgroup memory and IO controllers provide a lot of statistics that are useful for tuning your software and understanding the internals of the cache.

Linux Page Cache is closely tightened with Linux Memory Management, cgroup and virtual file system (VFS). Core building block is a per cgroup pair of active and inactive lists:

- The first pair for anonymous memory (for instance, allocated with `malloc()` or not file backended `mmap()`).
- The second pair for Page cache file memory (all file operations including `read()`, `write()`, `mmap()` accesses, etc.)

The least recently used algorithm LRU:

- These 2 lists from a double clock data structure.
- Linux should choose pages that have not been used recently (inactive) based on the fact that the pages that have not seen used recently will not be used frequently in a short period of time.
- Both the active and inactive lists adopt the form of FIFO for their entries.

![](https://biriukov.dev/docs/page-cache/images/lru.png)

For example, a user process has just read some data from disks. This action triggered the kernel to load data to the cache. It was the first time when the kernel had to access the file. Hence it added a page `h` to the head of the inactive list:

![](https://biriukov.dev/docs/page-cache/images/eviction-1.png)

Some time has passed, the system loads 2 more pages: `i` and `j`.

![](https://biriukov.dev/docs/page-cache/images/eviction-2.png)

Now, a new file operation to the page `h` promotes the page to the active LRU list by putting it at the head. This action also ousts the page `1` to the head of the inactive LRU list and shifts all other members:

![](https://biriukov.dev/docs/page-cache/images/eviction-3.png)

As time flies, page `h` looses its head position in the active LRU list.

![](https://biriukov.dev/docs/page-cache/images/eviction-4.png)

But a new file access to the `h`’s position in the file returns h back to the head of the active LRU list.

![](https://biriukov.dev/docs/page-cache/images/eviction-5.png)

But it’s worth mentioning that the real process of pages promotion and demotion is much more complicated and sophisticated.

First of all, if a system has NUMA hardware nodes (`man 8 numastat`), it has twice more LRU lists. The reason is that the kernel tries to store memory information in the NUMA nodes in order to have fewer lock contentions.

In addition, Linux Page Cache also has special shadow and referenced flag logic for promotion, demotion and re-promotion pages.

Shadow entries help to mitigate the memory thrashing problem. This issue happens when the programs’ working set size is close to or greater than the real memory size (maybe cgroup limit or the system RAM limitation).

### 4.2. Manual pages eviction with `POSIX_FADV_DONTNEED`

```shell
$ vmtouch /var/tmp/file1.db -e
           Files: 1
     Directories: 0
   Evicted Pages: 32768 (128M)
         Elapsed: 7.2e-05 seconds
$ vmtouch /var/tmp/file1.db
           Files: 1
     Directories: 0
  Resident Pages: 0/32768  0/128M  0%
         Elapsed: 0.000526 seconds
```

```python
import os

with open("/var/tmp/file1.db", "br") as f:
    fd = f.fileno()
    os.posix_fadvise(fd, 0, os.fstat(fd).st_size, os.POSIX_FADV_DONTNEED)
```

```shell
# Read the entire test file into Page cache
$ dd if=/var/tmp/file1.db of=/dev/null
262144+0 records in
262144+0 records out
134217728 bytes (134 MB, 128 MiB) copied, 0,186082 s, 721 MB/s

$ python3 evict_full_file.py
$ vmtouch /var/tmp/file1.db
           Files: 1G
     Directories: 0
  Resident Pages: 0/32768  0/128M  0%
         Elapsed: 0.000278 seconds
```

### 4.3. Make your memory unevictable

Kernel provides a bunch of syscalls for doing that: `mlock()`, `mlock2()` (\*) and `mlockall()`. As with the `mincore()`, you must map the file first.

You likely need to increase the limit:

```shell
$ ulimit -l

$ grep unevic /sys/fs/cgroup/user.slice/user-1000.slice/session-c2.scope/memory.stat
unevictable 189382656
```

### 4.4. Page cache, `vm.swappiness` and modern kernels

Page Cache should be the first and the only option for the memory eviction and reclaiming. But if the system has swap, the kernel has one more option. It can swap out the anonymous (not file-backed) pages. So, in order to control which inactive LRU list to prefer for scans, the kernel has the `sysctl vm.swappiness` knob.

```shell
$ sudo sysctl -a | grep swap
// From 0..200 Higher means more swappy
// 100 value means that the kernel considers anonymous and Page cache pages equally in terms of reclamation.
vm.swappiness = 60
```

### 4.4. Understanding memory reclaim process with `/proc/pid/pagemap`

There is a `/proc/PID/pagemap` file that contains the page table information of the PID. The page table, basically speaking, is an internal kernel map between page frames (real physical memory pages stored in RAM) and virtual pages of the process. Each process in the linux system has its own virtual memory address space which is completely independent form other processes and physical memory addresses.

## 5. `mmap()` file access

Each process has its own region where `mmap()` maps files.

![](https://biriukov.dev/docs/page-cache/images/mmap.png)

```python
import mmap
import os
from time import sleep

print("pid:", os.getpid())

with open("/var/tmp/file1.db", "rb") as f:
    with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
        sleep(10000)
```

Run it and get the pid, then:

```shell
$ pmap -x 105768 | less

105768:   python test_mmap.py
Address           Kbytes     RSS   Dirty Mode  Mapping
00007b26bb400000  131072       0       0 r--s- file1.db

# RSS column = 0 -> how much memory in KiB our process has already referenced -> 0 means that our process hasn't accessed any pages yet.
```

### 5.1. What is page fault?

- The page fault is the CPU mechanism for communicating with the Linux Kernel and its memory subsystem. The page fault is a building block of the Virtual Memory concept and demand paging. Briefly speaking, the kernel usually doesn't allocate physical memory immediately after a memory request is done by `mmap()` or `malloc()`. Instead, the kernel creates some records it the process's page table structure and uses it as a storage for its memory promises.
- There are 2 useful types of page faults:
  - **minor**: A minor basically means that there will be no disk access in order to fulfill a process’s memory access.
  - **major**: A major page fault means that there will be a disk IO operation.
- For example, if we load a half of a file with `dd` in Page cache and afterward access this first half from a program with `mmap()`, we will trigger minor page faults. But if the process tries to read within the same area the second half of the file, the kernel will have to go to the disk in order to load the pages, and the system will generate major page faults.

```python
import mmap
import os
from random import randint
from time import sleep

with open("/var/tmp/file1.db", "r") as f:
    fd = f.fileno()
    size = os.stat(fd).st_size
    with mmap.mmap(fd, 0, prot=mmap.PROT_READ) as mm:
        try:
            while True:
                pos = randint(0, size-4)
                print(mm[pos:pos+4])
                sleep(0.05)
        except KeyboardInterrupt:
            pass
```

```shell
# Terminal 1
# show the system memory statistics per second including page faults.
$ sar -B 1


05:45:55 PM  pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
05:45:56 PM   8164.00      0.00     39.00      4.00      5.00      0.00      0.00      0.00      0.00
05:45:57 PM   2604.00      0.00     20.00      1.00      1.00      0.00      0.00      0.00      0.00
05:45:59 PM   5600.00      0.00     22.00      3.00      2.00      0.00      0.00      0.00      0.00

# Terminal 2
# show major page faults and corresponding file paths
$ sudo perf trace -F maj --no-syscalls

5278.737 ( 0.000 ms): python3/64915 majfault [__memmove_avx_unaligned_erms+0xab] => /var/tmp/file1.db@0x2aeffb6 (d.)
5329.946 ( 0.000 ms): python3/64915 majfault [__memmove_avx_unaligned_erms+0xab] => /var/tmp/file1.db@0x539b6d9 (d.)
5383.701 ( 0.000 ms): python3/64915 majfault [__memmove_avx_unaligned_erms+0xab] => /var/tmp/file1.db@0xb3dbc7 (d.)
5434.786 ( 0.000 ms): python3/64915 majfault [__memmove_avx_unaligned_erms+0xab] => /var/tmp/file1.db@0x18f7c4f (d.)

# Terminal 3
$ python ./mmap_random_read.py
```

- The cgroup also has per cgroup stats regarding page faults:

```shell
$ grep fault /sys/fs/cgroup/user.slice/user-1000.slice/session-c2.scope/memory.stat

workingset_refault_anon 49248
workingset_refault_file 479383
pgfault 155384729
pgmajfault 77618
thp_fault_alloc 6
```
