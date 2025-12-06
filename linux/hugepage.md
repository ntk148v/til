# HugePages

## 1. Standard page size: 4 KB on most x86_64 systems.

HugePage sizes: Typically 2 MB (HugePages) or 1 GB (Gigantic Pages), depending on architecture and kernel configuration.

HugePages are a Linux kernel feature that allows the OS to use memory pages significantly larger than the default 4KB page size. They are primarily used to improve performance for memory-intensive workloads.

- Standard page size: 4 KB on most x86_64 systems.
- HugePage sizes: Typically 2 MB (HugePages) or 1 GB (Gigantic Pages), depending on architecture and kernel configuration.

## 2. Why they improve performance?

- Reduced TLB pressure: CPUs use a Translation Lookaside Buffer (TLB) to translate virtual to physical memory. Larger pages mean fewer total pages, which reduces TLB misses and improves throughput.
- Lower kernel overhead: Managing millions of 4 KB pages is more expensive than managing thousands of 2 MB pages.
- Improved performance for large in-memory datasets: Databases (Oracle, PostgreSQL, MySQL), JVM applications, and high-performance computing workloads benefit from more stable memory mappings.

## 3. Two types of HugePages

1. Static (Pre-allocated) HugePages

- Reserved at boot or runtime.
- Guaranteed availability for processes that need them.
- Cannot be used for normal memory once reserved.

2. Transparent Huge Pages (THP)

- Kernel automatically promotes memory regions into huge pages.
- Easier to use but can introduce latency spikes due to page compaction.
- Often disabled for latency-sensitive applications (e.g., databases).

## 4. Check HugePages status

```shell
cat /proc/meminfo | grep -i huge
# Configure
sudo sysctl -w vm.nr_hugepages=1024
# Enable/disable Transparent HugePages
cat /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
```

## 5. Use and not to use

**Use cases**

- Database servers: Oracle, PostgreSQL, MySQL, DB2
- JVM-based systems: large heap sizes
- High-performance computing: scientific simulations, ML workloads
- Virtualization: KVM, QEMU

**When not to use HugePages**

- Small memory footprint applications
- Systems with highly fragmented memory
- Latency-sensitive environments using THP (static HugePages may still be appropriate)
