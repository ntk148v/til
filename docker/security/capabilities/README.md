# Capabilities

Source:

- <https://docs.docker.com/engine/security/#linux-kernel-capabilities>
- <https://github.com/riyazdf/dockercon-workshop/tree/master/capabilities>

## 1. Introduction

- The Linux kernel is able to break down the privileges of the `root` user into distinct units referred to as **capabilities**.
- This breaking down of root privileges into granular capabilities allows you to:
  - Remove individual capabilities from the `root` user account, making it less powerful/dangerous.
  - Add privileges to non-root users at a very granular level.
- Capabilities apply to both files and threads:
  - File capabilities allow users to execute programs with higher privileges.
  - Thread capabilities keep track of the current state of capabilities in running programs.
- Typical servers run several processes as `root`, including the SSH daemon, cron daemon, logging daemons, kernel modules, network configuration tools, and more. A container is different, because almost all of those tasks are handled by the infrastructure around the container. This means that in most cases, containers do not need “real” root privileges at all. And therefore, containers can run with a reduced capability set; meaning that “root” within a container has much less privileges than the real “root”.
- Docker sets the _bounding set_ before starting a container. You can use Docker commands to add `--cap-add` or remove `--cap-remove` capabilities or from the _bounding set_.
- By default, Docker drops all capabilities execept [those needed](https://github.com/moby/moby/blob/master/oci/caps/defaults.go#L6-L19), using a whitelist approach. The following list contains all capabilities that are enabled by default when you run a docker container with their descriptions from the **capabilities**(7) man page:
  - `CHOWN` - Make arbitrary changes to file UIDs and GIDs
  - `DAC_OVERRIDE` - Discretionary access control (DAC) - Bypass file read, write, and execute permission checks.
  - `FSETID` - Don’t clear set-user-ID and set-group-ID mode bits when a file is modified; set the set-group-ID bit for a file whose GID does not match the file system or any of the supplementary GIDs of the calling process.
  - `FOWNER` - Bypass permission checks on operations that normally require the file system UID of the process to match the UID of the file, excluding those operations covered by CAP_DAC_OVERRIDE and CAP_DAC_READ_SEARCH.
  - `MKNOD` - Create special files using mknod(2).
  - `NET_RAW` - Use RAW and PACKET sockets; bind to any address for transparent proxying.
  - `SETGID` - Make arbitrary manipulations of process GIDs and supplementary GID list; forge GID when passing socket credentials via UNIX domain sockets; write a group ID mapping in a user namespace.
  - `SETUID` - Make arbitrary manipulations of process UIDs; forge UID when passing socket credentials via UNIX domain sockets; write a user ID mapping in a user namespace.
  - `SETFCAP` - Set file capabilities.
  - `SETPCAP` - If file capabilities are not supported: grant or remove any capability in the caller’s permitted capability set to or from any other process.
  - `NET_BIND_SERVICE` - Bind a socket to Internet domain privileged ports (port numbers less than 1024).
  - `SYS_CHROOT` - Use chroot(2) to change to a different root directory.
  - `KILL` - Bypass permission checks for sending signals. This includes use of the ioctl(2) KDSIGACCEPT operation.
  - `AUDIT_WRITE` - Write records to kernel auditing log.
- Options to work with Capabilities and Docker:
  - Manual mangement within the container:

  ```shell
  $ docker run --cap-add ALL
  ```

  - Restricted capabilities (still root):

  ```shell
  $ docker run --cap-drop ALL --cap-add ABC
  ```

  - No capabilities:

  ```shell
  $ docker run --user
  ```

- The Linux kernel prefixes all capability constants with "`CAP_`". For example, `CAP_CHOWN`, `CAP_NET_ADMIN`, `CAP_SETUID`, `CAP_SYSADMIN` etc. Docker capability constants are not prefixed with "`CAP_`" but otherwise match the kernel's constants. For more information on capabilities, including a full list, see the [capabilities man page](http://man7.org/linux/man-pages/man7/capabilities.7.html).

## 2. Playground

- Build image - alpine with `libcap` and `libcap-ng`:
  - **libcap** focuses on manipulating capabilities.
  - **libcap-ng** has some useful tools for auditing.

```Dockerfile
FROM alpine
RUN apk add --no-cache libcap libcap-ng libcap-ng-utils
```

```shell
$ docker build -t alpine-cap .
```

- Let's play, start container with default capabilities and user:

```shell
$ docker run --rm -it alpine-cap sh
# By default, container is started with root user.
/ # whoami
root
# Check list of default capabilities
/ # capsh --print
Current: cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap=ep
Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
Ambient set =
Current IAB: !cap_dac_read_search,!cap_linux_immutable,!cap_net_broadcast,!cap_net_admin,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_lease,!cap_audit_control,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=0(root) euid=0(root)
gid=0(root)
groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
Guessed mode: HYBRID (4)
```

- Explain the `capsh` output:
  - **Current** is multiple sets separated by spaces.
  - Multiple capabilities within the same set are separated by commas `,`.
  - The letters following the `+` at the end of each set are as follows:
    - `e`: effective
    - `i`: inheritable
    - `p`: permitted

- Drop all capabilities:

```shell
$ docker run --rm -it --cap-drop ALL alpine-cap sh
/ # capsh --print
Current: =
Bounding set =
Ambient set =
Current IAB: !cap_chown,!cap_dac_override,!cap_dac_read_search,!cap_fowner,!cap_fsetid,!cap_kill,!cap_setgid,!cap_setuid,!cap_setpcap,!cap_linux_immutable,!cap_net_bind_service,!cap_net_broadcast,!cap_net_admin,!cap_net_raw,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_chroot,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_mknod,!cap_lease,!cap_audit_write,!cap_audit_control,!cap_setfcap,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=0(root) euid=0(root)
gid=0(root)
groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
Guessed mode: HYBRID (4)
# You can't execute chown cause root user doesn't have CAP_CHOWN capability anymore.
/ # chown nobody /
chown: /: Operation not permitted
```

- Drop all but add `CAP_CHOWN`:

```shell
$ docker run --rm -it --cap-drop ALL --cap-add CHOWN alpine-cap sh
/ # capsh --print
Current: cap_chown=ep
Bounding set =cap_chown
Ambient set =
Current IAB: !cap_dac_override,!cap_dac_read_search,!cap_fowner,!cap_fsetid,!cap_kill,!cap_setgid,!cap_setuid,!cap_setpcap,!cap_linux_immutable,!cap_net_bind_service,!cap_net_broadcast,!cap_net_admin,!cap_net_raw,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_chroot,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_mknod,!cap_lease,!cap_audit_write,!cap_audit_control,!cap_setfcap,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=0(root) euid=0(root)
gid=0(root)
groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
Guessed mode: HYBRID (4)
# Able to execute chown
/ # chown nobody /
```

- Create a new container start with `nobody` user:

```shell
$ docker run --rm -it --user nobody alpine-cap sh
~ $ capsh --print
Current: =
Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
Ambient set =
Current IAB: !cap_dac_read_search,!cap_linux_immutable,!cap_net_broadcast,!cap_net_admin,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_lease,!cap_audit_control,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=65534(nobody) euid=65534(nobody)
gid=65534(nobody)
groups=65534(nobody)
Guessed mode: HYBRID (4)
~ $ chown nobody /tmp
chown: /tmp: Operation not permitted
```

- How about adding capabilities to container start with `nobody` user? Let's try:
  - Docker doesn't yet support adding capabilities to non-root users.

```shell
$ docker run --rm -it --user nobody --cap-add CAP_CHOWN alpine-cap sh
# Not working!
~ $ capsh --print
Current: =
Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
Ambient set =
Current IAB: !cap_dac_read_search,!cap_linux_immutable,!cap_net_broadcast,!cap_net_admin,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_lease,!cap_audit_control,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=65534(nobody) euid=65534(nobody)
gid=65534(nobody)
groups=65534(nobody)
Guessed mode: HYBRID (4)
~ $ chown nobody /
chown: /: Operation not permitted
~ $ chown nobody /tmp
chown: /tmp: Operation not permitted
```

- Advanced:

```shell
$ docker run --rm -it alpine-cap sh
# List all capabilities
/ # capsh --print
Current: cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap=ep
Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
Ambient set =
Current IAB: !cap_dac_read_search,!cap_linux_immutable,!cap_net_broadcast,!cap_net_admin,!cap_ipc_lock,!cap_ipc_owner,!cap_sys_module,!cap_sys_rawio,!cap_sys_ptrace,!cap_sys_pacct,!cap_sys_admin,!cap_sys_boot,!cap_sys_nice,!cap_sys_resource,!cap_sys_time,!cap_sys_tty_config,!cap_lease,!cap_audit_control,!cap_mac_override,!cap_mac_admin,!cap_syslog,!cap_wake_alarm,!cap_block_suspend,!cap_audit_read,!cap_perfmon,!cap_bpf,!cap_checkpoint_restore
Securebits: 00/0x0/1'b0 (no-new-privs=0)
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=0(root) euid=0(root)
gid=0(root)
groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
Guessed mode: HYBRID (4)
/ # touch /tmp/test1 /tmp/test2
# Modify capabilities on a file with libcap
/ # setcap cap_chown=ep /tmp/test1
/ # getcap /tmp/test1
/tmp/test1 cap_chown=ep
# Modify capabilities on a file with libcap-ng
/ # filecap /tmp/test2
/ # filecap /tmp/test2 chown
/ # filecap /tmp/test2
set       file                 capabilities  rootid
effective /tmp/test2    chown
```
