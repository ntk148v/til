# Linux Network Performance

Source:

- <https://github.com/leandromoreira/linux-network-performance-parameters/>
- <https://access.redhat.com/sites/default/files/attachments/20150325_network_performance_tuning.pdf>
- <https://blog.cloudflare.com/how-to-achieve-low-latency/>
- <https://blog.packagecloud.io/illustrated-guide-monitoring-tuning-linux-networking-stack-receiving-data/>
- <https://blog.packagecloud.io/monitoring-tuning-linux-networking-stack-receiving-data/>
- <https://blog.packagecloud.io/monitoring-tuning-linux-networking-stack-sending-data/>
- <https://openwrt.org/docs/guide-developer/networking/praxis>
- <https://www.coverfire.com/articles/queueing-in-the-linux-network-stack/>
- <https://blog.cloudflare.com/how-to-achieve-low-latency/>

Table of Contents:

- [Linux Network Performance](#linux-network-performance)
  - [1. Linux Networking stack: Receiving data](#1-linux-networking-stack-receiving-data)
    - [1.1. Linux network packet reception](#11-linux-network-packet-reception)
    - [1.2. Linux kernel network transmission](#12-linux-kernel-network-transmission)
  - [2. Network Performance tuning](#2-network-performance-tuning)
    - [2.1. The NIC Ring Buffer](#21-the-nic-ring-buffer)
    - [2.2. Interrupt Coalescence (IC) - rx-usecs, tx-usecs, rx-frames, tx-frames (hardware IRQ)](#22-interrupt-coalescence-ic---rx-usecs-tx-usecs-rx-frames-tx-frames-hardware-irq)
    - [2.3. Interrupt Coalescing (soft IRQ) and Ingress QDisc](#23-interrupt-coalescing-soft-irq-and-ingress-qdisc)

## 1. Linux Networking stack: Receiving data

- It's a getting started. Before perform any tuning, let make sure that we understand how computers running Linux receive packets.
- You check the summary of *PackageCloud's article* here. This is a very detailed explaination.

  <details>
  <summary>Click to expand</summary>
  - In network devices, it is common for the NIC to raise an **IRQ** to signal that a packet has arrived and is ready to be processed.
    - An IRQ (Interrupt Request) is a hardware signal sent to the processor instructing it to suspend its current activity and handle some external event, such as a keyboard input or a mouse movement.
    - In Linux, IRQ mappings are stored in **/proc/interrupts**.
    - When an IRQ handler is executed by the Linux kernel, it runs at a very, very high priority and often blocks additional IRQs from being generated. As such, IRQ handlers in device drivers must execute as quickly as possible and defer all long running work to execute outside of this context. This is why the **softIRQ** system exists.
    - **softIRQ** system is a system that kernel uses to process work outside of the device driver IRQ context. In the case of network devices, the softIRQQ system is responsible for processing incoming packets

  - Initial setup (from step 1-4):

    ![](https://cdn.buttercms.com/hwT5dgTatRdfG7UshrAF)

    - softIRQ kernel threads are created (1 per CPU).
    - The ksoftirqd threads begin executing their processing loops.
    - `softnet_data` structures are created (1 per CPU), hold references to important data for processing network data. `poll_list` is created (1 per CPU).
    - `net_dev_init` then registers the `NET_RX_SOFTIRQ` softirq with the softirq system by calling `open_softirq` - this registration is called `net_rx_action`,

  - Alright, Linux just init and setup networking stack to wait for data arrival:

    ![](https://cdn.buttercms.com/yharphBYTEm2Kt4G2fT9)

    - Data is received by the NIC (Network Interface Card) from the network.
    - The NIC uses DMA (Direct Memory Access) to write the network data to RAM (in ring buffer).
      - Some NICs are "multiqueue" NICs, meaning that they can DMA incoming packets to one of many ring buffers in RAM.
    - The NIC raises an IRQ.
    - The device driver's registered IRQ handler is executed.
    - The IRQ is cleared on the NIC, so that it can generate IRQs for net packet arrivals.
    - NAPI softIRQ poll loop is started with a call to `napi_schedule`.

  - Check initial setup diagram (setup 5-8):
    - The call to `napi_schedule` in the driver adds the driver's NAPI poll structure to the `poll_list` for the current CPU.
    - The softirq pending a bit is set so that the `ksoftirqd` process on this CPU knows that there are packets to process.
    - `run_ksoftirqd` function (which is being run in a loop by the `ksoftirq` kernel thread) executes.
    - `__do_softirq` is called which checks the pending bitfield, sees that a softIRQ is pending, and calls the handler registerd for the pending softIRQ: `net_rx_action` (softIRQ kernel thread executes this, not the driver IRQ handler).
  - Now, data processing begins:
    - `net_rx_action` loop starts by checking the NAPI poll list for  NAPI structures.
    - The `budget` and elapsed time are checked to ensure that the softIRQ will not monopolize CPU time.
    - The registered `poll` function is called.
    - The driver's `poll` functio harvests packets from the ring buffer in RAM.
    - Packets are handed over to `napi_gro_receive` (GRO - Generic Receive Offloading).
      - GRO is a widely used SW-based offloading technique to reduce per-packet processing overheads.
      - By reassembling small packets into larger ones, GRO enables applications to process fewer large packets directly, thus reducing the number of packets to be processed.
    - Packets are either held for GRO and the call chain ends here or packets are passed on to `netif_receive_skb` to proceed up toward the protocol stacks.
  - Network data processing continues from `netif_receive_skb`, but the path of the data depends on whether or not Receive Packet Steering (RPS) is enabled or not.

    ![](https://cdn.buttercms.com/uoaSO7cgTwKaH1esQgWX)

    - If RPS is disabled:
      - 1. `netif_receive_skb` passed the data onto `__netif_receive_core`.
      - 6. `__netif_receive_core` delivers the data to any taps.
      - 7. `__netif_receive_core` delivers data to registed protocol layer handlers.
    - If RPS is enabled:
      - 1. `netif_receive_skb` passes the data on to `enqueue_to_backlog`.
      - 2. Packets are placed on a per-CPU input queue for processing.
      - 3. The remote CPU’s NAPI structure is added to that CPU’s poll_list and an IPI is queued which will trigger the softIRQ kernel thread on the remote CPU to wake-up if it is not running already.
      - 4. When the `ksoftirqd` kernel thread on the remote CPU runs, it follows the same pattern describe in the previous section, but this time, the registered poll function is `process_backlog` which harvests packets from the current CPU’s input queue.
      - 5. Packets are passed on toward `__net_receive_skb_core`.
      - 6. `__netif_receive_core` delivers data to any taps (like PCAP).
      - 7. `__netif_receive_core` delivers data to registered protocol layer handlers.

  - Protocol stacks, netfilter, BPF, and finally the userland socket.
    - Packets are received by the IPv4 protocol layer with `ip_rcv`.
    - Netfilter and a routing optimization are performed.
    - Data destined for the current system is delivered to higher-level protocol layers, like UDP.
    - Packets are received by the UDP protocol layer with `udp_rcv` and are queued to the receive buffer of a userland socket by `udp_queue_rcv_skb` and `sock_queue_rcv`. Prior to queuing to the receive buffer, BPF are processed.

  </details>

- Linux queue:

![](https://github.com/leandromoreira/linux-network-performance-parameters/raw/master/img/linux_network_flow.png)

### 1.1. Linux network packet reception

![](https://pic002.cnblogs.com/images/2012/360373/2012110119582618.png)

1. Packet arrives at the NIC
2. NIC verifies `MAC` (if not on promiscuous mode) and `FCS` and decide to drop or to continue
3. NIC does [DMA (Direct Memory Access) packets at RAM](https://en.wikipedia.org/wiki/Direct_memory_access), in a region previously prepared (mapped) by the driver.
4. NIC enqueues references to the packets at receive ring buffer queue `rx` until `rx-usecs` timeout or `rx-frames`. Let's talk about the RX ring buffer:
   - It is a [circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) where an overflow simply overwrites existing data.
   - It is used to store incoming packets until they can be processed by the device driver. The device driver drains the RX ring, typically via SoftIRQs (we will talk about it then), which puts the incoming packets into a kernel data structure called an `sk_buff` or `skb` (Socket Kernel Buffers - [SKBs](http://vger.kernel.org/~davem/skb.html)) to begin its journey through the kernel and up to the application which owns the relevant socket.
   - Fixed size, FIFO and located at RAM (of course).
5. NIC raises a `HardIRQ` - Hard Interrupt.
   - The Hard IRQ can be expensive in terms of CPU usage, especially when holding kernel locks.
   - Hard interrupts can be seen in `/proc/interrupts`.

    ```shell
    # For example, the columns represent the number of incoming interrupts as a counter value
    egrep “CPU0|eth3” /proc/interrupts
        CPU0 CPU1 CPU2 CPU3 CPU4 CPU5
    110:    0    0    0    0    0    0   IR-PCI-MSI-edge   eth3-rx-0
    111:    0    0    0    0    0    0   IR-PCI-MSI-edge   eth3-rx-1
    112:    0    0    0    0    0    0   IR-PCI-MSI-edge   eth3-rx-2
    113:    2    0    0    0    0    0   IR-PCI-MSI-edge   eth3-rx-3
    114:    0    0    0    0    0    0   IR-PCI-MSI-edge   eth3-tx
    ```

6. CPU runs the `IRQ handler` that runs the driver's code.
7. Driver will `schedule a [NAPI](https://en.wikipedia.org/wiki/New_API)`, clear the hard IRQ and return
8. Driver raise a `SoftIRQ (NET_RX_SOFTIRQ)`.
   - It is a kernel routines which are scheduled to run at a time when other tasks will not be interrupted.
   - Purpose: drain the network adapter receive Rx ring buffer.
   - Check command:

    ```shell
    ps aux | grep ksoftirq
                                                                      # ksotirqd/<cpu-number>
    root          13  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/0]
    root          22  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/1]
    root          28  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/2]
    root          34  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/3]
    root          40  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/4]
    root          46  0.0  0.0      0     0 ?        S    Dec13   0:00 [ksoftirqd/5]
    ```

   - Monitor command:

    ```shell
    watch -n1 grep RX /proc/softirqs
    watch -n1 grep TX /proc/softirqs
    ```

9. NAPI polls data from the rx ring buffer until `netdev_budget_usecs` timeout or `netdev_budget` and `dev_weight` packets.
   - If the SoftIRQs do not run for long enough, the rate of incoming data could exceed the kernel's capability to drain the buffer last enough. As a result, the NIC buffers will overflow and traffic will be lost. Occasionaly, it is necessary to increase the time that SoftIRQs are allowed to run on the CPU. This is known as the `netdev_budget`.
     - Check command, the default value is 300, it means the SoftIRQ process to drain 300 messages from the NIC before getting off the CPU.

      ```shell
      sysctl net.core.netdev_budget
      net.core.netdev_budget = 300
      ```

   - `netdev_budget_usecs`: The maximum number of microseconds in 1 NAPI polling cycle. Polling will exit when either `netdev_budget_usecs` have elapsed during the poll cycle or the number of packets processed reaches `netdev_budget`.
     - Check command:

      ```shell
      sysctl net.core.netdev_budget_usecs

      net.core.netdev_budget_usecs = 8000
      ```

10. Linux also allocates memory to `sk_buff`.
11. Linux fills the metadata: protocol, interface, setmatchheader, removes ethernet
12. Linux passes the skb to the kernel stack (`netif_receive_skb`)
13. It sets the network header, clone `skb` to taps (i.e. tcpdump) and pass it to tc ingress
14. Packets are handled to a qdisc sized `netdev_max_backlog` with its algorithm defined by `default_qdisc`
15. It calls `ip_rcv` and packets are handled to IP
16. It calls netfilter (`PREROUTING`)
17. It looks at the routing table, if forwarding or local
18. If it's local it calls netfilter (`LOCAL_IN`)
19. It calls the L4 protocol (for instance `tcp_v4_rcv`)
20. It finds the right socket
21. It goes to the tcp finite state machine
22. Enqueue the packet to the receive buffer and sized as `tcp_rmem` rules
    - If `tcp_moderate_rcvbuf is enabled kernel will auto-tune the receive buffer
23. Kernel will signalize that there is data available to apps (epoll or any polling system)
24. Application wakes up and reads the data

### 1.2. Linux kernel network transmission

// WIP

## 2. Network Performance tuning

Tuning a NIC for optimum throughput and latency is a complex process with many factors to consider. There is no generic configuration that can be broadly applied to every system.

There are factors should be considered for network performance tuning. Note that, the interface card name may be different in your device, change the appropriate value.

Ok, let's follow through the Packet reception and do some tuning.

### 2.1. The NIC Ring Buffer

![](https://myaut.github.io/dtrace-stap-book/images/net.png)

- Firstly, check out step (4) - NIC Ring buffer. It's a circular buffer, fixed size, FIFO, located at RAM. Buffer to smoothly accept bursts of connections without dropping them, you might need to increase these queues when you see drops or overrun, aka there are more packets coming than the kernel is able to consume them, the side effect might be increased latency.
- Ring buffer's size is commonly set to a smaller size then the maximum. Often, increasing the receive buffer size is alone enough to prevent packet drops, as it can allow the kernel slightly more time to drain the buffer.
  - Check command:

  ```shell
  ethtool -g eth3
  Ring parameters for eth3:
  Pre-set maximums:
  RX: 8192
  RX Mini: 0
  RX Jumbo: 0
  TX: 8192
  Current hardware settings:
  RX: 1024
  RX Mini: 0
  RX Jumbo: 0
  TX: 512
  # eth3's inteface has the space for 8KB but only using 1KB
  ```

  - Change command:

  ```shell
  # Increase both the Rx and Tx buffers to the maximum
  ethtool -G eth3 rx 8192 tx 8192
  ```

  - Persist the value:
    - RHEL/CentOS: Use `/sbin/ifup-local`, follow [here](https://access.redhat.com/solutions/8694) for detail.
    - Ubuntu: follow [here](https://unix.stackexchange.com/questions/542546/what-is-the-systemd-native-way-to-manage-nic-ring-buffer-sizes-before-bonded-int)

  - How to monitor:

  ```shell
  ethtool -S eth3 | grep -e "err" -e "drop" -e "over" -e "miss" -e "timeout" -e "reset" -e "restar" -e "collis" -e "over" | grep -v "\: 0"
  ```

### 2.2. Interrupt Coalescence (IC) - rx-usecs, tx-usecs, rx-frames, tx-frames (hardware IRQ)

- Move on to step (5), hard interrupt - HardIRQ. NIC enqueue references to the packets at receive ring buffer queue rx until rx-usecs timeout or rx-frames, then raises a HardIRQ. This is called *Interrupt coalescence*:
  - The amount of traffic that a network will receive (number of frames) `rx/tx-frames`, or time that passes after receiving traffic (timeout) `rx/tx-usecs`.
    - Interrupting too soon: poor system performance (the kernel stops a running task to handle the hardIRQ)
    - Interrupting too late: traffic isn't taken off the NIC soon enough -> more traffic -> overwrite -> traffic loss!

- Updating *Interrupt coalescence* can reduce CPU usage, hardIRQ, might be increase throughput at cost of latency
- Tuning:
  - Check command:
    - Adaptive mode enables the card to auto-moderate the IC. The driver will inspect traffic patterns and kernel receive patterns, and  estimate coalescing settings on-the-fly which aim to prevent packet loss -> useful if many small packets are received.
    - Higher interrupt coalescence favors bandwidth over latency: VOIP application (latency-sensitive) may require less coalescence than a file transfer (throughput-sensitive)

  ```shell
  ethtool -c eth3

  Coalesce parameters for eth3:
  Adaptive RX: on TX: off # Adaptive mdoe
  stats-block-usecs: 0
  sample-interval: 0
  pkt-rate-low: 400000
  pkt-rate-high: 450000
  rx-usecs: 16
  rx-frames: 44
  rx-usecs-irq: 0
  rx-frames-irq: 0
  ```

  - Change command:
    - Allow at least some packets to buffer in the NIC, and at least some time to pass, before interrupting the kernel. The values depend on system capabilities and traffic received.

  ```shell
  # Turn adaptive mode off
  # Interrupt the kernel immediately upon reception of any traffic
  ethtool -C eth3 adaptive-rx off rx-usecs 0 rx-frames 0
  ```

  - How to monitor:

### 2.3. Interrupt Coalescing (soft IRQ) and Ingress QDisc

- `net.core.netdev_budget_usecs`:
  - Tuning:
    - Change command:

    ```shell
    sysctl -w net.core.netdev_budget_usecs <value>
    ```

    - Persist the value, check [this](https://access.redhat.com/discussions/2944681)
    - How to monitor:
      - If any of columns beside the 1st column are increasing, need to change budgets!

    ```shell
    cat softnet_stat

    0073d76b 00000000 000049ae 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    000000d2 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    0000015c 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    0000002a 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    ```

- `net.core.netdev_budget`:

// WIP
