# sysctl

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
