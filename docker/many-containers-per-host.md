# Run many containers per host

Source: <https://sven.stormbind.net/blog/posts/docker_from_30_to_230/>

- Conntrack table: Since the defaut docker networking setup involves a shitload of NAT, it shouldn't bet surprising that nf_conntrack will start to drop packets at some point.

```bash
net.netfilter.nf_conntrack_max = 524288 # May be larger
```

- Inotify watches and Cadvisor:

```bash
# default
fs.inotify.max_user_instances = 4096
fs.inotify.max_user_watches = 32768

# tuning
fs.inotify.max_user_instances = 4096
fs.inotify.max_user_watches = 32768
```

- Running out of PIDs: by default, pid_max is 32768, actual limit on 64 bit system is `2^22` according to [man 5 doc](https://man7.org/linux/man-pages/man5/proc.5.html).

```bash
# Change
/proc/sys/kernel/pid_max
```

- Ephmeral ports

```bash
net.ipv4.ip_local_port_range = 11000 60999
```
