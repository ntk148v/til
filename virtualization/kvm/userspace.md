# KVM userspace

Source:

- <https://www.redhat.com/en/blog/all-you-need-know-about-kvm-userspace>
- <https://www.ubicloud.com/blog/cloud-virtualization-red-hat-aws-firecracker-and-ubicloud-internals>

KVM itself is "just" a Linux device driver and only one part of our virtualization stack. Userspace components such as QEMU and libvirt, and other kernel subsystems such as SELinux, have a major part in making the stack full-featured and secure.

![](https://doc.opensuse.org/documentation/leap/virtualization/html/book-virtualization/images/kvm_qemu.png)

## 1. QEMU and libvirt

QEMU and libvirt have complementary tasks. QEMU is the virtual machine monitor (VMM): it provides hardware emulation and a low-level interface to the virtual machine. A QEMU process is a virtual machine on its own: you can terminate it by sending a signal to the process, examine processor consumption using top, and so on.

Because the QEMU process handles input and commands from the guest, it's exposed to potentially malicious activity. Therefore, it should run in a confined environment, where it only has access to the resources it needs to run the virtual machine. This is the principle of least privilege, which QEMU and libvirt are designed to follow

Libvirt, on the other hand, is not visible to the guests, so it is the best place to confine QEMU processes; it does not matter if setting up the restricted environment requires high privileges. Libvirt combines many technologies to confine QEMU, ranging from file system ownership and permissions to cgroups and SELinux multi-category security. Together, these technologies seek to ensure that QEMU cannot access resources from other virtual machines.

![](https://www.redhat.com/rhdc/managed-files/styles/default_800/private/image1_21_0.png.webp?itok=MjBv848H)

## 2. The world outside

- The first alternative KVM user space options is [kvmtool](https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/).
- [crosvm](https://github.com/google/crosvm).
- The virtual machine monitor that Amazon uses for Lambda, called [Firecracker](https://firecracker-microvm.github.io/). Firecracker has a very minimal feature set; in fact you will even need a specially-compiled kernel for your virtual machine instead of using one from your favorite distro. Amazon's management stack for Firecracker is not open source, except for a simple sandboxing tool called jailer. This tool takes care of setting up namespaces and seccomp in a suitable way for a Firecracker process.
- Amazon engineers also started a project called rust-vmm, a collaboration to develop common libraries for virtualization projects written in Rust. These libraries, or "crates" in Rust parlance, could be used by virtual machine monitors, vhost-user[3] servers, or other specialized KVM use cases. Intel has created one such VMM, called [cloud-hypervisor](https://github.com/intel/cloud-hypervisorhttps://github.com/intel/cloud-hypervisor), which could also be considered the rust-vmm reference implementation.
- Two projects that blur the boundaries between containers and VM, [gVisor](https://gvisor.dev/) and [Kata Containers](https://katacontainers.io/).
