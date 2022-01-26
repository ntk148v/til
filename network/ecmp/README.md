# Equal-cost multi-path routing (ECMP)

Source:

- <https://en.wikipedia.org/wiki/Equal-cost_multi-path_routing>
- <https://tools.ietf.org/html/rfc2992>

## 1. What is ECMP?

- A routing strategy where packets towards a single destination IP address are load-balanced over multiple best paths with equal metrics.
- Multi-path routing can be used in conjunction with most routing protocols because it is a per-hop local decision made independently at each router. It can substantially increase bandwidth by load balancing traffic over multiple paths; however, there may be significant problems in deploying it in practice.
- RFC 2992 analyzed one particular multipath routing strategy involving the assignment of flows through hashing flow-related data in the packet header, called hash-threshold.
  - The router first selects a key by performing a hash (e.g., CRC16) over the packet header fields that identify a flow.
  - The N next-hops have been assigned unique regions in the key space
  - The router uses the key to determine which region and thus which next-hop to use
- ECMP hashing

```
hash(5tuple) % number of paths
```

![](https://cdn.haproxy.com/wp-content/uploads/2020/02/4.-Equal-cost-multi-path-routing.png)

- Pros
  - Easy to scale out
- Cons
  - Only "equal" load balancing is possible (can't run different generation of hardware)
  - Massive rehashing in case of maintenance/"draining" of a backend

## 2. BGP and ECMP

- Bandwidth will increase -> Gigabit ethernet link that provided bandwidth to spare a year ago may be insufficient -> solution?
  - Upgrade to faster link.
  - Use links in parallel -> ECMP
- How traffic is split over multiple parallel links.
  - Transmit packet 1 over link A, packet 2 over link B, packet 3 over link A, packet 4 over link B, and so on (**per-packet** load balancing)
  - Problem: packets 1, 3 and 4 are 1500-byte data packets that belong to the same TCP session, but packet 2 is a small TCP ACK packet, packet 3 has to wait for packet 1 to be transmitted, but packet 4 doesn't have to wait nearly as long behind the much shorter packet 2 -> packet 4 ends up being transmitted before packet 3.
  - Per-packet load balancing causes reordering. In theory, that's fine, as TCP will simply buffer the reordered packets and deliver the data inside to the receiving application in the right order. However, receiving packets out of order makes TCP think there was packet loss, so it retransmits packets and slows down its transmission rate -> Routers and switches work hard to make sure that all packets that belong to the same TCP session (or UDP flow) are transmitted over the same link.
  - Single TCP session can only make use of 1 link -> ECMP is only useful if the traffic consists of multiple TCP sessions.
- Perform load balancing is based on the 3-tuple: the protocol number in the IP header and the IP source and destination addresses -> best way is using the 5-tuple: the protocol number, the IP addresses and the TCP or UDP source and destination port numbers.
  - Routers and switches implementing ECMP calculate a hash function over these fields and the use (part of) the resulting hash value to select the link to transmit.
  - In the practice, it can still take as many as a thousand TCP sessions before all the links are utilized equally.
- Before the ECMP algorithm can distribute packets over parallel links, routing protocols such as BGP must first be convinced to use mutiple links in parallel. There are 3 ways BGP and ECMP can work together:
  - Bundling the links at the Ethernet level, using IEEE 802.3ad or **EtherChannel**.
  - With one BGP session oever mutiple links using loopback addresses
  - With a separate BGP session over each of the parallel links
- 1st: EtherChannel is a proprietary Cisco mechanism to allow multiple Ethernet ports to be used as if it's a single, higher-bandwidth port. In 2000, the IEEE standardized a very similar mechanism under the name 802.3ad (Link Aggregation Control Protocol (LACP), with negotiates the bundling of Ethernet ports. By foregoing LACP and  grouping the ports statically, it's usually possible to make different implementations like 802.3ad and EtherChannel and other link bundling mechanisms from other vendors work together.
  - Bundled ports are a single interface with a single IP address. So BGP can simply be configured as usual and the traffic is distributed over the ports using the ECMP algorithm.
- 2nd: an alternative is to configure each port with its own IP subnet, but then still run a single BGP session over the collection of ports.
  - 2 GE interfaces have subnets 10.0.1.0/30 and 10.0.2.0/30.
  - The local router also has IP address 192.168.0.1/32 configured on its loopback interface.
  - Address 172.16.31.2 is the loopback interface of the router at the other end of both Gigabit Ethernet links.
  - To make sure the BGP updates use the loopback address on our end, we configure *update-source loopback0*
  - We also need *ebgp-multihop 2* because the extra level of indirection may lead the router to think there's an extra router on the path.
  - BGP session will come up and prefixes learned over the session will have as their  next hop addres 172.16.31.2. This address points to both of the GE ports, so packets will be load balanced over both ports using ECMP

```
!
interface GigabitEthernet0/1
ip address 10.0.1.1 255.255.255.252
interface GigabitEthernet0/2
ip address 10.0.2.1 255.255.255.252
interface loopback0
ip address 192.168.0.1 255.255.255.255
!
ip route 172.16.31.2 255.255.255.255 10.0.1.2
ip route 172.16.31.2 255.255.255.255 10.0.2.2
!
router bgp 123
neighbor 172.16.31.2 remote-as 456
neighbor 172.16.31.2 update-source loopback0
neighbor 172.16.31.2 ebgp-multihop 2
!
```

- 3rd: Run BGP over multiple links is to simply configure a BGP session over each link:
  - BGP would now have two copies of each prefix: one learned from neighbor 10.0.1.2 and one from neighbor 10.0.2.2 and then try to figure out which of these is best. Eventually this will come down to the tie breaker rules and one will win.
  - With *maximum-paths 2* in effect, the router will install two copies of a route in the main routing table, which will trigger ECMP between the two routes.

```
!
interface GigabitEthernet0/1
ip address 10.0.1.1 255.255.255.252
!
interface GigabitEthernet0/2
ip address 10.0.2.1 255.255.255.252
!
router bgp 123
neighbor 10.0.1.2 remote-as 456
neighbor 10.0.2.2 remote-as 456
maximum-paths 2
!
```
