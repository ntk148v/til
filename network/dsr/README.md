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
- Disable ARP for VIP.

```
arp_announce - INTEGER
	Define different restriction levels for announcing the local
	source IP address from IP packets in ARP requests sent on
	interface:
	0 - (default) Use any local address, configured on any interface
	1 - Try to avoid local addresses that are not in the target's
	subnet for this interface. This mode is useful when target
	hosts reachable via this interface require the source IP
	address in ARP requests to be part of their logical network
	configured on the receiving interface. When we generate the
	request we will check all our subnets that include the
	target IP and will preserve the source address if it is from
	such subnet. If there is no such subnet we select source
	address according to the rules for level 2.
	2 - Always use the best local address for this target.
	In this mode we ignore the source address in the IP packet
	and try to select local address that we prefer for talks with
	the target host. Such local address is selected by looking
	for primary IP addresses on all our subnets on the outgoing
	interface that include the target IP address. If no suitable
	local address is found we select the first local address
	we have on the outgoing interface or on all other interfaces,
	with the hope we will receive reply for our request and
	even sometimes no matter the source IP address we announce.

	The max value from conf/{all,interface}/arp_announce is used.

	Increasing the restriction level gives more chance for
	receiving answer from the resolved target while decreasing
	the level announces more valid sender's information.

arp_ignore - INTEGER
	Define different modes for sending replies in response to
	received ARP requests that resolve local target IP addresses:
	0 - (default): reply for any local target IP address, configured
	on any interface
	1 - reply only if the target IP address is local address
	configured on the incoming interface
	2 - reply only if the target IP address is local address
	configured on the incoming interface and both with the
	sender's IP address are part from same subnet on this interface
	3 - do not reply for local addresses configured with scope host,
	only resolutions for global and link addresses are replied
	4-7 - reserved
	8 - do not reply for all local addresses

	The max value from conf/{all,interface}/arp_ignore is used
	when ARP request is received on the {interface}
```

```bash
net.ipv4.conf.eth0.arp_ignore = 1
net.ipv4.conf.eth0.arp_announce = 2
```
