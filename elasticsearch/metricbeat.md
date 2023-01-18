# Metricbeat Overview

## Overview

* Metricbeat is a *lightweight* shipper that you can install on your servers to periodically collect *metrics from the operating systems and from services* running on the server.

* Metricbeat can insert the collected metrics directly into Elasticsearch or send them to Logstash, Redis or Kafka.

* Metricbeat is an Elastic [Beat](https://www.elastic.co/products/beats). It’s based on the `libbeat` framework. (Golang)

![Beats Platform](https://www.elastic.co/guide/en/beats/libbeat/6.7/images/beats-platform.png)

* One binary, lots of [modules](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-modules.html).

## Getting started with Metricbeat

Check [official documentation](<https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-getting-started.html>).

Important points:

* Default metricbeat configuration file: `metricbeat.yml`.

* To configure Metricbeat:

  * Enable the modules that you want to run (by default, Metricbeat collects system metrics only).
  * Add module configs to the `metricbeat.yml` ([Standard config options](https://www.elastic.co/guide/en/beats/metricbeat/current/configuration-metricbeat.html#module-config-options)). For example, like this.

  ```yaml
   module: apache
    metricsets: ["status"]
    hosts: ["http://127.0.0.1/"]
    period: 10s
    fields:
      dc: west
    tags: ["tag"]
    processors:
    ....
  ```

  * Configure the output.

* Multiple modules in just one metricbeat configure.

* [Index templates](https://www.elastic.co/guide/en/elasticsearch/reference/6.7/indices-templates.html) are used to define settings and mappings that determine how fields should be analyzed --> recommend to use default template.

## How Metricbeat works

* Metricbeat consists of *modules* and *metricsets*.
* A Metricbeat *module* defines the basic logic for collecting data from a specific service (details about the service - how to connect, how often to collect metrics and which metrics to collect).

* Each module has one or more metricsets. A *metricset* is the part of the module that fetchs and structures the data.

![Modules and metricsets](https://www.elastic.co/guide/en/beats/metricbeat/current/images/module-overview.png)

* Metricsets make it easier for you by *grouping sets of related metrics together* in a single request returned by the remote server.

* Metricbeat retrieves metrics by periodically - reuses connections whenever possible.
* Metricbeat sends the events asynchronously.
* Metricbeat events:
  * Event structure
  * Error event structure

## Compare with Prometheus stack

This is my personal points.

| Metricbeat - Elastic stack                                   | Prometheus stack                                             |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| One binary, a lot of modules --> just deploy 1 time and spend time to enable and configure modules. | There are a number of libraries and servers which help in exporting existing metrics from third-party systems as Prometheus metrics. --> more lightweight (sometimes), easier to extend. |
| Push model                                                   | Pull model                                                   |
| Metricsets + reuse connections                               | ?                                                            |
| Flat model                                                   | Flat model                                                   |
| No service discovery mechanism                               | Service discovery mechanism: checked.                        |
| Allow to set a dictionary of fields that will be sent with metricset events | Not allowed generally                                        |
| Metric tags                                                  | Metric labels                                                |
| Elasticsearch natively supports replication shards. Elasticsearch is "highly available" by design and by default. | Run identical Prometheus servers on two or more separate machines. Identical alerts will be deduplicated by the [Alertmanager](https://github.com/prometheus/alertmanager). |

Btw, Metric could collects Prometheus metrics. Check [this](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-metricset-prometheus-collector.html).

> The Prometheus `collector` metricset fetches data from [prometheus exporters](https://prometheus.io/docs/instrumenting/exporters/).
>
> All events with the same labels are grouped together as one event. The fields exported by this metricset vary depending on the Prometheus exporter that you’re using.
