# systemd-cgtop

systemd-cgtop shows the top control groups of the local Linux control group hierarchy, ordered by their CPU, memory, or disk I/O load. The display is refreshed in regular intervals (by default every 1s), similar in style to top. If a control group path is specified, shows only the services of the specified control group.

Resource usage is only accounted for control groups with the appropriate controllers turned on: "memory" controller for memory usage and "io" controller for disk I/O consumption. If resource monitoring for these resources is required, it is recommended to add the MemoryAccounting=1 and IOAccounting=1 settings in the unit files in question.

The CPU load value can be between 0 and 100 times the number of processors the system has. For example, if the system has 8 processors, the CPU load value is going to be between 0% and 800%. The number of processors can be found in "/proc/cpuinfo".

To emphasize: unless "MemoryAccounting=1" and "IOAccounting=1" are enabled for the services in question, no resource accounting will be available for system services and the data shown by systemd-cgtop will be incomplete.
