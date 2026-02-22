# Reduce Shard Usage

Source: <https://docs.bonsai.io/article/124-reducing-shard-usage>

- [Reduce Shard Usage](#reduce-shard-usage)
  - [1. Deleting Unneeded Indices](#1-deleting-unneeded-indices)
  - [2. Use a different sharding scheme](#2-use-a-different-sharding-scheme)
  - [Reduce replication](#reduce-replication)
  - [Data collocation](#data-collocation)

## 1. Deleting Unneeded Indices

- List all indices wih [cat indices API](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/cat-indices.html), find your unneeded indices.
- Delete them with [Delete index API](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/indices-delete-index.html).

## 2. Use a different sharding scheme

- It’s possible that for some reason one or more indices were created with far more shards than necessary.
- A check of `/_cat/indices`:

```
health status index                                            pri rep     docs.count docs.deleted store.size pri.store.size
green  open   scaling-2020.05.17        qyNXa5HBSs-F9ic5gMwl0Q 5   2       424        0            470.1kb    235kb
green  open   tomcat-2020.05.24         IS1w3pRjQ6mZLMPQLhNnIQ 5   2       1138       0            2.4mb      1.2mb
# 5 primary shards 2 replicas
```

- The number of primary shards can not be changed once an index has been created. To fix this, you will need to manually [create a new index with the desired shard scheme](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/indices-create-index.html) and [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/docs-reindex.html) the data.
- Quickly apply to new indices with [template](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/indices-templates.html).
- Shrink API: <https://blog.ruanbekker.com/blog/2019/04/06/shrink-your-elasticsearch-index-by-reducing-the-shard-count-with-the-shards-api/>

## Reduce replication

- For most use-cases, _a single replica is perfectly sufficient for redundancy and load capacity_.
- Reducing the replica count for the index is allowed, check the [Update settings API](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/indices-update-settings.html),
- `Replication = Avalability + redundancy`, you **can** set all replicas to 0 so as to fit as many indices into your cluster as possible. This means that your primary data has no live backup. If a node in your cluster goes offline, data loss is basically guaranteed. So always keep replicas >= 1.

## Data collocation

- Reducing usage using alias and custom routing rules to collocate different data models onto the same group of shards.
- Data collocation: Many Elasticsearch clients use an index per model paradigm as the default for data organization.

![](https://d33v4339jhl8k0.cloudfront.net/docs/assets/5bd08cb42c7d3a01757a5894/images/5c6c67402c7d3a66e32ea836/file-LLMPZ7B6hQ.jpg)

- :disappointed_relieved: Not sure how to use it, check it later :confused:.
