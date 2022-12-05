# Iptables

Source:

- <https://www.thegeekstuff.com/2011/01/iptables-fundamentals/>
- <https://www.opsist.com/blog/2015/08/11/how-do-i-see-what-iptables-is-doing.html>
- <https://www.digitalocean.com/community/tutorials/a-deep-dive-into-iptables-and-netfilter-architecture>
- <https://www.sobyte.net/post/2022-04/understanding-netfilter-and-iptables/> - advanced

- [Iptables](#iptables)
  - [1. Introduction](#1-introduction)
  - [2. Netfilter hooks](#2-netfilter-hooks)
  - [3. iptables tables and chains](#3-iptables-tables-and-chains)
  - [4. iptables rules](#4-iptables-rules)
  - [5. iptables drawbacks](#5-iptables-drawbacks)
  - [6. iptables TRACE](#6-iptables-trace)

## 1. Introduction

- iptables is used to manage packet filtering and NAT rules.
- iptables works with the kernel `netfilter` packet filtering framework.
  - iptables is replaced with `nftables`, but `iptables` syntax is still commonly used as a baseline.
- iptables on a high-level.

```shell
iptables
    tables
        chains
            rules
```

## 2. Netfilter hooks

- There are 4 netfilter hooks that programs can register with. As packets progress through the stack, they will trigger the kernel modules that have registered with these hooks.
  - `NF_IP_PRE_ROUTING`: triggered by any incoming traffic very soon after entering network stack. This hook is processed before any routing decisions have been made regarding where to send the packet.
  - `NF_IP_LOCAL_IN`: triggered after an incoming packet has been routed if the packet is destined for the local system.
  - `NF_IP_FORWARD`: triggered after an incoming packet has been routed if the packet is to be forwarded to another host.
  - `NF_IP_LOCAL_OUT`: triggered by any locally created outbound traffic as soon as it hits the network stack.
  - `NF_IP_POST_ROUTING`: triggerd by any outgoing or forwarded traffic after routing has taken place and just before being sent out on the wire.

![](https://people.netfilter.org/pablo/nf-hooks.png)

## 3. iptables tables and chains

- The names of the built-in chains mirror the names of the netfilter hooks they are associated with:
  - `PREROUTING`: Triggered by the `NF_IP_PRE_ROUTING` hook.
  - `INPUT`: Triggered by the `NF_IP_LOCAL_IN` hook.
  - `FORWARD`: Triggered by the `NF_IP_FORWARD` hook.
  - `OUTPUT`: Triggered by the `NF_IP_LOCAL_OUT` hook.
  - `POSTROUTING`: Triggered by the `NF_IP_POST_ROUTING` hook.
- iptables has the following 4 (or 5 in RedHat/CentOS) built-in tables.
  - Filter table: default table, built-in chains:
    - INPUT chain: incoming to firewall. For packets coming to the local server.
    - OUTPUT chain: outgoing from firewall. For packets generated locally and going out of the local server.
    - FORWARD chain: Packet for another NIC on the local server. For packets routed through the local server.
  - NAT table: built-in chains, is used to implement network address translation rules. As packets enter the network stack, rules in this table will determine whether and how modify the packet's source or destination addresses in order to impact the way that the packet and any response traffic are routed.
    - PREROUTING chain: alters packets before routing, i.e Packet translation happens immediately after the packet comes to the system (and before routing). This helps to translate the destination ip address of the packets to something that matches the routing on the local server -> DNAT.
    - POSTROUTING chain: alters packets after routing, i.e Packet translation happens when the packets are leaving the system. This helps to translate the source ip address of the packets to something that might match the routing on the destination server -> SNAT.
    - OUTPUT chain: NAT for locally generated packets on the firewall.
  - Mangle table: is used to alter the IP headers of the packet in various way (for e.x., adjust the TTL,...) Mangle table has the following built-in chains:
    - PREROUTING chain
    - OUTPUT chain
    - FORWARD chain
    - INPUT chain
    - POSTROUTING chain
  - Raw table: iptables firewall is stateful, meaning that packets are evaluated in regards to their relation to previous packets. The connection tracking features built on top of the `netfilter` framework allow `iptables` to view packets as part of an ongoing connection or session instead of as a stream of discrete, unrelated packets. The connection tracking logic is usually applied very soon after the packet hits the network interface. The `raw` table has a very narrowly defined function. Its only purpose is to provide a mechanism for marking packets in order to opt-out of connection tracking. Raw table has the following built-in chains:
    - PREROUTING chain.
    - OUTPUT chain.
  - Security table (RedHat/CentOS distros only): is used to set internal SELinux security context marks on packets, which will affect how SELinux or other systems that can interpret SELinux security contexts handle the packets.
- Process flow:

![](https://stuffphilwrites.com/wp-content/uploads/2014/09/FW-IDS-iptables-Flowchart-v2019-04-30-1.png)

- You can follow TRACE tutorial bellow to get process flow.
- Tables & Chains relationship.

|                               | PREROUTING | INPUT | FORWARD | OUTPUT | POSTROUTING |
| ----------------------------- | ---------- | ----- | ------- | ------ | ----------- |
| (routing decision)            |            |       |         | x      |             |
| raw                           | x          |       |         | x      |             |
| (connection tracking enabled) | x          |       |         | x      |             |
| mangle                        | x          | x     | x       | x      | x           |
| nat (DNAT)                    | x          |       |         | x      |             |
| (routing decision)            | x          |       |         | x      |             |
| filter                        |            | x     | x       | x      |             |
| security                      |            | x     | x       | x      |             |
| nat (SNAT)                    |            | x     |         |        | x           |

- Chain traversal order: Assuming that the server knows how to route a packet and that the firewall rules permit its transmission, the following flows represent the paths that will be traversed in different situations:
  - Incoming packets destined for the local system: PREROUTING (raw, mangle, nat) -> INPUT (mangle, filter, security, nat)
  - Incoming packets destined to another host: PREROUTING -> FORWARD -> POSTROUTING
  - Locally generated packets: OUTPUT -> POSTROUTING

## 4. iptables rules

- Key points:
  - Rules contain a criteria and a target.
  - If the criteria is matched, it goes to the rules specified in the target (or) executes the special values mentioned in the target.
  - If the criteria is not matched, it moves on to the next rule.
- Target values:
  - ACCEPT – Firewall will accept the packet.
  - DROP – Firewall will drop the packet.
  - QUEUE – Firewall will pass the packet to the userspace.
  - RETURN – Firewall will stop executing the next set of rules in the current chain for this packet. The control will be returned to the calling chain.
- Available states: connection tracked by the connection tracking system will be in one of the following states:
  - `NEW`:
  - `ESTABLISHED`:
  - `RELATED`:
  - `INVALID`:
  - `UNTRACKED`:
  - `SNAT`:
  - `DNAT`:
- Check rules

```shell
# num – Rule number within the particular chain
# target – Special target variable that we discussed above
# prot – Protocols. tcp, udp, icmp, etc.,
# opt – Special options for that specific rule.
# source – Source ip-address of the packet
# destination – Destination ip-address for the packet
iptables --list
iptables -t nat --list
```

## 5. iptables drawbacks

- Lack of incremental updates.
- Performance:
  - iptables rules are global --> For every packet, incoming interface needs to be checked and execution of rules branched to the set of rules appropriate for the particular interface.
  - Switch context.
- ...

## 6. iptables TRACE

- Ubuntu 22.04
- Copy this scrip to `iptables-trace.sh`.

```shell
#!/bin/sh
if [ $# != "2" ] || ! [ "${2}" -eq "${2}" ] 2> /dev/null
then
    if [ ${1} != "enable" ] && [ ${1} != "disable" ]
    then
        echo "Usage: ${0} [enable|disable] port"
        exit 1
    fi
fi

if [ ${1} = "enable" ]
then
    modprobe nf_log_ipv4
    sysctl -w net.netfilter.nf_log.2=nf_log_ipv4
    iptables -t raw -A PREROUTING -p tcp --dport ${2} -j TRACE
    iptables -t raw -A OUTPUT -p tcp --dport ${2} -j TRACE
    iptables -t raw -A PREROUTING -p udp --dport ${2} -j TRACE
    iptables -t raw -A OUTPUT -p udp --dport ${2} -j TRACE
    echo "iptables trace is enabled for port ${2}"
    echo "run \"xtables-monitor -t\" to view trace"
else
    iptables -t raw -D OUTPUT -p tcp --dport ${2} -j TRACE
    iptables -t raw -D PREROUTING -p tcp --dport ${2} -j TRACE
    iptables -t raw -D OUTPUT -p udp --dport ${2} -j TRACE
    iptables -t raw -D PREROUTING -p udp --dport ${2} -j TRACE
    sysctl -w net.netfilter.nf_log.2=NONE
    echo "iptables trace is disabled for port ${2}"
fi
```

- Enable tracing.

```shell
iptables-trace enable 8000
xtables-monitor -t
```

- Disable tracing.

```shell
iptables-trace disable 8000
```

- Note that, you may find there is some sources that configures trace, then uses rsyslog/dmesg (check `/var/log/kern.log`). But it may not work (in my case), cause this is iptables-legacy method. Your system switched to iptables-over-nftables.

  ```shell
  $ update-alternatives --list iptables
  /usr/sbin/iptables-legacy
  /usr/sbin/iptables-nft
  $ update-alternatives --display iptables
  iptables - auto mode
    link best version is /usr/sbin/iptables-nft
    link currently points to /usr/sbin/iptables-nft
    link iptables is /usr/sbin/iptables
  [...]
  ```

  - The `TRACE` target framework is specifically diefferent with this variant, to benefit from the advantages of the _nftables_ API. It's described in the manuals for the [iptables TRACE target](https://manpages.debian.org/iptables/iptables-extensions.8#TRACE) and [xtables-monitor](https://manpages.debian.org/iptables/xtables-monitor.8).
  - That means a lot of documentation and many blogs are becoming stale and showing only the legacy method.
  - Now with iptables-nft, one can just run this to display traces:

  ```shell
  xtables-monitor -t
  ```
