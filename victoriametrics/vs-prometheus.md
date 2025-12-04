Below are **8 focused, high-quality references** (official docs, deep dives, and case studies) that back the key points I used earlier: VictoriaMetrics’ column-oriented parts (timestamps/values), global inverted index (TSID/MetricID), efficient merges/deduplication, and comparative case studies showing resource savings versus Prometheus. I list each reference with a one-sentence summary of which claim it supports so you can jump straight to the most relevant material.

---

# Primary (official) documentation & engineering blogs

1. **VictoriaMetrics — official docs (home)** — central documentation for VM (architecture, components, deployment). Supports general architectural claims and links to component docs. ([docs.victoriametrics.com][1])
   _Use for:_ overview, links to specific storage pages and articles.

2. **VictoriaMetrics — Single-node & Cluster pages** — descriptions of single-node and cluster architectures (how vmstorage/vminsert/vmselect are organized). Supports claims about components and scalability modes. ([docs.victoriametrics.com][2])
   _Use for:_ cluster vs single-node behavior, deployment topology.

3. **vmstorage internals (blog): “How vmstorage Processes Data: Retention, Merging, Deduplication…”** — engineering post describing how parts are written, merging/retention logic and deduplication. Supports merge/compaction, deduplication, and part-level layout discussion. ([VictoriaMetrics][3])
   _Use for:_ stream merges, retention, deduplication behavior.

4. **vmstorage index internals: “How IndexDB works” (VictoriaMetrics blog)** — explains MetricID↔TSID mappings, per-tag mappings and how the global indexes are organized. Supports the global inverted index / TSID explanation. ([VictoriaMetrics][4])
   _Use for:_ details on global index and posting lists.

5. **VictoriaMetrics articles & performance tips (docs/blogs)** — collection of articles including string interning, performance techniques and part layout (timestamps/values per part). Supports columnar/time/value separation and memory optimizations. ([docs.victoriametrics.com][5])
   _Use for:_ concrete optimizations (string interning, selective loading).

---

# Comparative / independent analyses and case studies

6. **Prometheus — Storage (official docs)** — Prometheus TSDB block model, 2-hour blocks, per-block index; supports the discussion of Prometheus’ per-block index and compaction behavior. ([prometheus.io][6])
   _Use for:_ Prometheus block format and compaction constraints.

7. **PingCAP (TiDB) case study: “Migrating Prometheus → VictoriaMetrics”** — real-world migration and resource-usage comparison (why they switched, TCO, instance sizes). Supports claims about observed resource savings in production migration. ([TiDB][7])
   _Use for:_ concrete production-scale comparison and why teams migrate.

8. **Independent write-ups / explainers (blogs, medium, community posts)** — several third-party analyses summarizing VM internals, columnar parts, and comparative experiences (e.g., Medium posts, dbdb.io, Groundcover explainer). These provide independent corroboration and useful diagrams/interpretations. ([Medium][8])
   _Use for:_ alternative explanations, diagrams, and community benchmarks.

---

# Quick mapping: which references support which major claims

- **VM stores timestamps & values in separate per-part files (column-like layout):** vmstorage blog + articles. ([VictoriaMetrics][3])
- **VM uses a global index (MetricID→TSID, tag→metricIDs):** IndexDB post. ([VictoriaMetrics][4])
- **VM merges/compacts via streaming/parts (lower write amplification):** vmstorage internals. ([VictoriaMetrics][3])
- **Prometheus uses 2-hour blocks with per-block indexes (leads to duplicated index data):** Prometheus storage docs. ([prometheus.io][6])
- **Real-world resource improvements after migrating from Prometheus to VM:** PingCAP TiDB migration case study. ([TiDB][7])

---

# If you want next steps

I can do any of the following (pick one and I’ll proceed):

- Compile a **downloadable pack** (PDF or Markdown) with excerpts and relevant snippets from the sources above (with full links and short quotes).
- Extract and compare **specific on-disk file formats** (exact file names, byte layout) from VM docs vs Prometheus TSDB format.
- Produce a **brief annotated benchmark** plan you can run (prometheus + remote_write → VM) with metrics to capture (disk, RAM, CPU, query latency) and expected outcomes.

Which of those would you like me to prepare now?

[1]: https://docs.victoriametrics.com/?utm_source=chatgpt.com "Welcome to VictoriaMetrics Docs"
[2]: https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/?utm_source=chatgpt.com "VictoriaMetrics: Single-node version"
[3]: https://victoriametrics.com/blog/vmstorage-retention-merging-deduplication/?utm_source=chatgpt.com "How vmstorage Processes Data: Retention, Merging, ..."
[4]: https://victoriametrics.com/blog/vmstorage-how-indexdb-works/?utm_source=chatgpt.com "How vmstorage's IndexDB Works"
[5]: https://docs.victoriametrics.com/victoriametrics/articles/?utm_source=chatgpt.com "VictoriaMetrics: Articles"
[6]: https://prometheus.io/docs/prometheus/latest/storage/?utm_source=chatgpt.com "Storage"
[7]: https://www.pingcap.com/blog/tidb-observability-migrating-prometheus-victoriametrics/?utm_source=chatgpt.com "Moving from Prometheus to VictoriaMetrics"
[8]: https://alexmarket.medium.com/victoriametrics-a-look-inside-its-innards-b00eaa2a1e32?utm_source=chatgpt.com "VictoriaMetrics: a look inside its innards. | by Alex - Medium"
