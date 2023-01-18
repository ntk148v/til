# eBPF

Source:

- <https://ebpf.io/what-is-ebpf/>
- <https://docs.cilium.io/en/stable/bpf/>
- <https://www.containiq.com/post/ebpf>

- [eBPF](#ebpf)
  - [1. Introduction](#1-introduction)
  - [2. How it works \& Concepts](#2-how-it-works--concepts)
    - [2.1. Hook Overview](#21-hook-overview)
    - [2.2. Loader \& Verification archiecture](#22-loader--verification-archiecture)
    - [2.3. Maps](#23-maps)
    - [2.4. Helper calls](#24-helper-calls)
    - [2.5. Tail \& Function calls](#25-tail--function-calls)
    - [2.6. JIT](#26-jit)
  - [3. Thoughs about eBPF](#3-thoughs-about-ebpf)
  - [4. Hello World!](#4-hello-world)
    - [4.1. Hello World with BCC!](#41-hello-world-with-bcc)

A big picture.

![](https://ebpf.io/static/overview-a213bbbda01b911f9ab529d969acd225.png)

## 1. Introduction

The best eBPF introduction by [Brendan Gregg](https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html):

- eBPF does to Linux what JavaScript does to HTML. (Sort of). So instead of a static HTML website, JavaScript lets you define mini programs that run on events like mouse clicks, which are run in a safe virtual machine in the browser. And with eBPF, instead of a fixed kernel, you can now write mini programs that run on events like disk I/O, which are run in a safe virtual machine in the kernel. In reality, eBPF is more like the v8 virtual machien that runs JavaScript, rather JavaScript itself. eBPF is part of the Linux kernel.
- Programs in eBPF directly is incedibly hard, the same as coding in v8 bytecode. But no on codes in v8: they code in JavaScript, or foten a framework on top of JavaScript (Angular, React, etc.). It's the same with eBPF. People will use it and code in it via frameworks.

## 2. How it works & Concepts

eBPF programs are event-driven, which means they can be hooked to certain events and will be run by the kernel when that particular event occurs. The program can store information in maps, print to ring buffers, or call a subset of kernel functions defined by a special API. The map and ring buffer structures are managed by the kernel, and the same map can be accessed by multiple eBPF programs in order to share data.

eBPF programs follow these steps:

- The bytecode of the eBPF program is sent to kernel along with a program type that determines where the program needs to be attached, which in-kernel helper fucntions the verifier will allow to be called, whether network packet data can be accessed direclty, and what type of object will pass as the first argument to the program.
- The kernel runs a verifier on the bytecode. The verifier runs serveral security checks on the bytecode, which make sure that the program terminates and does not contain any loop that could potentially lock up the kernel. It aslo simulates the execution of the eBPF program and checks the state of the virtual machine at every step to ensure the register and stack states are valid. Finally, it uses the program type to restrict the allowed kernel function calls from the program.
- The bytecode is JIT-compiled into native code and attached to the specified location.
- When the specified event occurs, the program is executed and writes data to the ring buffer or the map.
- The map or ring buffer can be read by the user space to get the program result.

![](https://assets-global.website-files.com/5fbfbba70f3f813561ef7b9f/623371d2777dda3c246c43f0_eBPF.png)

### 2.1. Hook Overview

- eBPF programs are event-driven and are run when the kernel or an application passes a certain hook point.
  - Pre-defined hooks include system calls, function entry/exit, kernel tracepoints, network events, and several others.
  - Can create kernel probe (kprobe) or user probe (uprobe) to attach eBPF programs almost anywhere in kernel or user applications.

![](https://ebpf.io/static/syscall_hook-67a7e1bfcabb2ab7a46b359ae9cee71a.png)

### 2.2. Loader & Verification archiecture

- The desired hook has been identified -> eBPF program can be loaded into the Linux kernel using the bpf system call.

![](https://ebpf.io/static/go-ec58640488770cf5e5b4160ae7c04ae0.png)

- As the program is loaded into the Linux kernel, it passes through 2 steps before being attached to the requested hook:

  ![](https://ebpf.io/static/loader-dff8db7daed55496f43076808c62be8f.png)

  - Verification: validates that the program meets several conditions.
  - Just-In-Time (JIT) Compilation: translates the generic bytecode of the program into the machine specific instruction set to optimize execution speed of the program.

### 2.3. Maps

![](https://ebpf.io/static/map_architecture-6b0f37504ff7d44559b740bab0012d02.png)

![](https://docs.cilium.io/en/stable/_images/bpf_map.png)

- Maps are efficient key/value stores that reside in kernel space. THey can accessed by eBPF program in order to keep state among multiple eBPF program invocations. They can also be accessed through file descriptors from user space and can be arbitrarily shared with other eBPF programs or user space applications.

### 2.4. Helper calls

- eBPF programs can make function calls into helper functions (offered by the kernel).

![](https://ebpf.io/static/helper-84af75c9a5b2c2abf127110cda48b8e2.png)

- Helper functions are a concept which enables eBPF programs to consult a core kernel defined set of function calls in order to retrieve/push data from/to the kernel.
- Available helper functions may differ for each eBPF program type.

### 2.5. Tail & Function calls

- eBPF programs are composable with the concept of tail and function calls:
  - Function calls allow defining and calling functions within eBPF program.
  - Tail calls can call and execute eBPF program and replace the execution context, similar to how the execve() system call operates for regular processes.

![](https://ebpf.io/static/tailcall-a4d7f4b6a449cdee9515c6ff36c89346.png)

### 2.6. JIT

![](https://docs.cilium.io/en/stable/_images/bpf_jit.png)

- Enable JIT:

```shell
echo 1 > /proc/sys/net/core/bpf_jit_enable
```

- JIT compilers speed up execution of the eBPF program significantly since they reduce the per instruction cost compared to the interpreter.

## 3. Thoughs about eBPF

- When to use eBPF:
  - Profiling and tracing user space processes.
  - Traffic control, so that packets are directly sent to their destination.
  - Security policies in container environments.
  - XDP (eXpress Data Path) to provide a high-performance, programmable network data path.
- When not to use eBPF:
  - eBPF prohibits loops and other high-level constructs -> simple and restricted -> want more control over how the programs are executed, write a kernel module.
  - Executing eBPF consumes CPU cycles -> a high CPU usage.

## 4. Hello World

- Writing an eBPF directly in the bytecode is extremely hard -> write in other languages and compile it to the eBPF bytecode -> use [BCC (BPF Compiler Collection)](https://github.com/iovisor/bcc) and [libbpf](https://github.com/libbpf/libbpf).

### 4.1. Hello World with BCC

- BCC is a toolset based on eBPF that allows you to analyze both OS and network performance of Linux distros with ease.
- [Install BCC(<https://github.com/iovisor/bcc/blob/master/INSTALL.md>).
- Create python file:

```python
from bcc import BPF

# Write the C program inside Python and store it as a string variable.
# or write it in a separate file and read that file into Python program.
#
# kprobe__sys_clone
# The name of the fucntion tells BCC where to attach it.
# `kprobe__` - a kprobe to trace a kernel function.
# `sys_clone` - which kernel function to trace.
#               The function can include as many of the probed function
#               arguments as you want, as long as the first argument `ctx`.
# `bpf_trace_printk` - print hello world to the kernel's common trace_pipe
program = """
int kprobe__sys_clone(void *ctx) {
    bpf_trace_printk("Hello World!\\n");
    return 0;
}
"""

# Load BPF program
b = BPF(text=program)

print("Tracing... Hit Ctrl+C to end")

# output
# Read kernel's trace_pipe and print the messages
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMMAND", "PID", "MESSAGE"))
while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    except KeyboardInterrupt:
        print("Bye bye!")
        break
    except Exception as e:
        raise e
    print("%-18.9f %-16s %-6d %s" % (ts, task.decode(), pid, msg.decode()))

```

- Result:
  - Execute any command like `ls` or `cat` that will trigger `clone` call.
  - eBPF program will be executed and the output will be printed.

```shell
$ sudo python bpf-hello-world.py
TIME(s)            COMMAND          PID    MESSAGE
75209.957294000    <...>            38238  Hello World!
75209.980749000    code             38238  Hello World!
75210.004654000    code             38238  Hello World!
75210.027218000    code             38238  Hello World!
75210.032995000    git              40834  Hello World!
```

- For more code examples, check the [BCC examples directory](https://github.com/iovisor/bcc/tree/master/examples).
