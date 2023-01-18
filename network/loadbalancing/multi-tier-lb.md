# Multi-tier load-balancing with Linux

Source:

- <https://vincent.bernat.ch/en/blog/2018-multi-tier-loadbalancer>

## 1. [Tier 0] DNS load-balancing

- Optional.
- Useful if your setup is spanned across multiple datacenters, or multiple cloud regions, or if you want to break a large load-balancing cluster into smaller ones.

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-dns.svg)

- [gdnsd](https://gdnsd.org/) is an authoritative-only DNS server with integrated healthchecking.

## 2. [Tier 1] ECMP routing

- On most modern routed IP networks, redundant paths exist between clients and servers. For each packet, routers have to choose a path. When the cost associated to edach path is equal, incoming flows are load-ablanced among the available destinations.

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-ecmp.svg)

- ECMP routing b rings the ability to scale horizontally both tiers.
- A common way to implement such a solution is to use [BGP](../bgp/README.md).
- If we assume you already have BGP-enabled routers available, [ExaBGP](../bgp/exabgp.md) is a flexible solution to let the load-balancers (LBs) advertise their availability.
- Issues:
  - Not resilient when an expected or unexpected change happens. When adding/removing LB, the number of available routes for a desitionation changes -> Flow are reshuffled (hashing) -> break existing connections.

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-ecmp-failure1.svg)

- Each router may choose its own routes. When a router becomes unavailable, the second one maay route the same flows differently.

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-ecmp-failure2.svg)

- Some hardware vendors support resilient hashing.

## 3. [Tier 2] L4 load-balancing

- This tier routes IP datagrams but the scheduler uses both destination IP and port to choose an available L7 LB.
- Ensure all members take the same scheduling decision for an incoming packet.
- 2 options:
  - stateful L4 load-balancing with state synchronization across the members
  - stateless L4 load-balancing with consistent hashing (*)
- Solutions:
  - [IPVS](http://www.linuxvirtualserver.org/software/ipvs.html) + Keepalived + Google Maglev scheduler
  - XDP + Consistent hashing + [Katran](https://engineering.fb.com/open-source/open-sourcing-katran-a-scalable-network-load-balancer/)
  - [GLB Director](https://github.com/github/glb-director) + [Rendezvous hashing](https://en.wikipedia.org/wiki/Rendezvous_hashing)

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-l4.svg)

- Expect packets from a flow to be able to move freely between the components of the first two tiers while sticking to the same L7 LB.
- Add/remov an L4 LB, existing flows are not impacted because each LB takes the same decision, as long as they see the same set of L7 LBs.

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-l4-failure1.svg)

- Add an L7 LB, existing flows are not impacted either because only new connections will be scheduled to it (if we use IPVS, IPVS will look at its local connection table and continue to forward packets to the original destination).

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-l4-failure2.svg)

## 4. [Tier 3] L7 load-balancing

- Provide high availability, by forwarding requests to only healthy backends, and scalability, by spreading requests fairly between them.
- Addition servicesL:
  - TLS termination
  - HTTP routing
  - Header rewriting
  - Rate-limiting
  - ...

![](https://d2pzklc15kok91.cloudfront.net/images/multitier-lb-l7.svg)

- To improve performance, let L7 LB sends back answers directly to the clients without involving the L4 ([Direct server return](../dsr/README.md))
- [HAProxy](https://www.haproxy.org/), [Traefik](https://traefik.io/traefik/), [Envoy](https://www.envoyproxy.io/)...
