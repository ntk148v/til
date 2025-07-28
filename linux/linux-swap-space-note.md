# Swap space note

<https://ntk148v.github.io/blog/posts/linux-swap-space-note/>

Source:

- [RedHad guideline](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/installation_guide/sect-disk-partitioning-setup-x86#sect-recommended-partitioning-scheme-x86)
- [Chris Down's post](https://chrisdown.name/2018/01/02/in-defence-of-swap.html)
- [Linux Hint - Understanding vm.swappiness](https://linuxhint.com/understanding_vm_swappiness/)

## 1. What is Swap?

Swap file systems support virtual memory, data is written to a swap file system when there is not enough RAM to store the data your system is processing.

## 2. Swap partition size

### 2.1. Old rule of thumb

```
swap = 2 * the-amount-of-RAM
```

So if a computer had 64KB of RAM, a swap partition of 128KB would be an optimum size. This rule took into the facts that RAM sizes were typically quite small at the time. Nowadays, RAM has become a `cheap` & `affordable` commondity, so the 2x rule is outdated.

### 2.2. What is the right amount of swap space?

Choosing the correct swap size is important. Too much swap space can hide memory leaks, also the storage space is allocated but idle. It can affect the system performance in general.

Follow the RedHat (CentOS 7x & RHEL 7) guide, the recommended size of a swap partition depending on the amount of RAM & whether you want sufficient memory for your system.

```
swap <= 10% * total-size-hard-drives && swap <= 128GB (if hibernation is allowed)
```

| Amount of RAM | Recommended swap space | Recommended swap space if allowing for hibernation |
| ------------- | ---------------------- | -------------------------------------------------- |
| < 2GB         | 2 \* the-amount-of-RAM | 3 \* the-amount-of-RAM                             |
| > 2GB - 8GB   | the-amount-of-RAM      | 2 \* the-amount-of-RAM                             |
| > 8GB - 64GB  | >= 4GB                 | 1.5 \* the-amount-of-RAM                           |
| > 64GB        | >= 4GB                 | Hibernation not recommended                        |

## 3. Common misconceptions & gotchas

### 3.1. Increasing swap size would increase performance

- No, it wouldn't. Remember that the slowest part of memory is your hard-disk - _swap_ just provides the ability to use more memory by swapping some pages out to the disk, which is **slow** compared to RAM operations. Swap can also [increase disk I/O & CPU load](https://askubuntu.com/questions/367881/does-swap-file-usage-increase-disk-i-o-and-cpu-load). This is a tradeoff. Without swap, the OOM may get you. It causes a downtime and in the real life scenario, the application can be slow a bit rather than down completely.

### 3.2. Swappiness

- The linux kernel tunable parameter `vm.swappiness` (/proc/sys/vm/swappiness) can be used to define how aggressively memory pages are swapped to disk.
- The default value: `60`. The lower the value, the less swapping is used & the more memory pages are kept in the physical memory.

  ```
  * 0: swap is disable.
  * 1: minimum amount of swapping without disabling it entirely.
  * 10: recommended value to improve performance when sufficient memory exists in a system
  * 100: aggressive swapping
  ```

- Useful commands:

  ```bash
  # Check the current value
  sysctl vm.swappiness
  # Adjust the value
  echo 10 > /proc/sys/vm/swappiness
  sysctl -w vm.swappiness=10
  echo "vm.swappiness = 10" >> /etc/sysctl.conf
  ```

- On SSDs, swapping out anonymous pages and reclaiming file pages are essentially equivalent in terms of performance/latency. On older spinning disks, swap reads are slower due to random reads, so a lower vm.swappiness setting makes sense there.

### 3.3. Using swap as emergency memory

- Swap is not generally about getting emergency memory, it's about making memory reclamation egalitarian and efficient. In fact, using it as "emergency memory" is generally actively harmful.

## 4. Check which processes are eating swap on linux

Source: <https://superuser.com/questions/1677225/check-which-processes-are-eating-swap-on-linux>

- Use [smem](https://manpages.debian.org/bullseye/smem/smem.8.en.html):
- Use [smemstat](http://manpages.org/smemstat/8): `smemstat -mT`
- Use `top` and `htop` by adding SWAP column.
