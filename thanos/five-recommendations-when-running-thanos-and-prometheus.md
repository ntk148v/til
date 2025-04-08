# 5 recommendations when running Thanos and Prometheus

The key recommendations include:

1. **Implement Caching**: Utilize Thanos Query Frontend with caching mechanisms like Memcached to enhance query performance by reducing response times.

2. **Downsample Metrics**: Use Thanos Compact to downsample and compact data, retaining high-resolution data for a limited period and lower-resolution data for longer durations, thereby optimizing storage and query efficiency.

3. **Manage Metrics Quality**: Limit the collection of high-cardinality metrics and disable unnecessary collectors in Node Exporter to maintain performance and avoid resource overuse.

4. **Shard Long-Term Storage**: Distribute large metric datasets across multiple Thanos Store instances by sharding S3 storage, which improves query performance and scalability.

5. **Ensure Scalability and High Availability**: Adopt manual or semi-automatic scaling strategies for Prometheus, such as running independent Prometheus shards for different service groups, to achieve high availability and scalability.

These practices have enabled Zapier to efficiently manage and scale their monitoring infrastructure, handling up to 130 TB of metrics data.
