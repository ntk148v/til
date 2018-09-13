# Linux Memory

## Context

* Yesterday, I got a several alerts that said container elasticsearch uses too much memory - around 60GB. 60GB, damn it! A huge number, right?
* But hold on, something was missed here. `docker stats elasticsearch` result was just 30GB.
* Anything wrong? Double check at alert rules, it seems correct. So why two results was too different?

## Cadvisor/cgroup memory usage definition

* Cadvisor gets container's memory stats through cgroups. The memory metrics that tracked in the cadvisor here:

```
# HELP container_memory_cache Number of bytes of page cache memory.
# TYPE container_memory_cache gauge
container_memory_cache{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 14
# HELP container_memory_failcnt Number of memory usage hits limits
# TYPE container_memory_failcnt counter
container_memory_failcnt{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 0
# HELP container_memory_failures_total Cumulative count of memory allocation failures.
# TYPE container_memory_failures_total counter
container_memory_failures_total{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",scope="container",type="pgfault",zone_name="hello"} 10
container_memory_failures_total{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",scope="container",type="pgmajfault",zone_name="hello"} 11
container_memory_failures_total{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",scope="hierarchy",type="pgfault",zone_name="hello"} 12
container_memory_failures_total{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",scope="hierarchy",type="pgmajfault",zone_name="hello"} 13
# HELP container_memory_mapped_file Size of memory mapped files in bytes.
# TYPE container_memory_mapped_file gauge
container_memory_mapped_file{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 16
# HELP container_memory_max_usage_bytes Maximum memory usage recorded in bytes
# TYPE container_memory_max_usage_bytes gauge
container_memory_max_usage_bytes{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 8
# HELP container_memory_rss Size of RSS in bytes.
# TYPE container_memory_rss gauge
container_memory_rss{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 15
# HELP container_memory_swap Container swap usage in bytes.
# TYPE container_memory_swap gauge
container_memory_swap{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 8192
# HELP container_memory_usage_bytes Current memory usage in bytes, including all memory regardless of when it was accessed
# TYPE container_memory_usage_bytes gauge
container_memory_usage_bytes{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 8
# HELP container_memory_working_set_bytes Current working set in bytes.
# TYPE container_memory_working_set_bytes gauge
container_memory_working_set_bytes{container_env_foo_env="prod",container_label_foo_label="bar",id="testcontainer",image="test",name="testcontaineralias",zone_name="hello"} 9
```

* The metric I've used is `container_memory_usage_bytes` which isn't extact memory usage. According [cgroup memory usage\_in\_byte definition](https://www.kernel.org/doc/Documentation/cgroup-v1/memory.txt), *For efficiency, as other kernel components, memory cgroup uses some optimization to avoid unnecessary cacheline false sharing. usage_in_bytes is affected by the method and doesn't show 'exact' value of memory (and swap) usage, it's a fuzz value for efficient access.* It means Memory usage is total usage including `cold` pages which the kernel can reclaim safely under pressure. In simple words, `container_memory_usage_bytes` includes filesystem caches items that can be evicted under memory pressure (About memory pressure, check cgroup link above).

* This explanation makes everything in context be clear now. The difference between `docker stats` result and `container_memory_usage_bytes` is cache!

* So using `container_memory_usage_bytes` is not suitable now. The better metric is `container_memory_working_set_bytes` as this is what the OOM killer is watching for. Memory working set is the bytes of memory that the kernel deems to be necessary for continuing to run the processes in the container. Kernel cnanot tolerate overcommitment of the sum total of working set (Refer [github issue](https://github.com/google/cadvisor/issues/913)).
