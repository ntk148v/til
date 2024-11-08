# Python 3.13 Performance: Free-Threading

Source: <https://codspeed.io/blog/state-of-python-3-13-performance-free-threading>

CPython 3.13:

- CPython can now run in **free-threaded mode**, with the global interpreter lock (GIL) disabled
  - An experimental feature in Python 3.13 that allows CPython to run without the Global interpreter lock (GIL). The GIL is a mutex preventing multiple threads from executing Python bytecode simultaneously. This design choice has simplified CPython's memory management and made the C API easier to work with. However, it has also been one of the most significant barriers to utilizing modern multi-core processors effectively.
  - The traditional solution has been to use the `multiprocessing` module, which spawns separate Python processes instead of threads and while this approach works, it comes with significant limitations:
    - Memory overhead.
    - Communication cost.
    - Startup time.
- a brand new **just-in-time (JIT)** compiler has been added
- CPython now bundles the `mimalloc` allocator out of the box
