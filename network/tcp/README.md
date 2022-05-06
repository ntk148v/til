# TCP

Source: <https://sookocheff.com/post/networking/how-does-tcp-work/>

> TCP = transmission control protocol

## 1. TCP Segments

- TCP divides a stream of data into chunks, and then adds a TCP header to each chunk to create a TCP segment
- Format [RFC 793](https://tools.ietf.org/html/rfc793)

```
0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgement Number                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## 2. Establishing a TCP connection - 3-way handshake

- SYN:
  - The client picks a random sequence number x
  - The client sends a packet with the `SYN` flag set and the `Sequence Number` field set to x.
- SYN-ACK
  - The server increments x by one
  - The server picks a random sequence number y
  - The server sends a packet with the `SYN` and `ACK` flags set, the `Sequence Number` field set to y, and the `Acknowledgement Number` field set to x.
- ACK
  - The client increments x and y by one.
  - The client sends a packet with the `ACK` flag sent, the `Sequence Number` field set to x, and the `Acknowledgement Number` field set to y.

![](https://sookocheff.com/post/networking/how-does-tcp-work/assets/three-way-handshake.png)

## 3. Sending Data

- TCP uses sequence numbers to verify the correct delivery and ordering of TCP segments.

![](https://sookocheff.com/post/networking/how-does-tcp-work/assets/sending-data.png)

## 4. Closing a connection

- To close a TCP connection, a sender transmits a packet with the `FIN` flag set, indicating that the sender has no more data it wishes to send.
- After receipt of a `FIN` segment the receiver should refuse any additional data from the client.
