# Resolve unassigned shards in Elastisearch

Source: <https://www.datadoghq.com/blog/elasticsearch-unassigned-shards/>

- [Resolve unassigned shards in Elastisearch](#resolve-unassigned-shards-in-elastisearch)

  - [1. Reason 1: Shard allocation is purposefully delayed](#1-reason-1-shard-allocation-is-purposefully-delayed)
  - [2. Reason 2: Too many shards, not enough nodes](#2-reason-2-too-many-shards-not-enough-nodes)
  - [3. Reason 3: You need to re-enable shard allocation](#3-reason-3-you-need-to-re-enable-shard-allocation)
  - [4. Reason 4: Shard data no longer exists in the cluster](#4-reason-4-shard-data-no-longer-exists-in-the-cluster)
  - [5. Reason 5: Low disk latency](#5-reason-5-low-disk-latency)

- In Elasticsearch, a healthy cluster is a balanced cluster: primary and replica shards are distributed across all nodes for durable reliability in case of node failure.
- But what should you do when you see shards lingering in an `UNASSIGNED` state?
- Pinpointing problematic shards:

  - Elasticsearch's cat shards API/cluster allocation explain API will tell you which shards are unassigned, and why:

  ```bash
  curl -XGET localhost:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason| grep UNASSIGNED
  # For Elasticsearch 5+
  curl -XGET localhost:9200/_cluster/allocation/explain?pretty
  ```

## 1. Reason 1: Shard allocation is purposefully delayed

- When a node leaves the cluster, the master node temporarily delays shard reallocation to avoid needlessly wasting resources on rebalancing shards, in the event the original node is able to recover within a certain period of time.

```
[TIMESTAMP][INFO][cluster.routing] [PRIMARY NODE NAME] delaying allocation for [54] unassigned shards, next check in [1m]
```

- Modify the delay period like so:

```bash
curl -XPUT "localhost:9200/<INDEX_NAME>/_settings?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index.unassigned.node_left.delayed_timeout": "5m"
  }
}'
```

## 2. Reason 2: Too many shards, not enough nodes

- As nodes join and leave the cluster, the primary node reassigns shards automatically, ensuring that multiple copies of a shard aren’t assigned to the same node.
- A unassigned shard -> there are not enough nodes to distribute the shards accordingly.
- Make sure that every index is inited with fewer replicas/primary shard than the number of nodes `N >= R + 1`.
- Solutions: Add more data nodes or Reduce the replication factor:

```bash
curl -XPUT "localhost:9200/<INDEX_NAME>/_settings?pretty" -H 'Content-Type: application/json' -d' { "number_of_replicas": 2 }'
```

## 3. Reason 3: You need to re-enable shard allocation

- Disable and forget to re-enable it.
- Solution: Enable it!

```bash
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
    "transient" : {
        "cluster.routing.allocation.enable" : "all"
    }
}
'
```

## 4. Reason 4: Shard data no longer exists in the cluster

- The node left the cluster before the data could be replicated.
- The node may have encountered an issue while rebooting. Nomarlly, when a node resumes its connection to the cluster, it relays inforamtion about its on-disk shards to the primary node, which then transitions those shards from "unassigned" to "assigned/started". When this process fails for some reason (node's storage has been damaged in some way), the shards may remain unassigned.
- Solutions:

  - Try to recover and rejoin the cluster (and do not force allocate the primary shard)
  - Force allocate the shard using the Cluster Reroute API, and reindex the missing data using the original data source, or from a backup

  ```bash
  # Must specify "accept_data_loss: true"
  curl -XPOST "localhost:9200/_cluster/reroute?pretty" -H 'Content-Type: application/json' -d'
  {
      "commands" : [
          {
            "allocate_empty_primary" : {
                  "index" : "constant-updates",
                  "shard" : 0,
                  "node" : "<NODE_NAME>",
                  "accept_data_loss" : "true"
            }
          }
      ]
  }
  '
  ```

## 5. Reason 5: Low disk latency

- The primary node may not be able to assign shards if there are not engouh nodes with sufficient disk space (>==85% disk in use).
- Check disk space:

```bash
curl -s 'localhost:9200/_cat/allocation?v'
```

- Solutions: If your nodes have large disk capacities, the default low watermark may be too low -> Increase the low disk watermark

```bash
curl -XPUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "90%"
  }
}'
```

## 6. Reason 6: Multiple Elasticsearch versions

- This problem only arises in clusters running more than one version of Elasticsearch.
- Check version!
