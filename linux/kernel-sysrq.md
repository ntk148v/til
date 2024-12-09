---
title: "Linux Magic System Request Key Hacks"
date: "2024-12-05T09:44:34+07:00"
tags: ["linux", "tips", "tech"]
comments: true
toc: true
draft: false
---

Source: <https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html>

## Giới thiệu

Trong quá trình vận hành, bạn đã bao giờ gặp tình trạng hệ thống Linux của mình bị "treo" hoặc không phản hồi? Khi đó, hãy sử dụng **Magic System Request Key (SysRq)** để được cứu rỗi. Vậy nó là gì và có thể làm gì?

SysRq là một tính năng của Linux, cho phép người dùng gửi "tín hiệu cầu cứu" trực tiếp đến kernel của hệ điều hành.

{{< figure class="figure" caption="sysrq - from trufflesecurity.com" src="https://framerusercontent.com/images/wjLSwytVCtdnGhq2xK8m6qSo4.png" >}}

## Cấu hình SysRq

Để cấu hình SysRq, bạn có thể sử dụng command sau:

```shell
echo "number" >/proc/sys/kernel/sysrq
```

Giá trị của "number" có thể nằm trong các trường hợp sau:

```shell
  0         - disable sysrq completely
  1         - enable all functions of sysrq
  >1        – bitmask to allow specific sysrq functions
  2 =   0x2 - enable control of console logging level
  4 =   0x4 - enable control of keyboard (SAK, unraw)
  8 =   0x8 - enable debugging dumps of processes etc.
 16 =  0x10 - enable sync command
 32 =  0x20 - enable remount read-only
 64 =  0x40 - enable signalling of processes (term, kill, oom-kill)
128 =  0x80 - allow reboot/poweroff
256 = 0x100 - allow nicing of all RT tasks
```

Kiểm tra giá trị hiện tại của sysrq:

```shell
root@vm1:/home/kien# cat /proc/sys/kernel/sysrq
176
# 176 không match với giá trị nào, well, thực ra 176 ở đây là 16+32+128 = 176
#
# 16 =  0x10 - enable sync command
# 32 =  0x20 - enable remount read-only
# 128 =  0x80 - allow reboot/poweroff

# Để test, bật hết lên cho đơn giản
root@vm1:/home/kien# root@vm1:/home/kien# echo 1 > /proc/sys/kernel/sysrq
```

## Cách sử dụng

Bạn có thể sử dụng tính năng bằng cách ấn tổ hợp phím (tùy thuộc hệ điều hành, đối với x86 là `ALT-SysRq-<command key>`, bàn phím của bạn thường sẽ có SysRq keyboard, để ý nhé) hoặc echo ký tự commands vào `/proc/sysrq-trigger`.

```shell
echo <command key> > /proc/sysrq-trigger
```

