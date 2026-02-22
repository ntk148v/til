# Instrumentation

A set of guidelines for instrumenting your code.

## How to instrument

> TL;DR: Everything.

The 3 types of services:

- Online-serving systems (most DB and HTTP requests):
  - Key metrics: the number of performed queries, errors and latency, the number of in-progress requests.
  - Should be monitored on both the client and server side.
- Offline processing:
  - Key metrics: the items coming in, how many are in progress, the last time you processed something, how many items were sent out, batches going in and out.
  - Approach: send a heartbeat through the system -> each stage can export the most recent heartbeat timestamp it has seen, letting you know how long items are taking to propagate through the system.
- Batch jobs:
  - Key metrics: the last time it succeeded.
  - For batch jobs that take more than a few minutes to run, it is useful to also scrape them using pull-based monitoring.
  - For batch jobs that run very often (say, more often than every 15 minutes), you could consider converting them into daemons and handling them as offline-processing jobs.
- Subsystems: In addition to the three main types of services, systems have sub-parts that should also be monitored.
- Libraries:
  - Libraries should provide instrumentation with no additional configuration required by users.
  - A library is used to access some resource outside of the process -> track the overall query count, errors.
  - Libraries should provide instrumentation with no additional configuration required by users.
  - A library is used to access some resource outside of the process -> track the overall query count, errors.
  - A library may be used by multiple independent parts of an application against different resources, so take care to distinguish users with labels where appropriate.
- Logging:
  - Key metrics: How often log message has been happening and for how long, total number of info/error/warning lines that were logged byh the application as a whole.
- Failures:
  - Key metrics: the total number of attempts.
- Threadpools:
  - Key metrics: the number of queued requests, the number of threads in use, the total number of threads, the number of tasks processed, how long they took, how long things were waiting in the queue.
- Caches:
  - Key metrics: total queues, hits, overall latency and then the query count, errors, and latency of whatever online-serving system the cache is in front of.
- Collectors:
  - Key metrics: how long the collection took in seconds and another for the number of errors encountered.

## Things to watch out for

- Use labels.
- Do not overuse labels.
- Counter vs. gauge, summaray vs. histogram.
- Timestamps, not time since.
- Inner loops.
- Avoid missing metrics.
