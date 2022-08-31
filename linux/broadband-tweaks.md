# Linux Broadband Tweaks

Source: <https://www.speedguide.net/articles/linux-tweaking-121>

> Raising network limits for high speed, high latency networks under Linux

## 1. Locating the TCP/IP parameters

- All TCP/IP tunning parameters are located under `/proc/sys/net/...`.

## 2. Applying TCP/IP parameters at system boot

- TCP/IP parameters in Linux are located in /proc/sys/net/ipv4 and /proc/sys/net/core . This is part of the Virtual filesystem which resides in system memory (RAM), and any changes to it are volatile, they are reset when the machine is rebooted.
- There are two methods to apply the settings at each reboot.
  - Edit `/etc/sysctl.conf`.

  ```
  net.core.rmem_default = 256960
  net.core.rmem_max = 256960
  net.core.wmem_default = 256960
  net.core.wmem_max = 256960
  net.ipv4.tcp_timestamps = 0
  net.ipv4.tcp_sack = 0
  net.ipv4.tcp_window_scaling = 1
  ```

  - Edit `/etc/rc.local, /etc/rc.d/rc.local` (depending on distribution).

  ```bash
  echo 256960 > /proc/sys/net/core/rmem_default
  echo 256960 > /proc/sys/net/core/rmem_max
  echo 256960 > /proc/sys/net/core/wmem_default
  echo 256960 > /proc/sys/net/core/wmem_max
  echo 0 > /proc/sys/net/ipv4/tcp_timestamps
  echo 0 > /proc/sys/net/ipv4/tcp_sack
  echo 1 > /proc/sys/net/ipv4/tcp_window_scaling
  ```

## 3. Changing current values

```bash
# To make any new sysctl.conf changes take effect without rebooting:
sysctl -p

# To see a list of all relevant tweakable sysctl parameters, along with their current values, try the following in your terminal:
sysctl -a | grep tcp

# To set a single sysctl value:
sysctl -w variable=value
```

## 4. TCP parameters to consider

- `TCP_FIN_TIMEOUT`: determines the time that muyst elapse before TCP/IP can release a closed connection and reuse its resources. During this `TIME_WAIT` state, reopening the connection to the client costs less than establishing a new connection. By reducing the value of this entry, TCP/IP can release closed connections faster, making more resources available for new connections. Adjust this in the presence of many connections sitting in the `TIME_WAIT` state:

```
sysctl.conf syntax:
net.ipv4.tcp_fin_timeout = 15

(default: 60 seconds, recommended 15-30 seconds)

alternative rc.local syntax:
echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout
```

- `TCP_KEEPALIVE_INTERVAL`: determines the wait time between isAlive interval probes.

```
sysctl.conf syntax:
net.ipv4.tcp_keepalive_intvl = 30

(default: 75 seconds, recommended: 15-30 seconds)

alternative rc.local syntax:
echo 30 > /proc/sys/net/ipv4/tcp_keepalive_intvl
```

- `TCP_KEEPALIVE_PROBES`: determines the number of probes before timing out.

```
sysctl.conf syntax:
net.ipv4.tcp_keepalive_probes = 5

(default: 9, recommended 5)

alternative rc.local syntax:
echo 5 > /proc/sys/net/ipv4/tcp_keepalive_probes
```

- `TCP_TW_RECYCLE`: enables fast recycling of TIME_WAIT sockets. The default value is 0 (disabled). The sysctl documentation incorrectly states the default as enabled. It can be changed to 1 (enabled) in many cases. Known to cause some issues with hoststated (load balancing and fail over) if enabled, should be used with caution.

```
sysctl.conf syntax:
net.ipv4.tcp_tw_recycle=1

(boolean, default: 0)

alternative rc.local syntax:
echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle
```

- `TCP_TW_REUSE`: allow reusing sockets in `TIME_WAIT` state for new connections when it is safe from protocol viewpoint. Default value is 0 (disabled). It generally a safer alternative to `TCP_TW_RECYCLE`.

```
sysctl.conf syntax:
net.ipv4.tcp_tw_reuse=1

(boolean, default: 0)

alternative rc.local syntax:
echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse
```

## 4. Linux Netfilter tweaks

```bash
# List netfilter parameters
sysctl -a | grep netfilter

# Reduce number of connections in TIME_WAIT state -> decrease the number of seconds
# connections are kept in this state before being dropped
# reduce TIME_WAIT from the 120s default to 30-60s
net.netfilter.nf_conntrack_tcp_timeout_time_wait=30
# reduce FIN_WAIT from teh 120s default to 30-60s
net.netfilter.nf_conntrack_tcp_timeout_fin_wait=30
```

## 5. Determine connection states

```bash
# List all current connections to the machine
netstat -tan | grep ':80 ' | awk '{print $6}' | sort | uniq -c
```

## 6. SYN flood protection

```bash
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_syn_retries = 6
net.ipv4.tcp_synack_retries = 3
net.ipv4.tcp_syncookies = 1
```
