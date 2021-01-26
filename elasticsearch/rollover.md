# Rollover

- [Rollover](#rollover)
  - [1. What is rollover?](#1-what-is-rollover)
  - [2. Concepts](#2-concepts)
  - [2. How to?](#2-how-to)

## 1. What is rollover?

- Creates a new index for a rollover target when the existing index reaches a certain size, number of docs, or age. A rollover target can be either _an index alias_ or _a data stream_.
- Using rolling indices enables you to:
  - Optimize the active index for high ingest rates on high-performance hot nodes.
  - Optimize for search performance on warm nodes.
  - Shift older, less frequently accessed data to less expensive cold nodes.
  - Delete data according to your retention policies by removing entire indices.

## 2. Concepts

- [Data streams](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-data-stream.html).

  - Data streams are designed for append-only data.
  - A data stream consists of one or more hidden, auto-generated backing indices. Each data stream tracks its generation:

  ```
  .ds-<data-stream>-<generation>
  ```

  ![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/data-streams/data-streams-diagram.svg)

- [Index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html): specifies the settings for each new index in the series. You optimize this configuration for ingestion, typically using as many shards as you have hot nodes.
- [Index aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html): references the entire set of indices.
- [ILM](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html): policies to automatically manage indices according to your performance, resiliency and retention requirements.

## 2. How to?

- Datastreams (append-only data). Requires an index template that contains:
  - A name or wildcard pattern.
  - Timestamp field.
  - Mappings and settings applied to each backing.
- Indices aliases (frequently update or delete existing data).
