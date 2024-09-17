# Virtual machine CPU metrics

Libvirt virtual machine (domain) has multiple CPU metrics:

- `VIR_DOMAIN_CPU_STATS_CPUTIME`: cpu usage (sum of both vcpu and hypervisor usage) in nanoseconds, as a ullong.
- `VIR_DOMAIN_CPU_STATS_SYSTEMTIME`: cpu time charged to system instructions in nanoseconds, as a ullong.
- `VIR_DOMAIN_CPU_STATS_USERTIME`: cpu time charged to user instructions in nanoseconds, as a ullong.
- `VIR_DOMAIN_CPU_STATS_VCPUTIME`: vcpu usage in nanoseconds (cpu_time excluding hypervisor time), as a ullong.

If you want to visualize the CPU usage of the machine, you should use `VIR_DOMAIN_CPU_STATS_VCPUTIME` instead of `VIR_DOMAIN_CPU_STATS_CPUTIME` because `VIR_DOMAIN_CPU_STATS_CPUTIME` can be over 100%, it doesn't look right.
