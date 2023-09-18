# Grab logging stack

Source: <https://engineering.grab.com/how-built-logging-stack>

## 1. Problems & Issues

- Grab needs logging - that's it, for many reasons.
- Size and growth rate ruled out several available logging systems: 25TB of logging/day.

## 2. Built a Multi-petabyte cluster

### 2.1. Information gathering

- How much data/day? How many days were retained? What's a reasonable response time to wait for?

### 2.2. Getting feet wet

- Elasticsearch - data store -> horizontal scaling -> only increase the number of Elasticsearch nodes.

### 2.3. Initial design

- Each node in cluster performs all responsibilities:
  - Ingest: used for transforming and enriching documents before sending them to data nodes for indexing.
  - Coordinator: proxy node for directing search and indexing requests.
  - Master: used to control cluster operations and determine a quorum on indexed documents.
  - Data: nodes that hold the indexed data.
- Not going well.
- Separating nodes can be a huge help in tracing down problems.

### 2.4. Monitoring

- You need a robust metric sytem.

## 3. Pitfalls

### 3.1. Common problems

- Common problems encountered when creating an Elasticsearch cluster.
- Check out Elastic's blog.

### 3.2. Grab's problem

- Field data cache:

  - Field data cache went from virtually zero memory used in the heap to 20GB -> this breaks down to allowing 70% of your total heap being allocated to a single search in the form of field data.
  - It's very helpful to keep the field names and values in memory for quick lookup. But, if you have several trillion documents, you might want to watch out.
  - Can't disable indexing that field.

- Translog compression:

  - Compression seems an obvious choice for shipping shards between nodes.
  - Lucense segments are already compressed -> disable compression, shipping time for a 50GB shard went from 1h to 20m.

- Segment memory:

  - Heap memory is exhausted.
  - Allocated too many shards to nodes: looking up the total segment memory used per index should give a good idea of how many shards you can put on a node before you start running out of heap space.

- Index mapping and field types:

  - Indexed fields in completely unnecessary ways: fields no one would ever search against and which could be dropped from index memory.

- Picking the wrong analyzer:
  - By default, Elasticsearch's Standard Analyzer.
