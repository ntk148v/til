# ClickHouse Cloud & Observability Evolution

Source:

- <https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year>
- <https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog>
- <https://clickhouse.com/blog/scaling-observability-beyond-100pb-wide-events-replacing-otel>

## 1. Building ClickHouse Cloud From Scratch

The first post outlines the architectural shift from traditional on-premise deployments to a serverless, cloud-native model.

### Architectural Decisions

- **Separation of Storage and Compute:** The team moved away from the "shared-nothing" model. By using **Amazon S3/GCS** as the primary storage layer and **local NVMe for caching**, they solved the "rebalancing" problem. In a shared-nothing setup, adding nodes requires physical data movement; here, a new node simply points to the same object store.
- **Cellular Infrastructure:** To avoid "blast radius" issues and cloud provider limits (like AWS API throttling or regional instance shortages), ClickHouse Cloud is organized into **Cells**. Each cell is a self-contained unit of infrastructure, preventing a single failure from impacting the entire global fleet.
- **Control vs. Data Plane:**
- **Control Plane (AWS):** Manages user accounts, billing, and global orchestration. It communicates with the Data Plane via a technology-agnostic REST API.
- **Data Plane (Multi-cloud):** Deployed on Kubernetes (EKS/GKE). It uses a custom **ClickHouse Operator** to automate cluster lifecycles, scaling, and backups.

### Scaling and Idling

- **Custom Idling:** To keep costs low for serverless users, they built a custom "Idler" and "Scaler."
- **Activator Pattern:** When a query hits a paused service, an **Envoy-based proxy** intercepts the request, triggers the "activator" to spin up the compute pods, and then forwards the query once the pods are ready.

---

## 2. The 19 PiB Logging Platform (LogHouse 1.0)

This post explains the technical implementation of replacing Datadog to save millions in observability costs.

### Economic Drivers

- **The Cost Gap:** Datadog's list price for 10 trillion rows/month with 30-day retention was projected at **$26M/month**.
- **Retention Improvement:** Moving to ClickHouse allowed the team to increase log retention from **7 days to 6 months** while still reducing costs by over 99%.

### Technical Implementation

- **Schema Optimization:** They used the `MergeTree` engine family. To handle high-cardinality metadata, they utilized the **`Map(String, String)`** type, which allows for flexible log attributes without pre-defining every possible column.
- **Ingestion Pipeline (Early Stage):**
- **OTel Agents:** Deployed as DaemonSets on every Kubernetes node.
- **OTel Gateways:** A centralized bank of collectors that performed heavy processing (tagging, routing to specific tables) before sending data to ClickHouse in the **Native protocol** for maximum speed.

- **No Kafka:** Unlike ELK stacks, they skipped Kafka. ClickHouse is fast enough at ingesting (millions of rows/sec) that a buffer was deemed an unnecessary moving part. Instead, they relied on OTel’s internal memory buffering for short bursts.

---

## 3. Scaling to 100 PB and Replacing OTel (LogHouse 2.0)

The final post covers the massive scaling challenges encountered as the data grew 5x in one year.

### The Death of OTel at Extreme Scale

- **The Problem:** At 20 million rows per second, the OpenTelemetry pipeline would have required **8,000 CPU cores** just for parsing and marshalling JSON. The "text logs via stdout" approach was too expensive and lost data during spikes.
- **Loss of Fidelity:** Standard output logs only capture what the application prints. ClickHouse’s "Gold" is in its **System Tables** (query logs, trace logs, metric logs), which OTel struggled to scrape efficiently.

### The SysEx Innovation

- **System Tables Exporter (SysEx):** A custom Go-based tool that performs a **byte-for-byte copy** of data from a source ClickHouse system table to the central LogHouse cluster.
- **Zero-Marshalling:** By contributing to the Go-ClickHouse client, they enabled SysEx to stream data in the **ClickHouse Native Format** without ever decoding it into Go objects. This reduced CPU usage by **90%** compared to OTel.
- **Dynamic Schema Generation:** SysEx automatically detects when a source ClickHouse version adds new columns to a system table and updates the LogHouse schema to match, ensuring no telemetry is lost during upgrades.

### Transition to Observability 2.0

- **Wide Events over Metrics:** Instead of pre-aggregating data into Prometheus metrics (which causes "cardinality explosion"), they now log **Wide Events**. Every single event is stored as a rich row with 100+ dimensions.
- **HyperDX & ClickStack:** Following the acquisition of HyperDX, they transitioned to a unified UI. This replaces the "three pillars" (logs, metrics, traces) with a single searchable warehouse where all telemetry is correlated by default using a Lucene-like syntax.
- **Scale Stats:** \* **Uncompressed Data:** 100+ Petabytes.
- **Total Rows:** ~500 Trillion.
- **Compression:** Managed to keep the actual disk footprint manageable through ClickHouse's column-oriented compression.
