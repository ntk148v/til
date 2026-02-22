# LVS - Linux Virtual Server

- [LVS - Linux Virtual Server](#lvs---linux-virtual-server)
  - [1. Introduction](#1-introduction)
  - [2. LVS scheduling algorithms](#2-lvs-scheduling-algorithms)
  - [3. Three dispatching modes of LVS](#3-three-dispatching-modes-of-lvs)
    - [3.1. LVS NAT](#31-lvs-nat)
    - [3.2. LVS DR](#32-lvs-dr)
    - [3.3. LVS TUN](#33-lvs-tun)

Source:

- <http://www.linuxvirtualserver.org/about.html>
- <http://www.linuxvirtualserver.org/Documents.html>
- <https://programmer.group/lvs-load-balancing.html>
- <https://www.codetd.com/en/article/9370382>
- <http://www.austintek.com/LVS/LVS-HOWTO/>

## 1. Introduction

- Build a high-performance and high available server for Linux using clustering technology, which provides good scalability, reliability and serviceability.
- LVS Framework

![](http://www.linuxvirtualserver.org/lvs_framework.jpg)

- IPVS: is an advanced IP load balancing software implemented inside the Linux kernel. The IPVS code was already included into the standard Linux kernel 2.4 and 2.6.
- KTCPVS: implements application-level load balancing inside the Linux kernel, currently under development.

- LVS working modes are divided into NAT mode, TUN mode, DR mode and Full NAT mode.
- Working principle of LVS

![](https://programmer.group/images/article/baee7a4c35abb85aa97718cb27494e34.jpg)

- When the user sends a request to the load balancing scheduler (Direct Server), the scheduler sends the request to the kernel space.
- The provisioning chain will first receive the user request, judge the target IP, determine the local IP, and send the data packet to the INPUT chain.
- IPVS works on the INPUT chain. When the user request reaches the INPUT, IPVS will compare the user request with the defined cluster service. If the user requests the defined cluster service, IPVS will forcibly modify the target IP address and port in the packet and send the new packet to the POSTROUTING chain.
- After the POSTROUTING link receives the data packet, it is found that the target IP address is just its own back-end server. At this time, the data packet is finally sent to the back-end server through routing.

## 2. LVS scheduling algorithms

- Static algorithm scheduling:
  - round robin scheduling (RR)
  - weighted round robin scheduling (WRR)
  - source hash scheduling (SH)
  - destination hash (TH)
  - maglev hash (MH): Check [here](https://blog.acolyer.org/2016/03/21/maglev-a-fast-and-reliable-software-network-load-balancer/)
- Dynamic algorithm scheduling
  - least connection scheduling (LC)
  - weighted least connection scheduling (WLC)
  - locality based LC (LBLC)
  - locality based least connection with replication (LBLCR)
  - short expectation delay (SED)
  - nevel queue (NQ)

## 3. Three dispatching modes of LVS

### 3.1. LVS NAT

![](https://programmer.group/images/article/d861020b9a5606cf64c62e6429b6937f.jpg)

- Flows:
  - When the user request arrives at the Director Server, the requested data message will first arrive at the preouting chain in the kernel space. At this time, the source IP of the message is CIP and the target IP is VIP
  - The preouting check finds that the destination IP of the packet is local, and sends the packet to the INPUT chain
  - IPVS compares whether the service requested by the packet is a cluster service. If so, modify the target IP address of the packet to the back-end server IP, and then send the packet to the POSTROUTING chain. At this time, the source IP of the message is CIP and the target IP is RIP
  - The POSTROUTING chain sends packets to the Real Server through routing
  - The Real Server compares and finds that the target is its own IP, starts to build a response message and sends it back to the Director Server. At this time, the source IP of the message is RIP and the target IP is CIP
  - Before responding to the client, the Director Server will modify the source IP address to its own VIP address, and then respond to the client. At this time, the source IP of the message is VIP and the target IP is CIP

- Advantages:
  - Support port mapping
  - RS can use any operating system
  - Save public IP address.
  - And DIP RIP should use the same private network address, and RS gateway to point DIP.
  - Use nat Another benefit is that the backend host relatively safe.
- Disadvantages:
  - Request and response packets go through the Director forwards; when a high load, Director could become a system bottleneck (that is inefficient means).

### 3.2. LVS DR

![](https://programmer.group/images/article/d923f0f6bd8fe876afd989646fa2f411.jpg)

- Flows:
  - When the user request arrives at the Director Server, the requested data message will first arrive at the preouting chain in the kernel space. At this time, the source IP of the message is CIP and the target IP is VIP
  - The preouting check finds that the destination IP of the packet is local, and sends the packet to the INPUT chain
  - IPVS compares whether the service requested by the packet is a cluster service. If so, modify the source MAC address in the request message to the MAC address of DIP, modify the target MAC address to the MAC address of RIP, and then send the packet to the POSTROUTING chain. At this time, the source IP and destination IP are not modified. Only the MAC address whose source MAC address is DIP and the destination MAC address is RIP are modified
  - Since DS and RS are in the same network, they are transmitted through layer 2. The POSTROUTING chain checks that the target MAC address is the MAC address of RIP, and then the packet will be sent to the Real Server.
  - When RS finds that the MAC address of the request message is its own MAC address, it receives the message. After processing, the response message is transmitted to eth0 network card through lo interface, and then sent out. At this time, the source IP address is VIP and the target IP is CIP
  - The response message is finally delivered to the client
- Advantages:
  - RIP can use private addresses, you can also use public addresses.
  - DIP RIP and requires only the address of the same network segment.
  - Scheduling request message via the Director, but no response packet via the Director.
  - RS can use most OS
- Disadvantages:
  - It does not support port mapping.
  - Not across the LAN.

### 3.3. LVS TUN

![](https://programmer.group/images/article/cda100ed429579984caece170cafb845.jpg)

- Flows:
  - When the user request arrives at the Director Server, the requested data message will first arrive at the preouting chain in the kernel space. At this time, the source IP of the message is CIP and the target IP is VIP.
  - The preouting check finds that the destination IP of the packet is local, and sends the packet to the INPUT chain
  - IPVS compares whether the service requested by the packet is a cluster service. If so, encapsulate a layer of IP message at the head of the request message. The encapsulated source IP is DIP and the target IP is RIP. Then it is sent to the POSTROUTING chain. At this time, the source IP is DIP and the destination IP is RIP
  - The POSTROUTING chain sends the data packet to the RS according to the latest encapsulated IP message (because there is an additional layer of IP header encapsulated in the outer layer, it can be understood that it is transmitted through the tunnel at this time). At this time, the source IP is DIP and the destination IP is RIP
  - After receiving the message, RS finds that it is its own IP address, so it receives the message. After removing the outermost IP, it will find that there is another layer of IP header inside, and the target is its own lo interface VIP. At this time, RS starts to process the request. After processing, it will send it to eth0 network card through lo interface, and then transfer it outward. At this time, the source IP address is VIP and the target IP is CIP
  - The response message is finally delivered to the client
- Advantages:
  - RIP, VIP, DIP should use the public network address, the gateway does not point to the DIP and the RS;
  - Only accept incoming requests, to solve the problem of LVS-NAT, reduce the load.
  - Scheduling request message via the Director, but without a response packet via the Director.
- Disadvantages:
  - Director does not point so I do not support port mapping.
  - RS's OS must support tunneling.
  - Tunneling extra cost performance, increased overhead.
