# Kernel configuration

Source: <https://tldp.org/HOWTO/SCSI-2.4-HOWTO/kconfig.html>

The Linux kernel configuration is usually found in the kernel source in the file: `/usr/src/linux-headers-<version>/.config`. It is not recommeneded to edit this file directly but to use on of these configuration options:

- **make config** - starts a character based questions and answer session
- **make menuconfig** - starts a terminal-oriented configuration tool (using `ncurses`)
- **make xconfig** - starts a X based configuration tool

The descriptions of these selections that is displayed by the associated help button can be found in the flat ASCII file: `/usr/src/linux-headers-<version>/Documentation/Configure.help`
Ultimately these configuration tools edit the `.config` file. An option will either indicate some driver is built into the kernel ("=y") or will be built as a module ("=m") or is not selected. The unselected state can either be indicated by a line starting with "#" (e.g. "# CONFIG_SCSI is not set") or by the absence of the relevant line from the `.config` file.

- Step-by-step to use **make menuconfig**:

  - Go to the directory `/usr/src/linux-headers-<version>/` as root, in my case, the path is `/usr/src/linux-headers-5.13.0-39-generic/`.

  ```bash
  root@ubuntu /usr/src/linux-headers-5.13.0-39-generic #
  ```

  - Install the required packages (Ubuntu only):

  ```bash
  root@ubuntu /usr/src/linux-headers-5.13.0-39-generic # sudo apt install libncurses5-dev libncursesw5-dev bison flex -y
  ```

  - Run, then a terminal-oriented menu will show up:

  ```bash
  root@ubuntu /usr/src/linux-headers-5.13.0-39-generic # make menuconfig
  ```

![](./images/kernel-menuconfig.png)
