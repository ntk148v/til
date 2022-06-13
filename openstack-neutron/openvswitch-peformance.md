# How connection tracking in Open vSwitch helps OpenStack performance

Source:

- <https://www.redhat.com/en/blog/how-connection-tracking-open-vswitch-helps-openstack-performance>
- <https://thesaitech.wordpress.com/2019/02/15/a-comparative-study-of-openstack-networking-architectures/>
- <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/10/html/networking_guide/sec-dvr>
- <https://dial.uclouvain.be/memoire/ucl/en/object/thesis:3661/datastream/PDF_01/view>

## 1. Introduction

- Stateful Firewall: requires keep track of the connections to and from the machine.
- It's core of OpenStack's Security Groups. It allows the hypervisor to protect virtual machines from unwanted traffic.
- Connection tracking (conntrack): The host needs to keep track of individual connections and be able to match packets to the connections.
  - Connections are a different concept to flows: connections are bidirectional and need to be established, while flows are unidirectional and stateless.
- Open vSwitch is an advanced programmable software switch. Neutron uses it for OpenStack networking - to connect virtual machines together and to create overlay network connecting the nodes.
- Packet switching in Open vSwitch datapath is based on flows and solely on flows --> stateless --> not a good situation when we need a stateful firewall.

## 2. Bending iptables

- Linux kernel contains connection tracking module and it can be used to implement a stateful firewall.
  - Only available only to the Linux kernel firewall at the IP protocol layer ("iptables").
  - Open vSwitch does not operate at the IP protocol layer, it's at one layer below (L2).
  - Not all packets processed by the kernel are subject to iptables processing.
- In order to still make use of iptables to implement a stateful firewall, it used a trick: Linux bridge contains its own filtering mechanism called ebtables.
  - It's possible to call iptables chains from ebtables.
- Where to put this on the OpenStack packet traversal path? The stateful firewall needs to be inserted between the VM and "integration bridge" (br-int).
  - Insert a Linux bridge between the VM and br-int.

![](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/2016/07/old-ovs-in-openstack.png?itok=UuonfAv3)

- 1st VM is connected to the host through the tap1 interface. A packet coming out of the VM is then directed to the Linux bridge qbr1. On that bridge, ebtables call into iptables where the incoming packet is matched according to configured rules. If the packet is approved, it passes the bridge and is sent out to the second interface connected to the bridge. That's qvb1 which is one side of the veth pair.
- Veth pair is a pair of interfaces that are internally connected to each other. Whatever is sent to one of the interfaces is received by the other one and vice versa. Why the veth pair is needed here? Because we need something that could interconnect the Linux bridge and the Open vSwitch integration bridge.
- Now the packet reached br-int and is directed to the 2nd VM. It goes out of br-int to qvo2, then through qvb2 it reaches the bridge qbr2. The packet goes through ebtables and iptables and finally reaches tap2 which is the target VM.
- This is obviously very complex. All those bridges and interfaces add cost in extra CPU processing and extra latency. The performance suffers.

## 3. Connection tracking in Open vSwitch to the Rescue

- Include the connection tracking directly in Open vSwitch.
- VMs can connect directly to the integration bridge and stateful firewall is implemented just using Open vSwitch rules alone.

![](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/2016/07/new-ovs-conntract.png?itok=xSBgberi)

- A packet coming out of the 1st VM (tap1) is directed to the br-int. It's examined using the configured rules and either dropped or directly output to the 2nd VM (tap2) --> save packet processing costs --> increase performance.
  - Packet enqueueing on veth pair.
  - Bridge processing on per-VM bridge.
  - ebtables overhead: enable tables without any rules configured.
  - iptables overhead: iptables rules are global --> For every packet, incoming interface needs to be checked and execution of rules branched to the set of rules appropriate for the particular interface --> Costly, espacially with a high number of VMs. Open vSwitch hash only global rules, thus we still need to match for the incoming interface, but unlike ipables, the lookup is done using port number and more importantly, using a hash table.

## 4. In Summary

- Without Open vSwitch conntrack:
  - A Linux bridge needs to be inserted between a VM and the integration bridge.
  - This bridge is connected to the integration bridge by a veth pair.
  - Packets traversing the bridge are processed by ebtables and iptables, implementing the stateful firewall.
  - There's substantial performance penalty caused by veth, bridge, ebtables and iptables overhead.
- With Open vSwitch conntrack:
  - VMs are connected directly to the integration bridge.
  - The stateful firewall is implemented directly at the integration bridge using hash tables.
