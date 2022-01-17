# Katran

- [Katran](#katran)
  - [1. Introduction](#1-introduction)
  - [2. Requirements/Considerations](#2-requirementsconsiderations)
  - [3. Scenarios](#3-scenarios)
    - [3.1. Load balacing network topology](#31-load-balacing-network-topology)
    - [3.2. Load balacing failure scenario](#32-load-balacing-failure-scenario)

Source:

- <https://engineering.fb.com/2018/05/22/open-source/open-sourcing-katran-a-scalable-network-load-balancer>
- <https://www.youtube.com/watch?v=da9Qw7v5qLM>

## 1. Introduction

- Katran is a C++ library and [BPF](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter) program to build high-performance layer 4 load balancing forwarding plane. Katran leverages [XDP infrastructure](https://www.iovisor.org/technology/xdp) from the kernel to provide an in-kernel facility for fast packet's processing.
- Features:
  - Blazing fast (especially w/ XDP in driver mode).
  - Performance scaling linearly with a number of NIC's RX queues.
  - RSS friendly encapsulation.
- The overall architecture of the system is similar to that of the [first-generation L4LB](./1stgenlb.md):
  - [ExaBGP](https://github.com/Exa-Networks/exabgp) announces to the world which VIPs a particular Katran instance is responsible for.
  - Packets destined to a VIP are sent to Katran instances using an [ECMP](https://en.wikipedia.org/wiki/Equal-cost_multi-path_routing) mechanism.
  - Katran selects a backend and forwards the packet to the correct backend server <-- differences
    - Early and efficient packet handling: XDP + BPF
    - Inexpensive and more stable hashing: Extended version of the Maglev hash to select the backend server.
    - More resilient local state
    - [RSS](https://docs.microsoft.com/en-us/windows-hardware/drivers/network/introduction-to-receive-side-scaling)-friendly encapsulation

![](https://engineering.fb.com/wp-content/uploads/2018/05/figure-4.jpg?resize=1536,1007)

## 2. Requirements/Considerations

- katran works only in DSR (direct service response) mode.
- Network topology should be L3 based (everything above the top of the rack switch should be routed). This is because we are 'offloading' routing decision for sending packets to the real server to first routing device (by unconditionally sending all packets from katran there.)
- katran doesn't support fragmentation (it cannot forward the fragmented packet, nor it can fragment them by itself if resulting packet size is bigger then MTU). This could be mitigated either by increasing MTU inside your network or by changing advertising TCP MSS from L7 lbs (this is recommended even if you have increased MTU, as it will prevent fragmentation related issues towards some of the client. For example, if instead of default TCP MSS 1460 (for ipv4) you will advertise 1450 - it will help clients behind PPPoE connection).
- katran doesn't support packets w/ IP options set.
- Maximum packet size cannot be bigger than 3.5k (and 1.5k by default).
- katran is built with the assumption that it's going to be used in a "load balancer on a stick" scenario: where single interface would be used both for traffic "from user to L4 lb (ingress)" and "from L4 lb to L7 lb (egress)

## 3. Scenarios

### 3.1. Load balacing network topology

![](https://github.com/facebookincubator/katran/raw/main/imgs/katran_pktflow.png)

- katran receives packet
- Checks if the destination of the packet is configured as a VIP (virtual IP address - IP address of the service).
- For an incoming packet toward a VIP - katran is checking if it saw packet from the same session before, and if it has - it sends the packet to the same real (actual server/l7 lb which then processes/terminates the TCP session).
- If it's a new session - from 5 tuples in the packet, calculate a hash value.
- Using this hash value - pick a real server.
- Update session table with this lookup information so that katran can simply lookup this information for the next packet in the session and not calculate the hash again.
Encapsulate packet in another IP packet and send to the real.

### 3.2. Load balacing failure scenario

![](https://github.com/facebookincubator/katran/raw/main/imgs/katran_consistency.png)

As we use only the data from the packet's headers to calculate a hash value, which is then used to pick a real server, different L4 lbs are consistent in real server selection, even w/o explicit state sharing amongst each other. This feature allows us to restart/drain single L4 lb w/o affecting TCP sessions, going to the L7 lbs.
