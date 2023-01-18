# Linux vs. Unix

- [Linux vs. Unix](#linux-vs-unix)
  - [1. What is UNIX?](#1-what-is-unix)
  - [2. What is Linux?](#2-what-is-linux)
  - [3. Linux vs.Unix kernel](#3-linux-vsunix-kernel)

<https://www.softwaretestinghelp.com/unix-vs-linux/>

People do confuse a lot between the terms Unix and Linux. Linux and Unix are different but they do have a relationship with each other as Linux is derived from Unix.

## 1. What is UNIX?

- The design of Unix systems is based on "Unix philosophy" which includes the following characteristics:

  - Usage of plain text for data storage.
  - Hierarchical file system.
  - Handling devices and some specific kinds of inter-process communication (IPC) as files.
  - Employing a huge number of software tools.
  - Multiple small, simple and modular programs which can be threaded together via a command-line interpreter using pipes.

- Unix is a complete OS as everything (all required application tied together) comes from a single vendor.

![](https://cdn.softwaretestinghelp.com/wp-content/qa/uploads/2019/02/Capture-1.jpg)

- The master control program of Unix is its `kernel`, full control over the entire system.
- In the outer layers of the architecture, we have the shell, commands, and application programs. Shell is the interface between the user and the kernel.

## 2. What is Linux?

- Linux is not Unix, but it is a Unix-like operating system (\*nix).
- [According to Linux kernel README](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/README.rst#what-is-linux), Linux is a clone of the OS Unix system, written from scratch by Linus Torvalds.
- Linux is just the kernel and not the complete OS. Linux distribution is an OS that is created from a collection of software built upon the Linux kernel.

![](https://cdn.softwaretestinghelp.com/wp-content/qa/uploads/2019/02/Screen-Shot-2018-01-04-at-10.44.39-AM.png)

## 3. Linux vs.Unix kernel

- As Linux alone is just a kernel, it is worth discussing the major differences between the Linux kernal and Unix kernel.
- Kernel type:
  - Linux: monolithic
  - Unix: can be monolithic, microkernel and hybrid.

![](https://cdn.softwaretestinghelp.com/wp-content/qa/uploads/2019/02/1920px-OS-structure2.svg.png)

- Khong-hieu-lam :(
