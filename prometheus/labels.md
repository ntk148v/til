# Prometheus labels

### Labels

* Labels are a key part of Prometheus. and one of the things that make it powerful.
* Labels are key-value pairs associated with time series that in addition to the metric name uniquely identify them.
* Labels come from two sources, *instrumentation labels* and *target labels*.
* Instrumentation labels as the name indicates come from your instrumentation. They are about things that are known inside your application or library, such as the type HTTP requests it receives, which databases it talks to and other internals.
* Target labels identify a specific monitoring target, that is a target that Prometheus scrapes. They relate more to your architecture and may include which application it is, what datacenter it lives in, if it is in a development or production environment.
* Target labels come from service discovery and relabeling.

## Relabeling

> NOTE: These two following pictures was gotten from [Life of label](https://www.robustperception.io/life-of-a-label). These one may be out-dated, based on Prometheus 0.17.0.

### relabel\_configs

![relabel_configs](https://www.robustperception.io/wp-content/uploads/2016/03/Life-of-a-Label-Target-Labels-495x640.png)

### metric\_relabel\_configs

![metrics_relabel_configs](https://www.robustperception.io/wp-content/uploads/2016/03/Life-of-a-Label-Scraping-445x640.png)

### relabel\_configs vs metric\_relabel\_configs

* Prometheus needs to know what to scrape, and that's the where service discovery and `relabel_configs` come in. Relabel configs allow you to select which targets you want to scraped, and what the target labels will be. So if you want to say scrape this type of machine but not that one, use `relabel_configs`.

* `metrics_relabel_configs` by contrast are applied after the scrape has happened, but before the data is ingested by the storage system. So if there are some expensive metrics you want to drop, or labels coming from the scrape itself that you want to manipulate that's where `metrics_relabel_configs` applies.

* So as a simple rule of thumb: `relabel_configs` happens before the scrape, `metrics_relabel_configs` happens after the scrape. And if one doesn't work you can always try the other!

### Use cases

Check [Prometheus relabeling tricks](https://medium.com/quiq-blog/prometheus-relabeling-tricks-6ae62c56cbda)

* Drop unnecessary metrics

```
- job_name: cadvisor
  ...
  metric_relabel_configs:
  - source_labels: [__name__]
    regex: '(container_tasks_state|container_memory_failures_total)'
    action: drop
```

* Drop unnecessary time-series

```
- job_name: cadvisor
  ...
  metric_relabel_configs:
  - source_labels: [id]
    regex: '/system.slice/var-lib-docker-containers.*-shm.mount'
    action: drop
  - source_labels: [container_label_JenkinsId]
    regex: '.+'
    action: drop
```

* Drop sensitive or unwanted labels from metrics

```
- job_name: cadvisor
  ...
  metric_relabel_configs:
  - regex: 'container_label_com_amazonaws_ecs_task_arn'
    action: labeldrop
```

* Amend label format of the final metrics

```
- job_name: cadvisor
  ...
  metric_relabel_configs:
  - source_labels: [image]
    regex: '.*/(.*)'
    replacement: '$1'
    target_label: id
  - source_labels: [service]
    regex: 'ecs-.*:ecs-([a-z]+-*[a-z]*).*:[0-9]+'
    replacement: '$1'
    target_label: service
```

### Real-world use case

* **Scenario**: You have OpenStack cluster and you want to monitor its instance metrics dynamically. Ok, assume you got all instance (per project) metrics but endpoint (and instance) was something like `10.240.203.210:9100/...`. You are unable to know which instance when look at this. So let's change this to instance name.

```
- job_name: 'openstack-node-exporter'
    openstack_sd_configs:
      - role: instance
        identity_endpoint: '...'
        username: '...'
        password: '...'
        domain_name: '...'
        port: 9100 # default node-exporter port
        refresh_interval: 20s
        region: '...'
        project_name: '...'
        all_tenants: true

    relabel_configs:
      # keep only acgive instances
      - source_labels: [__meta_openstack_instance_status]
        action: keep
        regex: ACTIVE

      # replace the default instance by the Openstack instance name
      - source_labels: [__meta_openstack_instance_name]
        target_label: instance

      # amend label format of the final metrics
      - source_labels: [__meta_openstack_tag_service]
        target_label: service
        replacement: $1
```
