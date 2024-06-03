# Predictable Network Interface Names

Source:

- <https://systemd.io/PREDICTABLE_INTERFACE_NAMES/>
- <https://www.freedesktop.org/software/systemd/man/latest/systemd.net-naming-scheme.html>
- <https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/>

Starting with v197 systemd/udev will automatically assign **predictable, stable network interface names** for all local Ethernet, WLAN and WWAN interfaces. This is a departure from the traditional interface naming scheme (`eth0`, `eth1`, `wlan0`, …), but should fix real problems.

## 1. The problem.

The classic naming scheme for network interfaces applied by the kernel is to simply assign names beginning with `eth0`, `eth1`, … to all interfaces as they are probed by the drivers. As the driver probing is generally not predictable for modern technology this means that as soon as multiple network interfaces are available the assignment of the names eth0, eth1 and so on is generally not fixed anymore and it might very well happen that eth0 on one boot ends up being eth1 on the next. This can have serious security implications, for example in firewall rules which are coded for certain naming schemes, and which are hence very sensitive to unpredictable changing names.

## 2. What precisely has changed in v197?

The following different naming schemes for network interfaces are now supported by udev natively:

- Names incorporating Firmware/BIOS provided index numbers for on-board devices (example: `eno1`)
- Names incorporating Firmware/BIOS provided PCI Express hotplug slot index numbers (example: `ens1`)
- Names incorporating physical/geographical location of the connector of the hardware (example: `enp2s0`)
- Names incorporating the interfaces’s MAC address (example: `enx78e7d1ea46da`)
- Classic, unpredictable kernel-native ethX naming (example: `eth0`)

## 3. What good does this do?

- Stable interface names across reboots
- Stable interface names even when hardware is added or removed, i.e. no re-enumeration takes place (to the level the firmware permits this)
- Stable interface names when kernels or drivers are updated/changed
- Stable interface names even if you have to replace broken ethernet cards by new ones
- The names are automatically determined without user configuration, they just work
- The interface names are fully predictable, i.e. just by looking at lspci you can figure out what the interface is going to be called
- Fully stateless operation, changing the hardware configuration will not result in changes in /etc
- Compatibility with read-only root
- The network interface naming now follows more closely the scheme used for aliasing block device nodes and other device nodes in /dev via symlinks
- Applicability to both x86 and non-x86 machines
- The same on all distributions that adopted systemd/udev

## 4. Naming

Depending on the network type, the following prefixes (first two characters) are used:

| prefix | network type                       |
| ------ | ---------------------------------- |
| en     | Ethernet                           |
| ib     | InfiniBand                         |
| sl     | Serial line IP (slip)              |
| wl     | Wireless local area network (WLAN) |
| ww     | Wireless wide area network (WWAN)  |

Ethernet network interface names are assigned as follows:

- **eno**: Names containing the index numbers provided by firmware/BIOS for on-board devices, example: eno1 (eno = Onboard).
- **ens**: Names containing the PCI Express hotplug slot numbers provided by the firmware/BIOS, example: ens1 (ens = Slot).
- **enp**: Names containing the physical/geographical location of the hardware's port, example: enp2s0 (enp = Position).
- **enx**: Names containing the MAC address of the interface (example: enx78e7d1ea46da).
- **eth**: Classic unpredictable kernel-native ethX naming (example: eth0).
