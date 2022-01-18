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
