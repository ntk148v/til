# mmap

Source:

- <https://realpython.com/python-mmap/>
- <https://learn.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files>
- <https://stackoverflow.com/questions/35891525/mmap-for-writing-sequential-log-file-for-speed>

Table of content:

- [mmap](#mmap)
  - [1. Memory-mapped file - mmap](#1-memory-mapped-file---mmap)
  - [2. File I/O](#2-file-io)
  - [3. Read \& write with mmap](#3-read--write-with-mmap)
    - [3.1. Read](#31-read)
  - [3.2. Search a Memory-mapped file](#32-search-a-memory-mapped-file)
    - [3.3. Write](#33-write)
  - [4. Conclusion](#4-conclusion)

My colleague says that he wants to write log file, using **memory-mapped file** (`mmap`) technique for _speed_.

## 1. Memory-mapped file - mmap

- Memory mapping is a technique that uses lower-level operating system APIs to load a file directly into computer memory.
- Computer memory is a big, complicated topic; in this guide, the term **memory** refers to Random-access memory, RAM.
- There are several types of computer memory:
  - Physical memory:
    - Typically comes on cards that are connected to the computer's motherboard.
    - The amount of [volatile memory](https://en.wikipedia.org/wiki/Volatile_memory) that's available for programs to use while running.
  - Virtual memory:
    - A way of handling memory management.
    - The OS uses virtual memory to make it appear that you have more memory than you do. Behind the scenes, OS uses parts of nonvolatile storage, such as SSD, to simulate additional RAM.
    - In order to do this, OS must maintain a mapping between physical and virtual memory: [page table](https://en.wikipedia.org/wiki/Page_table)
    - `mmap` uses virtual memory to efficiently share large amounts of data between multiple processes, threads, taksks that are happening concurrently.
  - Shared memory:
    - Another technique provided by OS that allows multiple programs to access the same data simultaneously.
    - `mmap` uses shared memory to efficiently share large amounts of data between multiple Python processes, threads, and tasks that are happening concurrently.
- A memory-mapped file contains the content of a file in virtual memory. This mapping between a file and memory space enables an application, including multiple processes, to modify the file by reading and writing directly to the memory.
- There are two types of memory-mapped files:
  - Persisted memory-mapped files: Persisted files are memory-mapped files that are associated with a source file on a disk. When the last process has finished working with the file, the data is saved to the source file on the disk. These memory-mapped are suitable for working with extremely large source files.
  - Non-persisted memory-mapped files: Non-persisted fiels are memory-mapped files that are not associated with a file on a disk. When the last process has finished working with the file, the data is lost and the file is reclaimed by garbage collection. These files are suitable for creating shared memory for inter-process communications (IPC).

## 2. File I/O

- In order to fully appreciate what memory mapping does, it's useful to consider regular file I/O from a lower-level perspective:
  - **Transferring** cojntrol to the kernel or core OS code with system calls.
  - **Interracting** with the physical disk where the file resides.
  - **Copying** the data into different buffers between user space and kernel space.

```python
def regular_io(filename):
    # Read entire file into physical memory
    with open(filename, mode="r", encoding="utf8") as file_obj:
        # read() signals the OS to do a lot of sophisticated work
        # read() performs several system calls
        text = file_obj.read()
        print(text)
```

- The most important thing to remember is that system calls are relatively expensive computationally speaking, so the fewer system calls you do, the faster your code will likely execute.
- In addition to the system calls, the call to `read()` also invovles a lot of potentially unncessary copying of data between multiple data buffers before the data gets all the way back to your program. -> add latency and can slow down program -> mmap
- A memory-mapped file I/O approach sacrifices memory usage for speed, which is classically called the [space-time tradeoff](https://en.wikipedia.org/wiki/Space-time_tradeoff).

## 3. Read & write with mmap

> **NOTE**: These results were gathered using Ubuntu 22.04 and Python 3.10. Since memory mapping is very dependent on the operating system implementations, your results may vary.

### 3.1. Read

```python
def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as file_obj:
        # Ensure that the mode you use with open() is compatible with mmap.mmap()
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            text = mmap_obj.read()
            # Text is mmap object
            print(text)
```

- Benchmark:

```python
import timeit

# Benchmark time
print("regular_io", timeit.repeat(
    "regular_io(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import regular_io, filename"))

print("mmap_io", timeit.repeat(
    "mmap_io(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import mmap_io, filename"))
```

- Result:

```shell
regular_io [6.941209831999913, 7.164341439000054, 6.920215922000352]
mmap_io [0.2982539229997201, 0.2962546029993973, 0.2988888530007898]
```

## 3.2. Search a Memory-mapped file

```python
import mmap
import timeit

filename = input("Enter the absolute file path: ")
if not filename:
    filename = "/tmp/a"


def regular_io_find(filename):
    with open(filename, mode="r", errors="ignore") as file_obj:
        text = file_obj.read()
        return text.find(" the ")


def mmap_io_find(filename):
    with open(filename, mode="r", errors="ignore") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            return mmap_obj.find(b" the ")


print("regular_io_find", timeit.repeat(
    "regular_io_find(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import regular_io_find, filename"))
print("mmap_io_find", timeit.repeat(
    "mmap_io_find(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import mmap_io_find, filename"))
```

```shell
regular_io_find [8.58905833999961, 7.636531751999428, 7.965919309999663]
mmap_io_find [0.3894387399996049, 0.38593113499973697, 0.4086118739996891]
```

### 3.3. Write

```python
import timeit
import os
import shutil
import mmap

filename = input("Enter the absolute file path: ")
if not filename:
    filename = "/tmp/a"


def mmap_io_write(filename):
    with open(filename, mode="r+") as file_obj:
        #  ACCESS_WRITE specifies write-through semantics, meaning the data will be written through memory and persisted on disk.
        # ACCESS_COPY does not write the changes to disk, even if flush() is called.
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            mmap_obj[10:16] = b"python"
            mmap_obj.flush()


def regular_io_find_and_replace(filename):
    with open(filename, "r", errors="ignore") as orig_file_obj:
        with open("/tmp/b", "w", errors="ignore") as new_file_obj:
            orig_text = orig_file_obj.read()
            new_text = orig_text.replace(" the ", " eht ")
            new_file_obj.write(new_text)

    shutil.copyfile("/tmp/b", filename)
    os.remove("/tmp/b")


def mmap_io_find_and_replace(filename):
    with open(filename, mode="r+", errors="ignore") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            orig_text = mmap_obj.read()
            new_text = orig_text.replace(b" the ", b" eht ")
            mmap_obj[:] = new_text
            mmap_obj.flush()


print("regular_io_find_and_replace", timeit.repeat(
    "regular_io_find_and_replace(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import regular_io_find_and_replace, filename"))

print("mmap_io_find_and_replace", timeit.repeat(
    "mmap_io_find_and_replace(filename)",
    repeat=3,
    number=1,
    setup="from __main__ import mmap_io_find_and_replace, filename"))

```

- Actually, in this scenario, the memory-mapped approach is slower.
- TODO: Test with sequential data writing.

## 4. Conclusion

> **NOTE**: I will test it first.

- Do not use `mmap` for sequential data writing. It will just cause much more overhead and will lead to much more "unnatural" code than a simple writing alogrithm using `fwrite`.
- Use `mmap` for random access reads to large files.
