# Keepalived

## 1. Verify Keepalived IP Failover workng or not

By default keepalived uses 224.0.0.18 IP address for VRRP (Virtual Router Redundancy Protocol) for communication between two nodes for health check.

To verify, you can use tcpdump command:

```shell
$ sudo tcpdump -v -i eth0 host 224.0.0.18
$ sudo tcpdump -vvv -n -i eth0 host 224.0.0.18
# try multicast sub/net
$ sudo tcpdump -i eth0 -s0 -vv net 224.0.0.0/4
```

A note about firewall rule:

```shell
$ sudo iptables -I INPUT -i eth0 -d 224.0.0.0/8 -j ACCEPT
$ sudo iptables -I INPUT -i eth1 -p vrrp -j ACCEPT
$ sudo iptables -A INPUT -p 112 -i eth0 -j ACCEPT
$ sudo iptables -A OUTPUT -p 112 -o eth0 -j ACCEPT
```
