# Docker networking

> A clumsy Docker networking notes.

Source:

- <https://argus-sec.com/docker-networking-behind-the-scenes/>
- <https://docs.docker.com/network/>
- <https://github.com/KamranAzeem/learn-docker/blob/master/docs/docker-networking-deep-dive.md>
- <https://docs.docker.com/engine/tutorials/networkingcontainers/>
- <https://docs.docker.com/network/iptables/>

Table of Contents:

- [Docker networking](#docker-networking)
  - [1. Concepts](#1-concepts)
  - [2. Deep dive - network namespace](#2-deep-dive---network-namespace)
  - [3. Docker networking subsystem](#3-docker-networking-subsystem)
    - [3.1. docker0 - default bridge network](#31-docker0---default-bridge-network)
    - [3.2. User-defined bridge network](#32-user-defined-bridge-network)
    - [3.3. Composed-defined bridge network](#33-composed-defined-bridge-network)
    - [3.4. Other aspect of bridge networks](#34-other-aspect-of-bridge-networks)
    - [3.5. Host network](#35-host-network)
    - [3.6. None network](#36-none-network)
    - [3.7. Interesting things](#37-interesting-things)
  - [4. Deep dive - How can containers transfer data to the kernel, and from there, to outside world?](#4-deep-dive---how-can-containers-transfer-data-to-the-kernel-and-from-there-to-outside-world)
    - [4.1. Port forwarding](#41-port-forwarding)
    - [4.2. Host networking](#42-host-networking)
  - [5. Restrict connections - Docker and iptables](#5-restrict-connections---docker-and-iptables)

## 1. Concepts

- [Network namespace](https://man7.org/linux/man-pages/man8/ip-netns.8.html): by namespacing, the kernel is able to logically separate its processes to multiple different network “areas”. Each network looks like a “standalone” network area, with its own stack, Ethernet devices, routes and firewall rules.
- [Network bridge](https://wiki.archlinux.org/index.php/Network_bridge): switch like virtual device that enables communications between network devices connected to the bridge, creating something kinda LAN. In the case you're wondering, **a software bridge is bridge is just another name for a (software) network switch**.
- **Veth pair**: is basically a virtual network cable which have a virtual network interface device on each end.

## 2. Deep dive - network namespace

![](https://res.cloudinary.com/practicaldev/image/fetch/s--tGvJLH6y--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/i/pszchqfvcjpl13dextrc.png)

- When Docker creates and runs a container, it creates a separate network namespace and puts the container into it. Then, Docker connects the new container network to linux bridge **docker0** using a veth pair. This also enables container be conneted to the host network and other container networks in the same bridge.
- By default Docker does not add container network namespaces to the linux runtime data which is what you see when you run the `ip netns` command.

```shell
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

## 3. Docker networking subsystem

- Docker’s networking subsystem is pluggable, using drivers. Several drivers exist by default, and provide core networking functionality.
- The following networks are available to you _by default_, when you install Docker on your computer:
  - `bridge`: The default network driver. If you don't specify a driver, this is the type of network are creating. Bridge networks are usually used when your applications run in standalone containers that need to communicate.
  - `host` - Uses host network: For standalone containers, remove network isolation between container and the Docker host, the use the host's networking directly.
  - `none` - isolated/no networking:
- Other Docker network available, but are not covered in this document:
  - `overlay` - Swarm mode: Overlay networks connect multiple Docker daemons together and enable swarm services to communicate with each other. You can also use overlay networks to facilitate communication between a swarm service and a standalone container, or between two standalone containers on different Docker daemons. This strategy removes the need to do OS-level routing between these containers
  - `macvlan` - legacy applications needing direct connection to physical network: Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. The Docker daemon routes traffic to containers by their MAC addresses. Using the macvlan driver is sometimes the best choice when dealing with legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host’s network stack.
  - `ipvlan`: IPvlan networks give users total control over both IPv4 and IPv6 addressing. The VLAN driver builds on top of that in giving operators complete control of layer 2 VLAN tagging and even IPvlan L3 routing for users interested in underlay network integration.
  - 3rd party network plugins.

### 3.1. docker0 - default bridge network

![](https://docs.docker.com/engine/tutorials/bridge1.png)

- By default, all containers are connected to the default bridge network, unless explicitly configured to connect to some other network.
- Containers talk to the docker host and outside world (`ip_fowrad=1` and NAT).
- Docker host can talk to all containers using their IP addresses.
- The (default) bridge network (interface) is visible/available on the host computer as `docker0`.
- At start up, Docker engine finds an unused network subnet on the docker host and assigns the first IP address of that nework to the default bridge.
- There is no **service discovery** on default bridge.
- `docker0` state is DOWN when there are no running containers attached to this network interface/bridge.
- Communications on the default bridge:
  - The container inherits the DNS setting of the Docker daemon, including the `/etc/hosts` and `/etc/resolv.conf`.
  - Since there is no service discovery, containers must know IP of each other to be able to talk.

### 3.2. User-defined bridge network

- User can create their own docker network.
- Create a bridge network:

```shell
$ docker network create mynet
$ docker network ls
$ docker network inspect mynet
# Check with ip addr show, it should show up as a network
# inteface on the host with the name br-<random-string>
$ ip addr show
```

- DNS-based service discovery:

```shell
$ docker run --name=web --network=mynet -d wbitt/network-multitool
e2d841b7a02916aa25a2fa5ceace0427ad7c0ccc967ad01fb5cc423460f0e990

$ docker run --name=db --network=mynet -e MYSQL_ROOT_PASSWORD=secret -d mysql
492ba8a9277d96876f0a605d9434723aed774978a40023e778a97815216754f0

$ docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED              STATUS              PORTS                                  NAMES
e2d841b7a029   wbitt/network-multitool   "/bin/sh /docker/ent…"   15 seconds ago       Up 14 seconds       80/tcp, 443/tcp, 1180/tcp, 11443/tcp   web
492ba8a9277d   mysql                     "docker-entrypoint.s…"   About a minute ago   Up About a minute   3306/tcp, 33060/tcp                    db

# Ping each other
$ docker exec -it web bash
e2d841b7a029:/# ping -c 1 db
PING db (172.18.0.2) 56(84) bytes of data.
64 bytes from db.mynet (172.18.0.2): icmp_seq=1 ttl=64 time=0.096 ms

--- db ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.096/0.096/0.096/0.000 ms
e2d841b7a029:/# dig db

; <<>> DiG 9.18.16 <<>> db
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57615
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;db.                            IN      A

;; ANSWER SECTION:
db.                     600     IN      A       172.18.0.2

;; Query time: 0 msec
;; SERVER: 127.0.0.11#53(127.0.0.11) (UDP)
;; WHEN: Tue Dec 12 03:18:39 UTC 2023
;; MSG SIZE  rcvd: 38

e2d841b7a029:/#
```

- There is an **embedded DNS** in the Docker service.

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/docker-service-discovery-2.png)

```shell
$ docker exec -it web bash
e2d841b7a029:/# cat /etc/resolv.conf
nameserver 127.0.0.11
options edns0 trust-ad ndots:0
e2d841b7a029:/# netstat -ntlup
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.11:45541        0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      1/nginx: master pro
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1/nginx: master pro
udp        0      0 127.0.0.11:42758        0.0.0.0:*
```

- The `/etc/resolv.conf` says that the DNS is available at `127.0.0.1:53` but the netstat output doesn't show any process listening on port 53.
- Create a new container with more _powers_.
  - The ports 33715 and 41120 do not look like DNS server ports.
  - Check iptables magic: Any DNS query traffic looking for `127.0.0.1:53` is redirected to `127.0.0.1:33715` (TCP), and to `127.0.0.1:41120` (UDP).
  - There is a Docker process running on these ports inside the container, which are actually Docker's embedded DNS's hooks.

```shell
$ docker run \
    --name tool \
    --network mynet \
    --cap-add=NET_ADMIN \
    --cap-add=NET_RAW \
    -it wbitt/network-multitool /bin/bash
ccd72fe225c8:/# dig -c db
;; Warning, ignoring invalid class db

; <<>> DiG 9.18.16 <<>> -c db
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 17778
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;.                              IN      NS

;; ANSWER SECTION:
.                       31133   IN      NS      d.root-servers.net.
.                       31133   IN      NS      l.root-servers.net.
.                       31133   IN      NS      k.root-servers.net.
.                       31133   IN      NS      i.root-servers.net.
.                       31133   IN      NS      j.root-servers.net.
.                       31133   IN      NS      e.root-servers.net.
.                       31133   IN      NS      h.root-servers.net.
.                       31133   IN      NS      g.root-servers.net.
.                       31133   IN      NS      a.root-servers.net.
.                       31133   IN      NS      f.root-servers.net.
.                       31133   IN      NS      c.root-servers.net.
.                       31133   IN      NS      b.root-servers.net.
.                       31133   IN      NS      m.root-servers.net.

;; Query time: 8 msec
;; SERVER: 127.0.0.11#53(127.0.0.11) (UDP)
;; WHEN: Tue Dec 12 03:20:07 UTC 2023
;; MSG SIZE  rcvd: 239

ccd72fe225c8:/# netstat -ntlup
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.11:39527        0.0.0.0:*               LISTEN      -
udp        0      0 127.0.0.11:35031        0.0.0.0:*                           -
ccd72fe225c8:/# iptables-nft-save
# Generated by iptables-nft-save v1.8.9 (nf_tables) on Tue Dec 12 03:20:27 2023
*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
:DOCKER_OUTPUT - [0:0]
:DOCKER_POSTROUTING - [0:0]
-A OUTPUT -d 127.0.0.11/32 -j DOCKER_OUTPUT
-A POSTROUTING -d 127.0.0.11/32 -j DOCKER_POSTROUTING
-A DOCKER_OUTPUT -d 127.0.0.11/32 -p tcp -m tcp --dport 53 -j DNAT --to-destination 127.0.0.11:39527
-A DOCKER_OUTPUT -d 127.0.0.11/32 -p udp -m udp --dport 53 -j DNAT --to-destination 127.0.0.11:35031
-A DOCKER_POSTROUTING -s 127.0.0.11/32 -p tcp -m tcp --sport 39527 -j SNAT --to-source :53
-A DOCKER_POSTROUTING -s 127.0.0.11/32 -p udp -m udp --sport 35031 -j SNAT --to-source :53
COMMIT
# Completed on Tue Dec 12 03:20:27 2023
```

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/docker-service-discovery-1.png)

### 3.3. Composed-defined bridge network

- This is exactly the same as user-defined bridge, except `docker-compose` creates it automatically when you bring up a stack.

### 3.4. Other aspect of bridge networks

- No service discovery and no communication between different bridge networks.
- All containers on any Docker brige network, are accessible from the host on the network layer.

### 3.5. Host network

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/docker-host-network.png)

- The container shares the host’s networking namespace.
- Container's network stack is not isolated from the Docker host.
- No `veth` pairs are created on host.
- Port mapping doesn't take effect.
- Useful to optimize performance.
- Only works on Linux hosts.

### 3.6. None network

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/docker-none-network.png)

- The container networking is disabled.
- Only loopback device is available.
- No `veth` pairs.
- Port-mapping doesn't take effect.
- Used as a security sandbox.

### 3.7. Interesting things

- Join a container to process-namespace of another container.

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/join-container-process.png)

```shell
docker run --name busybox \
                 --pid container:db \
                 --rm -it busybox /bin/sh
/ # ps aux
# Same process
PID   USER     TIME  COMMAND
    1 999       0:06 mysqld
  247 root      0:00 /bin/sh
  252 root      0:00 ps aux
# Different network namespace
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
61: eth0@if62: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

- Join the network and process namespace of the main container.

![](https://github.com/KamranAzeem/learn-docker/raw/master/docs/images/join-container-process-network.png)

```shell
docker run --name busybox \
                 --pid container:db \
                 --network container:db --rm -it busybox /bin/sh
/ # ps aux
PID   USER     TIME  COMMAND
    1 999       0:07 mysqld
  266 root      0:00 /bin/sh
  272 root      0:00 ps aux
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
55: eth0@if56: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever
/ #

$ docker inspect mynet
...
            "5659a70ca7c03103cc68db01a3e035547587da65f3d473f84383cec246aa09db": {
                "Name": "db",
                "EndpointID": "62bbed15dd8f75e53d1312ab157e5f24f19e7dbcbc7d2647220515e39bd3b936",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
...
```

## 4. Deep dive - How can containers transfer data to the kernel, and from there, to outside world?

- Port forwarding (bridge network): forwards traffic on a **specific** port from a container to the kernel.
- Host networking (host network): disables the **network namepspace stack** isolation from the Docker host.
- You can see 5 rule sections (chains): **PREROUTING**, INPUT, OUTPUT, **POSTROUTING** and **DOCKER**.
  - PREROUTING: rules altering packets before they come into the network stack (immediately after being received by an interface).
  - POSTROUTING: rules altering packets before they go out from the network stack (right before leaving an interface).
  - DOCKER: rules altering packets before they enter/leave the Docker bridge interface.

```shell
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

### 4.1. Port forwarding

- docker0 - default bridge network

```shell
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
c5804a4e9bfc   bridge    bridge    local
ebc10f5c8f92   host      host      local
4fcd98f9753c   none      null      local
```

- Docker network and iptables.

```shell
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

```shell
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

### 4.2. Host networking

```shell
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

```shell
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

## 5. Restrict connections - Docker and iptables

- On Linux, Docker manipulates `iptables` rules to provide network isolation.
- Docker install 2 custom iptables chains named `DOCKER-USER` and `DOCKER`, and it ensures that incoming packets are _always_ checked by these two chains first.
- All of Docker's `iptables` rules are added to the `DOCKER` chain -> Do not manipulate this chain manually -> _Must_ change `DOCKER-USER` chain instead (apply before any rules Docker creates automatically).
- Rules added to the `FORWARD` chain (manually/by tools) - are evaluated after these chains.

```shell
DOCKER-USER -> DOCKER -> FOWARD
```

- Sample rules:

```shell
# restricts external access from all IP addresses except 192.168.1.X
$ iptables -I DOCKER-USER -i ext_if ! -s 192.168.1.1 -j DROP
$ iptables -I DOCKER-USER -i ext_if ! -s 192.168.1.0/24 -j DROP
$ iptables -I DOCKER-USER -m iprange -i ext_if ! --src-range 192.168.1.1-192.168.1.3 -j DROP
# ...
# If Docker host acts as a router
$ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```

- `DOCKER` rules are created automatically by Docker daemon. Can we prevent Docker from doing it? Yeah, we can, but we shouldn't. It will more than likely break container networking for the Docker engine.

```json
# /etc/docker/daemon.json
{
  "iptables": false
}
```
