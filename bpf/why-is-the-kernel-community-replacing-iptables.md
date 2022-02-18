# Why is the kernel community replacing iptables with BPF?

Source: <https://cilium.io/blog/2018/04/17/why-is-the-kernel-community-replacing-iptables>

- [bpfilter](https://lwn.net/Articles/747551/) replaces the long-standing in-kernel implementation of iptables with high-performance network filtering powered by Linux BPF.
- iptables - primary tool to implement firewalls and packet filters on Linux for many years.
  - Flexibility and quick fixes
  - Debug a 5k rules iptables setup... bruh :cursing_face:
  - Lack of incremental updates: The entire list of rules has to be replaced each time a new rule is added
  - IP/port based mechanisms
  - Simple scope:
    - Protect local applications from receiving unwanted network traffic (INPUT chain)
    - Protect local applications sending undesired network traffic (OUTPUT chain)
    - Filter network traffic forwarded/routed by a Linux system (FORWARD chain).
- [ipset](http://ipset.netfilter.org/) allows to compress list of rules matching on IP addresses and/or port combinations into a hash table to reduce the number of iptables rules overall.
- The following graph as presented by Quentin Monnet at FRnOG 30 shows some early measurements of bpfilter in comparison with iptables and nftables.

![](https://cilium.io/static/85849c12cb9c051c9534710e3c6da493/2d289/bpfilter_performance.png)
