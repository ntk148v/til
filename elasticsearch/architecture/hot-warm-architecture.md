# Elasticsearch Hot-Warm architecture

Source: <https://www.elastic.co/blog/sizing-hot-warm-architectures-for-logging-and-metrics-in-the-elasticsearch-service-on-elastic-cloud>

- [Elasticsearch Hot-Warm architecture](#elasticsearch-hot-warm-architecture)
  - [1. The basic architecture](#1-the-basic-architecture)
  - [2. Hot-warm architecture](#2-hot-warm-architecture)
  - [3. Which architecture should I pick?](#3-which-architecture-should-i-pick)
  - [4. How much storage do I need?](#4-how-much-storage-do-i-need)
  - [5. How do I balance ingest and querying?](#5-how-do-i-balance-ingest-and-querying)
  - [6. How do I use all this storage?](#6-how-do-i-use-all-this-storage)

## 1. The basic architecture

![](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt5365b41d3c2bc21c/5c57e2988d25f6030ca0437d/uniform_cluster.png)

- All data nodes have the same specification and handle all roles. -> a homogenous/uniform clsuter architecture.
- All data nodes share the indexing and query load evently.

## 2. Hot-warm architecture

![](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte59c4541ff94d917/5c57e292a2b68bd90b9fee90/hot-warm_cluster.png)

- The architecture has 2 different types of data nodes with different hardware profiles: `hot` and `warm` data nodes.
- Hot data nodes hold all the most recent indices and therefore handle all indexing load in the cluster. -> CPU and I/O intensive, SSDs.
- Warm data nodes handle long-term storage of read-only indices in the cluster in a cost efficient way. -> good amount CPU and RAM, spinning disk/SAN.
- Once indices on the host nodes exceed the retention period for those nodes and are no longer indexed into, they get relocated to the warm nodes.

## 3. Which architecture should I pick?

- The type(s) of storage available to the cluster.
- Retention period.

## 4. How much storage do I need?

- The ratio between the volume of raw data and how much space this will take up on disk once indexed and replicated in Elasticsearch will depend a lot on the type of data and how this is indexed.

![](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt2797824a3f597c02/5c57e28c713ebdec0ba06f99/data_index_lifecycle.png)

## 5. How do I balance ingest and querying?

- The maximum indexing throughput of the cluster.
- How much space the data will take up on disk.

## 6. How do I use all this storage?

In hot-warm architectures, the warm nodes are expected to be able to hold large amounts of data. This also applies to data nodes in a uniform architecture with a long retention period.

- Make sure mappings are optimized.
- Keep shards as large as possible: A good rule of thumb is to keep the average shard size for long-term retention at 20-30GB.
- Tune for storage volume.
- Avoid unnecessary load.
