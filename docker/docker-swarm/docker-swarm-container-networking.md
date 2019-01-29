# Docker Swarm Container Networking

> NOTE: [Check here](https://neuvector.com/network-security/docker-swarm-container-networking/)
>       Note that this is not completed. Check the above link to the full version with cool diagrams.

With built-in orchestration and by removing dependencies on the external KV store, Docker Swarm allows DevOps to quickly deploy a multi-host docker cluster that “just works”. Although not without controversies, when compared to Kubernetes, Docker Swarm’s ease-of-use is one of it’s most cited advantages. 

## Deployment

First, let's create an overlay network and deploy containers. Docker swarm cluster has two nodes.

```bash
$ docker network create --opt encrypted --subnet 100.0.0.0/24 -d overlay net1
$ docker service create --name redis --network net1 redis
$ docker service create --name node --network net1 nvbeta/node
$ docker service create --name nginx --network net1 -p 1080:80 nvbeta/swarm_nginx
```

![logical-view](https://neuvector.com/wp-content/uploads/2017/01/logicview.png)

## Networks

```bash
$ docker network ls

NETWORK ID          NAME                DRIVER              SCOPE
62a0995662ed        bridge              bridge              local
4cd81d849158        docker_gwbridge     bridge              local
4ed9ce66850e        host                host                local
das46zk71z4g        ingress             overlay             swarm
y5rtwtq7bj4u        net1                overlay             swarm
a9af664b25b4        none                null                local
```

* `net1`: the overlay network we create for east-west communication between containers.
* `docker_gwbridge`: the network created by Docker. It allows the container to the host that it is running on.
* `ingress`: the network created by Docker. Docker Swarm uses this network to expose services to the external network and provide the routing mesh.

### net1

Because all services are created with the “–network net1” option, each of them must have one interface connecting to the ‘net1’ network.

```bash
# Check in node1
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS               NAMES
a80aaba1a6d0        nvbeta/node:latest   "nodemon /src/index.…"   3 minutes ago       Up 3 minutes        8888/tcp            node.1.vu2ex7oikbbz951nc947zwyx6
```

By creating a symbolic link to the docker netns folder, we can find out all network namespaces on node1

```
$ cd /var/run
$ sudo ln -s /var/run/docker/netns netns
$ sudo ip netns
acd51a308dfe (id: 4)
1-y5rtwtq7bj (id: 2)
lb_y5rtwtq7b (id: 3)
1-das46zk71z (id: 0)
ingress_sbox (id: 1)
```

Comparing the namespace names with the Docker swarm network IDs, we can guess that namespace `1-y5rtwtq7bj` is used for `net1` network, whose ID is `y5rtwtq7bj4u`. This can be confirmed by comparing interfaces in the namespace and containers.

Interface list in the containers

```
# node1
$ docker exec -it node.1.vu2ex7oikbbz951nc947zwyx6 ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
14: eth0@if15: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1424 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 02:42:64:00:00:06 brd ff:ff:ff:ff:ff:ff
16: eth1@if17: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
```

Interface list in the namespace

```
# node1
$ sudo ip netns exec 1-y5rtwtq7bj ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1424 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 56:6a:7b:b4:cd:56 brd ff:ff:ff:ff:ff:ff
11: vxlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1424 qdisc noqueue master br0 state UNKNOWN mode DEFAULT group default 
    link/ether fa:43:1f:b6:17:25 brd ff:ff:ff:ff:ff:ff link-netnsid 0
13: veth0@if12: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1424 qdisc noqueue master br0 state UP mode DEFAULT group default 
    link/ether 56:6a:7b:b4:cd:56 brd ff:ff:ff:ff:ff:ff link-netnsid 1
15: veth1@if14: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1424 qdisc noqueue master br0 state UP mode DEFAULT group default 
    link/ether fe:fd:3e:54:70:60 brd ff:ff:ff:ff:ff:ff link-netnsid 2
```

Note that `br0` is the Linux Bridge where all the interfaces are connected to, `vxlan0` is the VTEP interface for VXLAN overlay network. For each veth pair that Docker creates for the container, the device inside the container always has an ID number which is 1 number greater than the device Id of the other end.

### docker\_gwbridge

The docker\_gwbridge on each host is very much like the docker0 bridge in the single-host Docker environment. Each container  has a leg connecting to it and it's reachable from the host that the container is running on.

However, unlike the docker0 bridge, it is not used to connect to the external network. For Docker Swarm services that publisjes ports, Docker creates a dedicated `ingress` network for it.

### ingress

```
$ sudo ip netns exec ingress_sbox ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
7: eth0@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default 
    link/ether 02:42:0a:ff:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.255.0.2/16 brd 10.255.255.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet 10.255.0.4/32 brd 10.255.0.4 scope global eth0
       valid_lft forever preferred_lft forever
9: eth1@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:12:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet 172.18.0.2/16 brd 172.18.255.255 scope global eth1
       valid_lft forever preferred_lft forever

$ docker network inspect ingress
[
    {
        "Name": "ingress",
        "Id": "das46zk71z4gzja9lalsn9vs5",
        "Created": "2019-01-29T01:25:09.873453838Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": true,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "ingress-sbox": {
                "Name": "ingress-endpoint",
                "EndpointID": "a87d66a7a0afb3fa7a53c22fee91cb7a62538bf66b4d69f661eb1181aaefbeb9",
                "MacAddress": "02:42:0a:ff:00:02",
                "IPv4Address": "10.255.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4096"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "d8bafa53602e",
                "IP": "192.168.122.124"
            },
            {
                "Name": "2228e30afa2a",
                "IP": "192.168.122.127"
            }
        ]
    }
]

$ docker network inspect docker_gwbridge
[
    {
        "Name": "docker_gwbridge",
        "Id": "4cd81d84915887245af64614c1acdf1b176d943cec146139d6405431839296b6",
        "Created": "2019-01-23T10:43:50.179274578Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "a80aaba1a6d0af6e10be34434e5556c514b9c71cbcda006da622747367b552ec": {
                "Name": "gateway_acd51a308dfe",
                "EndpointID": "96bce71ac3655b212165c0452eb5918e036cfe15d98cd6ebda7093d95a7b1f26",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            },
            "ingress-sbox": {
                "Name": "gateway_ingress-sbox",
                "EndpointID": "c73d6b2709e3949ed948812eed2e0ad58ef7ee8402e29b5579b6dd8816a49245",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.enable_icc": "false",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.name": "docker_gwbridge"
        },
        "Labels": {}
    }
]
```

The endpoints’ MAC/IP addresses on these networks match the interface MAC/IP addresses in the namespace `ingress_sbox`. This namespace is for the hidden container named ingress-sbox, which has one leg on the host network and another leg on ingress network.

One of the major features of Docker Swarm is the ‘routing mesh’ for containers that publish ports. No matter which node the container instance is actually running on, you can access it through any node. How is it done? Let’s dig deeper into this hidden container.

In our application, it’s the ‘nginx’ service that publishes port 80 and maps to port 1080 on the host, but the ‘nginx’ container is not running on node 1.

```bash
# node1
$ sudo iptables -t nat -nvL
Chain PREROUTING (policy ACCEPT 274 packets, 26671 bytes)
 pkts bytes target     prot opt in     out     source               destination         
  203 12432 DOCKER-INGRESS  all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL
  240 14733 DOCKER     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT 206 packets, 13224 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 241 packets, 15135 bytes)
 pkts bytes target     prot opt in     out     source               destination         
   17   911 DOCKER-INGRESS  all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL
    1    60 DOCKER     all  --  *      *       0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT 241 packets, 15135 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 MASQUERADE  all  --  *      docker_gwbridge  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match src-type LOCAL
    0     0 MASQUERADE  all  --  *      !docker0  172.17.0.0/16        0.0.0.0/0           
    0     0 MASQUERADE  all  --  *      !docker_gwbridge  172.18.0.0/16        0.0.0.0/0           

Chain DOCKER (2 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 RETURN     all  --  docker0 *       0.0.0.0/0            0.0.0.0/0           
    0     0 RETURN     all  --  docker_gwbridge *       0.0.0.0/0            0.0.0.0/0           

Chain DOCKER-INGRESS (2 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:1080 to:172.18.0.2:1080
  220 13343 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0           

sudo ip netns exec ingress_sbox iptables -nvL -t nat
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DOCKER_OUTPUT  all  --  *      *       0.0.0.0/0            127.0.0.11          

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DOCKER_POSTROUTING  all  --  *      *       0.0.0.0/0            127.0.0.11          
    0     0 SNAT       all  --  *      *       0.0.0.0/0            10.255.0.0/16        ipvs to:10.255.0.2

Chain DOCKER_OUTPUT (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            127.0.0.11           tcp dpt:53 to:127.0.0.11:45211
    0     0 DNAT       udp  --  *      *       0.0.0.0/0            127.0.0.11           udp dpt:53 to:127.0.0.11:57576

Chain DOCKER_POSTROUTING (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 SNAT       tcp  --  *      *       127.0.0.11           0.0.0.0/0            tcp spt:45211 to::53
    0     0 SNAT       udp  --  *      *       127.0.0.11           0.0.0.0/0            udp spt:57576 to::53
```

As you can see, iptables rules redirect the traffic to port 1080 to port 80 in the hidden container `ingress_sbox` then the POSTROUTING chain puts the packewts on ip  10.255.0.2, which is the IP address of interface on `ingress` network.

Notice ‘ipvs’ in the SNAT rule. ‘ipvs‘ is a load balancer implementation in the Linux kernel. It’s a little-known tool that has been in the kernel for 16 years.

```bash
$ sudo ip netns exec ingress_sbox iptables -nvL -t mangle
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 MARK       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:1080 MARK set 0x102

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 MARK       all  --  *      *       0.0.0.0/0            10.255.0.4           MARK set 0x102

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

```
