# OpenStack networking

Source:

- <https://www.openstack.org/blog/ovs-and-ovn-explained-the-networking-stack-behind-openstack/>

## 1. What is SDN?

Software-Defined Networking (SDN) changes the game by separating the control plane from the data plane. A central SDN controller decides where traffic should go, and the underlying switches and routers simply follow those instructions. This separation brings three major benefits to cloud environments:

|                         |                                                                     |
| ----------------------- | ------------------------------------------------------------------- |
| **Benefit**             | Why it matters in cloud environments                                |
| **Centralized control** | You manage network policy centrally, not per-switch                 |
| **Programmability**     | Networks adapt dynamically as VMs are created, migrated, or deleted |
| **Automation**          | No manual switch configuration                                      |

OVS and OVN are SDN technologies. OVS provides the high-performance data plane on each hypervisor. OVN provides the distributed control plane that tells OVS what to do. Together, they implement SDN for OpenStack Neutron.

## 2. What is Open vSwitch?

Open vSwitch (OVS) is an open source virtual switch that speaks OpenFlow, supports tunnel encapsulation (VXLAN, GRE, Geneve), and integrates with KVM, Xen, and other virtualization platforms. Unlike basic Linux bridges, OVS was built for large data center environments: it handles high throughput via a kernel module, gives you visibility with sFlow/NetFlow, and lets you apply QoS per flow.
