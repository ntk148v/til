# High System Load with Low CPU Utilization on Linux?

Source:

- <https://tanelpoder.com/posts/high-system-load-low-cpu-utilization-on-linux/>
- <https://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html>

Table of contents:

- [High System Load with Low CPU Utilization on Linux?](#high-system-load-with-low-cpu-utilization-on-linux)
  - [1. Introduction - Terminology](#1-introduction---terminology)
  - [2. Troubleshooting high system load on Linux](#2-troubleshooting-high-system-load-on-linux)
  - [3. Drilling down deeper - WCHAN](#3-drilling-down-deeper---wchan)
  - [4. Drilling down deeper - kernel stack](#4-drilling-down-deeper---kernel-stack)

## 1. Introduction - Terminology

- The _system load_ metric aims to represent the system "resource demand" as just a single number. On classic Unixes, it only counts the demand for CPU (threads in Runnable state).
- The _unit_ of system load metric is "number of processes/threads" (or _tasks_ as the scheduling unit is called on Linux). The load average is an average number of threads over a time period (last 1, 5, 15 mins) that _"compete for CPU"_ on classic unixes or _"either compete for CPU or wait in an uninterruptible sleep state"_ on Linux.
- **Runnable** state means "not blocked by anything", ready to run on CPU. The thread is either currently running on CPU or waiting in the CPU runqueue for the OS scheduler to put it onto CPU.
- On Linux, the system load includes threads both in Runnable (R) and in Uninterruptible sleep (D) states (typically disk I/O, but not always).

So, on Linux, an absurdly high load figure can be caused by having lots of threads in Uninterruptible sleep (D) state, in addition to CPU demand.

## 2. Troubleshooting high system load on Linux

![](https://tanelpoder.com/files/images/linux-load.png)

_The system load, incorrectly labeled as "runnable processes" by the above monitoring tool, jumped to over 3000!_

Let's confirm this with standard OS level commands:

```shell
[tanel@linux01 ~]$ w
 11:49:29 up 13 days, 13:55,  2 users,  load average: 3446.04, 1242.09, 450.47
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
tanel    pts/0    192.168.0.159    Thu14   21:09m  0.05s  0.05s -bash
tanel    pts/1    192.168.0.159    11:46    1.00s  0.36s  0.23s w
```

Does this mean that we have a huge demand for CPU time? Must have losts of theads in the CPU runqueue, right?

```shell
[tanel@linux01 ~]$ sar -u 5
11:58:51 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
11:58:56 AM     all     36.64      0.00      4.42     17.17      0.00     41.77
11:59:01 AM     all     41.04      0.00      3.72     26.67      0.00     28.57
11:59:06 AM     all     35.38      0.00      2.95     28.39      0.00     33.27
```

But the CPUs are well over 50% idle! CPU utilization is around 40-45% when adding %user, %nice and %system together. %iowait means that the CPU is idle, it just happens to have a synchronous I/O submitted by a thread on it before becoming idle.

So, we don’t seem to have a CPU oversubscription scenario in this case. Is there a way to systematically drill down deeper by measuring what (and who) is contributing to this load then?

Yes, and it’s super simple. Remember, the current system load is just the number of threads (called tasks) on Linux that are either in R or D state. We can just run ps to list the current number of threads in these states:

```shell
# ps -eo s,user will list the thread state field first and any other fields of interest (like username), later. The grep ^[RD] filters out any threads in various “idle” and “sleeping” states that don’t contribute to Linux load (S,T,t,Z,I etc).
[tanel@linux01 ~]$ ps -eo s,user | grep ^[RD] | sort | uniq -c | sort -nbr | head -20
   3045 D root
     20 R oracle
      3 R root
      1 R tanel
```

Is there some daemon that has gone crazy and has all these active processes/threads trying to do IO?

Let’s add one more column to ps to list the command line/program name too:

```shell
[tanel@linux01 ~]$ ps -eo s,user,cmd | grep ^[RD] | sort | uniq -c | sort -nbr | head -20
     15 R oracle   oracleLIN19C (LOCAL=NO)
      3 D oracle   oracleLIN19C (LOCAL=NO)
      1 R tanel    ps -eo s,user,cmd
      1 R root     xcapture -o /backup/tanel/0xtools/xcaplog -c exe,cmdline,kstack
      1 D root     [kworker/6:99]
      1 D root     [kworker/6:98]
      1 D root     [kworker/6:97]
      1 D root     [kworker/6:96]
      1 D root     [kworker/6:95]
      1 D root     [kworker/6:94]
      1 D root     [kworker/6:93]
      1 D root     [kworker/6:92]
      1 D root     [kworker/6:91]
      1 D root     [kworker/6:90]
      1 D root     [kworker/6:9]
      1 D root     [kworker/6:89]
      1 D root     [kworker/6:88]
      1 D root     [kworker/6:87]
      1 D root     [kworker/6:86]
      1 D root     [kworker/6:85]
```

Use [Linux Process Snapper](https://tanelpoder.com/psnapper/):

```shell
[tanel@linux01 ~]$ psn

Linux Process Snapper v0.18 by Tanel Poder [https://0x.tools]
Sampling /proc/stat for 5 seconds... finished.


=== Active Threads ================================================

 samples | avg_threads | comm             | state
-------------------------------------------------------------------
   10628 |     3542.67 | (kworker/*:*)    | Disk (Uninterruptible)
      37 |       12.33 | (oracle_*_l)     | Running (ON CPU)
      17 |        5.67 | (oracle_*_l)     | Disk (Uninterruptible)
       2 |        0.67 | (xcapture)       | Running (ON CPU)
       1 |        0.33 | (ora_lg*_xe)     | Disk (Uninterruptible)
       1 |        0.33 | (ora_lgwr_lin*)  | Disk (Uninterruptible)
       1 |        0.33 | (ora_lgwr_lin*c) | Disk (Uninterruptible)


samples: 3 (expected: 100)
total processes: 10470, threads: 11530
runtime: 6.13, measure time: 6.03
```

By default, pSnapper replaces any digits in the task’s comm field before aggregating (the comm2 field would leave them intact). Now it’s easy to see that our extreme system load spike was caused by a large number of kworker kernel threads (with “root” as process owner). So this is not about some userland daemon running under root, but a kernel problem.

## 3. Drilling down deeper - WCHAN

System load is in hundreds this time:

```shell
[tanel@linux01 ~]$ w
 13:47:03 up 7 days, 15:53,  3 users,  load average: 496.62, 698.40, 440.26
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
tanel    pts/0    192.168.0.159    13:36    7:03   0.06s  0.06s -bash
tanel    pts/1    192.168.0.159    13:41    7.00s  0.32s  0.23s w
tanel    pts/2    192.168.0.159    13:42    3:03   0.23s  0.02s sshd: tanel [pri
```

```shell
[tanel@linux01 ~]$ sudo psn -G syscall,wchan

Linux Process Snapper v0.18 by Tanel Poder [https://0x.tools]
Sampling /proc/syscall, stat, wchan for 5 seconds... finished.


=== Active Threads ==========================================================================================

 samples | avg_threads | comm             | state                  | syscall         | wchan
-------------------------------------------------------------------------------------------------------------
     511 |      255.50 | (kworker/*:*)    | Disk (Uninterruptible) | [kernel_thread] | blkdev_issue_flush
     506 |      253.00 | (oracle_*_l)     | Disk (Uninterruptible) | pread64         | do_blockdev_direct_IO
      28 |       14.00 | (oracle_*_l)     | Running (ON CPU)       | [running]       | 0
       1 |        0.50 | (collectl)       | Running (ON CPU)       | [running]       | 0
       1 |        0.50 | (mysqld)         | Running (ON CPU)       | [running]       | 0
       1 |        0.50 | (ora_lgwr_lin*c) | Disk (Uninterruptible) | io_submit       | inode_dio_wait
       1 |        0.50 | (oracle_*_l)     | Disk (Uninterruptible) | pread64         | 0
       1 |        0.50 | (oracle_*_l)     | Running (ON CPU)       | [running]       | SYSC_semtimedop
       1 |        0.50 | (oracle_*_l)     | Running (ON CPU)       | [running]       | read_events
       1 |        0.50 | (oracle_*_l)     | Running (ON CPU)       | read            | 0
       1 |        0.50 | (oracle_*_l)     | Running (ON CPU)       | semtimedop      | SYSC_sem
```

In the above breakdown of current system load, close to half of activity was caused by kernel `kworker` threads that were currently sleeping in `blkdev_issue_flush` kernel function responsible for an internal fsync to ensure that the writes get persisted to storage. The remaining "close to half" active threads were by oracle processes, waiting in a synchronous pread64 system call, in `do_blockdev_direct_IO` kernel function.

From the "Running (ON CPU)" lines you see that there was some CPU usage too, but doesn’t seem to be anywhere near to the hundreds of threads in I/O sleeps.

While doing these tests, I ran an Oracle benchmark with 1000 concurrent connections (that were sometimes idle), so the 253 sessions waiting in the synchronous `pread64` system calls can be easily explained. Synchronous single block reads are done for index tree walking & index-based table block access, for example. But why do we see so many kworker kernel threads waiting for I/O too?

The answer is asynchronous I/O and I/Os done against higher level block devices (like the device-mapper `dm` devices for LVM and `md` devices for software RAID). With asynchronous I/O, the thread completing an I/O request in kernel memory structures is different from the (application) thread submitting the I/O. That’s where the kernel kworker threads come in and the story gets more complex with LVMs/dm/md devices (as there are multiple layers of I/O queues on the request path).

You don’t have to guess where the bottleneck resides, just dig deeper using what pSnapper offers. One typical question is that which file(s) or devices are we waiting for the most? Let’s add `filename` (or filenamesum that consolidates filenames with digits in them into one) into the breakdown:

```shell
[tanel@linux01 ~]$ sudo psn -G syscall,filenamesum

Linux Process Snapper v0.18 by Tanel Poder [https://0x.tools]
Sampling /proc/syscall, stat for 5 seconds... finished.


=== Active Threads =======================================================================================================

 samples | avg_threads | comm            | state                  | syscall         | filenamesum
--------------------------------------------------------------------------------------------------------------------------
    2027 |      506.75 | (kworker/*:*)   | Disk (Uninterruptible) | [kernel_thread] |
    1963 |      490.75 | (oracle_*_l)    | Disk (Uninterruptible) | pread64         | /data/oracle/LIN*C/soe_bigfile.dbf
      87 |       21.75 | (oracle_*_l)    | Running (ON CPU)       | [running]       |
      13 |        3.25 | (kworker/*:*)   | Running (ON CPU)       | [running]       |
       4 |        1.00 | (oracle_*_l)    | Running (ON CPU)       | read            | socket:[*]
       2 |        0.50 | (collectl)      | Running (ON CPU)       | [running]       |
       1 |        0.25 | (java)          | Running (ON CPU)       | futex           |
       1 |        0.25 | (ora_ckpt_xe)   | Disk (Uninterruptible) | pread64         | /data/oracle/XE/control*.ctl
       1 |        0.25 | (ora_m*_linprd) | Running (ON CPU)       | [running]       |
       1 |        0.25 | (ora_m*_lintes) | Running (ON CPU)       | [running]       |
```

## 4. Drilling down deeper - kernel stack

Let’s dig even deeper. You’ll need to scroll right to see the full picture, I’ve highlighted some things in all the way to the right. We can sample the kernel stack of a thread too (kernel threads and also userspace application threads, when they happen to be executing kernel code):

```shell
[tanel@linux01 ~]$ sudo psn -p -G syscall,wchan,kstack

Linux Process Snapper v0.18 by Tanel Poder [https://0x.tools]
Sampling /proc/wchan, stack, syscall, stat for 5 seconds... finished.


=== Active Threads =======================================================================================================================================================================================================================================================================================================================================================================================

 samples | avg_threads | comm          | state                  | syscall         | wchan                        | kstack
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     281 |      140.50 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | blkdev_issue_flush           | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->generic_write_sync()->xfs_file_fsync()->xfs_blkdev_issue_flush()->blkdev_issue_flush()
     211 |      105.50 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | call_rwsem_down_read_failed  | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->generic_write_sync()->xfs_file_fsync()->xfs_ilock()->call_rwsem_down_read_failed()
     169 |       84.50 | (oracle_*_li) | Disk (Uninterruptible) | pread64         | call_rwsem_down_write_failed | system_call_fastpath()->SyS_pread64()->vfs_read()->do_sync_read()->xfs_file_aio_read()->xfs_file_dio_aio_read()->touch_atime()->update_time()->xfs_vn_update_time()->xfs_ilock()->call_rwsem_down_write_failed()
      64 |       32.00 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | xfs_log_force_lsn            | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->generic_write_sync()->xfs_file_fsync()->xfs_log_force_lsn()
      24 |       12.00 | (oracle_*_li) | Disk (Uninterruptible) | pread64         | call_rwsem_down_read_failed  | system_call_fastpath()->SyS_pread64()->vfs_read()->do_sync_read()->xfs_file_aio_read()->xfs_file_dio_aio_read()->__blockdev_direct_IO()->do_blockdev_direct_IO()->xfs_get_blocks_direct()->__xfs_get_blocks()->xfs_ilock_data_map_shared()->xfs_ilock()->call_rwsem_down_read_failed()
       5 |        2.50 | (oracle_*_li) | Disk (Uninterruptible) | pread64         | do_blockdev_direct_IO        | system_call_fastpath()->SyS_pread64()->vfs_read()->do_sync_read()->xfs_file_aio_read()->xfs_file_dio_aio_read()->__blockdev_direct_IO()->do_blockdev_direct_IO()
       3 |        1.50 | (oracle_*_li) | Running (ON CPU)       | [running]       | 0                            | system_call_fastpath()->SyS_pread64()->vfs_read()->do_sync_read()->xfs_file_aio_read()->xfs_file_dio_aio_read()->__blockdev_direct_IO()->do_blockdev_direct_IO()
       2 |        1.00 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | call_rwsem_down_write_failed | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->xfs_end_io_direct_write()->xfs_iomap_write_unwritten()->xfs_ilock()->call_rwsem_down_write_failed()
       2 |        1.00 | (kworker/*:*) | Running (ON CPU)       | [running]       | 0                            | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->generic_write_sync()->xfs_file_fsync()->xfs_blkdev_issue_flush()->blkdev_issue_flush()
       2 |        1.00 | (oracle_*_li) | Disk (Uninterruptible) | io_submit       | call_rwsem_down_write_failed | system_call_fastpath()->SyS_io_submit()->do_io_submit()->xfs_file_aio_read()->xfs_file_dio_aio_read()->touch_atime()->update_time()->xfs_vn_update_time()->xfs_ilock()->call_rwsem_down_write_failed()
       1 |        0.50 | (java)        | Running (ON CPU)       | futex           | futex_wait_queue_me          | system_call_fastpath()->SyS_futex()->do_futex()->futex_wait()->futex_wait_queue_me()
       1 |        0.50 | (ksoftirqd/*) | Running (ON CPU)       | [running]       | 0                            | ret_from_fork_nospec_begin()->kthread()->smpboot_thread_fn()
       1 |        0.50 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | worker_thread                | ret_from_fork_nospec_begin()->kthread()->worker_thread()
       1 |        0.50 | (kworker/*:*) | Disk (Uninterruptible) | [kernel_thread] | worker_thread                | ret_from_fork_nospec_begin()->kthread()->worker_thread()->process_one_work()->dio_aio_complete_work()->dio_complete()->generic_write_sync()->xfs_file_fsync()->xfs_blkdev_issue_flush()->blkdev_issue_flush()
       1 |        0.50 | (ora_lg*_xe)  | Disk (Uninterruptible) | io_submit       | inode_dio_wait               | system_call_fastpath()->SyS_io_submit()->do_io_submit()->xfs_file_aio_write()->xfs_file_dio_aio_write()->inode_dio_wait()
       1 |        0.50 | (oracle_*_li) | Disk (Uninterruptible) | [running]       | 0                            | -
```

Looks like a different hiccup has happened in my benchmark system now, additional WCHAN (kernel sleep location) values have popped up in the report: `call_rwsem_down_*_failed` by both Oracle and kworker threads and `xfs_log_force_lsn` waits by 32 kworker threads. `rwsem` stands for “reader-writer semaphore” that is essentially a low level lock. So, a large part of our system load (D state waits) are caused by some sort of locking in the kernel now and not by waiting for hardware I/O completion.

If you scroll all the way right and follow the kernel function call chain, it becomes (somewhat) evident that we are waiting for XFS inode locks when accessing (both reading and writing) files. Additionally, when searching what the `xfs_log_force_lsn` function does, you’d see that this is an XFS journal write that persists XFS metadata updates to disk so that you wouldn’t end up with a broken filesystem in case of a crash. XFS delayed logging must be ordered and checkpoints atomic, so there may be cases where one XFS-related kworker on one CPU will block other kworkers (that have assumed the same role) on remaining CPUs. For example, if the XFS log/checkpoint write is too slow for some reason. It’s probably not a coincidence that pSnapper shows exactly 32 threads waiting in `xfs_log_force_lsn` function on my 32 CPU system.
