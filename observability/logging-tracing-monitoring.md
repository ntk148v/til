# [Logging vs Tracing vs Monitoring](https://winderresearch.com/logging-vs-tracing-vs-monitoring/)

## Logging

- We use logging to represent state transformations within an application. When things go wrong, we need logs to establish what change in state caused the error. But the problem is that obtainining, transferring, storing and parsing logs is expensive. Because of this it is crucial to only log what is neccessary; only logs that can be acted upon should stored. Log only actionable information.
- Logging: identify **why**'s it happens.

## Tracing

- A trace represents a single user's journey through an entire stack of an application. It is often used for optimisation purposes. For example you would use it to establish little used part of a stack or bottlenecks within specific parts of the stack.
- But it adds significant complexity. There are often significant amounts of implementation code and is often designed as a push model, which means that applications could be affected by loading in the monitoring system.
- The libraries intended to simplify tracing are often more complicated than the code they serving.

## Instrumentation and Monitoring

- Instrumentating an application and monitoring the results represents the use of a system. It is most often used for diagnostic purposes. For example we would use monitoring systems to alert developers when the system is operating "normally".

![image](https://winderresearch.com/img/blog/2017/monitoring/monitor-all-the-things.jpg)

- Instrumentation tends to be very cheap to compute.
- Metrics to identify **what**'s going on.
