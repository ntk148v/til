# Docker networking

Source: https://argus-sec.com/docker-networking-behind-the-scenes/

- [Docker networking](#docker-networking)
  - [1. Concepts](#1-concepts)
  - [2. Deep dive - network namespace](#2-deep-dive---network-namespace)
  - [3. Deep dive - How can containers transfer data to the kernetl, and from there, to outside world?](#3-deep-dive---how-can-containers-transfer-data-to-the-kernetl-and-from-there-to-outside-world)
    - [3.1. Port forwarding](#31-port-forwarding)
    - [3.2. Host networking](#32-host-networking)

## 1. Concepts

- [Network namespace](https://man7.org/linux/man-pages/man8/ip-netns.8.html): by namespacing, the kernel is able to logically separate its processes to multiple different network “areas”. Each network looks like a “standalone” network area, with its own stack, Ethernet devices, routes and firewall rules.
- [Network bridge](https://wiki.archlinux.org/index.php/Network_bridge): switch like virtual device that enables communications between network devices connected to the bridge, creating something kinda LAN.
- **Veth pair**: is basically a virtual network cable which have a virtual network interface device on each end.

## 2. Deep dive - network namespace

![](https://res.cloudinary.com/practicaldev/image/fetch/s--tGvJLH6y--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/i/pszchqfvcjpl13dextrc.png)

- When Docker creates and runs a container, it creates a separate network namespace and puts the container into it. Then, Docker connects the new container network to linux bridge **docker0** using a veth pair. This also enables container be conneted to the host network and other container networks in the same bridge.
- By default Docker does not add container network namespaces to the linux runtime data which is what you see when you run the `ip netns` command.

```bash
$ sudo ip netns list
# Start a container
$ docker run --name nstest -it busybox
# Get container process id.
$ pid="$(docker inspect -f '{{.State.Pid}}' nstest)"
# Soft link the network namespace
$ sudo mkdir -p /var/run/netns/
$ sudo ln -sf /proc/$pid/ns/net /var/run/netns/nstest
$ sudo ip netns
nstest (id: 4)
$ sudo ip netns exec nstest ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
139912: eth0@if139913: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
$ ip a | grep docker
6: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
139913: veth24b6563@if139912: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
91788: veth571cae6@if91787: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP group default
$ ip a | grep 139913
139913: veth24b6563@if139912: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
$ brctl show
bridge name       bridge id           STP enabled     interfaces
docker0           8000.02421e03fc8a   no              veth24b6563
docker_gwbridge   8000.0242358d533d   no              veth571cae6
virbr0            8000.52540011765c   yes             virbr0-nic
```

## 3. Deep dive - How can containers transfer data to the kernetl, and from there, to outside world?

- Port forwarding - forwards traffic on a **specific** port from a container to the kernel.
- Host networking - disables the **network namepspace stack** isolation from the Docker host.

- You can see 5 rule sections (chains): **PREROUTING**, INPUT, OUTPUT, **POSTROUTING** and **DOCKER**.
  - PREROUTING: rules altering packets before they come into the network stack (immediately after being received by an interface).
  - POSTROUTING: rules altering packets before they go out from the network stack (right before leaving an interface).
  - DOCKER: rules altering packets before they enter/leave the Docker bridge interface.

```bash
$ sudo iptables -t nat -L -n
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0
MASQUERADE  all  --  172.19.0.0/16        0.0.0.0/0
LIBVIRT_PRT  all  --  0.0.0.0/0            0.0.0.0/0

Chain DOCKER (2 references)
target     prot opt source               destination
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
```

- The PREROUTING rules lists any packet targeting the DOCKER rules section, before they enter the interface network stack. Currently, the only rule is RETURN (returns back to the caller). The POSTROUTING describes how each source IP in the Docker subnet (e.g. 172.17.X.X) will be targeted as MASQUERADE when sent to any destination IP, which overrides the source IP with the interface IP.

### 3.1. Port forwarding

```bash
$ docker run -p 5000:5000 --rm -it python:3.7-slim python3 -m http.server 5000 --bind=0.0.0.0
$ sudo iptables -t nat -L -n
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0
MASQUERADE  all  --  172.19.0.0/16        0.0.0.0/0
LIBVIRT_PRT  all  --  0.0.0.0/0            0.0.0.0/0
# MASQUERADE is like SNAT (source NAT) target, but instead of overriding
# the source IP with static/elastic inet IP as "to-source" option, the
# external IP of the inet interface is determined dynamically by an algorithm.
# Back to our case, the traffic from IP address 172.17.0.2 (the container IP)
# on dpt (destination port) 5000 will be directed to the interface IP.
MASQUERADE  tcp  --  172.17.0.2           172.17.0.2           tcp dpt:5000

Chain DOCKER (2 references)
target     prot opt source               destination
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
# A new DNAT (destination NAT) target. DNAT is commonly used to publish a
# service from internal network to an external IP. The rule states that each
# IP packet from any IP on destination port 5000 will be altered to internal
# IP 172.17.0.2 on port 5000.
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:5000 to:172.17.0.2:5000
```

- Perform an http request.

```bash
$ curl -XGET http://localhost:5000
$ docker logs -f <python3.7-container-name>
Serving HTTP on 0.0.0.0 port 5000 (http://0.0.0.0:5000/) ...
172.17.0.1 - - [04/Mar/2021 03:38:57] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [04/Mar/2021 03:39:21] "GET / HTTP/1.1" 200 -
# - HTTP destination IP is localhost (127.0.0.1). The source IP is also localhost, and therefore the request is sent on the loopback interface.
# - As for the PREROUTING NAT rule – for any IP (including 127.0.0.1), an interface (e.g. loopback) chains the request to the DOCKER target.
# - In the DOCKER chain there is a DNAT rule. The rule alters the packet destination to 172.17.0.2:5000.
# - The POSTROUTING rule masquerades packets with source IP 172.17.0.2 and port 5000 by changing the source IP to the interface IP. As a result of this modification, the packet transfers through the docker0 interface.
# - Now, the packet has arrived at the docker0 interface (after rules 3+5 were applied on the packet). With the support of the veth tunnel, the gateway IP (172.17.0.1, which is effectively the packet source) now establishes a TCP connection with the container IP (172.17.0.2).
# - The webserver binds IP 0.0.0.0 and listens to port 5000, therefore it receives all the frames on its eth0 interface and answers the request.
```

### 3.2. Host networking

```bash
$ docker run --net=host --rm -it python:3.7-slim python3 -m http.server 5000 --bind=0.0.0.0
$ sudo iptables -t nat -L -n                                                                                                                                                                        ~
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
# Here here
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0
MASQUERADE  all  --  172.19.0.0/16        0.0.0.0/0
LIBVIRT_PRT  all  --  0.0.0.0/0            0.0.0.0/0

Chain DOCKER (2 references)
target     prot opt source               destination
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
```

- POSTROUTING — the MASQUERADE rule for IP 127.17.0.2 is eliminated.
- DOCKER — there is a new DNAT target rule that is eliminated as well.

- Perform an http request.

```bash
$ curl -XGET http://localhost:5000
$ docker logs -f <python3.7-container-name>
Serving HTTP on 0.0.0.0 port 5000 (http://0.0.0.0:5000/) ...
127.0.0.1 - - [04/Mar/2021 03:46:41] "GET / HTTP/1.1" 200 -
# - HTTP destination IP is localhost (127.0.0.1). The source IP is also localhost, and therefore the request is sent on the loopback interface.
# - As for the PREROUTING NAT rule – for any IP (including 127.0.0.1), an interface (e.g. loopback) chains the request to the DOCKER target.
# - The DOCKER chain only has a RETURN target for any IP, so no rule applied here and the rule returns the routing decision to the caller target.
# - The POSTROUTING rule masquerades all the packets source IP on subnet 172.17.0.0/16 to the interface inet, the loopback interface IP (127.0.0.1).
# - We are left with the source IP 127.0.0.1 and destination IP 0.0.0.0 on port 5000, in the same network stack, which leaves the packet in the loopback interface and the webserver running as it would run on the OS kernel itself.
```
