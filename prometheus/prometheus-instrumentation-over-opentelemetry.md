# Prometheus instrumentation vs. OpenTelemetry

Source: <https://promlabs.com/blog/2025/07/17/why-i-recommend-native-prometheus-instrumentation-over-opentelemetry/>

## 1. OpenTelemetry vs. Prometheus scopes

![](https://promlabs.com/images/otel-vs-prometheus-scope.svg)

- OpenTelemetry handles all three signal types (logs, metrics, and traces), but only cares about the generation (instrumentation) and transfer of the generated signals to some third-party backend system. The transfer usually happens via the OpenTelemetry Protocol (OLTP).
- Prometheus only handles metrics (no logs or traces to be seen here), but it doesn't stop at generating them. Prometheus is a full monitoring system, so it also provides solutions for actively collecting and storing the data and making it queryable for dashboarding, alerting, and other use cases. The querying happens via the PromQL.

## 2. The basics of feeding OpenTelemetry metrics into Prometheus

![](https://promlabs.com/images/otel-prometheus-exporters.svg)

From the Collector, the metrics can make it into Prometheus in a few different ways:
- The Prometheus exporter.
- The Prometheus remote write exporter.
- Most common: The OTLP exporter uses OpenTelemetry's OTLP to push metrics to Prometheus.

## 3. Reasons against using OpenTelemetry with Prometheus

### 3.1. Reason 1: you throw away Prometheus's target health monitoring

- Prometheus's native monitoring model solves this challenge by combining two crucial concepts:
  - Service discovery.
  - Pull-based metrics collection with built-in health checks.

![](https://promlabs.com/images/prometheus-active-health-monitoring.svg)

- In contrast, OTLP is a push-based protocol and lacks any integration with Prometheus's service discovery capabilities.

### 3.2. Reason 2: You get echanged metric names and/or ugly PromQL selectors

- Character set differences: until Prometheus 3.0, Prometheus only allowed alphanumeric characters and underscores in label names, while also allowing colons in metric names. In contrast, OpenTelemetry allows dots, dashes, and other operator-like characters in metric and attribute (label) names - this makes me question whether using OTel metrics in a query language was ever a major design consideration. In practice, prior to Prometheus 3.0, this meant that the metric and attribute names coming from OpenTelemetry had to be translated to Prometheus-compatible names by replacing unsupported characters with underscores
- Unit and type suffixes: Prometheus's metric naming conventions require metric names to end with a suffix indicating the metric's unit, as well as a `_total` suffix for counter metrics. In contrast, OpenTelemetry's naming convention only treat the unit and type of a metric as separate metadata fields that are not supposed to be included in the metric name.
- UTF-8 support in Prometheus 3.0.

### 3.3. Reason 3: Resource labels vs. target labels - same name but different?

Both Prometheus and OpenTelemetry like to attach a set of labels (or attributes, in OTel terminology) that give you information about the source of a metric, such as the application or service that generated it. In OpenTelemetry, these are called resource attributes, while Prometheus calls them target labels.
- Prometheus target labels are attached to scraped metrics by the Prometheus server based on the target's metadata, which usually originates from a dynamic service discovery mechanism
- OpenTelemetry resource attributes are chosen by the application that generates the metrics and are usually way more numerous and detailed.

### 3.4. Reason 4: More Prometheus settings required for ingestion

This is admitted not a big downside.

### 3.5. Reason 5: OTel SDKs are complex and can be very slow

OTel is a large and complex system that tries to do a lot of things, including logs and traces and complex features around views and aggregations for metrics inside of its instrumentation libraries.
