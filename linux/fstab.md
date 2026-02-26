# Fstab

Source: <https://help.ubuntu.com/community/Fstab>

The configuration file `/etc/fstab` contains the necessary information to automate the process of mounting partitions. In a nutshell, mounting is the process where a raw (physical) partition is prepared for access and assigned a location on the file system tree (or mount point).

1. In general fstab is used for internal devices, CD/DVD devices, and network shares (samba/nfs/sshfs). Removable devices such as flash drives _can_ be added to fstab, but are typically mounted by gnome-volume-manager and are beyond the scope of this document.
2. Options for mount and fstab are similar.
3. Partitions listed in fstab can be configured to automatically mount during the boot process.
4. If a device/partition is not listed in fstab ONLY ROOT may mount the device/partition.
5. Users may mount a device/partition if the device is in fstab with the proper options.

The syntax of a fstab entry:

```text
[Device] [Mount Point] [File System Type] [Options] [Dump] [Pass]
```

| fields               | description                                                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `<device>`           | The device/partition (by `/dev` location or UUID) that contain a file system.                                                                                                                                            |
| `<mount point>`      | The directory on your root file system (aka mount point) from which it will be possible to access the content of the device/partition (note: swap has no mount point). Mount points should not have spaces in the names. |
| `<file system type>` | Type of file system                                                                                                                                                                                                      |
| `<options>`          | Mount options of access to the device/partition (see the man page for `mount`).                                                                                                                                          |
| `<dump>`             | Enable or disable backing up of the device/partition (the command _dump_). This field is usually set to `0`, which disables it.                                                                                          |
| `<pass num>`         | Controls the order in which _fsck_ checks the device/partition for errors at boot time. The root device should be `1`. Other partitions should be `2`, or `0` to disable checking.                                       |
