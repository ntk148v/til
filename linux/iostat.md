# iostat

Source:

- <https://dom.as/2009/03/11/iostat/>
- <https://support.datastax.com/s/article/HOW-TO-Use-iostat-to-diagnose-CPU-and-IO-bottlenecks>

`avgqu-sz`: Very very very important value – how many requests are there in a request queue. Low = either your system is not loaded, or has serialized I/O and cannot utilize underlying storage properly. High = your software stack is scalable enough to load properly underlying I/O. Queue size equal to amount of disks means (in best case of request distribution) that all your disks are busy. Queue size higher than amount of disks means that you are already trading I/O response time for better throughput (disks can optimize order of operations if they know them beforehand, thats what NCQ – Native Command Queueing does). If one complains about I/O performance issues when avgqu-sz is lower, then it is application specific stuff, that can be resolved with more aggressive read-ahead, less fsyncs, etc. One interesting part – avqu-sz, await, svctm and %util are iterdependent (`await = avgqu-sz * svctm / (%util/100)`)

As a general rule of thumb, look for these thresholds:

- Single HDD: An avgqu-sz > 2 consistently is a red flag. Mechanical disks can only do one thing at a time; a long queue means processes are stuck waiting for the physical disk head to move.
- SSD / NVMe: An avgqu-sz of 10–30 might be normal. Modern SSDs use "Parallelism" and require a deeper queue to reach their maximum rated speed.
- RAID Arrays: The "safe" number is generally equal to the number of physical disks in the array. If you have 8 disks, a queue size of 8 is often fine.

When avgqu-sz climbs too high for your specific hardware, it creates a "traffic jam" effect across the entire system:

| Impact Area         | Effect                                                                                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Increased Latency   | As the queue grows, the await (average wait time) spikes. Tasks that should take 2ms start taking 100ms+.                                                                 |
| Application "Hangs" | Applications performing "Synchronous I/O" (waiting for a save/load to finish) will appear to freeze or become unresponsive.                                               |
| CPU Wait (%iowait)  | You will see your CPU usage show high "iowait." This means the CPU is healthy and ready to work, but it is sitting idle because it's waiting for the disk to return data. |
| Throughput Drop     | Paradoxically, if the queue gets too long, the overhead of managing that queue can actually cause the total MB/s (throughput) to drop.                                    |
