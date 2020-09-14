# Monitoring Guide

- [Monitoring Guide](#monitoring-guide)
  - [1. Infrastructure and kernel metrics](#1-infrastructure-and-kernel-metrics)
  - [2. RabbitMQ metrics](#2-rabbitmq-metrics)
    - [2.1. Cluster-wide metrics](#21-cluster-wide-metrics)
    - [2.2. Node metrics](#22-node-metrics)
    - [2.3. Individual queue metrics](#23-individual-queue-metrics)
    - [2.4. Application-level metrics](#24-application-level-metrics)
  - [3. Some notes](#3-some-notes)

Source: https://www.rabbitmq.com/monitoring.html

## 1. Infrastructure and kernel metrics

- CPU stats (user, system, iowait & idle percentages)
- Memory usage (used, buffered, cached & free percentages)
- Virtual memory (dirty page flushes, writeback volume)
- Disk I/O (operation & amount of data transfered per unit time, time to service operations)
- Free disk space on the mount used for the node data directory
- File descriptors and [max_system_limit](https://www.rabbitmq.com/networking.html#open-file-handle-limit)
- TCP connections by state (`EASTABLISHED`, `CLOSE_WAIT`, `TIME_WAIT`)
- Network throughput (bytes received, bytes sent) & maximum network throughput
- Network latency (between all RabbitMQ nodes in a cluster as well as to/from clients)

## 2. RabbitMQ metrics

### 2.1. Cluster-wide metrics

- Cluster-wide metrics provide a high level view of cluster state.

| Metric                                                                      | JSON field name                                                                                                                     |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Cluster name                                                                | cluster_name                                                                                                                        |
| Cluster-wide message rates                                                  | message_stats                                                                                                                       |
| Total number of connections                                                 | object_totals.connections                                                                                                           |
| Total number of channels                                                    | object_totals.channels                                                                                                              |
| Total number of queues                                                      | object_totals.queues                                                                                                                |
| Total number of consumers                                                   | object_totals.consumers                                                                                                             |
| Total number of messages (ready plus unacknowledged)                        | queue_totals.messages                                                                                                               |
| Number of messages ready for delivery                                       | queue_totals.messages_ready                                                                                                         |
| Number of [unacknowledged](https://www.rabbitmq.com/confirms.html) messages | queue_totals.messages_unacknowledged                                                                                                |
| Messages published recently                                                 | message_stats.publish                                                                                                               |
| Message publish rate                                                        | message_stats.publish_details.rate                                                                                                  |
| Messages delivered to consumers recently                                    | message_stats.deliver_get                                                                                                           |
| Message delivery rate                                                       | message_stats.deliver_get.rate                                                                                                      |
| Other message stats                                                         | message_stats.\* (see [HTTP API reference](https://rawcdn.githack.com/rabbitmq/rabbitmq-management/v3.8.8/priv/www/api/index.html)) |

### 2.2. Node metrics

- There are 2 HTTP API endpoints that provide access to node-specific metrics:
  - GET /api/nodes/{node} returns stats for a single node
  - GET /api/nodes returns stats for all cluster members: return an array of objects -> prefer -> reduces the number of requests.

| Metric                                                                                        | JSON field name                   |
| --------------------------------------------------------------------------------------------- | --------------------------------- |
| Total amount of [memory used](https://www.rabbitmq.com/memory-use.html)                       | mem_used                          |
| Memory usage high watermark                                                                   | mem_limit                         |
| Is a [memory alarm](https://www.rabbitmq.com/memory.html) in effect?                          | mem_alarm                         |
| Free disk space low watermark                                                                 | disk_free_limit                   |
| Is a [disk alarm](https://www.rabbitmq.com/disk-alarms.html) in effect?                       | disk_free_alarm                   |
| [File descriptors available](https://www.rabbitmq.com/networking.html#open-file-handle-limit) | fd_total                          |
| File descriptors used                                                                         | fd_used                           |
| File descriptor open attempts                                                                 | io_file_handle_open_attempt_count |
| Sockets available                                                                             | sockets_total                     |
| Sockets used                                                                                  | sockets_used                      |
| Message store disk reads                                                                      | message_stats.disk_reads          |
| Message store disk writes                                                                     | message_stats.disk_writes         |
| Inter-node communication links                                                                | cluster_links                     |
| GC runs                                                                                       | gc_num                            |
| Bytes reclaimed by GC                                                                         | gc_bytes_reclaimed                |
| Erlang process limit                                                                          | proc_total                        |
| Erlang processes used                                                                         | proc_used                         |
| Runtime run queue                                                                             | run_queue                         |

### 2.3. Individual queue metrics

- Individual queue metrics are made available through the [HTTP API](https://www.rabbitmq.com/management.html#http-api) via the GET /api/queues/{vhost}/{qname} endpoint.

| Metric                                                                      | JSON field name                                                                                                                     |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Memory                                                                      | memory                                                                                                                              |
| Total number of messages (ready plus unacknowledged)                        | messages                                                                                                                            |
| Number of messages ready for delivery                                       | messages_ready                                                                                                                      |
| Number of [unacknowledged](https://www.rabbitmq.com/confirms.html) messages | messages_unacknowledged                                                                                                             |
| Messages published recently                                                 | message_stats.publish                                                                                                               |
| Message publishing rate                                                     | message_stats.publish_details.rate                                                                                                  |
| Messages delivered recently                                                 | message_stats.deliver_get                                                                                                           |
| Message delivery rate                                                       | message_stats.deliver_get.rate                                                                                                      |
| Other message stats                                                         | message_stats.\* (see [HTTP API reference](https://rawcdn.githack.com/rabbitmq/rabbitmq-management/v3.8.8/priv/www/api/index.html)) |

### 2.4. Application-level metrics

- What metrics applications track can be system-specific but some are relevant to most systems:
  - Connection opening rate
  - Channel opening rate
  - Connection failure (recovery) rate
  - Publishing rate
  - Delivery rate
  - Positive delivery acknowledgement rate
  - Negative delivery acknowledgement rate
  - Mean/95th percentile delivery processing latency

## 3. Some notes

- The recommended metric collection interval is 15 second. For production systems a collection interval of 30 or even 60 seconds is recommended. [Prometheus](https://www.rabbitmq.com/prometheus.html) exporter API is designed to be scraped every 15 seconds, including production systems.
- In a clustered environment every node can serve metric endpoint requests. Cluster-wide metrics can be fetched from any node that [can contact its peers](https://www.rabbitmq.com/management.html#clustering). That node will collect and combine data from its peers as needed before producing a response.
- Every node also can serve requests to endpoints that provide [node-specific metrics](https://www.rabbitmq.com/monitoring.html#node-metrics) for itself as well as other cluster nodes. Like with [infrastructure and OS metrics](https://www.rabbitmq.com/monitoring.html#system-metrics), node-specific metrics must be collected for each node. Monitoring tools can execute HTTP API requests against any node.
- As mentioned earlier, inter-node connectivity issues will [affect HTTP API behaviour](https://www.rabbitmq.com/management.html#clustering). Choose a random online node for monitoring requests. For example, using a load balancer or [round-robin DNS](https://en.wikipedia.org/wiki/Round-robin_DNS).
