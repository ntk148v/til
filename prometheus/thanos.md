# Thanos

Source: https://banzaicloud.com/blog/multi-cluster-monitoring/

- [Thanos](#thanos)
  - [1. Components](#1-components)
  - [2. How downsampling works?](#2-how-downsampling-works)
  - [3. Life of a query](#3-life-of-a-query)
  - [4. How deduplication works?](#4-how-deduplication-works)

## 1. Components

Thanos is built from a handful of components, each with a dedicated role within the architecture. The easiest way to gain a basic understanding of how these work is to take a quick look at the responsibilities assigned to each one.

- Sidecar
  - Serves as a sidecar container alongside Prometheus
  - Uploads Prometheus chunks to an object storage
  - Supports object stores like S3, Google Cloud Storage, Azure Storage and more
  - Prometheus operator, which we also use in our integrated monitoring service, solves the injection of this sidecar transparently
- Store
  - Retrieves chunks from object storage in order to provide long term metrics for Query
  - Supports time-based partitioning
  - Supports label-based partitioning
- Compact
  - Creates downsampled summaries of chunks to expedite queries for long time ranges
  - Has three levels; Raw chunks contain all samples, while 5m and 1h chunks contain aggregated samples for every five minutes or one hour respectively
- Query
  - Is the entry point for PromQL queries
  - Deduplicates results from different sources
  - Supports partial responses
- Rule
  - Is a simplified version of Prometheus that does not require a sidecar and does not scrape or do PromQL evaluations
  - Writes results back to the disk in the Prometheus 2.0 storage format
  - Participates in the system as a store node, which means that it exposes StoreAPI and uploads its generated TSDB blocks to an object store
- Bucket
  - Inspects data in object storage buckets

## 2. How downsampling works?

- Goal of downsampling: ~~save disk space~~. It provides a way to quicky evaluate queries with large time intervals, like months or years.
  - Downsampling doesn't save you any space but, instead, adds two new blocks for each raw block. These are slightly smaller than, or close to the size of raw blocks. This means that downsampling slightly increases the amount of storage space used, but it provides a massive performance and bandwidth use advantage when querying long intervals.
- 3 levels of granularity:
  - raw - raw scraped metrics from Prometheus.
  - 5m - for chunks compacted into 5 minutes.
  - 1h - for chunks compacted into 1 hour.
- A compacted chunk consists of 5 fields.

![](https://banzaicloud.com/img/blog/multi-cluster-monitoring/downsampling.png)

## 3. Life of a query

- PromQL query is posted to the `Querier`.
- It interprets the query and goes to a pre-filter.
- The query fans out its request for `stores`, `prometheuses` or other `queries` on the basis of labels and time-range requirements.
- The `Query` only sends and receives StoreAPI messages.
- After it has collected all the responses, it merges and deduplicates them.
- It then sends back the series for the user.

![](https://banzaicloud.com/img/blog/multi-cluster-monitoring/life_of_a_query.png)

## 4. How deduplication works?
