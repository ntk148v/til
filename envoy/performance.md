# Tuning Envoy for Performance


Well, when you try to find Nginx or HAproxy performance tuning, the results are detailed documentations: [this](https://www.nginx.com/blog/tuning-nginx/), [this](https://www.cloudbees.com/blog/performance-tuning-haproxy), [this](https://www.freecodecamp.org/news/how-we-fine-tuned-haproxy-to-achieve-2-000-000-concurrent-ssl-connections-d017e61a4d27/),...

Replace Nginx/HAproxy with Envoy, this is a different story. Therefore, I decide to write this guide.

- [Tuning Envoy for Performance](#tuning-envoy-for-performance)
  - [1. Getting started](#1-getting-started)
  - [2. First thing first, tuning your Linux OS](#2-first-thing-first-tuning-your-linux-os)
    - [2.1. The backlog queue](#21-the-backlog-queue)
    - [2.2. File descriptors](#22-file-descriptors)
    - [2.3. Ephemeral ports](#23-ephemeral-ports)
    - [2.4. TCP buffer](#24-tcp-buffer)
  - [3. Tuning Envoy](#3-tuning-envoy)

## 1. Getting started

- A basic understanding of the Envoy architecture and configuration concepts is assumed.
- Assume Envoy is deployed in Linux distro (kernel 2.6+).
- Change one settings at a time, and set it back to the default value if the change does not improve performance.
- Follow [How to benchmark Envoy guide](https://www.envoyproxy.io/docs/envoy/latest/faq/performance/how_to_benchmark_envoy).
- Every section is combined of 4 sections:
  - What: Quick intro about the change.
  - Why: Explain why you should make this change.
  - How: The ideal change.

## 2. First thing first, tuning your Linux OS

- Note that, you should check the kernel log for error messages indicating that a settings is too low, and adjust it as advised.

### 2.1. The backlog queue

- What:
  - The following settings relate to connections and how they are queued.
  - If you have a high rate of incoming connections, you may get uneven levels of performance (for example, some connections appear to be staling).
- Why: [The origin post](https://www.alibabacloud.com/blog/tcp-syn-queue-and-accept-queue-overflow-explained_599203)
  - SYN Queue and Accept Queue: During the TCP handshake process, the Linux kernel maintain these two queues. Both queues have length and size limits. If the limit is exceeded, the kernel discards the connection Drop or return the RST packet.

  ![](https://yqintl.alicdn.com/0f72fe628f4e77b59f92d149c8584476f8d6fc5d.png)

  - Check of relevant indicators

  ```shell
  # -n Does not resolve the service name
  # -t only show tcp sockets
  # -l Displays LISTEN-state sockets
  $ ss -int
  # Recv-Q: The size of the current accept queue, which means the 3 connections have been completed and are waiting for the application accept() TCP connections
  # Send-Q: The maximum length of the accept queue, which is the size of the accept queue.
  $ ss -nt
  # Recv-Q: The number of bytes received but not read by the application
  # Send-Q: The number of bytes sent but not ack.

  # Check the overflow status of TCP SYN queue and accept queue
  $ netstat -s | grep -i "listen"
  ```

  - The maximum length of TCP Accept queue is controlled by `min(somaxconn, backlog)` (Check [related kernel code, if you want](https://github.com/torvalds/linux/blob/master/net/socket.c)):
    - somaxconn (`/proc/sys/net/core/somaxconn`).
    - backlog is one of TCP protocol's listen function parameters, which is the size of the int listen(int sockfd, int backlog) function's backlog.
  - `tcp_max_syn_backlog` represents the maximal number of connections in SYN RECV queue (when your server received SYN, sent SYN-ACK and haven't received ACK yet).
  - Nginx blog has metioned `net.core.netdev_max_backlog`: The rate at which packets are buffered by the network card before being handed off to the CPU (per CPU core settings).
- How: Increase these values to improve performance on machines with a high amount of bandwidth. The exact numbers are depend on your system.
  - Increase `net.core.somaxconn`.

  ```shell
  # Increase value
  net.core.somaxconn=<value>
  # Restart service
  # Check the accept queue size
  $  ss -lnt
  ```

  - Increase `net.ipv4.tcp_max_syn_backlog`.

  ```shell
  # Increase value
  net.ipv4.tcp_max_syn_backlog=<value>
  ```

  - Increase `net.core.netdev_max_backlog`.

  ```shell
  # Increase value
  net.core.netdev_max_backlog=<value>
  ```

### 2.2. File descriptors

- What:
  - File descriptors are operating system resources used to represent connections and open files, among other things.
  - Proxy usually takes up to two file descriptors/connection:
    - 1 file descriptor for the client connection.
    - Another for the connection to the proxied server.
- Why:
  - Sockets are considered equilvalent to files from the system perspective!
  - `sys.fs.file-max`: The system-wide limit of file descriptors.
  - `nofile`: The user file descriptor limit, set in `/etc/security/limits.conf` file.
- How:
  - Increase the total file descriptors.

  ```shell
  # Update to 1 mil
  fs.file-max = 10000000
  # Update to 1 mil
  fs.nr_open = 10000000
  # Update /etc/security/limits.conf
  * soft nofile 10000000
  * hard nofile 10000000
  root soft nofile 10000000
  root hard nofile 10000000
  ```

### 2.3. Ephemeral ports

- What:
  - Each connection to an upstream server uses a temporary, or *ephemeral* port.
- Why:
  - `net.ipv4.ip_local_port_range`: the start and end of the range of port values. If you see that you are running out of ports, increase the range.
- How:
  - Increase the range of ports.

  ```shell
  net.ipv4.ip_local_port_range=1024    65023
  ```

### 2.4. TCP buffer

- What:
  - If your host handles a huge number of connections, it costs a lot of memory.
- Why:
  - `net.ipv4.tcp_rmem`: Contains 3 values that represent the minimum, default and maximum size of the TCP socket receive buffer.
  - `net.ipv4.tcp_wmem`: Similar to the `net.ipv4.tcp_rmem` this parameter consists of 3 values, a minimum, default, and maximum.
  - `net.ipv4.tcp_mem`: The overall.
- How:
  - Reduce these values in order to reduce memory use.

  ```shell
  net.ipv4.tcp_mem = 786432 1697152 1945728
  net.ipv4.tcp_rmem = 4096 4096 16777216
  net.ipv4.tcp_wmem = 4096 4096 16777216
  ```

## 3. Tuning Envoy

### 3.1. Concurrency

- What:
  - Envoy uses a single process with multiple *threads* architecture. A single primary thread controls various sporadic coordination tasks while some number of worker threads perform listening, filtering, and forwarding.
  - Once a connection is accepted by a listener, the connection spends the rest of its lifetime bound to a single worker thread.
  - Envoy does no have any blocking IO operations in the event loop, even logging is implemented in a non-blocking way.
- Why:
- How: Leave `--concurrency` be unset (providing one worker thread per logical core on your machine).

### 3.2. SO_REUSEPORT

- What:
  - By default, Envoy disable resuse port feature.
- Why:
  - Multiple server sockets listen on the sameport. Each server socket corresponds to a listening thread. When the kernel TCP stack receives a client connection request (SYN), according to the TCP 4-tuple (srcIP, srcPort, destIP, destPort) hash algorithm, select a listening thread, and wake it up. The new connection is bound to the thread that is woken up. So connections are more evenly distributed across threads than non-`SO_REUSEPORT` (in this case, all worker threads share on socket).
- How:
  - Config `enable_reuse_port` option (version >= 1.20). If you use the older version (1.18 for example), you can check `reuse_port`:
    - https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto
    - https://www.envoyproxy.io/docs/envoy/v1.18.3/api-v3/config/listener/v3/listener.proto