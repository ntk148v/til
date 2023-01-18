# Prometheus Service Discovery

> **NOTE**: It's a raw version, will re-work it soon :clown_face:

Service discovery (SD) enables you to provide that information to Prometheus from whichever database you store it in. Prometheus supports many common sources of service information, such as Consul, Amazon's EC2 and Kubernetes out of the box. If your particular source isn't already supported, you can use the file-based service discovery mechanism to hook it in. This could be by having your configuration management system, such as Ansible or Chef, write the list of machines and services they know about in the right format, or a script running regularly to pull it from whatever data source you use.

[TOC]

## Service Discovery Mechanisms

Service discovery isn't just about you providing a list of machines to Prometheus, or monitoring. It is a more general concern that you will see across your systems; applications need to find their dependencies to talk to, and hardware technicians need to know which machines are safe to turn off and repair.

A good service discovery mechanism will provide you with *metadata*. Metadata is what you will convert into target labels, and generally the more metadata you have, the better.

### Static

* Static configuration where targets are provided directly in the prometheus.yml.
* Combining with a configuration management tool such as Ansible, you could have its templating system write out a list of all the machines it knows about to have their Node exporters scraped.

```yaml
scape_configs:
  - job_name: node
    static_configs:
      - targets:
{% for host ini groups["all"] %}
        - {{ host }}:9100
{% endfor %}
```

### File

* File SD
* It reads monitoring targets from files you provide on the local filesystem.
* JSON or YAML formats.

```json
[
    {
        "targets": ["host1:9100", "host2:9100"],
        "labels": {
            "team": "infra",
            "job": "node"
        }
    },
    {
        "targets": ["host1:9090"],
        "labels": {
            "team": "monitoring",
            "job": "prometheus"
        }
    }
]
```

* Issue with JSON format is that the last item in a list or hash cannot have a trailing comma --> using JSON library to generate JSON files rather than trying to do it by hand.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
```

* Providing the targets with a file means it could come from templating in a configuration management system, a daemon that writes it out regularly, or even from a web service via a cronjob using wget.
* Changes are picked up automatically using inotify.

### Consul

* Consul service discovery is a service discovery mechanism that uses the network.
* Consul has an agent that runs on each of your machines, and these gossip amongst themselves. Applications talk only to the local agent on a machine.

![Image result for consul architecture](https://www.consul.io/assets/images/consul-arch-420ce04a.png)

* Sample config:

```yaml
scrape_configs:
  - job_name: consul
    consul_sd_configs:
      - server: 'localhost:8500'
```

## Relabelling

* Tell Prometheus how to map from metadata to targets using *relabelling*.
* Check [prometheus labels note.](./labels.md)

## Choosing what to scrape

* Which targets you actually want to scrape.
* *relabel action* + *regex*.
* Using a keep relabel action to only monitor targets with a team="infra" label.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
         - '*.json'
    relabel_configs:
      - source_labels: [team]
        regex: infra
        action: keep
```

* Two relabel actions requiring contradictory values for the team label.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
    relabel_configs:
      - source_labels: [team]
        regex: infra
        action: keep
      - source_labels: [team]
        regex: monitoring
        action: keep
```

* Using | to allow one label value or another.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
    relabel_configs:
      - source_labels: [team]
        regex: infra|monitoring
        action: keep
```

* Using multiple source labels.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
    relabel_configs:
      - source_labels: [job, team]
        regex: prometheus;monitoring
        action: drop
```

### Regular expressions

* [RE2](https://github.com/google/re2/wiki/Syntax) engine for regular expressions that comes with Go.

## Target labels

* Target labels are labels that are added to the labels of every time series returned from a scrape. They are **the identity of your targets**, and accordingly they should not generally vary over time as might be the case with version numbers or machine owners.
* It is common to add target labels for the broader scope of the application, such as whether it is in development or production, their region, datacenter, and which team manages them.
* Target labels ultimately allow you to select, group, and aggregate targets in PromQL.
* Cost: Every addtional label is one more you need to keep in mind for every single PromQL expression you write.
* As a rule of thumb your target labels should be a hierarchy, with each one adding additional distinctiveness

### Replace - How to aggregate monitoring data according to the environment?

* Using relabelling to specify your target labels: *replace action* - allows you to copy labels around, while also applying regular expressions.
* Using a replace relabel action to replace team="monitoring" with team="monitor"

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
     relabel_configs:
       - source_labels: [team]
         regex: monitoring
         replacement: monitor
         target_label: team
         action: replace

```

