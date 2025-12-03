# strace

## Overview and problem

strace is the system call tracer for Linux. It currently uses the arcane `ptrace()` (process trace) debugging interface, which operates in a violent manner: pausing the target process for each syscall so that the debugger can read state. And doing this twice: when the syscall begins, and when it ends.

This means strace pauses your application twice for each syscall, and context-switches each time between the application and strace. It's like putting traffic metering lights on your application.

```shell
BUGS: A traced process runs slowly.
– strace(1) man page
```

![](https://cdn.prod.website-files.com/681e366f54a6e3ce87159ca4/6877c803ead9a7e4d2016f57_Blog2-pic1-1024x555.png)

- Strace is based on a facility called ptrace that is exported by Linux and other operating systems. Ptrace can do many complex things and is used, for example, by debuggers like gdb to look into a running process.
- Strace uses it to instrument a target process and "listen" to that process's system calls. The ptrace mechanism makes it possible for strace to interrupt the traced process every time a system call is invoked, capture the call, decode it, and then resume the execution of the traced process.
- Everytime a system call is invoked (e.g. open, read, write, close), a transition from user level to kernel level is required – this is known as a **context switch**.
- By now it should be clear why strace is not very efficient: every original context switch now turns into multiple context switches, and the traced process is stuck waiting for strace to do its decoding

If you'd like to learn more about strace internal and ptrace(): <https://blog.nelhage.com/2010/08/write-yourself-an-strace-in-70-lines-of-code/>

## Alternatives

<https://www.brendangregg.com/blog/2015-07-08/choosing-a-linux-tracer.html>
<https://jvns.ca/blog/2017/07/05/linux-tracing-systems/>
<https://docs.kernel.org/trace/index.html>

### [perf trace](https://man7.org/linux/man-pages/man1/perf-trace.1.html)

The perf profiling infrastructure has added a new tool "perf trace". This tool should look loosely like the venerable 'strace' tool, but instead of using the ptrace() syscall, it uses the Linux tracing infrastructure. Its purpose is to make tracing easier for a wider audience of Linux users.

pert trace will show the events associated with the target, initially syscalls, but other system events like pagefaults, task lifetime events, scheduling events, etc. This tool is still in its early versions, so it is a live mode only tool and a lot of details things need to be improved, but eventually will work with perf.data files like the other perf tools, allowing a detached 'record' from analysis phases.

### dtrace

![](https://cdn.prod.website-files.com/681e366f54a6e3ce87159ca4/6877c803ead9a7e4d2016f54_Blog2-pic2.png)

An implementation of dynamic tracing.

- DTrace takes scripts written in a domain-specific language called D, converts them into bytecode, and then injects the bytecode into specific places in the kernel.
  - This script states that whenever the read system call is invoked, the tracer should print out the string "read has been called."

```c
syscall::read:entry {
    printf("read has been called.");
}
```

```shell
dtrace -s my_probe.d
```

- The bytecode can be executed when specific events happen, for example when a system call is invoked. The (usually) summarized script output can be collected through libdtrace by user level consumers, who print it on the screen or save it to disk.
- DTrace is very flexible, thanks to the versatility of D and the many places in the kernel where you can attach scripts (as well as in userspace). It is also much more efficient than strace, because no context switch is involved in processing a system call. Since scripts are run inline, however, there's still a chance that a complex or badly written D script can slow down the original execution. It's also possible that, even if single scripts are fast, running many of them at the same time could cause performance degradation.
