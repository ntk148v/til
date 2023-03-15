# Benthos

Source: <https://www.benthos.dev/docs/about>

## 1. Introduction

- Benthos is a declarative data streaming service that solves a wide range of data engineering problems with simple, chained, stateless processing steps. It implements transaction based resiliency with back pressure, so when connecting to at-least-once sources and sinks it's able to guarantee at-least-once delivery without needing to persist messages during transit.

![](https://www.benthos.dev/img/what-is-blob.svg)

- Benthos includes 3 components:
  - Input.
  - Processor.
  - Output.

## 2. Getting started

- Sample config:

```yaml
input:
  stdin: {}

pipeline:
  processors: []

output:
  stdout: {}
```
