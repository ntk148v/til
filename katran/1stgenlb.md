# FB 1st generation L4LB

## Components

- VIP announcement: This component simply announces the virtual IP addresses that the L4LB is responsible for to the world by peering with the network element (typically a switch) in front of the L4LB. The switch then uses an equal-cost multipath (ECMP) mechanism to distribute packets among the L4LBs announcing the VIP. We used ExaBGP for the VIP announcement because of its lightweight, flexible design.
- Backend server selection:
  - In order to send all packets from a client to the same backend, the L4LBs use a consistent hash that depends on the 5-tuple (source address, source port, destination address, destination port, and protocol) of the incoming packet -> remove the need for any state synchronization across multiple L4LBs + guarantee minimal disruption to existing connections when a backend leaves/joins the pool of backends.
  - Store backend choice for each 5-tuple as a lookup table to avoid duplicate computation of the hash on future packets.
- Forwarding plane: Once the L4LB picks the appropriate backend, the packets need to be forwarded to that host. To avoid restrictions such as keeping L4LB and backend hosts on the same L2 domain -> [IP-in-IP encapsulation](https://en.wikipedia.org/wiki/IP_in_IP) ([IPVS kernel module](https://en.wikipedia.org/wiki/IP_Virtual_Server)). The backends are configured to have the corresponding VIP on their loopback interface. This allows the backend to send packets on the return path directly to the client (instead of the L4LB). This optimization, often called direct server return (DSR), allows the L4LB to be constrained only by the incoming packet volume.
- Control plane: Performs functions:
  - Provide a simple interface (via a configuration file) to add/remove VIPs.
  - Healthcheck backend servers
  - Provide simple APIs to examine the state of the L4Lb and backendservers

## Drawbacks

- Colocating the L4LB and a backend on a single host increased the chance of device failure.
- L4Lb was a CPU-intensive component.
- Ran L4LBs and backend servers on a disjointed set of machines. (`num of L4LB < num of backends`)
- Packets had to traverse the regular Linux network stack

![](https://engineering.fb.com/wp-content/uploads/2018/05/figure-3.jpg?resize=1024,772)
