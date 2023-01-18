# Adaptive process and memory management for Python web servers

Source: <https://instagram-engineering.com/adaptive-process-and-memory-management-for-python-web-servers-15b0c410a043>

## Respawning in the uWSGI process model

### uWSGI process model

1. At start time, uWSGI master reads in a static config.
2. The uWSGi master forks a certain number of worker processes.
3. Each worker process handles one request at a time.

### The previous approach

Use 2/worker thresholds to control respawn: reload-on-rss and evil-reload-on-rss.

1. Initially, the master process allocates a piece of shared memory which contains an entry for each worker.
2. A worker process starts a background thread to collect its RSS usage and updates its entry in shared memory.
3. At the end of each request, a worker process checks whether its RSS is higher than reload-on-rss. If yes, the worker process performs some cleanup tasks, sets a deadline for itself and calls exit().
4. The master process checks the status of the workers against the following conditions:

* If a worker initiated the exit process but didn't finish before the deadline, the master process will sigkill it to avoid bigger issues.
* If the RSS of a worker exceeds evil-reload-on-rss, master process will sigkill it too.

## Problems

1. Legacy uWSGI respawn is based on worker RSS, which includes both shared and private memory. As mentioned earlier, the worker processes share a lot of pages with the master process.
2. uWSGI processes consume most of the host physical memory -> Instagram, resource usage varies widely across different hosts -> N-per-worker-threholds-based respawn is an unsuitable control for host level memory usage.
3. uWSGI uses a static config to decide the number of worker processes. However, most of the time the number of required workers is considerably lower than the maximum number of allowed workers -> 20-40% of the workers remain idle for ~90% of the time.

## Solutions

Guiding principles were:

* Reduce uWSGI respawn rate.
* Prevent resource waste.
* Have a tight control on host memory usage to ensure the health of the system.

### 1. Host memory-based respawn

2 thresholds, based on host level memory utilization.

Each worker process still runs a background thread to update its memory usage in shared memory. Master loop checks current host level memory utilization. if it's greater than L (lower bound), then the master process picks a certain number of workers with the highest memory usage and sets a flag in their corresponding entries in shared memory. At the end of each request, a worker checks this flag instead and acts accordingly. If host memory utilization is greater than U (Upper bound) then master would sigkill the workers immediately.

The number of workers to kill is decided by a simple quadratic algorithm. The closer it is to the upper limit, the more workers we’d like to kill to avoid OOM.

### 2. Adaptive respawn

The uWSGi master monitors the size of the tcp connection backlog. The expectation is that workers are able to quickly process requests, and that the queue is short. When process parallelism is more than needed, however, we may empty the listen queue while there could be some workers still sitting idle and consuming physical memory.

Implemented listen queue-based adaptive uWSGI respawn. Specifically, if there are at least certain number of idle workers, and if the listen queue is nearly empty, the master process will delay worker respawn. Otherwise, it’ll spawn additional worker processes (up to some limit).
