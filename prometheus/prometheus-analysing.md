# Analysing Prometheus

## Analysing Prometheus Memory Usage

https://www.robustperception.io/analysing-prometheus-memory-usage

Prometheus is linked with [pprof](https://golang.org/pkg/net/http/pprof/), a Go profiling tool that makes it easy to look at CPU and memory usage. To use it against a Prometheus server to investigate memory usage, ensure you have a working Go install and then run:

```
go tool pprof -svg http://<prometheus-ip>:9090/debug/pprof/heap > heap.svg
```

Output:

![](./imgs/heap12.svg)

Useful metrics:

- `process_resident_memory_bytes`: the amount of memory the Prometheus process is using from the kernel.
- `go_memstats_alloc_bytes`: how much Go is using from that. A large difference between these two could indicate spiky memory usage, or fragmentation issues.

## Using tsdb analyze to investigate churn and cardinality

- How many time series you have?
- How often the set of time series changes?

Usage:

```
./tsdb analyze /path/to/some/prometheus/datadir | less
```

Output:

```
# Overview
Block path: /some/datadir/01D2D1ZHR6N6XDFRBDXJ5SSHKB
Duration: 2h0m0s
Series: 15680
Label names: 52
Postings (unique label pairs): 2110
Postings entries (total label pairs): 71352

# Churn in label pairs
Label pairs most involved in churning:
17 job=node
11 __name__=node_systemd_unit_state
6 instance=foo:9100
4 instance=bar:9100
3 instance=baz:9100

# Cardinality for label pairs
Most common label pairs:
12503 job=node
8060 __name__=node_systemd_unit_state
4613 instance=foo:9100
3035 instance=bar:9100
2455 instance=baz:9100

Highest cardinality labels:
1037 name
589 __name__
53 ifDescr
53 le
50 ifName
```
