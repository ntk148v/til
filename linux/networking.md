# Linux networking

## 1. POSIX sockets and Packet flows

- Futher reading:

  - <https://blog.packagecloud.io/eng/2017/02/06/monitoring-tuning-linux-networking-stack-sending-data/>
  - <https://blog.packagecloud.io/eng/2016/06/22/monitoring-tuning-linux-networking-stack-receiving-data/>
  - <https://blog.packagecloud.io/eng/2016/10/11/monitoring-tuning-linux-networking-stack-receiving-data-illustrated/>
  - <https://github.com/ppnaik1890/Learning/blob/main/CS744_kernel-bypass_theory_slides.pdf>)

- Linux networking stack is based on [Berkely sockets](https://en.wikipedia.org/wiki/Berkeley_sockets) (BSD) -> POSIX sockets.
- Applications create a socket, which represents a flow, and use that socket's file descriptor to send and receive data over the network.
- Example: A server application that wants to accept TCP connections.
  - Create a socket with the `socket()` operation.
  - Bind the socket to an interface or an address with the `bind()` operation.
  - Start listening to incoming connections
  - When there is a new connection, the server application establishes a new connection with the `accept()` operation and then sends and receives data over the connection with the `sendmsg()` and `recvmsg()` operations.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/InternetSocketBasicDiagram_zhtw.png/220px-InternetSocketBasicDiagram_zhtw.png)

- Most in-kernel network stacks implement POSIX socket operations as _system calls_ (both control plane operations (`socket()`), and data plane operations (`sendmsg()`)). System calls -> context switching, CPU cache pollution.
- Socket API pushes the OS to adopt a design, which demands dynamic memory allocation and locking. When a packet arrives on the NIC, the OS first wraps the packet in a buffer object, called a socket buffer (`skb`) in Linux. The allocation of the buffer object puts much stress on the OS dynamic memory allocator. Once allocated, the OS then passes the buffer object down the in-kernel network stack for further processing. The buffer object lives until the application consumes all the data it holds with the `recvmsg()` system call. As the buffer object can be forwarded between CPU cores and accessed from multiple threads, locks must be used to protect against concurrent access.
- Packet processing overheads in the kernel
  - Too many context switches between kernel and userspace.
  - Packet copy between kernel and userspace.
  - Dynamic allocation of skb.
  - Per packate interrupt

## 2. Kernel-bypass networking

- Eliminates the overheads of in-kernel network stacks by moving protocol processing to userspace.
- The packet I/O is either handled by the hardware, the OS, or by userspace, depending on the specific kernel-bypass architecture in use.
  - RDMA (Remote Direct Memory Access)
  - TOE (TCP Offload Engine)
  - OpenOnload
  - DPDK (Data Plane Development Kit)
  - Netmap
  - FD.io (Fast Data Input Output) based on VPP (Vector Packet Processing)

## 3. Programmable packet processing

- Programmable packet processors allow execution of user-defined code either in the OS or the hardware.
  - XDP
