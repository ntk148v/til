# Prometheus Metrics

> A quick note when read [Sysdig blog post](https://sysdig.com/blog/prometheus-metrics/)

## Prometheus metrics format: tagged metrics

Prometheus metric format takes a flat approach to naming metrics. Instead of a hierachial, dot separated name, you have a name combined with a series of labels or tags:

```
<metric name>{<label name>=<label_value>,...}
```

Highly dimensional data basically means that you can associate any number of application specific labels to every metric you submit. These labels are the key-value pairs that will be used for grouping/graphing/segmentation/computation of composite views.

# Types of Prometheus metrics

The Prometheus client libraries offer four core metric types.
* Counter: A cumulative metric that represents a single numerical value that only ever goes up. There is a counter example in code above.
* Gauge: A gauge is a metric that represents a single numerical value that can arbitrarily go up and down.
* Histogram: A histogram samples observations (usually things like request durations or response sizes) and counts them in configurable buckets. It aslo provides a sum of all observed values.
* Summary: Similar to a histogram, a summary samples observations (usually things like request durations and response sizes). While it aslo provides a total count of observations and a sum of all observed values, it calculates configurable quantiles over a sliding time window.

There are currently only differentiated in the client libraries (to enable APIs tailored to the usage of the specific types) and in the wire protocol. The Prometheus server does not yet make use of the type information and flattens all data into untyped time series.

## When do you need to do code instrumentation?

Gaining insights of your applications sounds like a fantastic idea, and it is! But like all things in life, it has a few trade-offs to consider:
* Instrumenting with APM is simple code, but it is code nonetheless. This means that it need to be done at development time. This adds more complexity, and potentially brings software bugs. Legacy or external applications are typeically very hard to instrument.
* Performance overhead - no monitoring is free. If you plan to monitor critical, highly optimized loop code you may end up using more time emitting metrics than doing the actual work. More metrics in your monitoring backend will also require more computing resources there.

## How to add custom metrics to your application

First, if you haven't done it already, install Python Prometheus client:

```sh
sudo pip install prometheus_client
```

Execute [simple python script](./prometheus_custom_metric.py).
