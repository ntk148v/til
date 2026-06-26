# Memcached

> [!IMPORTANT]
> Memcached is an in-memory key-value store for small chunks of arbitrary data (strings, objects) from results of database calls, API calls, or page rendering. Latest stable: **1.6.42** (2025).

Sources:

- [docs.memcached.org](https://docs.memcached.org/)
- [Hussein Nasser - Memcached Architecture](https://hnasr.substack.com/p/memcached-architecture)
- [deepwiki.com/memcached](https://deepwiki.com/memcached/memcached)
- [UserInternals wiki](https://github.com/memcached/memcached/wiki/UserInternals)

## Table of Contents

- [1. What is memcached?](#1-what-is-memcached)
- [2. Memcached deep dive](#2-memcached-deep-dive)
  - [2.1. Memory Management](#21-memory-management)
  - [2.2. Threading](#22-threading)
  - [2.3. Least Recently Used (LRU)](#23-least-recently-used-lru)
  - [2.4. LRU Locking](#24-lru-locking)
  - [2.5. LRU Crawler](#25-lru-crawler)
  - [2.6. Reads and Writes](#26-reads-and-writes)
  - [2.7. Collisions](#27-collisions)

## 1. What is memcached?

Memcached is a high-performance, distributed memory caching system that speeds up dynamic web applications by caching results of database queries, API calls, or page rendering in RAM.

It is intentionally minimal. The server treats all data as opaque blobs - items are just a key, expiration time, optional flags, and raw bytes. Clients handle server selection and routing via consistent hashing. Memcached servers are completely independent: no replication, no synchronization, no broadcasting between them. All operations target O(1) time with minimal locking.

A cache, not a database. If the process dies, the data is gone. There is no persistence.

![](https://media.geeksforgeeks.org/wp-content/uploads/20240530170747/memcached-1024.png)

- Keys are strings, limited to 250 characters. Values can be any type, capped at 1 MB by default.
- Keys have a TTL (time-to-live), but this should not be relied upon - the LRU algorithm may evict items before expiry when memory fills up.
- Memcached does not persist data. If the process dies, the cache is gone. Cache, not database.

## 2. Memcached deep dive

> Deep dive based on [Hussein Nasser's article](https://hnasr.substack.com/p/memcached-architecture) and [deepwiki.com/memcached](https://deepwiki.com/memcached/memcached) with source references to the actual code.

Memcached is built from these core components:

1. **Main thread** - accepts connections, dispatches to worker threads
2. **Connection handler** - manages client connections via libevent
3. **Protocol parsing** - ASCII (text) and binary protocol, auto-negotiated
4. **Command processing** - executes get, set, delete, incr/decr, etc.
5. **Item management** - storage, retrieval, expiration of cached items
6. **Slab allocator** - memory management with size-specific chunks, avoids fragmentation
7. **Hash table** - O(1) key lookup, dynamically resizable
8. **Optional proxy system** - Lua-configurable request routing to backend servers
9. **Optional TLS** - encrypted client connections
10. **Optional external storage** - metadata in memory, large items on disk

### 2.1. Memory Management

When allocating items like arrays, strings or integers, they usually go to random places in the process memory. This leaves small gaps of unused memory scattered across the physical memory. This is fragmentation.

![](https://substackcdn.com/image/fetch/$s_!HsMs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44d352a-5d26-4b48-bc1c-e90179ea4b9c_293x432.png)

As gaps grow, finding a contiguous block large enough for a new allocation gets harder. Total free memory may be sufficient, but it's scattered across physical space.

Does an item fail if no contiguous block exists? Not exactly. Virtual memory gives the illusion of contiguous space by mapping to scattered physical pages behind the scenes. But this comes at a cost - TLB pressure, page-table walks, and multiple I/Os to fetch what could have been a single memory block. That cost adds up, which is why we avoid fragmentation.

Memcached avoids fragmentation by pre-allocating 1 MB memory pages and managing memory itself instead of relying on the OS allocator. This is also why values are capped at 1 MB by default.

Run with `-vv` to see the chunk layout:

```
$ memcached -vv
slab class   1: chunk size        80 perslab   13107
slab class   2: chunk size       104 perslab   10082
slab class   3: chunk size       136 perslab    7710
slab class   4: chunk size       176 perslab    5957
slab class   5: chunk size       224 perslab    4681
slab class   6: chunk size       280 perslab    3744
slab class   7: chunk size       352 perslab    2978
slab class   8: chunk size       440 perslab    2383
slab class   9: chunk size       552 perslab    1899
slab class  10: chunk size       696 perslab    1506
[... up to class 43 (1 MB chunk)]
```

![](https://substackcdn.com/image/fetch/$s_!8ufq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbbeeaca-f865-4fc5-ad89-cb6131ed3105_338x314.png)

The OS believes Memcached is using the allocated memory, but nothing is stored yet. As new items arrive, Memcached writes them sequentially into the page, packing them next to each other. This moves memory management from the OS to Memcached, eliminating external fragmentation.

Each page is divided into equal-sized **chunks**. The chunk size is determined by the **slab class**. For example, slab class 1 has 72-byte chunks, slab class 43 has 1 MB chunks. The sizes grow by a power-of-N factor (default 1.25) to balance granularity vs waste.

![](https://substackcdn.com/image/fetch/$s_!R8DJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb484e1e0-0fac-40bb-ab0d-d6fc5a68ad94_700x211.png)

![](https://substackcdn.com/image/fetch/$s_!y1jx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd0de457-c490-4abe-9c1b-1e1842ca8c6b_700x227.png)

Items consist of a key, value, and metadata, stored in chunks. If an item is 40 bytes, the closest chunk size is 72 bytes (slab class 1), wasting 32 bytes per chunk. This is internal fragmentation - the trade-off for avoiding external fragmentation. Clients should size their values to land near chunk boundaries to minimize waste.

Memcached places each item in the most appropriate slab class. Each slab class has multiple 1 MB pages. In slab class 1, each page contains 14,564 chunks (1 MB / 72 bytes). If an item is larger, say 900 KB, it doesn't fit class 1. Memcached finds class 43 (1 MB chunk size), the closest fit. The entire item fits on a single page.

Check slab usage at runtime:

```
$ echo "stats slabs" | nc localhost 11211
STAT 1:chunk_size 80
STAT 1:chunks_per_page 13107
STAT 1:total_pages 1
STAT 1:total_chunks 13107
STAT 1:used_chunks 2
STAT 1:free_chunks 13105
END
```

![](https://substackcdn.com/image/fetch/$s_!N_Fw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f3cdba3-d4cf-45e7-a0e5-2d0cbf9355c7_700x384.png)

But what happens if all allocated pages for this slab class are full?

Slab class 1 is full:

![](https://substackcdn.com/image/fetch/$s_!UPyC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6729b0a9-d595-4cbb-b5b3-68e96d1771ce_700x339.png)

Memcached handles this by allocating a new page and storing the item in a free chunk.

![](https://substackcdn.com/image/fetch/$s_!3kuR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6bb69bc-1086-4333-935b-455b9ffbafcf_700x328.png)

### 2.2. Threading

Memcached uses multiple threads (default 4, configurable via `-t`) to handle concurrent connections across CPU cores.

Memcached accepts remote clients over TCP. UDP is also supported but disabled by default since the [2018 reflection attack](https://www.cloudflare.com/learning/ddos/memcached-ddos-attack/).

A listener thread creates a TCP socket on port 11211, accepts incoming connections, and distributes them to a pool of worker threads. Each worker receives the connection's file descriptor and handles all I/O for it via libevent event loops.

Each worker thread can host multiple connections. Workers share the hash table and LRU structures through mutexes.

```
$ echo "stats" | nc localhost 11211 | grep threads
STAT threads 4
```

![](https://substackcdn.com/image/fetch/$s_!78h3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F065d679f-dd7b-4725-b226-8572beb026b7_382x417.png)

### 2.3. Least Recently Used (LRU)

Memcached uses a Least Recently Used (LRU) algorithm to manage eviction when memory is full. Data that hasn't been accessed in a while is released. This is why Memcached is considered transient memory - even with a TTL of one hour, a key may not survive if the cache is under pressure.

The LRU is implemented as a linked list:

- Every item in the store belongs to a linked list.
- Each slab class has its own LRU.
- On access, the item moves to the head. Unused items drift toward the tail and get evicted when memory fills.

![](https://substackcdn.com/image/fetch/$s_!2gsq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0d36f7c-4631-4c40-a131-03d52d011d6d_422x211.png)

LRU operations require locks, which creates a performance bottleneck under high concurrency — the original single-LRU-per-class design meant only one thread could update the LRU at a time.

Monitor evictions with `stats items`:

```
$ echo "stats items" | nc localhost 11211
STAT items:1:number 2
STAT items:1:age 345
STAT items:1:evicted 0
STAT items:1:evicted_nonzero 0
STAT items:1:evicted_time 0
END
```

If `evicted` is growing, the slab class is under memory pressure — items are being evicted before their TTL expires.

### 2.4. LRU Locking

Concurrent access to shared data structures requires mutexes. No two threads can modify the same LRU at the same time. This is the basic locking model, and it applies to all LRU operations.

In [2018](https://memcached.org/blog/modern-lru/), Memcached redesigned the LRU to split each slab class into four sub-LRUs by access temperature, each with its own mutex. This is called **Segmented LRU**.

A background thread called the **LRU maintainer** governs all sub-LRUs.

Each item has two bit flags tracking activity:

- **FETCHED**: set if the item has ever been requested
- **ACTIVE**: set if the item has been accessed a second time. Cleared when the item is bumped or moved.

![](https://memcached.org/blog/modern-lru/img/state_machine.png)

**HOT** acts as a probationary queue, since items are likely to exhibit strong temporal locality or very short TTLs (time-to-live). As a result, items are never bumped within HOT: once an item reaches the tail of the queue, it will be moved to WARM if the item is active (3), or COLD if it is inactive (5).

**WARM** acts as a buffer for scanning workloads, like web crawlers reading old posts. Items which never get hit twice cannot enter WARM. WARM items are given a greater chance of living out their TTLs, while also reducing lock contention. If a tail item is active, it gets bumped back to the head (4). Otherwise, the inactive item moves to COLD (7).

**COLD** contains the least active items. Inactive items will flow from HOT (5) and WARM (7) to COLD. Items are evicted from the tail of COLD once memory is full. If an item becomes active, it will be queued to be asynchronously moved to WARM (6). In the case of a burst or large volume of hits to COLD, the bump queue can overflow, and items will remain inactive. In overload scenarios, bumps from COLD become probabilistic, rather than block worker threads.

**TEMP** acts as a queue for new items with very short TTL's (2) (usually seconds). Items in TEMP are never bumped and never flow to other LRU's, saving CPU and lock contention. It is not currently enabled by default.

HOT and WARM LRU's are limited in size primarily by percentage of memory used, while COLD and TEMP are unlimited. HOT and WARM have a secondary tail age limit, relative to the age of the tail of COLD. This prevents very idle items from persisting in the active queues needlessly.

This is all tied together by the **LRU maintainer background thread**. It has a simple job:

- Iterate over every sub-LRU and peek at the tail item.
- Ensure each sub-LRU is respecting its limits, moving items when necessary.
- Reclaim expired tail items.
- Process any asynchronous bumps from the COLD LRU.

```
# Check LRU tail ages at runtime
$ echo "stats lru" | nc localhost 11211
STAT lru_hot_max_age 413
STAT lru_warm_max_age 1202
STAT lru_cold_max_age 7509
END
```

### 2.5. LRU Crawler

This implementation still has some outstanding issues: Sizing the cache is hard. Do I have too much RAM? Too little? With all that waste in the middle, it's hard to tell. Items with inconsistent access patterns (e.g. a user goes out to lunch or to sleep) may cause excessive misses. Larger (multi-kilobyte) expired items could make room for hundreds of smaller items, or allow them to be stored for longer.

Solving these issues lead to the LRU crawler, which is a mechanism for asynchronously walking through items in the cache. It is able to reclaim expired items, and can examine the entire cache or subsets of it.

The LRU crawler also supports an **eviction mode** - when memory is extremely low, it can proactively evict COLD items instead of waiting for a write to trigger eviction.

```
# Enable the LRU crawler
$ echo "lru_crawler enable" | nc localhost 11211
OK

# Check crawler stats
$ echo "stats lru_crawler" | nc localhost 11211 | head -5
```

![](https://memcached.org/blog/modern-lru/img/concurrentcrawler.png)

The crawler is a single background thread which inserts special crawler items into the _tail_ of each sub-LRU in every slab class. It then concurrently walks each crawler item backwards through the LRU's, from bottom to top. The crawler examines each item it passes to see if it's expired, reclaiming if so.

It will look at one item in class 1, HOT, then one item in class 1 WARM, and so on. If class 5 has ten items and class 1 has a million, it will complete its scan of class 5 quickly, then spend a long time finishing class 1.

A histogram of TTL remaining is built as it scans each sub LRU. It then uses the histogram to decide how aggressively to re-scan each LRU. For example, if class 1 has a million items with a 0 TTL it will scan class 1 at most once an hour. If class 5 has 100000 items and 1% of them will be expired in 5 minutes, it will schedule to re-run in five minutes. It can rescan every few seconds, if necessary.

![](https://memcached.org/blog/modern-lru/img/scheduling.png)

Scheduling is powerful: higher slab classes naturally have fewer items that take a lot more space. It can very quickly scan and re-scan large items to keep a low ratio of dead memory. It can scan class 50 over and over, even if it takes 10 minutes to scan class 1 once.

Combined with segmented LRU, the LRU crawler may learn that "HOT" is never worth scanning, but WARM and COLD give fruitful results. Or the opposite: if HOT has many low TTL items, the crawler can keep it clean while avoiding scanning the relatively large COLD. This helps reduce the amount of scan work even within a single slab class.

This secondary process covers most of the remaining inefficiencies of managing an LRU with TTL'ed data. A pure LRU has no concept of holes or expired items, and filesystem buffer pools often keep data around in similar sizes (say, 8k chunks).

Using a background process to pick at dead data, while self-focusing where it can be the most effective, reclaims almost all of the dead memory. It is now much easier to gauge how much memory a cache is actually taking.

### Item size and overhead

Each item consumes `sizeof(item struct) + key length + value length + flags` bytes. On 64-bit systems the item struct is 40 bytes with CAS enabled (default). The `sizes` utility shipped with the source shows the exact breakdown:

```
$ ./sizes
Item (no cas)   32
Item (cas)      40
Connection      320
Thread stats    176
```

A 100-byte value with a 20-byte key uses roughly `40 + 20 + 100 + 4 = 164` bytes total. This lands in slab class 4 (176-byte chunks, 5,957 items per page). Knowing your item overhead helps choose the right class.

### 2.6. Reads and Writes

#### 2.6.1. Reads

To locate an item for a given key, Memcached uses a hash table - an associative array where every element is equally fast to access once you know the index.

Given only a key, the server converts it to an index: hash the key, take modulo N (the hash table size). The result is a slot index between 0 and N-1, used to look up the item in O(1) time.

The slot points to memory on the appropriate slab class page. On a read hit, the item is moved to the head of its sub-LRU under a mutex lock.

```
$ echo "get mykey" | nc localhost 11211
VALUE mykey 0 5
hello
END
```

![](https://substackcdn.com/image/fetch/$s_!2alB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f5a920b-035d-4390-a587-c27e2c7bb163_600x338.gif)

When the key test is read, and we get item d, the LRU is updated so that d is now at the head of the linked list.

![](https://substackcdn.com/image/fetch/$s_!2gsq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0d36f7c-4631-4c40-a131-03d52d011d6d_422x211.png)

What happens if we read the key buzz pointing to item c? The LRU is updated so that c is now the head right after d.

![](https://substackcdn.com/image/fetch/$s_!mtTN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00b204de-69c4-427d-9c6f-5f63a9aba34d_517x229.png)

#### 2.6.2. Writes

To write a key with a new value of 44 bytes, the server hashes the key, finds its index in the hash table. If the slot is empty, a new pointer is created, a slab class chunk is allocated, and the item is stored.

```
$ echo "set mykey 0 3600 5" | nc localhost 11211
hello
STORED
```

The second argument (0) is the flags field - opaque to the server, returned on reads for the client to interpret. Common uses: serialization format or compression hint.

```
$ echo "set flagtest 1 300 4" | nc localhost 11211
test
STORED

$ echo "get flagtest" | nc localhost 11211
VALUE flagtest 1 4
test
END
```

![](https://substackcdn.com/image/fetch/$s_!foRh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43fcebf0-85be-4a22-b2f6-2106ba5e37eb_600x338.gif)

### 2.7. Collisions

Hash collisions are unavoidable. Two different keys can hash to the same slot. Memcached handles this with **chaining** - each hash slot points to a linked list of items sharing that hash.

![](https://substackcdn.com/image/fetch/$s_!JnMb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03739f18-28bf-48e1-bd0d-4e3593a0c857_600x338.gif)

When reading a key, the server walks the chain comparing keys until it finds a match. In the worst case this becomes O(N) within a chain.

Memcached measures chain depth using DTrace probes. If chains grow too long, read performance suffers.

```
$ echo "stats hash" | nc localhost 11211
STAT hash_power_level 16
STAT hash_bytes 524288
STAT hash_is_expanding 0
STAT hash_expand_count 1
END
```

When chain depth exceeds a threshold, Memcached resizes the hash table (doubles it) and rehashes all items. This runs on a background thread so worker threads aren't blocked.

- Hash table size is always a power of 2 for fast bitwise masking
- A separate maintenance thread handles hash table growth
