# `io_uring`

> WIP

Source:

- <https://developers.redhat.com/articles/2023/04/12/why-you-should-use-iouring-network-io>
- <http://https//kernel.dk/io_uring.pdf>
- <https://kernel-recipes.org/en/2019/talks/faster-io-through-io_uring/>
- <https://unixism.net/loti/>

Table of content:

## 1. Linux asynchronous APIs before `io_uring`

With synchronous programming, system calls that deal with reads or writes or remote connections in the case of [accept](http://man7.org/linux/man-pages/man2/accept.2.html) would block until data is read, written or a client connection is available, respectively -> process or thread is blocked.

What if you need to do something else?

- Create other threads to take care these other tasks.

What if you needed to remian active to accept client connections while also trying to read from client sockets and while also trying to read or write local file, all in on thread?

- This is where [select(2)](http://man7.org/linux/man-pages/man2/select.2.html), [poll(2)](http://man7.org/linux/man-pages/man2/poll.2.html) and the [epoll(7)](http://man7.org/linux/man-pages/man7/epoll.7.html) family of system calls come in.
- These system calls allow you to monitor a bunch of file descriptors (sockets are file descriptors, too) and let you know when one or more of them are ready.

Linux's [aio(7)](http://man7.org/linux/man-pages/man7/aio.7.html) family of system calls can deal asynchronously with both files and sockets. However, there are some limitations that you need to be aware of:

- Only files opened with `O_DIRECT` or those opened in unbuffered mode are supported by aio(7). This is undoubtedly its biggest limitation. Not all applications under the usual circumstances want to open files in unbuffered mode.
- Even in unbuffered mode, aio(7) can block if file metadata isn’t available. It will wait for that to be available.
- Some storage devices have a fixed number of slots for requests. aio(7) submission can block if all these slots are busy.
- 104 bytes in total need to be copied for submission and completion. There are also two different system calls (one each for submission and completion) that need to be made for I/O.

**The trouble with regular files**

On a server that is not very busy, reading or writing a file might not take a long time. Take FTP server example using an asynchronous design. When it is really busy with a lot of concurrent users who are downloading and uploading a lot of very large files all at the same time, there is one trouble you need to know about, as a programmer. On a server this busy, read(2) and write(2) calls can begin to block a lot. But won’t the select(2), poll(2) or the epoll(7) family of system calls help us here? Unfortunately not. These systems calls will _always_ tell regular files as being ready for I/O. This is their Achilles’ heel.

Unfortunately, this makes file descriptors non-uniform under asynchronous programming. File descriptors backing regular files are discriminated against. For this reason, libraries like `libuv` use a separate thread pool for I/O on regular files, exposing an API that hides this discrepancy from the user.

## 2. What is `io_uring`?

`io_uring` (previously known as `aioring`) is a Linux kernel system call interface for storage device asynchronous I/O operations addressing performance issues with similar interfaces provided by functions like `read()`/`write()` or `aio_read()`/`aio_write()`, etc. for operations on data accessed by file descriptors.

It has been a big win for file I/O, but might be offer only modest gains for network I/O, which already has non-blocking APIs. The gains are likely to come from the following:

- A reduced number of syscalls on servers that do a lot of context switching.
- A unified asynchronous API for both file and network I/O.

An `io_uring` is a pair of ring buffers in shared memory that are used as queues between user space and the kernel:

- Submission queue (SQ): A user space process uses the submission queue to send asynchronous I/O requests to the kernel.
- Completion queue (CQ): The kernel uses the completion queue to send the result of asynchronous I/O operations back to the user space.

![](https://developers.redhat.com/sites/default/files/styles/article_floated/public/uring_0.png.webp?itok=kNKFe-On)

This interface enables applications to move away from the traditional readiness-based model of I/O to a new completion-based model where async file and network I/O share a unified API.

## 3. The syscall API

The Linux kernel API for `io_uring` has 3 syscalls:

- `io_uring_setup`: Setup a context for performing asynchronous I/O.
- `io_uring_register`: Register files or user buffers for asynchronous I/O.
- `io_uring_enter`: Initiate and/or complete asynchronous I/O.

The first two syscalls are used to set up an `io_uring` instance and optionally to pre-register buffers that would be referenced by `io_uring` operations. Only `io_uring_enter` needs to be called for queue submission and consumption. The cost of an `io_uring_enter` call can be amortized over several I/O operations. For very busy servers, you can avoid `io_uring_enter` calls entirely by enabling busy-polling of the submission queue in the kernel. This comes at the cost of a kernel thread consuming CPU.

## 4. The mental model

The mental model you need to construct in order to use io_uring to build programs that process I/O asynchronously is fairly simple.

- There are 2 ring buffers: SQ and CQ.
- These ring buffers are shared between kernel and user space. You set these up with `io_uring_setup()` and then mapping them into user space with 2 [mmap](http://man7.org/linux/man-pages/man2/mmap.2.html) calls.
- You tell `io_uring` what you need to get done (read or write a file, accept client connections, etc), which you describe as part of submission queue entry (SQE) and add it to the tail of the submission ring buffer.
- You then tell the kernel via the `io_uring_enter()` system call that you've added an SQE to the submission queue ring buffer. You can add multiple SQEs before making the system call as well.
- Optionally, `io_uring_enter()` can also wait for a number of requests to be processed by the kernel before it returns so you know you're ready to read off the completion queue for results.
- The kernel processes requests submitted and adds completions queue events (CQEs) to the tail of the completion queue ring buffer.
- You read CQEs off the head of the completion queue ring buffer. There is one CQE corresponding to each SQE and it contains the status of that particular request.
- You continue adding SQEs and reaping CQEs as you need.
- There is a [polling mode available](https://unixism.net/loti/tutorial/sq_poll.html#sq-poll), in which the kernel polls for new entries in the SQ. This avoids the system call overhead of calling `io_uring_enter()` every time you submit entries for processing.
  - In this mode, right after your program sets up polling mode, `io_uring` starts a special kernel thread that polls the shared submission queue for entries your program might add.
  - That way, you just have to submit entries into the shared queue and the kernel thread should see it and pick up the submission queue entry without your program having to make the `io_uring_enter()` system call, which is usually taken care of by liburing.
  - **NOTE**: The kernel’s poller thread can take up a lot of CPU. You need to be careful about using this feature. Setting a very large sq_thread_idle value will cause the kernel thread to continue to consume CPU while there are no submissions happening from your program.

## 5. The liburing API

The [liburing](https://github.com/axboe/liburing) library provides a convenient way to use `io_uring`, hiding some of the complexity and providing functions to prepare all types of I/O operations for submission.
