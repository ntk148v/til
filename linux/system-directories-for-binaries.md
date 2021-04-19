# System directories for binaries

- [System directories for binaries](#system-directories-for-binaries)
  - [1. System directories for binaries](#1-system-directories-for-binaries)
  - [2. Where to put your own scripts?](#2-where-to-put-your-own-scripts)

## 1. System directories for binaries

Refer to the [Filesystem Hierarchy Standard for Linux](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard).

```bash
# Interesting command
$ man hier | grep -E 'bin$|sbin$|^.{7}(/bin)|^.{7}(/sbin)' -A2                                                                                                 ~
```

- `/bin`: This directory contains executable programs which are needed in single user mode and to bring the system up or repair it.

- `/sbin`: Like `/bin`, this directory holds commands needed to boot the system, but which are usually not executed by normal users.

- `/usr/X11R6/bin`: Binaries which belong to the X-Window system; often, there is a symbolic link from the more traditional `/usr/bin/X11` to here.

- `/usr/bin`: This is the primary directory for executable programs. Most programs executed by normal users which are not needed for booting or for repairing the system and which are not installed locally should be placed in this directory.
- `/usr/local/bin`: Binaries for programs local to the site.

- `/usr/local/sbin`: Locally installed programs for system administration.

- `/usr/sbin`: This directory contains program binaries for system administration which are not essential for the boot process, for mounting /usr, or for system repair.
- `~/.local/bin/` or `~/bin`: for user-scoped scripts.

## 2. Where to put your own scripts?

- For all users to access your scripts you can put them in `/usr/local/bin`.
- For user-scoped scripts put them in `~/bin` or `~/local/bin/`.
