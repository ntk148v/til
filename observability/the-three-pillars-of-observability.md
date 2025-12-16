# The Three Pillars of Observability

Observability refers to the ability to understand a system’s internal state based on the telemetry data it produces. Modern distributed and cloud-native systems are highly complex, making it difficult to diagnose issues without comprehensive visibility. To achieve such visibility, observability platforms rely primarily on three types of telemetry data—**metrics**, **logs**, and **traces**—often referred to as the _three pillars of observability_.

## Overview

In observability:

- **Metrics** provide quantitative views of system performance over time.
- **Logs** are detailed, timestamped records of discrete events.
- **Traces** map the progression of individual requests across system components.

Each pillar addresses different questions about system behavior and, when used together, they enable teams to identify, investigate, and resolve issues efficiently.

## Definitions and Key Characteristics

### Event Logs

Logs are immutable records of specific events that occur within a system. They typically include a timestamp and contextual data such as transaction IDs, IP addresses, error details, and configuration changes. Logs exist in different formats:

- **Plaintext:** simple text messages.
- **Structured:** typically JSON with explicit fields.
- **Binary:** such as Protobuf or system journal formats.

**Strengths**

- Provide rich local context and detailed insight into what happened.
- Easy to generate and capture in most systems.

**Limitations**

- Excessive logging can affect performance and create noise.
- Log aggregation and querying at scale can be resource-intensive.

### Metrics

Metrics are numerical representations of system performance measured over intervals of time. They enable trend analysis and performance monitoring. Common examples include CPU usage, memory utilization, latency, throughput, and error rates.

**Strengths**

- Efficient to store, process, and query, especially in time-series databases.
- Useful for alerting based on thresholds and for capacity planning.

**Limitations**

- Metrics lack detailed context about individual events or causal chains.
- High-resolution metrics can still produce large volumes of data.

### Traces

Traces represent the path and lifecycle of a request as it travels across components in a distributed system. They record causally related events and capture timing, dependencies, and the order of operations. Distributed tracing is especially important in microservices environments.

**Strengths**

- Illustrate where and how a request flows through the architecture.
- Help pinpoint performance bottlenecks and dependencies.

**Limitations**

- Requires instrumentation across all services involved in the request path.
- Can be complex to implement and manage at scale.

## Comparative Overview

| Pillar  | Primary Focus             | Typical Use Cases                           |
| ------- | ------------------------- | ------------------------------------------- |
| Metrics | “What” is happening       | High-level performance dashboards, alerting |
| Logs    | “Why” it happened         | Error diagnostics, root cause analysis      |
| Traces  | “Where/How” requests flow | Distributed request path analysis           |

Each pillar provides a piece of the overall picture. Metrics quickly surface anomalies, logs reveal detailed context, and traces connect events across systems for end-to-end insight.

## Advantages and Limitations (Merged Insights)

### Logs

**Advantages**

- Highly detailed and flexible.
- Can capture arbitrary event context.

**Limitations**

- Potential performance overhead during collection.
- Noise and storage costs can be significant.

### Metrics

**Advantages**

- Scalable for long-term trend analysis.
- Efficient alerting and aggregation.

**Limitations**

- Metrics alone do not reveal causality or detailed event context.

### Traces

**Advantages**

- Critical for understanding distributed systems.
- Reveals dependency interactions.

**Limitations**

- Complexity of instrumentation and data management.

## How the Three Pillars Work Together

Observability is most effective when metrics, logs, and traces are correlated and analyzed in tandem:

1. **Metrics** surface potential issues via trends and thresholds.
2. **Traces** reveal where problems occur within distributed workflows.
3. **Logs** provide the detailed context needed to diagnose root causes.

Together, these data sources give engineering teams a **holistic, context-rich, and actionable view** of system behavior.
## Beyond the Three Pillars

Although metrics, logs, and traces are the foundational telemetry signals for observability, some frameworks emphasize **additional supporting capabilities** such as:

- **Context:** environmental and topological metadata that enriches telemetry.
- **Correlation:** linking disparate signals for comprehensive analysis.
- **Alerting:** proactive notification of anomalies.
- **Profiling:** capturing detailed execution state for deep diagnostics.

These elements are often integrated with the three pillars to enhance overall observability effectiveness.

## Conclusion

The three pillars—**metrics**, **logs**, and **traces**—form the core telemetry foundation of observability in modern distributed systems. Each provides distinct insights into system behavior, and when combined, they enable fast detection, analysis, and resolution of operational issues across complex architectures.
