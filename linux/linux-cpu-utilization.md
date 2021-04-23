# Linux CPU Utilization

## Task

Display the current CPU utilization, as a percentage, calculated from `/proc/stat`.

## Solution

Most Linux kernels provide a virtual [/proc](https://www.kernel.org/doc/Documentation/filesystems/proc.txt) filesystem, providing an interface to various internal data structures.

One of these internal structures (`/proc/stat`) includes information on the amount of time (in `USER_HZ`) spent in various states. To determine the current level of CPU utilization from this information:
1. read the 1st line of `/proc/stat`
2. discard the first word of that first line (`cpu`)
3. sum all of the times found on that first line to get the total time
4. divide the 4th column (`idle`) by the total time, to get the fraction of time spent being idle
5. subtract the previous fraction from 1.0 to get the time spent being not idle
6. multiple by 100 to get a percentage
7. To get a more real-time utilization, simple repeat the steps above with some small sleep interval in between.

```bash
# cat /proc/stat
cpu  14786866 5251 3483876 75457666 367491 0 1796945 0 0 0
cpu0 4877246 1597 844536 17736624 88425 0 598115 0 0 0
cpu1 3054061 1076 890314 19490622 88362 0 566587 0 0 0
cpu2 3273462 1090 872208 19277044 99891 0 402594 0 0 0
cpu3 3582096 1488 876816 18953375 90812 0 229647 0 0 0
# ...
```

## Source code

1. [Python](https://github.com/ntk148v/testing/tree/master/python/cpu_util.py)
2. [Golang](https://github.com/ntk148v/testing/tree/master/golang/cpu-util/main.go)
