# LXC, LXD vs Docker

Table of contents:

- [LXC, LXD vs Docker](#lxc-lxd-vs-docker)
  - [Intro about both of them](#intro-about-both-of-them)
    - [1. LXC and LXD](#1-lxc-and-lxd)
    - [2. Docker](#2-docker)
  - [The similarity](#the-similarity)
  - [The difference](#the-difference)
  - [Benefits and Limitations](#benefits-and-limitations)
    - [1. LXC](#1-lxc)
    - [2. Docker](#2-docker-1)
  - [Refs](#refs)

![lxc vs docker ](http://i.stack.imgur.com/a5Neb.png)

_This is a 2 part series exploring Linux containers, container managers like LXC and Docker and the potential of containers as lightweight alternatives to virtualization_

## Intro about both of them

### 1. LXC and LXD

- **LXC** - a userspace interface for the Linux kernel containment features. Through a powerful API and simple tools, it lets Linux users easily create and manage system or application containers.
- **LXD** - a container "hypervisor" and a new user experience for LXC. Specifically, it's made of three components:
  - A system-wide daemon (lxd)
  - A command line client (lxc)
  - An OpenStack Nova plugin (nova-compute-lxd)

Basically, a self-contained OS userspace is created with it's isolated infrastructure. LXC underlies more directly on OS features for networking and storage than Docker.

![lxc](https://s3-ap-southeast-1.amazonaws.com/kipalog.com/lxc_architecture.png_3isdyqn10m)

### 2. Docker

![docker](http://zdnet2.cbsistatic.com/hub/i/r/2014/08/18/fe54db15-26bc-11e4-8c7f-00505685119a/thumbnail/770x578/4b06faaa09dee31dff99105f4951fe15/docker-libcontainer-unities-linux-container-powers.png)

More details [here](#)

## The similarity

[Operating-system-level virtualization](https://en.wikipedia.org/wiki/Operating-system-level_virtualization)

What all of them have in common, is that all these 3 technologies are related to containers.

Containers are a lightweight virtualization mechanism that does not require you to set up a virtual machine on an emulation of physical hardware. In Linux, what they have in common are the Kernel features used: `cgroups, namespaces(ipc, network, user, pid, mount)`. They also try to create more safe environments by creating unprivileged containers and integrating with security features like selinux. These technologies export APIs to better integrate with other softwares.

## The difference

The main difference is LXC containers have an init and can thus run multiprocesses and Docker containers don't have an init and can only run single processes.

The idea behind Docker is to reduce a container as much as possible to a single process and then manage that through Docker, to contain the app and base image to create the impression that the App is a single process inside the engine. Docker used lxc techonogy as underlying to communicate with the kernel but today, it uses it´s own library, libcontainer.

LXC sidesteps that with a normal OS environment and is thus immediately and cleanly compatible all the apps and tools and any management and orchestration layers and be a drop in replacement for VMs.

Beyond that Docker uses layers and disables storage persistence. LXC supports layers with aufs, overlayfs and has wide support for COW cloning and snapshots with btrfs, ZFS, LVM Thin and leaves it to user choice. Separating storage in LXC containers is a simple bind mount to the host or another container for users who choose to do so.

Both Docker and LXC set up a default NAT network. Docker additionally setups port forwarding to the host with the -p flag for instance '-p 80:80' forwards 80 from the host to the container. Given NAT containers can be accessed directly by the local host by their IPs and only need port forwarding when consumed by external services which can be done simply by an iptables rule when required, the reason for doing this is not very clear.

To compound matters Docker gives you very little control of the IP and hosts file and you can't set static IPs for containers which makes assigning services to IPs a bit of a conundrum. You need to use a '--links' flag to connect containers which adds an entry in the the /etc/hosts file of the linked container. The need to abstract away basic networking in this way seems a bit pointless and adds a needless layer of complexity.

With LXC it's a much simpler to assign static IPs, routable IPs, use multiple network devices, manage the /etc/hosts file and basically use the full stack of Linux network capabilities with no limitations. Want to connect containers across hosts? Users can setup quick overlays using GRE, L2TPV3 or VXLAN tunnels or any networking technology they are using currently. LXC containers will work for whatever works for VMs seamlessly.

## Benefits and Limitations

### 1. LXC

- Benefits:
  - Provides a “normal” OS environment that supports all the features and capabilities that are available in the Linux environment.
  - Behaves very much like a traditional VM and thus offers a lower barrier to entry for some organizations.
  - Does not require changes to the application being deployed.
  - Supports layers and enables Copy-On-Write cloning and snapshots, and is also file-system neutral.
  - Uses simple, intuitive, and standard IP addresses to access the containers and allows full access to the host file.
  - Supports static IP addressing, routable IPs, multiple network devices.
  - Provides full root access.
  - Allows you to create your own network interfaces.
- Limitations.
  - Does not have a nearly as prolific or responsive user community as Docker does.
  - Inconsistent feature support across different Linux distributions. LXC is primarily being maintained & developed by Canonical on Ubuntu platform.

### 2. Docker

- Benefits:
  - Reduces a container to a single process which is then easily managed with Docker tools.
  - Encapsulates application configuration and delivery complexity to dramatically simplify and eliminate the need to repeat these activities manually.
  - Provides a strongly supportive user community.
  - Provides a highly efficient compute environment for applications that are stateless and micro-services based, as well as many stateful applications like databases, message bus, etc.
  - Uses layers and disables storage persistence, which helps make Docker images very lightweight.
  - Is used very successfully by many groups, particularly Dev and Test, as well as microservices-based production environments.
  - Supports plug-in architecture for volume, network, and authentication to engage with partner ecosystems.
- Limitations:
  - Treats containers differently from a standard host, such as sharing the host’s IP address and providing access to the container via a selectable port. This approach can cause management issues when using traditional applications and management tools that require access to Linux utilities such as cron, ssh, daemons, and logging.
  - Uses layers and disables storage persistence, which results in reduced disk subsystem performance.
  - Is not ideal for stateful applications due to limited volume management in case of container failover.
  - Can require some training for administrators to understand the changes to their operating procedures.
  - Can require changes to the application being run in the container.

## Refs

1. [LXC and LXD](https://linuxcontainers.org/)
2. [Docker](http://www.docker.com/)
3. [Understanding the key differences between LXC and Docker](https://www.flockport.com/lxc-vs-docker/)
4. [What is the difference between Docker, LXD, and LXC](http://unix.stackexchange.com/questions/254956/what-is-the-difference-between-docker-lxd-and-lxc)
5. [LXC vs Docker](https://robinsystems.com/blog/linux-containers-comparison-lxc-docker/)
