# eBPF

Source:

- <https://ebpf.io/what-is-ebpf/>
- <https://docs.cilium.io/en/stable/bpf/>

A big picture.

![](https://ebpf.io/static/overview-a213bbbda01b911f9ab529d969acd225.png)

## 1. Introduction

The best eBPF introduction by [Brendan Gregg](https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html):

- eBPF does to Linux what JavaScript does to HTML. (Sort of). So instead of a static HTML website, JavaScript lets you define mini programs that run on events like mouse clicks, which are run in a safe virtual machine in the browser. And with eBPF, instead of a fixed kernel, you can now write mini programs that run on events like disk I/O, which are run in a safe virtual machine in the kernel. In reality, eBPF is more like the v8 virtual machien that runs JavaScript, rather JavaScript itself. eBPF is part of the Linux kernel.
- Programs in eBPF directly is incedibly hard, the same as coding in v8 bytecode. But no on codes in v8: they code in JavaScript, or foten a framework on top of JavaScript (Angular, React, etc.). It's the same with eBPF. People will use it and code in it via frameworks.

### 1.1. Hook Overview

- eBPF programs are event-driven and are run when the kernel or an application passes a certain hook point.
  - Pre-defined hooks include system calls, function entry/exit, kernel tracepoints, network events, and several others.
  - Can create kernel probe (kprobe) or user probe (uprobe) to attach eBPF programs almost anywhere in kernel or user applications.

![](https://ebpf.io/static/syscall_hook-67a7e1bfcabb2ab7a46b359ae9cee71a.png)

### 1.2. Loader & Verification archiecture

- The desired hook has been identified -> eBPF program can be loaded into the Linux kernel using the bpf system call.

![](https://ebpf.io/static/go-ec58640488770cf5e5b4160ae7c04ae0.png)

- As the program is loaded into the Linux kernel, it passes through 2 steps before being attached to the requested hook:

  ![](https://ebpf.io/static/loader-dff8db7daed55496f43076808c62be8f.png)

  - Verification: validates that the program meets several conditions.
  - Just-In-Time (JIT) Compilation: translates the generic bytecode of the program into the machine specific instruction set to optimize execution speed of the program.

### 1.3. Maps

![](https://ebpf.io/static/map_architecture-6b0f37504ff7d44559b740bab0012d02.png)

![](https://docs.cilium.io/en/stable/_images/bpf_map.png)

- Maps are efficient key/value stores that reside in kernel space. THey can accessed by eBPF program in order to keep state among multiple eBPF program invocations. They can also be accessed through file descriptors from user space and can be arbitrarily shared with other eBPF programs or user space applications.

### 1.4. Helper calls

- eBPF programs can make function calls into helper functions (offered by the kernel).

![](https://ebpf.io/static/helper-84af75c9a5b2c2abf127110cda48b8e2.png)

- Helper functions are a concept which enables eBPF programs to consult a core kernel defined set of function calls in order to retrieve/push data from/to the kernel.
- Available helper functions may differ for each eBPF program type.

### 1.5. Tail & Function calls

- eBPF programs are composable with the concept of tail and function calls:
  - Function calls allow defining and calling functions within eBPF program.
  - Tail calls can call and execute eBPF program and replace the execution context, similar to how the execve() system call operates for regular processes.

![](https://ebpf.io/static/tailcall-a4d7f4b6a449cdee9515c6ff36c89346.png)


### 1.6. JIT

![](https://docs.cilium.io/en/stable/_images/bpf_jit.png)

- Enable JIT:

```shell
echo 1 > /proc/sys/net/core/bpf_jit_enable
```

- JIT compilers speed up execution of the eBPF program significantly since they reduce the per instruction cost compared to the interpreter.

## 2. Development environment

- Setup a development environment for eBPF (for Ubuntu):

```shell
sudo apt-get install -y make gcc libssl-dev bc libelf-dev libcap-dev \
  clang gcc-multilib llvm libncurses5-dev git pkg-config libmnl-dev bison flex \
  graphviz
```
