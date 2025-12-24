# Virtual Memory vs. Resident Set Size

Source:

- <https://www.golinuxcloud.com/tutorial-linux-memory-management-overview/>
- <https://docs.hpc.qmul.ac.uk/using/memory/>
- <https://nghiant3223.github.io/2025/05/29/fundamental_of_virtual_memory.html>

Memory usage can be broadly simplified into two values:

- **Virtual Memory (VMEM)** which a program believes it has, represents total virtual memory allocated to a process, including shared libraries plus the entire reserved address space, regardless of whether it is currently in physical memory or swapped out.
- **Resident Set Size (RSS)** which is the actual amount of memory it uses, including shared memory but excluding swapped out-pages.

```shell
$ man top
       CODE  --  Code Size (KiB)
           The amount of physical memory currently devoted to executable
           code, also known as the Text Resident Set size or TRS.

       DATA  --  Data + Stack Size (KiB)
           The amount of private memory reserved by a process.  It is
           also known as the Data Resident Set or DRS.  Such memory may
           not yet be mapped to physical memory (RES) but will always be
           included in the virtual memory (VIRT) amount.

       RES  --  Resident Memory Size (KiB)
           A subset of the virtual address space (VIRT) representing the
           non-swapped physical memory a task is currently using.  It is
           also the sum of the ‘RSan’, ‘RSfd’ and ‘RSsh’ fields.

           It can include private anonymous pages, private pages mapped
           to files (including program images and shared libraries) plus
           shared anonymous pages.  All such memory is backed by the swap
           file represented separately under SWAP.

           Lastly, this field may also include shared file-backed pages
           which, when modified, act as a dedicated swap file and thus
           will never impact SWAP.

       RSS  --  Resident Memory, smaps (KiB)
           Another, more precise view of process non-swapped physical
           memory.  It is obtained from the ‘smaps_rollup’ file and is
           generally slightly larger than that shown for ‘RES’.

           Accessing smaps values is 10x more costly than other memory
           statistics and data for other users requires root privileges.

      VIRT  --  Virtual Memory Size (KiB)
           The total amount of virtual memory used by the task.  It
           includes all code, data and shared libraries plus pages that
           have been swapped out and pages that have been mapped but not
           used.

       SWAP  --  Swapped Size (KiB)
           The formerly resident portion of a task's address space
           written to the swap file when physical memory becomes over
           committed.
```

In order to make better use of physical memory, the operating system doesn't actually give a program the memory it requests until the program uses it. This means multiple applications can request memory and until they actually use it they won't affect the available RAM. Once data is written to the memory it is actually in use and part of the RSS - the size of the memory set that is resident in RAM.

The diagram below shows the memory usage for an example program. VMEM is much larger than the RSS which is in turn slightly larger than the actual RAM usage. Shared libraries (for example glibc make up the rest of the RSS. These common software libraries are only loaded into RAM once and then used by multiple applications. However these libraries are still counted in each applications RSS regardless of the number of applications using them.

![](https://docs.hpc.qmul.ac.uk/img/ram_diagram.png)

Virtual Memory and Resident Set Size can be seen in top as VIRT and RES:

```shell
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 2317 postgres  20   0  280800  41440  40336 S   0.0  0.0   0:13.47 postgres
 6250 dbmrun    20   0   22.4g   4.8g  24208 S   5.6  3.8 167:11.36 java
 3394 postgres  20   0  280908  24680  23512 S   0.0  0.0   0:10.72 postgres
 5350 ne3suser  20   0 7230864 633448  18368 S   0.0  0.5   9:04.33 jsvc
  950 root      20   0   56612  15884  15504 S   0.0  0.0   0:33.89 systemd-journal
 2462 ssrun     20   0 7386468 570392  14964 S   0.3  0.4   7:34.72 jsvc
 2421 ne3suser  20   0 9786720 455580  14732 S   0.3  0.3  22:02.68 jsvc
 3559 ssrun     20   0   34.9g   4.0g  14280 S   0.3  3.2  19:22.59 jsvc
```

- We can see in the `VIRT` section that huge amount of memory is allocated to the process such as for java 22.4GB of virtual memory is allocated while only 4.8GB is used
- If you add all of these `VIRT` memory to one another, you are getting far beyond the total of 128GB of physical RAM that is available in this system.
- That is what we call **memory over-allocation**.
- To tune the behavior of over committing memory, you can write to the `/proc/sys/vm/overcommit_memory` parameter. This parameter can have some values.
  - The default value is 0, which means that the kernel checks if it still has memory available before granting it. If that doesn’t give you the performance you need,
  - The value 1, means that the system thinks there is enough memory in all cases. This is good for performance of memory-intensive tasks but may result in processes getting killed automatically.
  - The value of 2, means that the kernel fails the memory request if there is not enough memory available.

This means that when any application or process requests for memory, kernel will always honour that request and "**give**". Please NOTE, that kernel gives certain amount of memory but this memory is not marked as "**used**". Instead this is considered as "**virtual memory**" and only when the application or process tries to write some data into the memory, kernel will mark that section of memory as "**used**".

So if suddenly one or some process would start using more resident memory (RES), the kernel needs to honour that request, and the result is that you can reach a situation where there is no more memory available. That is called OOM (Out Of Memory) situation when your system is running low on memory, and it is getting out of memory. In such case the out of memory killer becomes active, and it will kill the process that least requires to have the memory, and that is kind of a random situation, so you'll get a random process killed if your system is running out of memory.

**Key differences & when to use**

- VIRT >> RES: Very common in Linux. Shows the process has a large address space but only uses a fraction of it, often reserving space for future use.
- VIRT ~ RES: The process is sitting comfortably in physical memory, with little swapped out.
- RES is key: When watching system performance (using tools like `top`), focus on the RES (RSS) value to see real RAM usage, not the large VIRT number.
