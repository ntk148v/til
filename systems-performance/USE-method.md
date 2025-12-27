# USE method

Source: <https://www.brendangregg.com/usemethod.html>

## 1. Summary

> [!important]
> For every resource, check utilization, saturation, and errors.

Terminology definitions:
- resource: all physical server functional components (CPUs, disks, busses, ...).
- utilization: the average time that the resource was busy servicing work.
- saturation: the degree to which the resource has extra work which it can't service, often queued
- errors: the count of error events.

The metrics are usually expressed in the following terms:
- utilization: as a percent over a time interval. eg, "one disk is running at 90% utilization".
- saturation: as a queue length. eg, "the CPUs have an average run queue length of four".
- errors: scalar counts. eg, "this network interface has had fifty late collisions".

A burst of high utilization can cause saturation and performance issues, even though utilization is low when averaged over a long interval.

## 2. Resource list

- CPUs: sockets, cores, hardware threads (virtual CPUs)
- Memory: capacity
- Network interfaces
- Storage devices: I/O, capacity
- Controllers: storage, network cards
- Interconnects: CPUs, memory, I/O

The USE Method is most effective for resources that suffer performance degradation under high utilization or saturation, leading to a bottleneck. Caches improve performance under high utilization.

## 3. Suggested Interpretations

The USE Method helps you identify which metrics to use. After learning how to read them from the operating system, your next task is to interpret their current values.

The following are some general suggestions for interpreting metric types:

- **Utilization**: 100% utilization is usually a sign of a bottleneck (check saturation and its effect to confirm). High utilization (eg, beyond 70%) can begin to be a problem for a couple of reasons:
  - When utilization is measured over a relatively long time period (multiple seconds or minutes), a total utilization of, say, 70% can hide short bursts of 100% utilization.
  - Some system resources, such as hard disks, cannot be interrupted during an operation, even for higher-priority work. Once their utilization is over 70%, queueing delays can become more frequent and noticeable. Compare this to CPUs, which can be interrupted ("preempted") at almost any moment.
- **Saturation**: any degree of saturation can be a problem (non-zero). This may be measured as the length of a wait queue, or time spent waiting on the queue.
- **Errors**: non-zero error counters are worth investigating, especially if they are still increasing while performance is poor.

## 4. Strategy

![](https://www.brendangregg.com/USEmethod/usemethod_flow.png)
