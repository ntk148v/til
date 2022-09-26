# Iptables

Source:

- <https://www.thegeekstuff.com/2011/01/iptables-fundamentals/>
- <https://www.opsist.com/blog/2015/08/11/how-do-i-see-what-iptables-is-doing.html>

- [Iptables](#iptables)
  - [1. Introduction](#1-introduction)
  - [2. iptables tables and chains](#2-iptables-tables-and-chains)
  - [3. iptables rules](#3-iptables-rules)
  - [4. iptables drawbacks](#4-iptables-drawbacks)
  - [5. iptables TRACE](#5-iptables-trace)

## 1. Introduction

- iptables is used to manage packet filtering and NAT rules.
- iptables on a high-level.

```shell
iptables
    tables
        chains
            rules
```

## 2. iptables tables and chains

- iptables has the following 4 built-in tables.
  - Filter table: default table, built-in chains:
    - INPUT chain: incoming to firewall. For packets coming to the local server.
    - OUTPUT chain: outgoing from firewall. For packets generated locally and going out of the local server.
    - FORWARD chain: Packet for another NIC on the local server. For packets routed through the local server.
  - NAT table: built-in chains:
    - PREROUTING chain: alters packets before routing, i.e Packet translation happens immediately after the packet comes to the system (and before routing). This helps to translate the destination ip address of the packets to something that matches the routing on the local server -> DNAT.
    - POSTROUTING chain: alters packets after routing, i.e Packet translation happens when the packets are leaving the system. This helps to translate the source ip address of the packets to something that might match the routing on the destination server -> SNAT.
    - OUTPUT chain: NAT for locally generated packets on the firewall.
  - Mangle table: for specialized packet alteration. This alters QOS bits in the TCP header. Mangle table has the following built-in chains:
    - PREROUTING chain
    - OUTPUT chain
    - FORWARD chain
    - INPUT chain
    - POSTROUTING chain
  - Raw table: for configuration excemptions. Raw table has the following built-in chains:
    - PREROUTING chain.
    - OUTPUT chain.
- Process flow:

![](https://stuffphilwrites.com/wp-content/uploads/2014/09/FW-IDS-iptables-Flowchart-v2019-04-30-1.png)

- You can follow TRACE tutorial bellow to get process flow.

## 3. iptables rules

- Key points:
  - Rules contain a criteria and a target.
  - If the criteria is matched, it goes to the rules specified in the target (or) executes the special values mentioned in the target.
  - If the criteria is not matched, it moves on to the next rule.
- Target values:
  - ACCEPT – Firewall will accept the packet.
  - DROP – Firewall will drop the packet.
  - QUEUE – Firewall will pass the packet to the userspace.
  - RETURN – Firewall will stop executing the next set of rules in the current chain for this packet. The control will be returned to the calling chain.
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

## 4. iptables drawbacks

- Lack of incremental updates.
- Performance:
  - iptables rules are global --> For every packet, incoming interface needs to be checked and execution of rules branched to the set of rules appropriate for the particular interface.
  - Switch context.
- ...

## 5. iptables TRACE

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

  - The `TRACE` target framework is specifically diefferent with this variant, to benefit from the advantages of the *nftables* API. It's described in the manuals for the [iptables TRACE target](https://manpages.debian.org/iptables/iptables-extensions.8#TRACE) and [xtables-monitor](https://manpages.debian.org/iptables/xtables-monitor.8).
  - That means a lot of documentation and many blogs are becoming stale and showing only the legacy method.
  - Now with iptables-nft, one can just run this to display traces:

  ```shell
  xtables-monitor -t
  ```