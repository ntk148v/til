# Internal architecture

[Source](https://github.com/prometheus/prometheus/blob/master/documentation/internal_architecture.md)

## The overall Prometheus server architecture

![overall-prometheus-architecture](https://github.com/prometheus/prometheus/raw/master/documentation/images/internal_architecture.svg?sanitize=true)

> NOTE:
>
> - Code links and explanations are based on Prometheus v2.3.1
> - Arrows indicate request or connection initiation direction, not necessary dataflow direction.

## Main function

- Initializes and run alls other Prometheus server components + connect interdependent components to each other.
- 1st: `main()` defines and parses the
