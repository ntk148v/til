# Linux system UDP packet loss

Source: <https://www.sobyte.net/post/2022-05/Linux-udp-packet-drop-debug/>

## 1. The process of receiving network message on a Linux system

- The network message is sent to the NIC through the physical network cable.
- The network driver reads the message from the network into the ring buffer, a process that uses DMA (direct memroy access) and does nto require CPU participation.
- The kernel reads the message from the ring buffer, processes it, executes the IP and TCP/UDp layer logic, and finally puts the message into the application's socket buffer.
- The application reads the message from the socket buffer for processing.

![](https://cdn.jsdelivr.net/gh/b0xt/sobyte-images/2022/05/04/a90910fc53c84ee89fde4ed9cf8cdacd.png)

- In the process of receiving UDP messages, any of the processes in the diagram may actively or passively discard the messages, so packet loss may occur.
- Assume that the mchine has only one interface with the name `eth0`, `RX` - receive, `TX` - transmit.

## 2. Confirm that a UDP packet drop is occcurring

```bash
$ ethtool -S eth0
$ ifconfig eth0
$ netstat -s -u
Udp:
    517488890 packets received
    2487375 packets to unknown port received. # indicates that the target port where the UDP messages was received is no being listened to
    47533568 packet receive errors # not empty and keeps growing indicating that the system has UDP packet loss
    147264581 packets sent
    12851135 receive buffer errors # indicates the number of packets lost because the UDp receive buffer is too small
    0 send buffer errors
```

- NOTE: If number of packets lost/number of received (packet loss rate) <= 1/10000 -> OK.

## 3. NIC or driver packet loss

```bash
# Check hardware or driver
$ ethtool -S eth0 | grep rx_ | grep errors
     rx_crc_errors: 0
     rx_missed_errors: 0
     rx_long_length_errors: 0
     rx_short_length_errors: 0
     rx_align_errors: 0
     rx_errors: 0
     rx_length_errors: 0
     rx_over_errors: 0
     rx_frame_errors: 0
     rx_fifo_errors: 0
$ netstat -i # provide the packet reception and drop of each NIC, normally the output should be 0 for error or drop
# Check ring buffer
$ ethtool -g eth0
Ring parameters for eth0:
Pre-set maximums:
RX:        4096
RX Mini:    0
RX Jumbo:    0
TX:        4096
Current hardware settings:
RX:        256
RX Mini:    0
RX Jumbo:    0
TX:        256
# Set max ring buffer
$ ethtool -G eth0 rx 8192
```

## 4. Linux system packet loss

### 4.1. UDP packet error

- If the UDp message is modified during transmission, it will lead to checksum error or length error, which will be verified by Linux when receiving the UDP message, and the message will discarded once the error is invented.
- Disable UDP checksum

### 4.2. Firewall

- If system firewall drops packet, the behavior is generally all UDP mesages are not received properly -> A very large packet loss rate -> Check firewall rule first.

### 4.3. UDP buffer size is not enough

- After receiving a message, the Linux system saves the message in the buffer -> Buffer is full -> drop packets.
- Check parameters:
  - /proc/sys/net/core/rmem_max: the maximum value of receive buffer allowed to be set
  - /proc/sys/net/core/rmem_default: the default receive buffer value to be used
  - /proc/sys/net/core/wmem_max: the maximum value of send buffer allowed * /proc/sys/net/core/wmem_max: the maximum value of send buffer allowed
  - /proc/sys/net/core/wmem_dafault: the maximum value of send buffer to be used by default
- Change to make it effective immediately.

```bash
$ sysctl -w net.core.rmem_max=26214400 # 25M
```

- If a message is too large, split the data on the sender side to ensure that each message is within the MTU size.
- `netdev_max_backlog`: the number of messages that the Linux kernel can cache after reading messages from the NIC driver, default 1000.

```bash
$ sudo sysctl -w net.core.netdev_max_backlog=2000
```

### 4.4. System load is too high

- High system CPU, memory and IO load -> network packet loss.
- The Linux system itself is an interconnected system, and problems with any one component may affect the normal operation of other components.
- How to check?

## 5. Application packet loss

- The Linux system puts the received messages into the socket’s buffer, and the application reads messages from the buffer continuously. So there are two application-related factors that affect packet loss: the socket buffer size and the speed at which the application reads the packets.

## 6. Tool

- Check out [dropwatch](https://github.com/nhorman/dropwatch) (You have to install it from source).
- Install dropwatch ubuntu

```bash
# Ubuntu 20.04
sudo apt install binutils-dev libreadline-dev libnl-3-dev libnl-genl-3-dev libpcap-dev -y
git clone https://github.com/nhorman/dropwatch
cd dropwatch/
./autogen.sh && ./configure && make && sudo make install
```
