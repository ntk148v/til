# Direct Server Return (DSR)

Source:
- <https://kemptechnologies.com/white-papers/what-is-direct-server-return/>
- <https://www.haproxy.com/blog/layer-4-load-balancing-direct-server-return-mode/>
- <https://www.loadbalancer.org/blog/direct-server-return-is-simply-awesome-and-heres-why/>

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
