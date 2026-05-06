# Filesystem reserved space

<https://lwn.net/Articles/546473/>

By default, an ext3/ext4 filesystem will reserve 5% of its capacity for special processes that can continue to run when diskspace is running low. Purpose: Reserved space allows root-owned processes (e.g., syslog) to continue running and prevents severe fragmentation when a partition is nearly full.

First, check which mount you want to investigate.

    $  df -h
    Filesystem            Size  Used Avail Use% Mounted on
    /dev/partition        198G  180G   14G  93% /
    /dev/sda1              99M   41M   54M  44% /boot
    tmpfs                 2.0G     0  2.0G   0% /dev/shm

You can check your current reserved blocks value with tune2fs.

    $ tune2fs -l /dev/partition  | grep 'Reserved'
    Reserved block count:     120542571

You can lower the 5% barrier if you like, but I only suggest doing this for larger partitions. Since the default is 5%, I’ll lower it to 2% here.

    $ tune2fs
    tune2fs 1.47.0 (5-Feb-2023)
    Usage: tune2fs [-c max_mounts_count] [-e errors_behavior] [-f] [-g group]
            [-i interval[d|m|w]] [-j] [-J journal_options] [-l]
            [-m reserved_blocks_percent] [-o [^]mount_options[,...]]
            [-r reserved_blocks_count] [-u user] [-C mount_count]
            [-L volume_label] [-M last_mounted_dir]
            [-O [^]feature[,...]] [-Q quota_options]
            [-E extended-option[,...]] [-T last_check_time] [-U UUID]
            [-I new_inode_size] [-z undo_file] device
    $ tune2fs -m2 /dev/partition
    tune2fs 1.47.0 (5-Feb-2023)
    Setting reserved blocks percentage to 2% (48223887 blocks)
