# Systems Performance

> [!Important]
> This is my (incomplete) own note taking away from [Systems Performance: Enterprise and the Cloud](https://www.amazon.com/Systems-Performance-Enterprise-Brendan-Gregg/dp/0133390098).
> Read the book to build more complete understanding.

## 1. Methododologies

### 1.1. Terminology

|               |                                                                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IOPS          | Input/output operations per second - the rate of data transfer operations                                                                                       |
| Throughput    | The rate of work performed -> the data rate (bytes per second or bits per second)                                                                               |
| Response time | The time for an operation to complete (time spent waiting + time spent being serviced (service time))                                                           |
| Latency       | A measure of time an operation spends waiting to be serviced.                                                                                                   |
| Utilization   | A measure of how busy a resource is, based on how much time in a given interval it was actively performing work(time-based or capacity-based)                   |
| Saturation    | The degree to which a resource has queued work it cannot service                                                                                                |
| Bottleneck    | A resource that limits the performance of the system                                                                                                            |
| Workload      | The input to the system or the load applied                                                                                                                     |
| Cache         | A fast storage area that can duplicate or buffer a limited amount of data, to avoid communicating directly with a slower tier of storage -> improve performance |

### 1.2. Concepts

- Trade-offs:
  - Good/Fast/Cheap "pick two".
  - Common trade-off:
    - CPU and memory, memory can be used to cache results, reducing CPU usage.
    - Network buffer size: small buffer sizes -> reduce the memory overhead/connection; large size -> improve network throughput.
- Tuning efforts: Performance tuning is most effective when done closest to where the work is performed.

| Layer        | Example Tuning Targets                                             |
| ------------ | ------------------------------------------------------------------ |
| Application  | Application logic, request queue sizes, database queries performed |
| Database     | Database table layout, indexes, buffering                          |
| System calls | Memory-mapped or read/write, sync or async I/O flags               |
| File system  | Record size, cache size, file system tunables, journaling          |
| Storage      | RAID level, number and type of disks, storage tunables             |

- Different organizations and environments have different requirements for performance. You may have joined an organization where it is the norm to analyze much deeper than you’ve seen before, or even knew was possible
- When to stop analysis:
  - When you're explained the bulk of the performance problem.
  - When the potential ROI is less than the cost of analysis.
  - When there are bigger ROIs elsewhere.
- Performance recommendations, especially the values of tunable parameters, are valid only at a specific _point in time_.
- Problems of load vs. architecture.
- Scalability:
  - The performance of a system as its load increases.
  - knee-point, saturation point
- Common types of system performance metrics:
  - Throughput: Either operations or data volume per second
  - IOPS: I/O operations per second
  - Utilization: How busy a resource is, as a percentage
  - Latency: Operation time, as an average or percentile
- Profiling builds a picture of a target that can be studied and understood.
- Caching is frequently used to improve performance.
  - hit ratio

### 1.3. Perspective

- Two common perspectives for performance analysis:
  - _workload analysis_
  - _resource analysis_