{{< details title="Danh sách command key (ấn để show all)" open=false >}}
<table class="docutils align-default">
<thead>
<tr class="row-odd"><th class="head"><p>Command</p></th>
<th class="head"><p>Function</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">b</span></code></p></td>
<td><p>Will immediately reboot the system without syncing or unmounting
your disks.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">c</span></code></p></td>
<td><p>Will perform a system crash and a crashdump will be taken
if configured.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">d</span></code></p></td>
<td><p>Shows all locks that are held.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">e</span></code></p></td>
<td><p>Send a SIGTERM to all processes, except for init.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">f</span></code></p></td>
<td><p>Will call the oom killer to kill a memory hog process, but do not
panic if nothing can be killed.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">g</span></code></p></td>
<td><p>Used by kgdb (kernel debugger)</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">h</span></code></p></td>
<td><p>Will display help (actually any other key than those listed
here will display help. but <code class="docutils literal notranslate"><span class="pre">h</span></code> is easy to remember :-)</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">i</span></code></p></td>
<td><p>Send a SIGKILL to all processes, except for init.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">j</span></code></p></td>
<td><p>Forcibly “Just thaw it” - filesystems frozen by the FIFREEZE ioctl.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">k</span></code></p></td>
<td><p>Secure Access Key (SAK) Kills all programs on the current virtual
console. NOTE: See important comments below in SAK section.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">l</span></code></p></td>
<td><p>Shows a stack backtrace for all active CPUs.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">m</span></code></p></td>
<td><p>Will dump current memory info to your console.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">n</span></code></p></td>
<td><p>Used to make RT tasks nice-able</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">o</span></code></p></td>
<td><p>Will shut your system off (if configured and supported).</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">p</span></code></p></td>
<td><p>Will dump the current registers and flags to your console.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">q</span></code></p></td>
<td><p>Will dump per CPU lists of all armed hrtimers (but NOT regular
timer_list timers) and detailed information about all
clockevent devices.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">r</span></code></p></td>
<td><p>Turns off keyboard raw mode and sets it to XLATE.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">s</span></code></p></td>
<td><p>Will attempt to sync all mounted filesystems.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">t</span></code></p></td>
<td><p>Will dump a list of current tasks and their information to your
console.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">u</span></code></p></td>
<td><p>Will attempt to remount all mounted filesystems read-only.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">v</span></code></p></td>
<td><p>Forcefully restores framebuffer console</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">v</span></code></p></td>
<td><p>Causes ETM buffer dump [ARM-specific]</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">w</span></code></p></td>
<td><p>Dumps tasks that are in uninterruptible (blocked) state.</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">x</span></code></p></td>
<td><p>Used by xmon interface on ppc/powerpc platforms.
Show global PMU Registers on sparc64.
Dump all TLB entries on MIPS.</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">y</span></code></p></td>
<td><p>Show global CPU Registers [SPARC-64 specific]</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">z</span></code></p></td>
<td><p>Dump the ftrace buffer</p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">0</span></code>-<code class="docutils literal notranslate"><span class="pre">9</span></code></p></td>
<td><p>Sets the console log level, controlling which kernel messages
will be printed to your console. (<code class="docutils literal notranslate"><span class="pre">0</span></code>, for example would make
it so that only emergency messages like PANICs or OOPSes would
make it to your console.)</p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">R</span></code></p></td>
<td><p>Replay the kernel log messages on consoles.</p></td>
</tr>
</tbody>
</table>
{{</ details >}}

## Một số command keys hữu ích

> Để dễ hình dung, ví dụ dưới đây sẽ sử dụng phương án echo ký tự vào /proc/sysrq-trigger

### Poweroff

```shell
root@vm1:/home/kien# echo o > /proc/sysrq-trigger
```

### Reboot

```shell
root@vm1:/home/kien# echo b > /proc/sysrq-trigger
```

### Crash

Trigger crashdump thủ công nếu hệ thống bị treo. Đây cũng là một cách hay để giả lập kernel crashdump.

```shell
root@vm1:/home/kien# echo c > /proc/sysrq-trigger
```

### Đồng bộ filesystems

```shell
root@vm1:/home/kien# echo s > /proc/sysrq-trigger
```

### Remount filesystem read-only

```shell
root@vm1:/home/kien# echo u > /proc/sysrq-trigger
root@vm1:/home/kien# touch abc
touch: cannot touch 'abc': Read-only file system
```

### Kill tất cả processes trừ tiến trình init

Command key này đặc biệt hữu ích nếu bạn có tiến trình không thể kill, đặc biệt nếu tiến trình đó liên tục spawning ra các tiến trình khác.

```shell
# Linux gửi SIGTERM đến tất cả các processes, trừ init
root@vm1:/home/kien# echo e > /proc/sysrq-trigger

# Linux gửi SIGKILL đến tất cả các processes, trừ init
root@vm1:/home/kien# echo i > /proc/sysrq-trigger
```

### Gọi OOM Killer

OOM Killer được gọi và hoàn thành nhiệm vụ của nó - kill tiến trình gây high memory usage.

```shell
root@vm1:/home/kien# echo f > /proc/sysrq-trigger
# Check kern.log để kiểm tra log
3585:Dec  5 03:31:40 vm1 kernel: [  195.899186] sysrq: Manual OOM execution
3586:Dec  5 03:31:40 vm1 kernel: [  195.901176] kworker/0:1 invoked oom-killer: gfp_mask=0xcc0(GFP_KERNEL), order=-1, oom_score_adj=0
```

### Xem danh sách blocked state processes

```shell
root@vm1:/home/kien# echo w > /proc/sysrq-trigger
# Check kern.log để kiểm tra
Dec  5 03:33:02 vm1 kernel: [  277.781446] sysrq: Show Blocked State
```
