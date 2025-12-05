# Virtual memory

Source:

- <https://tldp.org/LDP/tlk/mm/memory.html>
- <https://docs.kernel.org/admin-guide/mm/concepts.html>

## What is virtual memory, anyway?

Virtual memory makes the system appear to have more memory than it actually has by sharing it between competing processes as they need it.

Virtual memory is used by all current operating systems. It simply means that the memory address a program requests is virtualized – not necessarily related to a physical memory address.

- The program may request the content of memory address 1000.
- The computer looks at where the current map for address 1000 is pointing, and returns the contents of that address. (Virtual address 1000 may be mapped to physical address 20).
- Of course, if the memory is virtualized, that means that there is no need to actually have physical memory on the server for every address the programs think they can address – so the programs can believe the server to have more memory than it physically does.
- Virtual memory addresses do not need to be mapped to anything until they are allocated by a program. And a virtual memory address can be mapped not to a physical block of memory for storage, but to a block on a hard drive.

## 2. How virtual memory works: Key mechanisms

![](https://tldp.org/LDP/tlk/mm/vm.gif)

- Each process gets its **own virtual address space**. When the process accesses memory, it uses virtual addresses. Under the hood, the system (OS + hardware) translates those virtual access addresses to real physical addresses.
- The mapping from virtual addresses -> physical addresses is maintained via **page tables**. Physical memory is split into "page frames", and virtual memory is split into "pages". Virtual pages get mapped to physical frames as needed.
- Because of this mechanism, the OS doesn’t have to allocate contiguous physical memory for a program’s entire virtual memory space. This simplifies memory allocation and avoids fragmentation issues.

## 3. Demand paging, Backing storage and swapping

Because it's rarely efficient or necessary to load a program’s entire memory footprint into RAM at once, modern systems use demand-based and dynamic memory management:

- **Demand paging** - only the pages that a process actually needs (i.e. accesses) are loaded into physical memory; other pages remain on disk until they are needed. If a process accesses a page that is not resident, a **page fault** is raised, and the OS loads the required page from disk.
- If physical RAM is scarce (or many processes are running), the OS may move seldom-used (inactive) pages from RAM to a special disk area (called **swap space**), freeing up RAM for active pages. Later, if those pages are needed again, they are read back into RAM.
- This swapping (or paging) to disk allows the system to support workloads that, in total, need more memory than the physical RAM alone — at the cost of performance, since disk I/O is much slower than RAM access.
- Swapping vs. Paging:
  - Paging moves individual pages between RAM and disk.
  - Swapping (much rarer today) refers to moving the entire process image out of RAM.

## 4. Benefits of virtual memory

Virtual memory does more than just make your computer's memory go further. The memory management subsystem provides:

- Large Address Spaces: The operating system makes the system appear as if it has a larger amount of memory than it actually has. The virtual memory can be many times larger than the physical memory in the system,
- Protection: Each process in the system has its own virtual address space. These virtual address spaces are completely separate from each other and so a process running one application cannot affect another. Also, the hardware virtual memory mechanisms allow areas of memory to be protected against writing. This protects code and data from being overwritten by rogue applications.
- Memory Mapping: Memory mapping is used to map image and data files into a processes address space. In memory mapping, the contents of a file are linked directly into the virtual address space of a process.
- Fair Physical Memory Allocation: The memory management subsystem allows each running process in the system a fair share of the physical memory of the system,
- Shared Virtual Memory:
  - Although virtual memory allows processes to have separate (virtual) address spaces, there are times when you need processes to share memory. For example there could be several processes in the system running the bash command shell. Rather than have several copies of bash, one in each processes virtual address space, it is better to have only one copy in physical memory and all of the processes running bash share it. Dynamic libraries are another common example of executing code shared between several processes.
  - Shared memory can also be used as an Inter Process Communication (IPC) mechanism, with two or more processes exchanging information via memory common to all of them. Linux supports the Unix TM System V shared memory IPC.

## 5. Costs and constraints

- Performance overhead: accessing pages from disk is orders of magnitude slower than accessing RAM. When the system relies heavily on disk-backed pages (known as thrashing), performance degrades significantly.
- Management Complexity: Maintaining mappings, handling page faults, and updating page tables introduce overhead.
- Physical Limits Still Matter: Virtual memory does not eliminate the need for sufficient physical RAM; it only allows more flexible and efficient usage of it.

## 6. Configuration

### 6.1. Swapping and Page-Reclaim Behavior

#### 6.1.1. **vm.swappiness**

Controls the kernel’s tendency to swap out anonymous memory (e.g., process heap/stack) versus evicting pagecache.

- **Range:** 0–100
- **Lower values:** Avoid swapping; keep anonymous pages in RAM.
- **Higher values:** Swap more aggressively.
- **Defaults:** Often 60.

**Guidance:**

- Database servers: 1–10
- General desktops: 30–60
- Memory-constrained systems: higher values may help avoid OOM

#### 6.1.2. **vm.vfs_cache_pressure**

Controls how aggressively the kernel reclaims memory used for directory and inode caches.

- **Lower values (<100):** Keep inode/dentry cache longer.
- **Higher values (>100):** Reclaim file metadata more aggressively.

**Usage:** Tune based on file system workload. Lower values can help workloads with heavy metadata access (build servers, file servers).

#### 6.1.3. **vm.page-cluster**

Determines how many pages the kernel reads/writes at once during swap I/O.

- Default typically 3 → 2³ = 8 pages per swap I/O.
- Lower values reduce I/O burst size (may help SSDs).
- Higher values increase batch I/O.

### 6.2. Out-of-Memory (OOM) Handling and Stability

#### 6.2.1. **vm.overcommit_memory**

Controls how the kernel accounts for process memory allocation.

- **0:** Heuristic overcommit (default).
- **1:** Allow all allocations (don’t check).
- **2:** Don’t overcommit beyond allowed memory (strict).

**Guidance:**

- For predictable environments like databases: set to **2**.
- For HPC workloads needing large mmap regions: sometimes set to **1**.

#### 6.2.2. **vm.overcommit_ratio**

Used when `overcommit_memory = 2`.
Defines how much memory can be committed as a percentage of RAM.

- Default: **50**
- Commit limit = Swap + (RAM \* ratio/100)

---

#### 6.2.3. **vm.oom_kill_allocating_task**

If set to 1, the kernel kills the task that triggered the OOM, not the largest memory consumer.

Useful in debugging or in controlled environments but risky in production.

#### 6.2.4. **vm.panic_on_oom**

Controls whether the kernel panics instead of killing a task on OOM.

- **0:** Try to kill processes.
- **1:** Panic on OOM.
- **2:** Always panic.

Used in clusters where memory exhaustion indicates catastrophic failure requiring failover.

### 6.3. Dirty Page and Writeback Controls

These parameters strongly influence write-heavy workloads.

#### 6.3.1. **vm.dirty_ratio**

Maximum percentage of dirty pages allowed before processes must write them out.

- High = more dirty pages = potential latency spikes.

#### 6.3.2. **vm.dirty_background_ratio**

Percentage at which background writeback starts.

- Lower = cleaner system = more regular I/O.

#### 6.3.3. **vm.dirty_bytes / vm.dirty_background_bytes**

Byte-based equivalents.
Preferred over ratios for servers with large RAM capacities.

#### 6.3.4. **vm.dirty_expire_centisecs**

Age after which dirty data is eligible for writeback.

#### 6.3.5. **vm.dirty_writeback_centisecs**

Frequency of writeback daemon wakeups.

### 6.4. Page Cache and Reclaim-Specific Controls

#### 6.4.1. **vm.min_free_kbytes**

Minimum amount of free memory the kernel keeps in reserve to avoid emergency slow-path allocations.

Increasing helps high-throughput networking and I/O.

#### 6.4.2. **vm.watermark_scale_factor**

Controls reclaim aggressiveness relative to memory pressures.

Useful for fine-tuning reclaim behavior in NUMA or high-memory systems.

#### 6.4.3. **vm.zone_reclaim_mode**

Enables reclaim before using remote memory on NUMA systems.

- Common values: 0 (off), 1 (reclaim local pages)

Not recommended for many workloads unless NUMA locality is critical.

### 6.5. Transparent Huge Pages (THP) Controls

#### 6.5.1. **vm.nr_hugepages**

Number of preallocated HugeTLB pages.

#### 6.5.2. **vm.nr_overcommit_hugepages**

Controls overcommit of hugepages.

#### 6.5.3. **vm.hugetlb_shm_group**

GID that can create hugepage-backed shared memory.

**Note:** THP is controlled via `/sys/kernel/mm/transparent_hugepage/` rather than sysctl, but affects virtual memory behavior.

### 6.6. Memory Control for Cgroups (indirect VM management)

While not purely sysctl, cgroup controllers largely replace many coarse tunings:

- `memory.high`
- `memory.max`
- `memory.swap.max`
- `memory.min`

These provide **granular per-service virtual memory constraints**, often more effective than global sysctl tuning.

### 6.7. Common Tuning Profiles by Workload

#### 6.7.1. Database Servers (PostgreSQL, MySQL)

- `vm.swappiness = 1–10`
- `vm.overcommit_memory = 2`
- `vm.overcommit_ratio = 100–150`
- Prefer `dirty_bytes` settings over ratios.

#### 6.7.2. File Servers / Build Servers

- `vm.vfs_cache_pressure = 10–50`
- `vm.swappiness = 30–60`
- Tune dirty_writeback settings for smoother I/O.

#### 6.7.3. High-throughput Application Servers

- `vm.min_free_kbytes` increased
- Moderate `swappiness`
- Consider adjusting watermark_scale_factor.

#### 6.7.4. Low-Latency / Real-Time Systems

- Minimal swapping → `swappiness = 0`
- Reduced dirty ratios
- Increased min_free_kbytes
- Disable THP if causing latency spikes
