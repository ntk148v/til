# Elasticsearch Garbage Collector

After Elasticsearch 6.5, garbage first garbage collector (G1GC) is started to support.

## 1. Concurrent Mark Sweep (CMS)

- Default.
- Design for short pauses.
- CMS uses application threads to trace reachable objects references concurrently.

```
## GC configuration
-XX:+UseConcMarkSweepGC
# CMS won't start until old gen's occupancy rate reaches 75%
# If JVM allocates too much memory, old gen of garbage collector is much larger than normal,
# CMS trigger operation will be delayed.
# It aslo means that a lot of space for long-lived objects, CMS takes a longer
# time to clear large old gen.
-XX:CMSInitiatingOccupancyFraction=75
-XX:+UseCMSInitiatingOccupancyFraction
```

- To get the best performance from CMS, run the JVM with the low memory (less than 8GB).

## 2. Garbage First Garbage Collector (G1GC)

- Low-pause, server-style generational garbage collector for JVM.
- The G1 GC uses concurrent and parallel phases to achieve its target pause time and to maintain good throughput. When G1 GC determines that a garbage collection is necessary, it collects the regions with the least live data first (garbage first).
  - Allocating objects to a young generation and promoting aged objects into an old generation.
  - Finding live objects in the old generation through a concurrent (parallel) marking phase. The JVM triggers the marking phase when the total Java heap occupancy exceeds the default threshold.
  - Recovering free memory by compacting live objects through parallel copying.
- G1GC is a regionalized and generational GC, which means that the Java object heatp (heap) is divided into a number of equally sized regions. Upon startup, the Java Virtual Machine (JVM) sets the region size. The region sizes can vary from 1 MB to 32 MB depending on the heap size. The goal is to have no more than 2048 regions.

- Memory structure for G1GC:

![](http://itdoc.hitachi.co.jp/manuals/link/has_v101001/0341420De/GUID-26DC006B-F4C4-40F7-B367-390F902A212A-low.gif)

- GC flow:

![](http://itdoc.hitachi.co.jp/manuals/link/has_v101001/0341420De/GUID-7DD40728-5469-455C-93FA-823F9536C6B7-low.gif)

- For details check:

  - <https://www.oracle.com/technical-resources/articles/java/g1gc.html>
  - <http://itdoc.hitachi.co.jp/manuals/link/has_v101001/0341420De/0027.HTM>

- Important defaults:

```
## GC configuration

-XX:+UseG1GC
# When G1GC is triggerd, stop the world phase begins. It can wait until your MaxGCPauseMillis parameter.
-XX:MaxGCPauseMillis=300
# Set the size of a G1 region. The value will be a power of two and can range from 1MB to 32MB.
# The goal is to have around 2048 regions based on the minimum Java heap size.
-XX:G1HeapRegionSize=n
# Set the percentage of the heap to use as the minimum for the young generation size.
# Default: 5% heapsize. (Experimental tag)
-XX:G1NewSizePercent=5
# Set the percentage of the heap to use as the maximum for the young generation size.
# Default: 60% heap size. (Experimental tag)
-XX:G1MaxNewSizePercent=60
# Set the value of the Stop-the-world (STW) worker threads. Set the value of n to the number of logical processors.
# The value of n is the same as the number of logical processors up to a value of 8.
-XX:ParallelGCThreads=n
# Sets the number of parallel marking threads.
# Sets n to approximately 1/4 of the number of parallel garbage collection threads (ParallelGCThreads).
-XX:ConcGCThreads=n
# Sets the Java heap occupancy threshold that triggers a marking cycle.
# Default: 45% heap size.
-XX:InitiatingHeapOccupancyPercent=45
# Sets the occupancy threshold for an old region to be included in a mixed garbage collection cycle.
# Default: 65% heap size. (Experimental tag)
-XX:G1MixedGCLiveThresholdPercent=65
# Sets the percentage of heap that you are willing to waste.
-XX:G1HeapWastePercent=10
# Sets the target number of mixed garbage collections after a marking cycle to collect
# old regions with at most G1MixedGCLIveThresholdPercent live data.
# Default: 8 mixed garbage collections.
-XX:G1MixedGCCountTarget=8
# Set an upper limit on the number of old regions to be collected during a mixed garbage collection cycle.
# Default: 10% heap size.
-XX:G1OldCSetRegionThresholdPercent=10
# Set the percentage of reserve memory to keep free so as to reduce the risk of to-space overflows.
# Default: 10% heap size.
-XX:G1ReservePercent=10
```

- The G1GC can help with if JVM heap size is larger than 8GB.
