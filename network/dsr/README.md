# Direct Server Return (DSR)

Source:
- <https://kemptechnologies.com/white-papers/what-is-direct-server-return/>
- <https://www.haproxy.com/blog/layer-4-load-balancing-direct-server-return-mode/>
- <https://www.loadbalancer.org/blog/direct-server-return-is-simply-awesome-and-heres-why/>
- <http://www.linuxvirtualserver.org/VS-DRouting.html>
- <https://debugged.it/blog/ipvs-the-linux-load-balancer/>

- Enables a server to respond directly to clients without having to go through the load balancer, which eliminates a bottleneck in the server-to-client path.
  - Traditional load balancer: client<->load balancer<->server (both request and response). The load balancer in the path of high volume response traffic becomes a bottleneck and adversely affects the communication.
  - DSR: LB sees onlyu the requests and just change the desination MAC address of the packets. The server answers directly to the client using the service IP configured on the loopback interface.

![](https://www.haproxy.com/wp-content/uploads/2011/07/layer4_dsr_data_flow.png)

- Pros
  - Fast
  - LB network bandwidth is not a bottleneck anymore
  - Cost effective
  - No infrastructure changes required
- Cons
  - The service VIP must be configured on a loopback interface on each backend and must not answer to ARP requests
  - No layer 7 advanced fatures are available
  - Persistence will restricted to source IP or desitination IP methods, so no cookies based persistence
- Traffic flow.

![](https://support.kemptechnologies.com/hc/article_attachments/360061899171/DsrFlow.png)

> More detail

- DSR is a method of bypassing the load balancer on the outbound connection. This can increase the performance of the load balancer by significantly reducing the amount of traffic running through the device and its packet rewrite processes. DSR tricks a real server into sending out a packet with the source address already rewritten to the address of the VIP. DSR accomplishes this by manipulating packets on the Layer 2 level to perform SLB. This is done through a process known as MAC Address Translation (MAT).
- MAC addresses are Layer 2 Ethernet hardware  addresses assigned to every Ethernet network interface when they are manufactured. With the exception of redundancy scenarios, MAC address are generally unique and do not change at all with a given device. On Ethernet network, MAC addresses guide IP packets to the correct physical device. They are just another layer of the abstraction of network workings.
- DSR uses a combination of MAT and special real-server configuration to perform SLB without going through the load balancer on the way out. A real server is configured with an IP address, as it would normally be, but it is also given the IP address of the VIP. Normally you cannot have two machines on a network with the same IP address because two MAC addreses can't bind the same IP address. To get around this, instead of binding the VIP address to the network interface, it is bound to the loopback interface.
- A loopback interface is a pseudointerface used for the internal communications of a server and is usually of no consequence to the configuration and utilization of a server. The loopback interface's universal IP address is 127.0.0.1. However, in the same way that you can give a regular interface multiple IP addresses (also known as IP aliases), loopback interfaces can be given IP aliases too. By having the VIP address configured on the loopback interface, we get around the problem of not having more than one machine configured with the same IP on a network. Since the VIP address is on the loopback interface, there is no conflict with other servers as it is not actually on a physical Ethernet network.
- The next step is to actually get traffic to this nonreal VIP interface. This is where MAT comes in.The load balancer takes the traffic on the VIP, and instead of  changing the destination IP address to that of the real server, DSR uses MAT to translate the destination MAC address. The real server would normally drop the traffic since it doesn't have the VIP's IP address, but because the VIP address is configured on the loopback inteface, we trick the server into accepting the traffic. The beauty of this process is that when the server responds and sends the traffic back out, the destination address is already that of the VIP, and sending the traffic unabated directly to the client's IP.
