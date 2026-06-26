# Memcached

Source:

- <https://docs.memcached.org/>
- <https://hnasr.substack.com/p/memcached-architecture>
- <https://www.geeksforgeeks.org/system-design/what-is-memcached/>
- <https://deepwiki.com/memcached/memcached>

Table of contents:
- [Memcached](#memcached)
  - [1. What is memcached?](#1-what-is-memcached)
  - [2. Memcached deep dive](#2-memcached-deep-dive)
    - [2.1. Memory Management](#21-memory-management)
    - [2.2. Threading](#22-threading)
    - [2.3. Least Recently Used (LRU)](#23-least-recently-used-lru)
    - [2.4. LRU Locking](#24-lru-locking)
    - [2.5. LRU Crawler](#25-lru-crawler)

## 1. What is memcached?

> [!IMPORTANT]
> Memcached is an in-memory key-value store for small chunks of arbitrary data (strings, objects) from results of database calls, API calls, or page rendering. Latest stable: **1.6.42** (2025).

Memcached operates as a high-performance, distributed memory caching system that can significantly improve the speed and scalability of web applications.

Memcached is simple yet powerful. Its simple design promotes quick deployment, ease of development, and solves many problems facing large data caches. The server does not care what your data looks like - items are made up of a key, an expiration time, optional flags, and raw data. Logic is split between client (server selection, routing, failover) and server (storage, eviction, memory management). Servers are disconnected from each other - no crosstalk, no synchronization, no broadcasting, no replication. All commands aim for O(1) performance.

![](https://media.geeksforgeeks.org/wp-content/uploads/20240530170747/memcached-1024.png)

- Keys in Memcached are strings, and they're limited to 250 characters. Values can be any type, but they are limited to 1MB by default.
- Keys also have an expiration date or time to live (TTL). However, this should not be relied on, as the least recently used (LRU) algorithm may remove expired keys before they are accessed.
- Memcached does not persist data. If the process dies, the cache is gone. This is by design - it is a cache, not a database.

## 2. Memcached deep dive

> Shoot out to the great article: <https://hnasr.substack.com/p/memcached-architecture>
> Additional details from [deepwiki.com/memcached](https://deepwiki.com/memcached/memcached) with source references to the actual code.

Memcached follows a client-server architecture. The core components are:

1. **Main thread** — handles initial setup, accepts connections, dispatches to worker threads
2. **Connection handler** — manages client connections via libevent, reads and writes data
3. **Protocol parsing** — processes both ASCII (text) and binary protocol (auto-negotiated)
4. **Command processing** — executes get, set, delete, incr/decr, etc.
5. **Item management** — storage, retrieval, expiration of cached items
6. **Slab allocator** — efficient memory management with size-specific chunks
7. **Hash table** — O(1) lookup by key, dynamically resizable
8. **Optional proxy system** — Lua-configurable request routing to backend servers
9. **Optional TLS** — encrypted client connections with certificate verification
10. **Optional external storage** — keep metadata in memory, large items on disk

### 2.1. Memory Management

When allocating items like arrays, strings or integers, they usually go to random places in the process memory. This leaves small gaps of unused memory scattered across the physical memory, a problem referred to as fragmentation.

![](https://substackcdn.com/image/fetch/$s_!HsMs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff44d352a-5d26-4b48-bc1c-e90179ea4b9c_293x432.png)

Fragmentation occurs when the gaps between allocated items continue to increase. This makes it difficult to find a contiguous block of memory that is large enough to hold new items. Technically, there might be enough memory to hold the item, but the memory is scattered all over the physical space.

Does that mean that the item fails to store if no contiguous memory exists? Not really, with the help of virtual memory, the OS gives the illusion that the app is using a contiguous block of memory. Behind the scenes, this block is mapped to tiny areas in physical memory.

When fragmentation occurs, it can cause a program to run more slowly, as the system assembles the memory fragments. The cost of virtual memory mapping and the cost of multiple I/Os to fetch what could have been a single block of memory is relatively high. That is why we try to avoid memory fragmentation.

Memcached avoids fragmentation by pre-allocating 1 MB-sized memory pages, which is why values are capped to 1 MB by default.

![](https://substackcdn.com/image/fetch/$s_!8ufq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbbeeaca-f865-4fc5-ad89-cb6131ed3105_338x314.png)

The OS thinks that Memcached is using the allocated memory, but Memcached isn't storing anything in it yet. As new items are created, Memcached will write item to the allocated page, forcing the item to be next to each other. This avoids fragmentation by moving memory management to Memcached instead of the OS.

The pages are divided into equal-sized **Chunks**. The chunk has a fixed size determined by the **slab class**. A slab class defines the chunk size, for example, Slab class 1 has a chunk size of 72 bytes while Slab class 43 has a chunk size of a 1MB.

![](https://substackcdn.com/image/fetch/$s_!R8DJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb484e1e0-0fac-40bb-ab0d-d6fc5a68ad94_700x211.png)

![](https://substackcdn.com/image/fetch/$s_!y1jx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd0de457-c490-4abe-9c1b-1e1842ca8c6b_700x227.png)

Items consist of a key, value, and some metadata, and they are stored in chunks. For example, if the item size is 40 bytes in size, a whole chunk is used to store the item. The closest chunk size to the 40-byte item is 72 bytes, which is slab class 1, leaving 32 bytes unused in the chunk. That is why the client should be smart to pick items that fit nicely in chunks, leaving as little unused space as possible.

Memcached tries to minimize the unused space by putting the item in the most appropriate slab class. Each slab class has multiple 1MB pages. In Slab class 1, there are 14,564 chunks per page since each chunk is 72 bytes. Slab classes follow a power-of-N factor (default 1.25) to balance granularity vs waste. If an item is less than or equal to 72 bytes, it'll fit nicely in the chunk. But if the item is larger, say 900 kilobytes, it doesn't fit the slab class 1. So, Memcached finds a slab class appropriate for the item. Slab class 43 of chunk size 1MB is the closest one, and the item will be put in that chunk. The entire item fits on a single page.

![](https://substackcdn.com/image/fetch/$s_!N_Fw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f3cdba3-d4cf-45e7-a0e5-2d0cbf9355c7_700x384.png)

But what happens if all allocated pages for this slab class are full?

Slab class 1 is full:

![](https://substackcdn.com/image/fetch/$s_!UPyC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6729b0a9-d595-4cbb-b5b3-68e96d1771ce_700x339.png)

Memcached handles this by allocating a new page and storing the item in a free chunk.

![](https://substackcdn.com/image/fetch/$s_!3kuR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6bb69bc-1086-4333-935b-455b9ffbafcf_700x328.png)

### 2.2. Threading

Memcached uses a multi-threaded architecture to efficiently utilize multiple CPU cores and handle concurrent connections. The number of worker threads defaults to 4, configurable via `-t`.

Memcached accepts remote clients; it has to have networking. Memcached uses TCP as its native transport. UDP is also supported, but was disabled by default because of an attack that happened in [2018 called the reflection attack](https://www.cloudflare.com/learning/ddos/memcached-ddos-attack/).

The Memcached listener thread creates a TCP socket to listen on port 11211. It has one thread that spins up and listens for incoming connections. This thread creates a socket and accepts incoming connections.

Memcached then distributes the connections to a pool of threads. When a new connection is established, Memcached allocates a thread from the pool and gives the connection file descriptor to that thread. That worker thread is now responsible for reading data from the connection.

If a stream of data or a request to get a key is sent to the connection, the thread polls the file descriptor to read the request. Each thread can host one or more connections, and the number of threads in the pool can be configured.

![](https://substackcdn.com/image/fetch/$s_!78h3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F065d679f-dd7b-4725-b226-8572beb026b7_382x417.png)

### 2.3. Least Recently Used (LRU)

Memcached uses a Least Recently Used (LRU) algorithm to manage item eviction when memory is full. Memcached releases anything in memory that hasn't been used for a very long time. That's another reason why Memcached is called transient memory. Even if you set the expiration for an hour, you can't rely on the key being there before the hour expires.

Memcached uses a data structure called a linked list LRU (Least Recently Used) to release items when memory is full.

- Every item in the Memcached key-value store is in a linked list.
- Every slab class has its own LRU.
- If an item is accessed, it is moved from its current position to the head. This process is repeated every time an item is accessed. As a result, items that are not used frequently will be pushed down to the tail of the list and eventually removed if the memory becomes full.

![](https://substackcdn.com/image/fetch/$s_!2gsq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0d36f7c-4631-4c40-a131-03d52d011d6d_422x211.png)

While the LRU is useful, it can also be quite costly in terms of performance. The locks that are necessary to maintain LRU can slow down throughput and complicate the application.

### 2.4. LRU Locking

No two threads can update the same data structure concurrently. To solve this, the thread that needs to update any data structure in memory must obtain a mutex, and other threads wait for the mutex to be freed. This is the basic locking model, and it is used in all applications. Memcached is no different from the LRU data structures.

In [2018](https://memcached.org/blog/modern-lru/), Memcached completely redesigned the LRU to introduce sub-LRUs per slab class breaking it by temperature - Segmented LRU.

An LRU is split into four sub-LRU's. Each sub-LRU has its own mutex lock. They are all governed by a single background thread called the "LRU maintainer", detailed below.

Each item has two bit flags indicating activity level.

- FETCHED: Set if an item has ever been requested
- ACTIVE: set if an item has been accessed for a second time. Removed when an item is bumped or moved.

![](https://memcached.org/blog/modern-lru/img/state_machine.png)

**HOT** acts as a probationary queue, since items are likely to exhibit strong temporal locality or very short TTLs (time-to-live). As a result, items are never bumped within HOT: once an item reaches the tail of the queue, it will be moved to WARM if the item is active (3), or COLD if it is inactive (5).

**WARM** acts as a buffer for scanning workloads, like web crawlers reading old posts. Items which never get hit twice cannot enter WARM. WARM items are given a greater chance of living out their TTL's, while also reducing lock contention. If a tail item has is active, we bump it back to the head (4). Otherwise, we move the inactive item to COLD (7).

**COLD** contains the least active items. Inactive items will flow from HOT (5) and WARM (7) to COLD. Items are evicted from the tail of COLD once memory is full. If an item becomes active, it will be queued to be asynchronously moved to WARM (6). In the case of a burst or large volume of hits to COLD, the bump queue can overflow, and items will remain inactive. In overload scenarios, bumps from COLD become probabilistic, rather than block worker threads.

**TEMP** acts as a queue for new items with very short TTL's (2) (usually seconds). Items in TEMP are never bumped and never flow to other LRU's, saving CPU and lock contention. It is not currently enabled by default.

HOT and WARM LRU's are limited in size primarily by percentage of memory used, while COLD and TEMP are unlimited. HOT and WARM have a secondary tail age limit, relative to the age of the tail of COLD. This prevents very idle items from persisting in the active queues needlessly.

This is all tied together by the **LRU maintainer background thread**. It has a simple job:

- Iterate over every sub-LRU and peek at the tail item.
- Ensure each sub-LRU is respecting its limits, moving items when necessary.
- Reclaim expired tail items.
- Process any asynchronous bumps from the COLD LRU.

### 2.5. LRU Crawler

This implementation still has some outstanding issues: Sizing the cache is hard. Do I have too much RAM? Too little? With all that waste in the middle, it's hard to tell. Items with inconsistent access patterns (e.g. a user goes out to lunch or to sleep) may cause excessive misses. Larger (multi-kilobyte) expired items could make room for hundreds of smaller items, or allow them to be stored for longer.

Solving these issues lead to the LRU crawler, which is a mechanism for asynchronously walking through items in the cache. It is able to reclaim expired items, and can examine the entire cache or subsets of it.

The LRU crawler also supports an **eviction mode** where it will forcefully evict COLD items when memory is low, going beyond just reclaiming expired items.

![](https://memcached.org/blog/modern-lru/img/concurrentcrawler.png)

The crawler is a single background thread which inserts special crawler items into the _tail_ of each sub-LRU in every slab class. It then concurrently walks each crawler item backwards through the LRU's, from bottom to top. The crawler examines each item it passes to see if it's expired, reclaiming if so.

It will look at one item in class 1, HOT, then one item in class 1 WARM, and so on. If class 5 has ten items and class 1 has a million, it will complete its scan of class 5 quickly, then spend a long time finishing class 1.

A histogram of TTL remaining is built as it scans each sub LRU. It then uses the histogram to decide how aggressively to re-scan each LRU. For example, if class 1 has a million items with a 0 TTL it will scan class 1 at most once an hour. If class 5 has 100000 items and 1% of them will be expired in 5 minutes, it will schedule to re-run in five minutes. It can rescan every few seconds, if necessary.

![](https://memcached.org/blog/modern-lru/img/scheduling.png)

Scheduling is powerful: higher slab classes naturally have fewer items that take a lot more space. It can very quickly scan and re-scan large items to keep a low ratio of dead memory. It can scan class 50 over and over, even if it takes 10 minutes to scan class 1 once.

Combined with segmented LRU, the LRU crawler may learn that "HOT" is never worth scanning, but WARM and COLD give fruitful results. Or the opposite: if HOT has many low TTL items, the crawler can keep it clean while avoiding scanning the relatively large COLD. This helps reduce the amount of scan work even within a single slab class.

This secondary process covers most of the remaining inefficiencies of managing an LRU with TTL'ed data. A pure LRU has no concept of holes or expired items, and filesystem buffer pools often keep data around in similar sizes (say, 8k chunks).

Using a background process to pick at dead data, while self-focusing where it can be the most effective, reclaims almost all of the dead memory. It is now much easier to gauge how much memory a cache is actually taking.
