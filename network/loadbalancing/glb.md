# GLB: Github's load balancer

Source: <https://github.blog/2018-08-08-glb-director-open-source-load-balancer/>

- [GLB: Github's load balancer](#glb-githubs-load-balancer)
  - [1. Scaling an IP using ECMP](#1-scaling-an-ip-using-ecmp)
  - [2. Split director/proxy load balancer design](#2-split-directorproxy-load-balancer-design)
  - [3. Removing all state from the director tier](#3-removing-all-state-from-the-director-tier)
  - [4. Maintaining invariants: rendezvous hashing](#4-maintaining-invariants-rendezvous-hashing)
  - [5. Draining, filling, adding and removing proxies](#5-draining-filling-adding-and-removing-proxies)
  - [6. Encapsulation within the datacenter](#6-encapsulation-within-the-datacenter)
  - [7. DPDK for 10G+ line rate packet processing](#7-dpdk-for-10g-line-rate-packet-processing)
  - [8. Bringing test suites to DPDK with Scapy](#8-bringing-test-suites-to-dpdk-with-scapy)
  - [9. Healthchecking of proxies for auto-failover](#9-healthchecking-of-proxies-for-auto-failover)
  - [10. Second chance on proxies with iptables](#10-second-chance-on-proxies-with-iptables)
  - [11. Overview](#11-overview)

## 1. Scaling an IP using ECMP

- ECMP: rather than routers picking a single best next hop, where they have multiple hops with the same cost (usually defined as the number of ASes to the destination), they instead hash traffic so that connetions are balanced across available paths of equal cost.

![](https://github.blog/wp-content/uploads/2019/02/ecmp-same-destination.png)

- ECMP is implemented by hashing each packet to determine a relatively consistent selection of one of the available paths.
  - Packets for the same ongoing TCP connection will typically traverse the same path, meaning that packets will arrive in the same order even when paths have different latencies.
- An alternative use of ECMP can come in to play when we want to shard traffic across multiple servers rather than to the same server over multiple paths.
  - Each server can announce the same IP address with BGP or another similar network protocol, causing connections to be sharded across those servers, with the routers blissfully unaware that the connections are being handled in different places, not all ending on the same machine as would traditionally be the case.

![](https://github.blog/wp-content/uploads/2019/02/ecmp-shard-traffic.png)

- Drawback: when the set of servers that are announcing the same IP change, connections must rebalance to maintain an equal balance of connections on each server --> break connections.

![](https://github.blog/wp-content/uploads/2019/02/ecmp-redist-break.png)

## 2. Split director/proxy load balancer design

- Implement some stateful tracking, using a tool like Linux Virtual Server (LVS).
- Create a new tier of "director" servers that take packets from the router via ECMP, but rather than relying on the router's ECMp hashing to choose the backend proxy server, we instead control the hashing and store state (which backend was chosen) for all in-progress connections. When we change the set of proxy tier servers, the director tier hopefully hasn't changed, and our connection will continue.

![](https://github.blog/wp-content/uploads/2019/02/ecmp-redist-lvs-no-state.png)

- Drawback: Add both a LVS director and backend proxy server at the same time. The new director receives some set of packets, but doesn't have any sate yet, so hashes it as a new connection and may get it wrong (and cause the connection to fail) --> Workaround: use [multicast connection syncing](http://www.linuxvirtualserver.org/docs/sync.html) to keep the connection state shared amongst all LVS director servers --> Require connection state to propagate, and also still require duplicate state - not only each proxy need state of each connection in the Linux kernel network stack, but every LVS director also needs to store a mapping of connection to backend proxy server.

## 3. Removing all state from the director tier

- Use the flow state already stored in the proxy servers as part of maintaining established Linux TCP connections from clients.
- For incoming connection, we pick a primary and secondary server that could handle that connection (The hashing to choose is done once, up front, and is stored in a lookup table). When a packet arrives on the primary server and isn't valid, it is forwarded to the secondary server.
- When a new proxy server is added, for 1/N connections it becomes the new primary, and the old primary becomes the secondary. This aallows existing flows to complete, because the proxy server can make the decisions with its local state, the single source of truth.

![](https://github.blog/wp-content/uploads/2019/02/ecmp-redist-glb.png)

- GLB director tier is completely stateless in terms of TCP flows.

## 4. Maintaining invariants: rendezvous hashing

- Static binary forwarding table, which is generated identically on each director server, to map incoming flows to a given primary and secondary server.

![](https://github.blog/wp-content/uploads/2019/02/forwarding-table-active.png)

## 5. Draining, filling, adding and removing proxies

## 6. Encapsulation within the datacenter

## 7. DPDK for 10G+ line rate packet processing

## 8. Bringing test suites to DPDK with Scapy

## 9. Healthchecking of proxies for auto-failover

## 10. Second chance on proxies with iptables

- A netfilter module and iptables taret that runs on every proxy server and allows the "second chance" design to function.
- Decide whether the inner TCP/IP packet inside every GUE packet is valid locally according to the Linux kernel TCP stack,and if it isn't, forwards it to the next proxy server (the secondary) rather than decapsulating it locally.

## 11. Overview

![](https://github.blog/wp-content/uploads/2019/02/glb-component-overview.png)
