# /proc

Source:

- <https://web.archive.org/web/20220302031247/https://ops.tips/blog/a-month-of-proc/>
- <https://www.geeksforgeeks.org/proc-file-system-linux/>
- <https://tldp.org/LDP/Linux-Filesystem-Hierarchy/html/proc.html>
- ,https://www.ibm.com/docs/en/ztpf/1.1.0.15?topic=reference-procfs-sysfs-targets>

Table of content:

- [/proc](#proc)
  - [1. What is `/proc`?](#1-what-is-proc)
  - [2. Walk through](#2-walk-through)

## 1. What is `/proc`?

- `procfs` is a special virtual file system that can be mounted in your direectory tree, allowing processes in userspace to read kernel information conveniently - using regular file I/O operations (like `read(2)` and `write(2)`).

```unknown
           process 123: how many files do proc321
                  |          has open?
                  |
(userspace)       *---> ls /proc/321/fd
                         \----+------/
                              |    ^
------------------------------|----|------------
                              |    |
                      .---<---*    |
                      |            |
                     kernel        *-----------<------.
(kernelspace)         |                               |
                      *--> list number of open file   |
                           descriptors for proc `321` |
                           in the root namespace      |
                                 |                    |
                                 *------------>-------'
                                     there you go!

```

- The "virtual" comes from the fact that there's not really a block device (like a SSD), that serves the files that we can access under the place where you mount `procfs` (usually `/proc`).
- Instead, there's just some code implementing the filesystem interface that gets called whenever you issue reads and writes against those praticular locations. For instance, when a user asks for the limits that apply to a given process, the following path gets followed under th hood:

```unknown
        cat /proc/13323/limits


(userspace)     fd = open("/proc/13323/limits")
                n = read(fd, buf, bufsize)
                     |
---------------------|--------------
                    vfs (common interface for interacting with
                     |   any filesystem)
                     |
                     *-> who's responsible for this `/proc`
                         mount?
                         procfs! let it handle the call.
                          |
                          |
(kernelspace)             *-> hey procfs, take this `read` call
                              for `/proc/13323/limits` please!
                                 |
                   sure! <-------*
                   I'll write the response
                   to the file.
                     |
                     *---> linux/fs/proc/base.c#proc_pid_limits
                           for limit := range limits {
                                fprintf(file, limit)
```

- In fact, quite a lot of system utilities are simply call to files in `/proc`. For example, `lsmod` is the same as `cat /proc/modules` while `lspci` is a synonym for `cat /proc/pci`. By altering files located in this directory you can even read/change kernel parameters (sysctl) while the system is running.
- The most distinctive thing about files in this directory is the fact that all of them have a file size of 0, with the exception of kcore, mtrr and self. A directory listing looks similar to the following:

```shell
$ ls -la /proc


total 525256
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 1
dr-xr-xr-x    3 daemon   root            0 Jan 19 15:00 109
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 170
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 173
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 178
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 2
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 3
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 4
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 421
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 425
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 433
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 439
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 444
dr-xr-xr-x    3 daemon   daemon          0 Jan 19 15:00 446
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 449
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 453
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 456
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 458
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 462
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 463
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 464
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 465
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 466
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 467
dr-xr-xr-x    3 gdm      gdm             0 Jan 19 15:00 472
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 483
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 5
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 6
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 7
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 8
-r--r--r--    1 root     root            0 Jan 19 15:00 apm
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 bus
-r--r--r--    1 root     root            0 Jan 19 15:00 cmdline
-r--r--r--    1 root     root            0 Jan 19 15:00 cpuinfo
-r--r--r--    1 root     root            0 Jan 19 15:00 devices
-r--r--r--    1 root     root            0 Jan 19 15:00 dma
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 driver
-r--r--r--    1 root     root            0 Jan 19 15:00 execdomains
-r--r--r--    1 root     root            0 Jan 19 15:00 fb
-r--r--r--    1 root     root            0 Jan 19 15:00 filesystems
dr-xr-xr-x    2 root     root            0 Jan 19 15:00 fs
dr-xr-xr-x    4 root     root            0 Jan 19 15:00 ide
-r--r--r--    1 root     root            0 Jan 19 15:00 interrupts
-r--r--r--    1 root     root            0 Jan 19 15:00 iomem
-r--r--r--    1 root     root            0 Jan 19 15:00 ioports
dr-xr-xr-x   18 root     root            0 Jan 19 15:00 irq
-r--------    1 root     root     536809472 Jan 19 15:00 kcore
-r--------    1 root     root            0 Jan 19 14:58 kmsg
-r--r--r--    1 root     root            0 Jan 19 15:00 ksyms
-r--r--r--    1 root     root            0 Jan 19 15:00 loadavg
-r--r--r--    1 root     root            0 Jan 19 15:00 locks
-r--r--r--    1 root     root            0 Jan 19 15:00 mdstat
-r--r--r--    1 root     root            0 Jan 19 15:00 meminfo
-r--r--r--    1 root     root            0 Jan 19 15:00 misc
-r--r--r--    1 root     root            0 Jan 19 15:00 modules
-r--r--r--    1 root     root            0 Jan 19 15:00 mounts
-rw-r--r--    1 root     root          137 Jan 19 14:59 mtrr
dr-xr-xr-x    3 root     root            0 Jan 19 15:00 net
dr-xr-xr-x    2 root     root            0 Jan 19 15:00 nv
-r--r--r--    1 root     root            0 Jan 19 15:00 partitions
-r--r--r--    1 root     root            0 Jan 19 15:00 pci
dr-xr-xr-x    4 root     root            0 Jan 19 15:00 scsi
lrwxrwxrwx    1 root     root           64 Jan 19 14:58 self -> 483
-rw-r--r--    1 root     root            0 Jan 19 15:00 slabinfo
-r--r--r--    1 root     root            0 Jan 19 15:00 stat
-r--r--r--    1 root     root            0 Jan 19 15:00 swaps
dr-xr-xr-x   10 root     root            0 Jan 19 15:00 sys
dr-xr-xr-x    2 root     root            0 Jan 19 15:00 sysvipc
dr-xr-xr-x    4 root     root            0 Jan 19 15:00 tty
-r--r--r--    1 root     root            0 Jan 19 15:00 uptime
-r--r--r--    1 root     root            0 Jan 19 15:00 version
```

- Each of the numbered directories corresponds to an actual process ID. Looking at the process table, you can match processes with the associated process ID. For example, the process table might indicate the following for the secure shell server:

```shell
$ ps ax | grep sshd
439 ? S 0:00 /usr/sbin/sshd
```

## 2. Walk through

- `/proc` includes a directory for each running process, including kernel processes, in directories named `/proc/PID`. But we will check some other files first:

| file              | Description                                                                                                                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /proc/crypto      | List of available cryptographic modules                                                                                                                                                             |
| /proc/diskstats   | Information (including device numbers) for each of the logical disk devices                                                                                                                         |
| /proc/filesystems | List of the file systems supported by the kernel at the time of listing                                                                                                                             |
| /proc/kmsg        | Holding messages output by the kernel                                                                                                                                                               |
| /proc/meminfo     | Summery of how the kernel is managing its memory                                                                                                                                                    |
| /proc/scsi        | Information about any devices connected via a SCSI or RAID controller                                                                                                                               |
| /proc/tty         | Information about the current terminals                                                                                                                                                             |
| /proc/version     | Containing the Linux kernel version, distribution number, gcc version number (used to build the kernel) and any other pertinent information relating to the version of the kernel currently running |

- `/proc/PID` directories:

| directory         | description                                     |
| ----------------- | ----------------------------------------------- |
| /proc/PID/cmdline | Command line arguments.                         |
| /proc/PID/cpu     | Current and last cpu in which it was executed.  |
| /proc/PID/cwd     | Link to the current working directory.          |
| /proc/PID/environ | Values of environment variables.                |
| /proc/PID/exe     | Link to the executable of this process.         |
| /proc/PID/fd      | Directory, which contains all file descriptors. |
| /proc/PID/maps    | Memory maps to executables and library files.   |
| /proc/PID/mem     | Memory held by this process.                    |
| /proc/PID/root    | Link to the root directory of this process.     |
| /proc/PID/stat    | Process status.                                 |
| /proc/PID/statm   | Process memory status information.              |
| /proc/PID/status  | Process status in human readable form.          |
