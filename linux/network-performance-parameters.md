# Linux Network Performance

Source:

- <https://github.com/leandromoreira/linux-network-performance-parameters/>
- <https://access.redhat.com/sites/default/files/attachments/20150325_network_performance_tuning.pdf>
- <https://blog.cloudflare.com/how-to-achieve-low-latency/>
- <https://blog.packagecloud.io/illustrated-guide-monitoring-tuning-linux-networking-stack-receiving-data/>
- <https://blog.packagecloud.io/monitoring-tuning-linux-networking-stack-receiving-data/>
- <https://blog.packagecloud.io/monitoring-tuning-linux-networking-stack-sending-data/>

Table of Contents:

- [Linux Network Performance](#linux-network-performance)
  - [1. Linux Networking stack: Receiving data](#1-linux-networking-stack-receiving-data)
  - [2. Network Performance tuning](#2-network-performance-tuning)
    - [2.1. The NIC Ring Buffer](#21-the-nic-ring-buffer)
    - [2.2. Interrupts and Interrupt Handlers (Hardware IRQ)](#22-interrupts-and-interrupt-handlers-hardware-irq)

## 1. Linux Networking stack: Receiving data

- It's a getting started. Before perform any tuning, let make sure that we understand how computers running Linux receive packets.
- In network devices, it is common for the NIC to raise an **IRQ** to signal that a packet has arrived and is ready to be processed.
  - An IRQ (Interrupt Request) is a hardware signal sent to the processor instructing it to suspend its current activity and handle some external event, such as a keyboard input or a mouse movement.
  - In Linux, IRQ mappings are stored in **/proc/interrupts**.
  - When an IRQ handler is executed by the Linux kernel, it runs at a very, very high priority and often blocks additional IRQs from being generated. As such, IRQ handlers in device drivers must execute as quickly as possible and defer all long running work to execute outside of this context. This is why the **softIRQ** system exists.
  - **softIRQ** system is a system that kernel uses to process work outside of the device driver IRQ context. In the case of network devices, the softIRQQ system is responsible for processing incoming packets.

```shell
$ cat /proc/interrupts

           CPU0       CPU1       CPU2       CPU3       CPU4       CPU5
  0:         34          0          0          0          0          0   IO-APIC   2-edge      timer
  1:          0          0          0          0       6665          0   IO-APIC   1-edge      i8042
  6:          3          0          0          0          0          0   IO-APIC   6-edge      floppy
  8:          0          0          0          0          0          0   IO-APIC   8-edge      rtc0
  9:          0          0          0          0          0          0   IO-APIC   9-fasteoi   acpi
 12:          0          0          0      18802          0          0   IO-APIC  12-edge      i8042
 17:          0          0          0          0         96     138101   IO-APIC  17-fasteoi   enp0s17
 18:          0          0          0      59389          0          0   IO-APIC  18-fasteoi   vmwgfx
 20:          0          0     129334          0          0          0   IO-APIC  20-fasteoi   ioc0, vboxguest
 21:          0      33641          0          0          0          0   IO-APIC  21-fasteoi   ahci[0000:00:0d.0], snd_intel8x0
 22:          0          0          0          0          0          0   IO-APIC  22-fasteoi   ohci_hcd:usb1
NMI:          0          0          0          0          0          0   Non-maskable interrupts
LOC:     334757     358153     379357     967057     353659     354675   Local timer interrupts
SPU:          0          0          0          0          0          0   Spurious interrupts
PMI:          0          0          0          0          0          0   Performance monitoring interrupts
IWI:          0          0          0          0          0          0   IRQ work interrupts
RTR:          0          0          0          0          0          0   APIC ICR read retries
RES:       2947       5427       4441       2254       4265       3757   Rescheduling interrupts
CAL:     717259     755848     747171     766289     752869     709762   Function call interrupts
TLB:      87230      90379      84499      85971      83204      88133   TLB shootdowns
TRM:          0          0          0          0          0          0   Thermal event interrupts
THR:          0          0          0          0          0          0   Threshold APIC interrupts
DFR:          0          0          0          0          0          0   Deferred Error APIC interrupts
MCE:          0          0          0          0          0          0   Machine check exceptions
MCP:          9          9          9          9          9          9   Machine check polls
ERR:          0
MIS:       1941
PIN:          0          0          0          0          0          0   Posted-interrupt notification event
NPI:          0          0          0          0          0          0   Nested posted-interrupt event
PIW:          0          0          0          0          0          0   Posted-interrupt wakeup event
```

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
- **NOTE**: I should find another flow diagram to catch up this section. It is way too complicated for me :<
  - [Network Data Flow through the Linux Kernel](https://openwrt.org/docs/guide-developer/networking/praxis)
- Linux network queues overview:

![](https://github.com/leandromoreira/linux-network-performance-parameters/raw/master/img/linux_network_flow.png)

## 2. Network Performance tuning

Tuning a NIC for optimum throughput and latency is a complex process with many factors to consider. There is no generic configuration that can be broadly applied to every system.

There are factors should be considered for network performance tuning. Note that, the interface card name may be different in your device, change the appropriate value.

### 2.1. The NIC Ring Buffer

![](https://myaut.github.io/dtrace-stap-book/images/net.png)

- **What**:
  - Receive ring buffers are shared between the device driver and the NIC. The card assigns a transmit (tx) and receive (rx) ring buffers.
  - The ring buffer is a circular buffer where an overflow simply overwrites existing data.
  - There are two ways to move data from the NIC to the kernel, hardware interrupts and software interrupts (SoftIRQs).
  - RX ring buffer is used to store incoming packets until they can be processed by the device driver. The device driver drains the RX ring, typically via SoftIRQs, which puts the incoming packets into a kernel data structure called an `sk_buff` or `skb` to begin its journey through the kernel and up to the application which owns the relevant socket.
  - Fixed size, usually implemented as FIFO, located at RAM.
- **Why**:
  - Buffer to smoothly accept bursts of connections without dropping them, you might need to increase these queues when you see drops or overrun, aka there are more packets coming than the kernel is able to consume them, the side effect might be increased latency.
- **How**: Ring buffer's size is commonly set to a smaller size then the maximum. Often, increasing the receive buffer size is alone enough to prevent packet drops, as it can allow the kernel slightly more time to drain the buffer.
  - Check command:

  ```shell
  $ ethtool -g eth3
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
  $ ethtool -G eth3 rx 8192 tx 8192
  ```

  - Persist the value:
    - RHEL/CentOS: Use `/sbin/ifup-local`, follow [here](https://access.redhat.com/solutions/8694) for detail.
    - Ubuntu: https://unix.stackexchange.com/questions/542546/what-is-the-systemd-native-way-to-manage-nic-ring-buffer-sizes-before-bonded-int

  - How to monitor:

  ```shell
  $ ethtool -S eth3 | grep -e "err" -e "drop" -e "over" -e "miss" -e "timeout" -e "reset" -e "restar" -e "collis" -e "over" | grep -v "\: 0"
  ```

### 2.2. Interrupts and Interrupt Handlers (Hardware IRQ)

- **What**:
- **Why**:
- **How**:
