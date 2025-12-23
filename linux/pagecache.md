# The page cache

Source:

- <https://notes.eddyerburgh.me/operating-systems/linux/the-page-cache-and-page-writeback>
- <https://biriukov.dev/docs/page-cache/0-linux-page-cache-for-sre/>

The page cache is a disk cache used to minimize disk I/O. Instead of read requests and write operations running against a disk, they run against an in-memory cache (unused areas of the memory) that only reads data from disk when needed and writes changes to disk periodically.

The page cache contains physical pages in RAM, which correspond to physical blocks on a disk. The page cache is dynamic: “it can grow to consume any free memory and shrink to relieve memory pressure”.

## 1. Approaches to caching

### 1.1. Read strategy

When the kernel begins a read operation, it first checks to see if the page is in the cache. If it is then the operation can be completed without requiring an expensive seek operation. This is called a cache hit. If the page isn’t in the cache (a cache miss) the kernel must schedule an I/O operation to read the data off the disk. Once the data has been read from the disk, the kernel adds the data to the cache for future usage

![](https://developer.qcloudimg.com/http-save/yehe-1140319/2a884b6b1e436adacf7c1b81fd04b1e9.png)

### 1.2. Write strategy

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
