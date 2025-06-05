# CPU Pinning (in OpenStack)

Source:

- <https://hpcclab.org/paperPdf/icpp20/icpp20.pdf>
- <https://mhsamsal.wordpress.com/2020/05/12/how-to-perform-cpu-pinning-for-kvm-virtual-machines-and-docker-containers/>

Table of contents:

- [CPU Pinning (in OpenStack)](#cpu-pinning-in-openstack)
  - [1. What is CPU Pinning?](#1-what-is-cpu-pinning)
  - [1.1. Operating system (OS) scheduler](#11-operating-system-os-scheduler)
  - [1.2. NUMA (non-uniform memory access)](#12-numa-non-uniform-memory-access)
  - [2. How to perform CPU Pinning](#2-how-to-perform-cpu-pinning)
    - [2.1. Pinning virtual machines in KVM](#21-pinning-virtual-machines-in-kvm)
    - [2.2. Pinning Docker containers](#22-pinning-docker-containers)
  - [3. Pinning in OpenStack](#3-pinning-in-openstack)
    - [3.1. Customize instance CPU pinning policies.](#31-customize-instance-cpu-pinning-policies)
    - [3.2. Customize instance emulator thread pinning policies.](#32-customize-instance-emulator-thread-pinning-policies)

## 1. What is CPU Pinning?

CPU pinning, or what is so called “processor affinity”, helps to bind a process to a certain set of CPU cores. In this way, the pinned process is executed only on the specified (pinned) CPU core(s). Although CPU pinning can drastically reduce the overhead of virtualized platforms, it is noteworthy that extensive use of pinning incurs a higher cost and makes the host management more challenging. Let's see why someone would need to enable CPU Pinning?

## 1.1. Operating system (OS) scheduler

- There are numerous processes being executed inside an OS and a queuing system is used to order and manage them. Because each processing core can execute just one process at a time, OS time shares the processes across the cores. Each process is executed for a limited time, known as "quantum", in a round-robin manner.

![](https://mhsamsal.wordpress.com/wp-content/uploads/2020/05/1.jpg?w=600)

## 1.2. NUMA (non-uniform memory access)

- Modern computers often have multiple (from 2 -> 10 of) processing cores that are all positioned on one CPU socket. Sever-class computers are designed to support as many as CPU cores possible, hence, they generally have several CPU sockets.
- Each CPU is assigned a set of memory (RAM) slots, however, the CPUs are able to share their memories via some interconnects (aka Bus).

![](https://mhsamsal.wordpress.com/wp-content/uploads/2020/05/3.jpg?w=600)

- The complexity of having multiple of cores across different CPU sockets: "what happens if a process is allocated on a different CPU cores in different quantums?" -> the process should reload its state and cache on the new CPU cores. It is also possible that the process needs to access its memory via the interconnect. In fact, the normal behavior of the OS scheduler is to disperse the processes as much as it can across all available CPU cores. Although the overhead of using interconnects and reloading the state is worthwhile for many processes to improve the overall CPU utilization, for time-sensitive processes it is better to override the OS scheduler and pinpoint a set of CPU cores to the process. Now, the definition of CPU pinning should makes sense, right?
- Each CPU socket representing one NUMA. Therefore, in a host with two CPU sockets, we can say there are two NUMA nodes.

```shell
numactl --hardware
```

![](https://mhsamsal.wordpress.com/wp-content/uploads/2020/05/5.jpg?w=768)

- You can see that there are 4 NUMA nodes (sockets) in this system, each featured with 28 CPU cores (totally 112 CPU cores). The exact CPU core ID working in each CPU socket is also shown. In addition, for each NUMA node, the total size of its memory and the amount of its free space is reported.
- For each NUMA node, the total size of its memory and the amount of its free space is reported. So, if you are to configure CPU pinning and want to find the best set of cores, you would better select them all inside one CPU socket to avoid the interconnect overhead.
- The last piece of information is a matrix showing the latency of using different NUMA nodes. The latency of each node to itself is the minimum. If you require more CPU cores than what is offered in one single socket, you would better to choose the socket that offers that least distance.

_Pinning could be used in order to tune the performance of a specific VM or container in a host_.

## 2. How to perform CPU Pinning

### 2.1. Pinning virtual machines in KVM

- Let's consider a VM, called "test", that is already created with default CPU configurations. In our scenario, we would like to pin 8 CPU cores to this VM.
- First, recall the `numactl` to know the NUMA nodes and the core IDs of each one.
- Modify the VM configuration file located in `/etc/libvirt/qemu/test.xml`
- Find the line starting with `vcpu`:

```xml
<vcpu placement='static'>8</vcpu>
```

- Change it:

```xml
<vcpu placement='static' cpuset='0,4,8,12,16,20,24,28'>8</vcpu>
```

- Restart libvirtd.

### 2.2. Pinning Docker containers

```shell
$ docker run --cpuset-cpus=0,4,8,12,16,20,24,28 --name test
```

## 3. Pinning in OpenStack

Source:

- <https://docs.openstack.org/nova/yoga/admin/cpu-topologies.html>
- <https://docs.redhat.com/en/documentation/red_hat_openstack_platform/10/html/ovs-dpdk_end_to_end_troubleshooting_guide/using_virsh_emulatorpin_in_virtual_environments_with_nfv>
- <https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_the_compute_service_for_instance_creation/assembly_configuring-cpus-on-compute-nodes#proc_configuring-emulator-threads_cpus>

> OpenStack release: Yoga
> Hypervisor: KVM + libvirt.

The NUMA topology and CPU pinning features in OpenStack provide high-level control over how instances run on hypervisor CPUs and the topology of virtual CPUs available to instances. These features help minimize latency and maximize performance.

### 3.1. Customize instance CPU pinning policies.

CPU pinning policies can be used to determine whether an instance should be pinned or not. They can be configured using the **hw:cpu_policy** extra spec and equivalent image metadata property. There are three policies: **dedicated**, **mixed** and **shared** (the default).

- The **dedicated** CPU policy is used to specify that all CPUs of an instance should use pinned CPUs.
- The **shared** CPU policy is used to specify that an instance should not use pinned CPUs.
- The **mixed** CPU policy is used to specify that an instance use pinned CPUs along with unpinned CPUs.

```shell

# Dedicated
$ openstack flavor set $FLAVOR --property hw:cpu_policy=dedicated

# Shared
$ openstack flavor set $FLAVOR --property hw:cpu_policy=shared

# Mixed
$ openstack flavor set $FLAVOR \
    --vcpus=4 \
    --property hw:cpu_policy=mixed \
    --property hw:cpu_dedicated_mask=0-1
```

### 3.2. Customize instance emulator thread pinning policies.

- In addition to the work of the guest OS and applications running in an instance, there is a small amount of overhead associated with the underlying hypervisor. By default, these overhead tasks - known collectively as emulator threads - run on the same host CPUs as the instance itself and will result in a minor performance penalty for the instance. This is not usually an issue, however, for things like real-time instances, it may not be acceptable for emulator thread to steal time from instance CPUs.
- Emulator threads handle interrupt requests and non-blocking processes for virtual machine hardware emulation.
- By default, nova will configure an emulator thread pin set which spans the pCPUs assigned to all vCPUs. If you are not using the `isolcpus` parameter, then emulator threads can be scheduled on any pCPU, and will periodically move from one pCPU to another. Therefore any of these CPUs can be preempted by qemu’s emulator threads, risking packet drops.

```shell
$ virsh dumpxml instance-0000001d
(...)
<vcpu placement='static'>4</vcpu>
<cputune>
    <shares>4096</shares>
    <vcpupin vcpu='0' cpuset='34'/>
    <vcpupin vcpu='1' cpuset='14'/>
    <vcpupin vcpu='2' cpuset='10'/>
    <vcpupin vcpu='3' cpuset='30'/>
    <emulatorpin cpuset='10,14,30,34'/>
</cputune>
(...)
```

- How emulatorpin works:

```shell
$ ps -T -p 73517
  PID    SPID TTY          TIME CMD
73517   73517 ?        00:00:00 qemu-kvm
73517   73527 ?        00:00:00 qemu-kvm
73517   73535 ?        00:00:06 CPU 0/KVM
73517   73536 ?        00:00:02 CPU 1/KVM
73517   73537 ?        00:00:03 CPU 2/KVM
73517   73538 ?        00:00:02 CPU 3/KVM
73517   73540 ?        00:00:00 vnc_worker

$ taskset -apc 73517
pid 73517's current affinity list: 10,14,30,34
pid 73527's current affinity list: 10,14,30,34
pid 73535's current affinity list: 34
pid 73536's current affinity list: 14
pid 73537's current affinity list: 10
pid 73538's current affinity list: 30
pid 73540's current affinity list: 10,14,30,34
```

```shell
# Check vcpupin
$ virsh vcpupin instance-0000001d | awk '$NF~/[0-9]+/ {print $NF}' | sort -n | while read CPU; do sed '/cpu#/,/runnable task/{//!d}' /proc/sched_debug | sed -n "/^cpu#${CPU},/,/^$/p" ; done

cpu#10, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/10    64         0.000000       107     0         0.000000        90.232791         0.000000 0 /
    ksoftirqd/10    65       -13.045337         3   120         0.000000         0.004679         0.000000 0 /
    kworker/10:0    66       -12.892617        40   120         0.000000         0.157359         0.000000 0 /
  kworker/10:0H    67        -9.320550         8   100         0.000000         0.015065         0.000000 0 /
    kworker/10:1 17996      9695.675528        23   120         0.000000         0.222805         0.000000 0 /
        qemu-kvm 73517      1994.534332     27105   120         0.000000       886.203254         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
        qemu-kvm 73527       722.347466        84   120         0.000000        18.236155         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
      CPU 2/KVM 73537      3356.749162     18051   120         0.000000      3370.045619         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu2
      vnc_worker 73540       354.007735         1   120         0.000000         0.047002         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
          worker 74584      1970.499537         5   120         0.000000         0.130143         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
          worker 74585      1970.492700         4   120         0.000000         0.071887         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
          worker 74586      1982.467246         3   120         0.000000         0.033604         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
          worker 74587      1994.520768         1   120         0.000000         0.076039         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
          worker 74588      2006.500153         1   120         0.000000         0.004878         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator

cpu#14, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/14    88         0.000000       107     0         0.000000        90.107596         0.000000 0 /
    ksoftirqd/14    89       -13.045376         3   120         0.000000         0.004782         0.000000 0 /
    kworker/14:0    90       -12.921990        40   120         0.000000         0.128166         0.000000 0 /
  kworker/14:0H    91        -9.321186         8   100         0.000000         0.016870         0.000000 0 /
    kworker/14:1 17999      6247.571171         5   120         0.000000         0.028576         0.000000 0 /
      CPU 1/KVM 73536      2274.381281      6679   120         0.000000      2287.691654         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu1

cpu#30, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/30   180         0.000000       107     0         0.000000        89.206960         0.000000 0 /
    ksoftirqd/30   181       -13.045892         3   120         0.000000         0.003828         0.000000 0 /
    kworker/30:0   182       -12.929272        40   120         0.000000         0.120754         0.000000 0 /
  kworker/30:0H   183        -9.321056         8   100         0.000000         0.018042         0.000000 0 /
    kworker/30:1 18012      6234.935501         5   120         0.000000         0.026505         0.000000 0 /
      CPU 3/KVM 73538      2474.183301     12595   120         0.000000      2487.479666         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu3

cpu#34, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/34   204         0.000000       107     0         0.000000        89.067908         0.000000 0 /
    ksoftirqd/34   205       -13.046824         3   120         0.000000         0.002884         0.000000 0 /
    kworker/34:0   206       -12.922407        40   120         0.000000         0.127423         0.000000 0 /
  kworker/34:0H   207        -9.320822         8   100         0.000000         0.017381         0.000000 0 /
    kworker/34:1 18016     10788.797590         7   120         0.000000         0.042631         0.000000 0 /
      CPU 0/KVM 73535      5969.227225     14233   120         0.000000      5983.425363         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu0

# Emulator threads can be moved by using virsh emulatorpi
$ virsh emulatorpin instance-0000001d 34

$ ps -T -p 73517
  PID    SPID TTY          TIME CMD
73517   73517 ?        00:00:00 qemu-kvm
73517   73527 ?        00:00:00 qemu-kvm
73517   73535 ?        00:00:06 CPU 0/KVM
73517   73536 ?        00:00:02 CPU 1/KVM
73517   73537 ?        00:00:03 CPU 2/KVM
73517   73538 ?        00:00:02 CPU 3/KVM
73517   73540 ?        00:00:00 vnc_worker

$ taskset -apc 73517
pid 73517's current affinity list: 34
pid 73527's current affinity list: 34
pid 73535's current affinity list: 34
pid 73536's current affinity list: 14
pid 73537's current affinity list: 10
pid 73538's current affinity list: 30
pid 73540's current affinity list: 34
```

```shell
# Note the number of switches in the historic data in /proc/sched_debug. In the following example, PID 73517 already moved to cpu#34. The other emulator workers did not run since the last output, and therefore still show on cpu#10
$ virsh vcpupin instance-0000001d | awk '$NF~/[0-9]+/ {print $NF}' | sort -n | while read CPU; do sed '/cpu#/,/runnable task/{//!d}' /proc/sched_debug | sed -n "/^cpu#${CPU},/,/^$/p" ; done
cpu#10, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/10    64         0.000000       107     0         0.000000        90.232791         0.000000 0 /
    ksoftirqd/10    65       -13.045337         3   120         0.000000         0.004679         0.000000 0 /
    kworker/10:0    66       -12.892617        40   120         0.000000         0.157359         0.000000 0 /
   kworker/10:0H    67        -9.320550         8   100         0.000000         0.015065         0.000000 0 /
    kworker/10:1 17996      9747.429082        26   120         0.000000         0.255547         0.000000 0 /
        qemu-kvm 73527       722.347466        84   120         0.000000        18.236155         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
       CPU 2/KVM 73537      3424.520709     21610   120         0.000000      3437.817166         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu2
      vnc_worker 73540       354.007735         1   120         0.000000         0.047002         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator

cpu#14, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/14    88         0.000000       107     0         0.000000        90.107596         0.000000 0 /
    ksoftirqd/14    89       -13.045376         3   120         0.000000         0.004782         0.000000 0 /
    kworker/14:0    90       -12.921990        40   120         0.000000         0.128166         0.000000 0 /
   kworker/14:0H    91        -9.321186         8   100         0.000000         0.016870         0.000000 0 /
    kworker/14:1 17999      6247.571171         5   120         0.000000         0.028576         0.000000 0 /
       CPU 1/KVM 73536      2283.094453      7028   120         0.000000      2296.404826         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu1

cpu#30, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/30   180         0.000000       107     0         0.000000        89.206960         0.000000 0 /
    ksoftirqd/30   181       -13.045892         3   120         0.000000         0.003828         0.000000 0 /
    kworker/30:0   182       -12.929272        40   120         0.000000         0.120754         0.000000 0 /
   kworker/30:0H   183        -9.321056         8   100         0.000000         0.018042         0.000000 0 /
    kworker/30:1 18012      6234.935501         5   120         0.000000         0.026505         0.000000 0 /
       CPU 3/KVM 73538      2521.828931     14047   120         0.000000      2535.125296         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu3

cpu#34, 2197.477 MHz
runnable tasks:
            task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
----------------------------------------------------------------------------------------------------------
    migration/34   204         0.000000       107     0         0.000000        89.067908         0.000000 0 /
    ksoftirqd/34   205       -13.046824         3   120         0.000000         0.002884         0.000000 0 /
    kworker/34:0   206       -12.922407        40   120         0.000000         0.127423         0.000000 0 /
   kworker/34:0H   207        -9.320822         8   100         0.000000         0.017381         0.000000 0 /
    kworker/34:1 18016     10788.797590         7   120         0.000000         0.042631         0.000000 0 /
        qemu-kvm 73517         2.613794     27706   120         0.000000       941.839262         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/emulator
       CPU 0/KVM 73535      5994.533905     15169   120         0.000000      6008.732043         0.000000 0 /machine.slice/machine-qemu\x2d1\x2dinstance\x2d0000001d.scope/vcpu0
```

- Emulator thread policies can be used to ensure emulator threads are run on cores separate from those used by the instance. There are two policies: **isolate** and **share**. The default is to run the emulator threads on the same core. The **isolate** emulator thread policy is used to specify that emulator threads for a given instance should be run on their own unique core, chosen from one of the host cores listed in `compute.cpu_dedicated_set`. To configure a flavor to use the isolate emulator thread policy, run:

```shell
openstack flavor set $FLAVOR \
  --property hw:cpu_policy=dedicated \
  --property hw:emulator_threads_policy=isolate
```

<table>
<thead valign="bottom">
<tr><th>&nbsp;</th>
<th><a href="#id38"><span id="user-content-id39">:oslo.config:option:`compute.cpu_shared_set`</span></a> set</th>
<th><a href="#id40"><span id="user-content-id41">:oslo.config:option:`compute.cpu_shared_set`</span></a> unset</th>
</tr>
</thead>
<tbody valign="top">
<tr><th><code>hw:emulator_treads_policy</code> unset (default)</th>
<td>Pinned to all of the instance's pCPUs</td>
<td>Pinned to all of the instance's pCPUs</td>
</tr>
<tr><th><code>hw:emulator_threads_policy</code> = <code>share</code></th>
<td>Pinned to <a href="#id42"><span id="user-content-id43">:oslo.config:option:`compute.cpu_shared_set`</span></a></td>
<td>Pinned to all of the instance's pCPUs</td>
</tr>
<tr><th><code>hw:emulator_threads_policy</code> = <code>isolate</code></th>
<td>Pinned to a single pCPU distinct from the instance's pCPUs</td>
<td>Pinned to a single pCPU distinct from the instance's pCPUs</td>
</tr>
</tbody>
</table>
