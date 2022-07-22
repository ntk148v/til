# Nabla Containers

Source: <https://nabla-containers.github.io>

- [Nabla Containers](#nabla-containers)
  - [1. Security problems](#1-security-problems)
  - [2. A new approach to container isolation](#2-a-new-approach-to-container-isolation)

## 1. Security problems

- Two kind of fundamental kinds of container and VM security problems: [Vertial Attach Profile (VAP) and Horizontal Attack Profile (HAP)](https://blog.hansenpartnership.com/containers-and-cloud-security/)
  - VAP: All the code, which is traversed to provide a service all the way from input to database update to output. This code, like all programs, contains bugs. The bug density varies, but the more code you traverse the greater your chance of exposure to a security hole
  - HAP: Stack security holes exploits -- which can jump into either the physical server host or VMs -- are HAPs.

## 2. A new approach to container isolation

![approach](https://nabla-containers.github.io/public/img/nabla-containers.png)

- A containerized application can avoid making a Linux system call if it links to a library OS componenet that implements the system call functionality.
- Nabla containers use library OS - unikernel -> avoid system calls -> reduce the attach surface.
  - Unikernel: Application images built with only the OS components they actually require, TCP, Stack, DHCP, NAT...
  - The OS becomes a "Library OS"
  - "Normal" applications which sit atop a generic monolthic Linux kernel - may unneeded features (floppy driver..., )
  - More about [unikernel](http://mjbright.blogspot.com/2017/05/unikernels-unikernels-unikernels.html)
- Solo5 - Port MirageOS to run on the Linux/KVM hypervisor.

![overview](https://nabla-containers.github.io/public/img/nabla-internals.png)

- Isolation: Limit access to the host kernel via the blocking of system calls.
