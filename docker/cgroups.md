# CGroup

Source: <https://docs.docker.com/config/containers/runmetrics/#control-groups>

- [CGroup](#cgroup)
  - [Enumerate cgroups](#enumerate-cgroups)
    - [cgroup v1](#cgroup-v1)
    - [cgroup v2](#cgroup-v2)
  - [Changing cgroup version](#changing-cgroup-version)
  - [Running Docker on cgroup v2](#running-docker-on-cgroup-v2)
  - [Find the cgroup for a given container](#find-the-cgroup-for-a-given-container)

Linux Containers rely on control groups which not only track groups of processes, but also expose metrics about CPU, memory, and block I/O  usage.

Control groups are exposed through a pseudo-filesystem. In recent distros, you should find this filesystem under `/sys/fs/cgroup`. Under that directory, you see multiple sub-directories, called devices, freezer, blkio, etc.; each sub-directory actually corresponds to a different cgroup hierarchy.

On older systems, the control groups might be mounted on /cgroup, without distinct hierarchies. In that case, instead of seeing the sub-directories, you see a bunch of files in that directory, and possibly some directories corresponding to existing containers.

To figure out where your control groups are mounted, you can run:

```shell
$ grep cgroup /proc/mounts
```

## Enumerate cgroups

The file layout of cgroups is significantly different between v1 and v2.

If /sys/fs/cgroup/cgroup.controllers is present on your system, you are using v2, otherwise you are using v1. Refer to the subsection that corresponds to your cgroup version.

cgroup v2 is used by default on the following distributions:

- Fedora (since 31)
- Debian GNU/Linux (since 11)
- Ubuntu (since 21.10)

### cgroup v1

You can look into `/proc/cgroups` to see the different control group subsystems known to the system, the hierarchy they belong to, and how many groups they contain.

You can also look at `/proc/<pid>/cgroup` to see which control groups a process belongs to. The control group is shown as a path relative to the root of the hierarchy mountpoint. / means the process has not been assigned to a group, while /lxc/pumpkin indicates that the process is a member of a container named pumpkin.

### cgroup v2

On cgroup v2 hosts, the content of `/proc/cgroups` isn’t meaningful. See `/sys/fs/cgroup/cgroup.controllers` to the available controllers.

## Changing cgroup version

Changing cgroup version requires rebooting the entire system.

On systemd-based systems, cgroup v2 can be enabled by adding `systemd.unified_cgroup_hierarchy=1` to the kernel cmdline. To revert the cgroup version to v1, you need to set `systemd.unified_cgroup_hierarchy=0` instead.

If grubby command is available on your system (e.g. on Fedora), the cmdline can be modified as follows:

```shell
$ sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
```

If grubby command is not available, edit the `GRUB_CMDLINE_LINUX` line in `/etc/default/grub` and `run sudo update-grub`.

## Running Docker on cgroup v2

Docker supports cgroup v2 since Docker 20.10. Running Docker on cgroup v2 also requires the following conditions to be satisfied:

- containerd: v1.4 or later
- runc: v1.0.0-rc91 or later
- Kernel: v4.15 or later (v5.2 or later is recommended)
Note that the cgroup v2 mode behaves slightly different from the cgroup v1 mode:

- The default cgroup driver (dockerd --exec-opt native.cgroupdriver) is “systemd” on v2, “cgroupfs” on v1.
- The default cgroup namespace mode (docker run --cgroupns) is “private” on v2, “host” on v1.
- The docker run flags --oom-kill-disable and --kernel-memory are discarded on v2.

## Find the cgroup for a given container

For each container, one cgroup is created in each hierarchy. On older systems with older versions of the LXC userland tools, the name of the cgroup is the name of the container. With more recent versions of the LXC tools, the cgroup is `lxc/<container_name`>.

For Docker containers using cgroups, the container name is the full ID or long ID of the container. If a container shows up as ae836c95b4c3 in `docker ps`, its long ID might be something like `ae836c95b4c3c9e9179e0e91015512da89fdec91612f63cebae57df9a5444c79`. You can look it up with `docker inspect` or `docker ps --no-trunc`.

Putting everything together to look at the memory metrics for a Docker container, take a look at the following paths:

- `/sys/fs/cgroup/memory/docker/<longid>/` on cgroup v1, cgroupfs driver
- `/sys/fs/cgroup/memory/system.slice/docker-<longid>.scope/` on cgroup v1, systemd driver
- `/sys/fs/cgroup/docker/<longid/>` on cgroup v2, cgroupfs driver
- `/sys/fs/cgroup/system.slice/docker-<longid>.scope/` on cgroup v2, systemd driver

To check driver and version, simply run `docker info`.
