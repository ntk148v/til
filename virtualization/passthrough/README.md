# Linux virtualization and PCI passthrough

Source: <https://developer.ibm.com/tutorials/l-pci-passthrough/>

Platform virtualization shares a platform across operating systems for more efficient resource use. A platform includes more than a processor—also storage, networking, and other hardware. Some resources virtualize easily (processor, storage); others don't (video adapter, serial port). PCI passthrough uses those resources efficiently when sharing is impossible or not useful.

## 1. Platform device emulation

- **Device emulation within the hypervisor**: common in VMware Workstation. The hypervisor emulates shared devices—virtual disks, virtual network adapters, and other platform elements.

  ![](https://developer.ibm.com/developer/default/tutorials/l-pci-passthrough/images/figure1.gif)

- **User space device emulation**: emulation lives in user space, not the hypervisor. QEMU (which also provides a hypervisor) does the emulation and is used by many hypervisors (KVM, VirtualBox).
  - Independent of the hypervisor, so it can be shared across hypervisors.
  - Avoids burdening the privileged hypervisor with arbitrary emulation.

  ![](https://developer.ibm.com/developer/default/tutorials/l-pci-passthrough/images/figure2.gif)

- **Advantages**: pushing emulation to user space shrinks the trusted computing base (TCB)—the set of components critical to security. Less code in the hypervisor means smaller bug surface and a more secure system, and fewer ways to leak privileges to untrusted users.

## 2. Device passthrough

Both emulation models pay an overhead cost. That cost is worthwhile when devices are shared by multiple guests; if sharing isn't needed, more efficient options exist.

At the highest level, device passthrough isolates a device to one guest for its exclusive use → performance, and exclusive use of devices that aren't inherently shareable.

- Near-native performance—ideal for networking or high-disk-I/O apps.
- Specialized PCI devices used by a single guest, or devices the hypervisor doesn't support, should be passed through.

![](https://developer.ibm.com/developer/default/tutorials/l-pci-passthrough/images/figure3.gif)

Early passthrough used a thin emulation model: the hypervisor provided software-based memory management (translating guest address space to host address space) → this lacked the performance and scalability large virtualization environments need.

## 3. Hardware support for device passthrough

Intel and AMD both support passthrough in newer architectures: Intel's VT-d and AMD's IOMMU.

- New CPUs map PCI physical addresses to guest virtual addresses.
- The hardware handles access and protection, so the guest uses the device like a non-virtualized one. Isolation also keeps other guests (or the hypervisor) from accessing it.

## 4. Problems with device passthrough

- **Live migration** suspends and moves a VM to a new host, supporting load balancing—but conflicts with passthrough devices.
- **PCI hotplug** lets devices come and go from a kernel, ideal for migration (unplug, then plug in at the new host).
- Emulated devices (e.g., virtual network adapters) migrate easily because emulation abstracts away the physical hardware—also supported by the Linux bonding driver, which bonds multiple logical adapters to one interface.

## 5. Next steps in I/O virtualization

- **PCIe** includes virtualization support.
- **Single-Root I/O Virtualization (SR-IOV)**: a PCIe device exports PCI physical functions plus virtual functions that share device resources. Virtualization happens at the end device, so no passthrough is needed—the hypervisor maps virtual functions to VMs for native performance with security and isolation.

  ![](https://developer.ibm.com/developer/default/tutorials/l-pci-passthrough/images/figure4.gif)
