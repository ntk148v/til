# eXpress Data Path (XDP)

Source:

- <https://en.wikipedia.org/wiki/Express_Data_Path>

## 1. Introduction

- XDP is an [eBPF](../linux/ebpf/README.md)-based on high-performance data path used to send and receive network packets at high rates by passing most of the operating system networking stack.
- Linux kernel >= 4.8.
- Benefits:
  - High performance.
  - New functions can be implemented dynamically with the integrated fast path without kernel modification.
  - Does not require any specialized hardware.
  - Does not require kernel bypass.
  - Does not replace the TCP/IP stack.
  - Works in concert with TCP/IP stack along with all the benefits of BPF.

## 2. How it works?

- XDP packet process includes an in kernel component that processes RX packet-pages direclty out of driver via a functional interface wihtout early allocation of skbuff's or software queues.
- No locking RX queue, and CPU can be dedicated to busy poll or interrupt model.
- BPF programs performs processing such as packet parsing, table look ups, creating/managing stateful filters, encap/decap packets, etc.

![](https://www.iovisor.org/wp-content/uploads/sites/8/2016/09/xdp-packet-processing-768x420.png)
