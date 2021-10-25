# Tuning

Source: https://medium.com/@pawilon/tuning-your-linux-kernel-and-haproxy-instance-for-high-loads-1a2105ea553e

## 1. Kernel tweaks

### 1.1. Number of open files

- Every incoming/outgoing connection needs to open a socket and each socket is a file on a Linux system.
- If you're configuring a loadbalancer serving content from backend servers then each incoming connections will open a minimum of two sockets, or even more, depending on the loadbalacing configuration.
- Two ways to configure max open files, depending on whether your distribution uses systemd or not.
  - Edit `/etc/security/limits.conf`.

  ```
  * soft nofile 100000
  * hard nofile 100000
  root soft nofile 100000
  root hard nofile 100000
  ```

  - If you’re on a system that uses systemd you will find that setting limits.conf doesn’t work as well. That’s because systemd doesn’t use the `/etc/security/limits.conf` at all, but instead uses it’s own configuration to determine the limits. Override the configuration for a specific service by editing file `/etc/systemd/system/<service_name>.service.d/override.conf`.

  ```
  [Service]
  LimitNOFILE=100000
  ```

  ```bash
  system daemon-reload
  system restart <service_name>
  ```

- Two other values that relate to maximum open files:

```bash
# Determine the maximum number of files in total that can be opened on the system
sysctl fs.file-max
# Determine the maximum vlaue that fs.file-max can be configured on
sysctl fs.nr-open
```

### 1.2. Conntrack

- `net.netfilter.nf_conntrack_max` determines the maximum number of connections that the kernel module will track.
- It’s recommended not to tweak `nf_conntrack_max` manually, but indirectly, by setting `nf_conntrack_buckets`.

```
nf_conntrack_max = 8 * nf_conntrack_buckets
```

- Configure on module load, by setting it in `/etc/modprobe.d/nf_conntrack`
