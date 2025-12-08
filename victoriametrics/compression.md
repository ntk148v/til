# Victoriametrics compression

Source: <https://faun.pub/victoriametrics-achieving-better-compression-for-time-series-data-than-gorilla-317bc1f95932?gi=08873e29bbc9>

Gorilla compression became standard in TSDB world — Prometheus uses Gorilla, InfluxDB uses Gorilla, M3 is inspired by Gorilla.

Gorilla compression from Facebook may be improved using simple techniques described above:

- Converting floating-point values to integer values by applying 10^X multiplier.
- Converting Counters to Gauges by applying delta-encoding.
- Applying general-purpose compression algorithms (zstd) on top of the encoded data.

These techniques give better compression ratio for VictoriaMetrics comparing to competitors — it compresses typical node_exporter time series data to 0.4 bytes per data point. This is 10x times better than 4 bytes per data point for the same data in Prometheus, which uses the original Gorilla compression algorithm.
