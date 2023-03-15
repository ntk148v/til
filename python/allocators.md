# Python allocators

Source:

- <https://bloomberg.github.io/memray/python_allocators.html>
- <https://www.honeybadger.io/blog/memory-management-in-python/>

Python has a layer of abstraction between code that allocates memory and the system allocator (malloc, free, realloc, etc). Although the system allocator is quite fast and efficient, it is still generic and is not tuned to the specific allocation patterns of the Python interpreter, especially those regarding small Python objects.

To improve performance and reduce fragmentation, Python has a specialized allocator that handles allocation of small objects and defers to the system allocator for large ones - `pymalloc`.

Requests greater than 512 bytes are routed to the system's allocator. This means that even if `pymalloc` is active, it will only affect requests for 512 bytes or less. For those small requests, the `pymalloc` allocator will allocate big chunks of memory from the system allocator and then subdivide those big chunks.

![](https://bloomberg.github.io/memray/_images/pymalloc.png)

![](https://www.honeybadger.io/images/blog/posts/memory-management-in-python/arenas_pools_and_blocks.png?1678844423)

`pymalloc` works with 3 hierarchical data structures:

- Arenas: These are chunks of memory that `pymalloc` directly requests from the system allocator using `mmap`. Arenas are always a multiple of 4 kilobytes. Arenas are subdivided into pools of different types.
- Pools: Pools contain fixed size blocks of memory. Each pool only contains blocks of a single consistent size, though different pools have blocks of different sizes. Pools are used to easily find, allocate, and free memory blocks of a given size.
- Blocks: These are the fundamental units of storage. Small allocation requests to `pymalloc` are always satisfied by returning a pointer to a specific block. This block can be bigger than what the allocation requested.