* Using a replace relabel action to remove a trailing from the team label.

```yaml
scrape_configs:
  - job_name: file
    file_sd_configs:
      - files:
          - '*.json'
    relabel_configs:
      - source_labels: [team]
        regex: '(.*)ing'
        replacement: '${1}'
        target_label: team
        action: replace
```

* Using a replace relabel action remove the team label

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
      - '*.json'
   relabel_configs:
    - source_labels: []
      regex: '(.*)'
      replacement: '${1}'
      target_label: team
      action: replace
```

* Using the defaults to remove the team label succinctly

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: []
      target_label: team
```

* Using the IP from Consul with port 9100 for the Node exporter

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_address]
      regex: '(.*)'
      replacement: '${1}:9100'
      target_label: __address__
```

* **Tip**: If relabelling produces 2 identical targets from one of your scrape  configs, they will be deduplicated automatically.

### job, instance and \_\_address\_\_

* If target has no `instance` label, it is defaulted to the value of the `__address__` label.
* `instance` along with `job` are two labels targets will always have, `job` being defaulted from the `job_name` configuration option.
* The`__address__` is the host and port Prometheus will connect to when scraping.
* **Tip**: Prometheus will perform DNS resolution on the `__address__` --> provide host:port rather than ip:port

### Labelmap

* The `labelmap` action is different from the `drop`, `keep` and `replace` actions you have already seen in that it applies to label names rather label values.

* Use the EC2 service tag as the job label, with all tags prefixed with monitor\_as additional target labels.

```yaml
scrape_configs:
  - job_name: ec2
    ec2_sd_configs:
      - region: <region>
        access_key: <access key>
        secret_key: <secret key>
    relabel_configs:
      - source_labels: [__meta_ec2_tag_service]
        target_label: job
      - regex: __meta_ec2_public_tag_monitor_(.*)
        replacement: '${1}'
        action: labelmap
```

### Lists

* Some service discovery mechanisms just have a list of tags. --> convert a list into key-value metadata. This is done by joining the items in the list with a comma and using the now-joined items as a label value. A comma is also put at the start and the end of the value, to make writing correct regular expressions easier.
* Keeping only Consul services with the prod tag

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_tag]
      regex:  '.*,prod,.*'
      action: keep
```

## How to scrape

### Duplicate Jobs

* `job_name` must be unique, as it is only a default, you are not prevented from having different scrape configs producing targets with the same job label.
* For example, if you had some jobs that required a different secretLabel clashes and honor_labels which were indicated by a Consul tag, you could segregate them using keep and drop actions, and then use a `replace` to set the `job` label

```yaml
- job_name: my_job
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel
    - source_labels: [__meta_consul_tag]
      regex:  '.*,specialsecret,.*'
      action: drop
   basic_auth:
     username: brian
     password: normalSecret

 - job_name: my_job_special_secret
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel
    - source_labels: [__meta_consul_tag]
      regex:  '.*,specialsecret,.*'
      action: keep
    - replacement: my_job
      target_label: job
   basic_auth:
     username: brian
     password: specialSecret
```

### metric\_label\_configs

* Check [labels](./labels.md)
* `labeldrop` and `labelkeep`: relabel actions that are unlikely to be ever required for target relabelling, but that can come up in metric relabelling.
* Similar to `labelmap`, they apply to label names rather than to label values. Instead of copying labels, `labeldrop` and `labelkeep` remove labels.
* Dropping all scraped labels that begin with node_

```yaml
scrape_configs:
 - job_name: misbehaving
   static_configs:
    - targets:
       - localhost:1234
   metric_relabel_configs:
    - regex: 'node_.*'
      action: labeldrop
```
