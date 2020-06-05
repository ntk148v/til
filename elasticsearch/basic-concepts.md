# Basic Concepts

Source:

- https://docs.bonsai.io
- https://www.elastic.co/guide/index.html

- [Basic Concepts](#basic-concepts)
  - [1. Shared nothing architecture](#1-shared-nothing-architecture)
  - [2. Near Realtime](#2-near-realtime)
  - [3. Cluster](#3-cluster)
  - [4. Node](#4-node)
  - [5. Index](#5-index)
  - [6. Document](#6-document)
  - [7. Mapping](#7-mapping)
  - [8. Sharding](#8-sharding)

## 1. Shared nothing architecture

The basic principle of Elasticsearch is the “shared nothing” architecture:

```
“A shared nothing architecture (SN) is a distributed computing architecture in which each node is independent and self-sufficient, and there is no single point of contention across the system. More specifically, none of the nodes share memory or disk storage.” Definition by Wikipedia
```

## 2. Near Realtime

Elasticsearch is a near real time search platform -> slight latency (~1 second) from the time you index a document until the time it becomes searchable.

## 3. Cluster

- A cluster is a collection of one or more nodes (servers) that together holds your entire data and pprovides federated indexing and search capabilities across all nodes.
- A cluster is identified by a **unique** name which by default is "elasticsearch".

## 4. Node

- A node is a single server that is part of your cluster, stores your data, and participates in the cluster's indexing and search capabilities.
- A node is identified by a name which by default is a random Universally Unique IDentifier (UUID) that is assigned to the node at the startup.
- Depending on the node configuration, multicast or unicast discovery is used.
- Node types:
  - Master node.
  - Data node.
  - Ingest node.

## 5. Index

- An index (noun) is a collection of documents that have somewhat similar characterisitics.
- An index is identified by a name (that must be all lowercase) and this name is sued to refer to the index when performing indexing search, update, and delete operations against the documents in it.
- The process of populating an Elasticsearch index (verb) with data. Indexing is the critical step in running a search engine. Without indexing your content, you will not be able to query it using Elasticsearch, or take advantage of any of the powerful search features Elasticsearch offers.

## 6. Document

- A document is a basic unit of information that can be indexed.
- The document is expressed in JSON.
- Within an index, you can store as many documents as you want.
- Documents are stored and indexed. The original is represented as “\_source” in the API besides the actual indexed fields of a document.

## 7. Mapping

A schema definition for the index. The schema can only be changed as long as no documents are indexed. Extending the mapping with new fields or adding sub-fields is possible at any time, but changing the type of fields is a more complex operation including re-indexing of the data.

## 8. Sharding

![](https://files.readme.io/qNFuyoeARFmlzsQfu4Ox_reduce-shards09.jpg)

- A shard is a single Lucene index instance, which is managed by Elasticsearch. Elasticsearch knows two types of shards:
  - Primary shards or active shards that hold the data.
  - Replica shards, or copies of the primary shard.
- Sharding is important for two primary reasons:
  - It allows you to horizontally split/scale your content volume.
  - It allows you to distribute and parallelize operations across shards (potentially on multiple nodes) thus increasing performance/throughput.
- To summarize, each index can be split into multiple shards. An index can also be replicated zero (meaning no replicas) or more times. Once replicated, each index will have primary shards (the original shards that were replicated from) and replica shards.
- _The number of primary shards can not be changed after an index has been created._
- _Replicas can be added and removed at any time._
- By default, each index is allocated 5 primary shards and 1 replica (2 nodes -> index - 5 primary shards and another 5 replica shards (1 complete replica) -> 10 shards/index)
- The total of shards:

```
total = primary * (1 + replicas)
```

![](https://files.readme.io/f5yajUc0QmaFq8b1gnYr_reduce-shards07.png)
