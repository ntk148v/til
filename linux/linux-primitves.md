# Linux Primitives

> **Disclaim**: I took the bellow lines while read [Limit Primitives slide](https://docs.google.com/presentation/d/10vFQfEUvpf7qYyksNqiy-bAxcy-bvF0OnUElCOtTTRc/edit#slide=id.g1012f66722_0_8). Be honest, I didn't understand all of these, it's too much for me :disappointed_relieved: :cold_sweat: :scream: Shame on me! Anw, I still push the note here and will dive in deep later.

## Linux is actually GNU user space

Apps <--> GNU libc and other userspace libraries

* Libraries provide many basic mechanisms
* Provides POSIX API, ISO C API, BSD/Unix compat
* There is more than one libc implementation
* We can package our own libc in a container or binary
* Container isolation works in the kernel level

** ## Linux container?

* No, there is no `Linux container` primitive in the kernel
* A `container` is a group of processes assoociated with common namespaces/cgroups/root...

## Processes

### Data Structures

* Both thread and processes are *tasks*.
  * task struct - has fields - notable fields: \*user, pid, tgid, \*files, \*fs, \*nsproxy
  * fs struct holds information on current root
  * pid struct maps processes to one or more tasks

### Fork & Exec

* \*nixs creted new processes using:
  * *fork()* - Duplicate the current **process**. glibc's fork() and pthread\_create() both call clone() syscall. *clone()* create a new task struct from parent.
  * *exec()* - Replace text/data/bss/stack with new program

## Users

* A process has several uid fields: uid, ruid, euid, fsuid
* No need to "add" users
* *useradd* manipulates /etc/passwd, /etc/shadow which are accessed by userspace tools
* User names are a userspace feature

## Capabilities

* Unix is a monotheisitc OS (traditional)
* Many things require root privileges.
* To avoid over-privileged processes, root power has been split to varous CAPABILITIES
* Capabilities are associated with files and processes using extended attributes

```
# Capabilities assoociated with an executable
$ getcap /usr/bin/traceroute6.iputils

/usr/bin/traceroute6.iputils = cap_net_raw+ep
```

## Mounts

Map a file system to a directory

* The Virtual File System provides a file system interface to userspace
* A mount maps some inode in the VFS tree to a file system
* bind mounts map inode in VFS to another inode.
* Mounts can be:
  * shared - all replicas are the same
  * slave - only receives mount/umount events
  * private - doesn't forward or receive propagations
  * unbindable - private + unbindable

## chroot(new\_root)

* Change the root directory for a process

![chroot](https://www.aquicklookat.com/wp-content/uploads/2015/01/clip_image002_0000.jpg)

## pivot\_root(new\_root, put\_old)

* Change the root directory for **all processes in current mnt namespace**.

## cgroups

* CGroups control account and limit system resources
* Filesystem based API (/sys/fs/cgroup mount)
* Hierarchy
* Accounting and resource limits - CPU, memory, blkio, network
* Control - device whitelist, freezer

## Namespace

* Consistent world view - needed for Checkpoint/Restore, Process migration
* Isolation, access control
* APIs:
  * clone: create a new process in a new namespace
  * unshare: create a new namespace for current process
  * setns: set process namespace from existing ns fd
  * /proc/<pid>/ns: fd to process namespace
