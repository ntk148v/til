---
title: Systemd-analyze
path: linux/systemd-analyze.md
---

Source: <https://www.freedesktop.org/software/systemd/man/systemd-analyze.html>

## Overview

- `systemd-analyze` - Analyze and debug system manager
- `systemd-analyze` is used to determine system boot-up performance statistics and retrieve other state and tracing information from the system and service manager, and to verify correctness of unit files. It is also used to access special functions useful for advanced system manager debugging.

## Usage

- **systemd-analyze time**

```bash
# Example 1. Show how long the boot took

# in a container
$ systemd-analyze time
Startup finished in 296ms (userspace)
multi-user.target reached after 275ms in userspace

# on a real machine
$ systemd-analyze time
Startup finished in 2.584s (kernel) + 19.176s (initrd) + 47.847s (userspace) = 1min 9.608s
multi-user.target reached after 47.820s in userspace
```

- **systemd-analyze blame**

```bash
# Example 2. Show which units took the most time during boot

$ systemd-analyze blame
         32.875s pmlogger.service
         20.905s systemd-networkd-wait-online.service
         13.299s dev-vda1.device
         ...
            23ms sysroot.mount
            11ms initrd-udevadm-cleanup-db.service
             3ms sys-kernel-config.mount
```

- **systemd-analyze critical-chain [UNIT...]**

```bash
# Example 3. systemd-analyze critical-chain
# prints a tree of the time-critical chain of units

$ systemd-analyze critical-chain
multi-user.target @47.820s
└─pmie.service @35.968s +548ms
  └─pmcd.service @33.715s +2.247s
    └─network-online.target @33.712s
      └─systemd-networkd-wait-online.service @12.804s +20.905s
        └─systemd-networkd.service @11.109s +1.690s
          └─systemd-udevd.service @9.201s +1.904s
            └─systemd-tmpfiles-setup-dev.service @7.306s +1.776s
              └─kmod-static-nodes.service @6.976s +177ms
                └─systemd-journald.socket
                  └─system.slice
                    └─-.slice

```

- **systemd-analyze dump**

```bash
# Example 4. Show the internal state of user manager

$ systemd-analyze --user dump
Timestamp userspace: Thu 2019-03-14 23:28:07 CET
Timestamp finish: Thu 2019-03-14 23:28:07 CET
Timestamp generators-start: Thu 2019-03-14 23:28:07 CET
Timestamp generators-finish: Thu 2019-03-14 23:28:07 CET
Timestamp units-load-start: Thu 2019-03-14 23:28:07 CET
Timestamp units-load-finish: Thu 2019-03-14 23:28:07 CET
-> Unit proc-timer_list.mount:
        Description: /proc/timer_list
        ...
-> Unit default.target:
        Description: Main user target
...
```

- **systemd-analyze plot**

```bash
# Example 5. Plot a bootchart

$ systemd-analyze plot >bootup.svg
$ eog bootup.svg&
```

- **systemd-analyze dot [pattern...]**

```bash
# Example 6. Plot all dependencies of any unit whose name starts with "avahi-daemon"

$ systemd-analyze dot 'avahi-daemon.*' | dot -Tsvg >avahi.svg
$ eog avahi.svg

# Example 7. Plot the dependencies between all known target units

$ systemd-analyze dot --to-pattern='*.target' --from-pattern='*.target' \
      | dot -Tsvg >targets.svg
$ eog targets.svg
```

- Want more? Check [source](https://www.freedesktop.org/software/systemd/man/systemd-analyze.html) for complete guides.
