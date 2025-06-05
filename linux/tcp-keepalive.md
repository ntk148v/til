# TCP keepalive

Source:

- <https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/>
- <https://codearcana.com/posts/2015/08/28/tcp-keepalive-is-a-lie.html>

Table of contents:

- [TCP keepalive](#tcp-keepalive)
  - [1. Overview](#1-overview)
    - [1.1. What is TCP keepalive?](#11-what-is-tcp-keepalive)
    - [1.2. Why use TCP keepalive?](#12-why-use-tcp-keepalive)
      - [1.2.1. Checking for dead peers](#121-checking-for-dead-peers)
      - [1.2.2. Preventing disconnection due to network inactivity.](#122-preventing-disconnection-due-to-network-inactivity)
  - [2. Using TCP keepalive under Linux](#2-using-tcp-keepalive-under-linux)

## 1. Overview

> TCP keepalive: keep TCP live. This means that you will be able to check your connected socket (also known as TCP sockets), and determine whether the connection is still up and running or if it has broken.

TCP_KEEPALIVE is an optional TCP socket option (disabled by default) intended to prevent servers from (RFC1122, p102)

### 1.1. What is TCP keepalive?

The concept: when you set up TCP connection, you associate a set of timers. Some of these timers deal with the keepalive procedure. When the keepalive timer reaches zero, you send your peer a keepalive probe packet with no data in it and the ACK flag turned on. You can do this because of the TCP/IP specifications, as a sort of duplicate ACK, and the remote checkpoint will have no arguments, as TCP is a stream-oriented protocol. On the other hand, you will receive a reply from the remote host (which doesn't need to support keepalive at all, just TCP/IP), with no data and ACK set.

If you receive a reply to your keepalive probe, you can assert that the connection is still up and running without worrying about the user-level implementation. In fact, TCP permits you to handle a stream, not packets, and so a zero-length data packet is not dangerous for the user program.

### 1.2. Why use TCP keepalive?

There are two target tasks for keepalive:

#### 1.2.1. Checking for dead peers

Keepalive can be used to advise you when your peer dies before it is able to notify you. This could happen for several reasons, like kernel panic or a brutal termination of the process.

Think of a simple TCP connection between Peer A and Peer B: there is the initial three-way handshake, with one SYN segment from A to B, the SYN/ACK back from B to A, and the final ACK from A to B. At this time, we're in a stable status: connection is established, and now we would normally wait for someone to send data over the channel. And here comes the problem: unplug the power supply from B and instantaneously it will go down, without sending anything over the network to notify A that the connection is going to be broken. A, from its side, is ready to receive data, and has no idea that B has crashed. Now restore the power supply to B and wait for the system to restart. A and B are now back again, but while A knows about a connection still active with B, B has no idea. The situation resolves itself when A tries to send data to B over the dead connection, and B replies with an RST packet, causing A to finally to close the connection.

Keepalive can tell you when another peer becomes unreachable without the risk of false-positives. In fact, if the problem is in the network between two peers, the keepalive action is to wait some time and then retry, sending the keepalive packet before marking the connection as broken.

```text
    _____                                                     _____
   |     |                                                   |     |
   |  A  |                                                   |  B  |
   |_____|                                                   |_____|
      ^                                                         ^
      |--->--->--->-------------- SYN -------------->--->--->---|
      |---<---<---<------------ SYN/ACK ------------<---<---<---|
      |--->--->--->-------------- ACK -------------->--->--->---|
      |                                                         |
      |                                       system crash ---> X
      |
      |                                     system restart ---> ^
      |                                                         |
      |--->--->--->-------------- PSH -------------->--->--->---|
      |---<---<---<-------------- RST --------------<---<---<---|
      |                                                         |
```

#### 1.2.2. Preventing disconnection due to network inactivity.

The other useful goal of keepalive is to prevent inactivity from disconnecting the channel.

Returning to Peers A and B, reconnect them. Once the channel is open, wait until an event occurs and then communicate this to the other peer. What if the event verifies after a long period of time? Our connection has its scope, but it's unknown to the proxy. So when we finally send data, the proxy isn't able to correctly handle it, and the connection breaks up.

Because the normal implementation puts the connection at the top of the list when one of its packets arrives and selects the last connection in the queue when it needs to eliminate an entry, periodically sending packets over the network is a good way to always be in a polar position with a minor risk of deletion.

```text
    _____           _____                                     _____
   |     |         |     |                                   |     |
   |  A  |         | NAT |                                   |  B  |
   |_____|         |_____|                                   |_____|
      ^               ^                                         ^
      |--->--->--->---|----------- SYN ------------->--->--->---|
      |---<---<---<---|--------- SYN/ACK -----------<---<---<---|
      |--->--->--->---|----------- ACK ------------->--->--->---|
      |               |                                         |
      |               | <--- connection deleted from table      |
      |               |                                         |
      |--->- PSH ->---| <--- invalid connection                 |
      |               |                                         |
```

## 2. Using TCP keepalive under Linux

Linux has built-in support for keepalive. You need to enable TCP/IP networking in order to use it. The procedures involving keepalive use three user-driven variables:

- `tcp_keepalive_time`: the interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe; after the connection is marked to need keepalive, this counter is not used any further
- `tcp_keepalive_intvl`: the interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime
- `tcp_keepalive_probes`: the number of unacknowledged probes to send before considering the connection dead and notifying the application layer

```shell
$ sysctl -a | grep keepalive

net.ipv4.tcp_keepalive_intvl = 75
net.ipv4.tcp_keepalive_probes = 9
net.ipv4.tcp_keepalive_time = 7200
```
