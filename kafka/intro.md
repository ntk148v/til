# Kafka 101

Table of contents:

- [Kafka 101](#kafka-101)
  - [1. What is Kafka?](#1-what-is-kafka)
  - [2. Basic concepts](#2-basic-concepts)
    - [2.1. The Log, Topic, Partition, and Replica](#21-the-log-topic-partition-and-replica)
    - [2.2. Broker](#22-broker)
    - [2.3. Writes](#23-writes)
    - [2.4. Reads](#24-reads)
  - [3. Record flow](#3-record-flow)
  - [4. Performance](#4-performance)
    - [4.1. Persistence to Disk](#41-persistence-to-disk)
    - [4.2. Pagecache](#42-pagecache)
  - [5. Fault tolerance](#5-fault-tolerance)
  - [6. Consensus](#6-consensus)
  - [7. Tiered storage](#7-tiered-storage)

Source:
- <https://highscalability.com/untitled-2/>

## 1. What is Kafka?

![](https://www.cloudkarafka.com/img/blog/durable-message-system.png)

-  A distributed streaming platform serving as the internet’s de-facto standard for real-time data streaming.
-  Originally developed in LinkedIn during 2011, Apache Kafka is one of the most popular open-source Apache projects out there.
   - Its development is path-dependent on the problems LinkedIn hit at the time. As they were one of the first companies to hit large scale distributed systems problems, they noticed the common problem of uncontrolled microservice proliferation:

  ![](https://lh7-us.googleusercontent.com/Zfsoz8lj4ftWa8N7t_0Zntof1skFW7l2jE2fejY3PixDz905PVwJvAmQ98mYvdA1xiWfm9XY5Yc5B0Gh0y-d8xiDCV4mEegvyrDXVKsxfJvrkbjM4u1nqlFTfT4xRLxLW9apTsbwWdTbUOFl9OicTRI)

   - To fix the growing complexity of service-to-service and persistence store permutations, they opted to develop a single platform which can serve as the source of truth.

  ![](https://lh7-us.googleusercontent.com/rmJNLP33hKiT7VX_J66qxdDJxFkjF9lmRT19t1calefx1c5yr2LX9YHCEYQe4b-HSvOL2GbRDRwrjhENC5AhppIex_ADIgWVBmY5123OUeZadE4DLcxPNZr5wgSXhmEdNuwXB4UA5TwEJ8EWXKTqrgo)

- There are four main parts in a Kafka system:
  - Broker: Handles all requests from clients (produce, consume, and metadata) and keeps data replicated within cluster. There can be one or more brokers in cluster.
  - Zookeeper: Keeps the states of the cluster (brokers, topics, users).
  - Producer: Sends records to a broker.
  - Consumer: Consumes batches of records from the broker.

## 2. Basic concepts

### 2.1. The Log, Topic, Partition, and Replica

- The data in the system is stored in **topics**. A Topic is a category/feed name to which records are stored and published.
- The fundamental basis of a topic is the **log** - a simple ordered data structure which stores records sequentially. Kafka retains records in the log, making the consumers responsible for tracking the position in the log, known as the “offset”.

![](https://lh7-us.googleusercontent.com/4xhy73ditKkt-DCSzW1LF04kvP-64rGSTQBw9z56aZPtX5Nu8Qwwz2skZNfkhzpShSq1RsbnvglD1WLMLBVz0sTxSXTh-Pf-uc3p5V_jxnyB2jh1h7hnRBdXXF3SXzSl8zMC0RKnBr3S0HXmTdaZlac)

- The log underpins a lot of Kafka's fundamental properties, so it is prudent for us to focus on it.
- It’s immutable and has O(1) writes and reads (as long as they’re from the tail or head). Therefore the speed of accessing its data doesn’t degrade the larger the log gets and, due to its immutability, it’s efficient for concurrent reads. But despite these benefits, the key benefit of the log and perhaps the chief reason it was chosen for Kafka is because it is optimized for HDDs. HDDs are very efficient with relation to linear reads and writes, and due to log's structure - linear reads/writes are the main thing you perform on it. HDDs have become 6,000,000 times cheaper (inflation-adjusted) per byte since their inception.
- Every topic is split into **partitions**, and the partitions themselves are replicated N times (according to the replication factor) into N **replicas** for durability and availability purposes. A simple analogy is that just how the basic storage unit in an operating system is a file, the basic storage unit in Kafka is a replica (of a partition).
- Each replica is nothing more than a few files itself, each of which embody the log data structure and sequentially form a larger log. Each record in the log is denoted by a specific offset, which is simply a monotonically-increasing number.

![](https://lh7-us.googleusercontent.com/MNnq81Tq5oIxmLQO15lVpS3QakHOV9QUM3FDAXfd8KtDTrLLXhjKpTiu8fvdZdtXt1M2gfGkISv0zoT-dW6zexkBWPge-cgfKlrGBNgpDqduF84zHsLG4Do7PQ32qjdkpACaMkSe0MO39YYbZF_ZzKw)

- The replication is leader-based, which is to say that only a single broker leads a certain partition at a time.
- Every partition has a set of replicas (called the “replica set”). A replica can be in two states - in-sync or out-of-sync. As the name suggests, out-of-sync replicas are ones that don’t have the latest data for the partition.

![](https://lh7-us.googleusercontent.com/VZt5mDe2_pKfSgKJXBFkVCs9HApzHRT69raARrqfoJKfhapjMHImjinQom0H13d5ALd56lNNLHFNFHK_wQzU7SxxO_YdbyiplV6aUv7-6u5RkO0GgdBaedio8ToMZrinA3_qerdnod3mXStN5xR3qwo)

- All records with the same key will arrive at the same partition.

### 2.2. Broker

- Cluster consists of one or more **brokers**.

![](https://www.cloudkarafka.com/img/blog/kafka-broker-beginner.png)

- Zookeeper manages the brokers in the cluster (number of Zookeeper should be odd).

### 2.3. Writes

- Writes can only go to that leader, which then asynchronously replicates the data to the N-1 followers.
- Clients that write data are called **producers**. Producers can configure the durability guarantees they want to have during writes via the “acks” property which denotes how many brokers have to acknowledge a write before the response is returned to the client.
  -  `acks=0` - the producer won’t even wait for a response from the broker, it immediately considers the write successful
  -  `acks=1` - a response is sent to the producer when the leader acknowledges the record (persists it to disk).
  -  `acks=all` (the default) - a response is sent to the producer only when all of the in-sync replicas persist the record. To further control the acks=all property and ensure it doesn’t regress to an acks=1 property when there is only one in-sync replica, the `min.insync.replicas` setting exists to denote the minimum number of in-sync replicas required to acknowledge a write that’s configured with `acks=all`.
- Producer will decide target partition to place any message, depending on:
  - Partition id, if it's specified within the message
  - key % num partitions, if no partition id is mentioned
  - Round robin if neither partition id nor message key are available in message, meaning only value is available

![](https://i.stack.imgur.com/qhGRl.png)

### 2.4. Reads

- Clients that read data are called **consumers**. Similarly, they’re client applications that use the Kafka library to read data from there and do some processing on it.
- Consumers form so-called **consumer groups**, which are simply a bunch of consumers who are logically grouped and synchronized together. They synchronize each other through talking to the broker - they are not connected to one another. They persist their progress (up to what offset they’ve consumed from any given partition) in a particular partition of a special Kafka topic called `__consumer_offsets`. The broker that is the leader of the partition acts as the so-called Group Coordinator for that consumer group, and it is this Coordinator that is responsible for maintaining the consumer group membership and liveliness. The broker that is the leader of the partition acts the so-called **Group Coordinator** for that consumer group, and it is this Cooridnator that is responsible for maintaining the consumer group membership and liveliness.
- The records in any single partition are ordered within it. Consumers are guaranteed to read it in the right order. To ensure that the order is preserved, the consumer group protocol ensures that no two consumers in the same consumer group can read from the same partition.

![](https://lh7-us.googleusercontent.com/j4wr_ABfOJlQYMv_-APWyL8oRCI9OhHc5e_P9U6OCaO1fbowZDaaMpALSyBQFe9QbK08D_fNq12ezSS-BAVYWdOo42OX8ir4qD-ZffrImLlrcxQ5o3yjcggW_S4z0lme0ZJ41u9n4LqB2o7136lBBwc)

- There can be many different consumer groups reading from the same topic.
- When multiple consumers are subscribed to a topic and belong to the same consumer group, each consumer in the group will receive messages from a different subset of the partitions in the topic.
  - 1 consumer group with 4 partitions.

  ![](https://www.oreilly.com/api/v2/epubs/9781491936153/files/assets/ktdg_04in01.png)

  - 4 partitions split to 2 consumers in a group.

  ![](https://www.oreilly.com/api/v2/epubs/9781491936153/files/assets/ktdg_04in02.png)

  - 4 consumers 4 partitions.

  ![](https://www.oreilly.com/api/v2/epubs/9781491936153/files/assets/ktdg_04in03.png)

  - 5 consumers 4 partitions (1 idle).

  ![](https://www.oreilly.com/api/v2/epubs/9781491936153/files/assets/ktdg_04in04.png)

  - 2 consumer groups 1 topics.

  ![](https://www.oreilly.com/api/v2/epubs/9781491936153/files/assets/ktdg_04in05.png)

- Create a new consumer group for each application that needs all the messages from one or more topics. Add consumers to an existing consumer group to scale the reading and processing of messages from the topics, so each additional consumer in a group will only get a subset of the messages.

## 3. Record flow

![](https://www.cloudkarafka.com/img/blog/consumer-group-kafka.png)

- The producer sends a record to partition 1 in topic 1 and since the partition is empty the record ends up at offset 0.

![](https://www.cloudkarafka.com/img/blog/apache-kafka-partition.png)

- Next record is added to partition 1 will and up at offset 1, and the next record at offset 2 and so on.

![](https://www.cloudkarafka.com/img/blog/apache-kafka-partitions-2.png)

- This is what is referred to as a commit log, each record is appended to the log and there is no way to change the existing records in the log. This is also the same offset that the consumer uses to specify where to start reading.

## 4. Performance

### 4.1. Persistence to Disk

_ Kafka actually stores all of its records to disk and doesn’t keep anything explicitly in memory.
- Kafka’s protocol groups messages together. This allows network requests to group messages together and reduce network overhead.
- The server, in turn, persists chunk of messages in one go - a linear HDD write. Consumers then fetch large linear chunks at once.
  - Linear reads/writes on a disk can be fast. HDDs are commonly discussed as slow because they are when you do numerous disk seeks, since you’re bottlenecked on the physical movement of the drive’s head as it moves to the new location. With a linear read/write, this isn’t a problem as you continuously read/write data with the head’s movement.
  - Going a step further - said linear operations are heavily optimized by the OS.
    - ** Read-ahead optimizations** prefetch large block multiples before they’re requested and stores them in memory, resulting in the next read not touching the disk.
    - **Write-behind optimizations** group small logical writes into big physical writes - Kafka does not use fsync, its writes get written to disk asynchronously.

### 4.2. Pagecache

- Modern OSes cache the disk in free RAM. This is called pagecache.
- Since Kafka stores messages in a standardized binary format unmodified throughout the whole flow (producer ➡ broker ➡ consumer), it can make use of the **zero-copy optimization**.
- Zero-copy, somewhat misleadingly named, is when the OS copies data from the pagecache directly to a socket, effectively bypassing Kafka’s JVM entirely. There are still copies of the data being made - but they’re reduced. This saves you a few extra copies and user <-> kernel mode switches.

![](https://lh7-us.googleusercontent.com/hxbcAb64tRajQx8LfhDSv8H8pPO8H_gSXQkm--raNYUX8LrEgV548X8hSx005Fsj3s8-DUeeH5G4vWEesN3hWbj4JbzAbhKPh6UuQXlNlZROobfBM4SLGh1Ns1nXDeJW6h0wZGkVogGzPYJFv9myrE0)

- While it sounds cool, it’s unlikely the zero-copy plays a large role in optimizing Kafka due to two main reasons - first, CPU is rarely the bottleneck in well-optimized Kafka deployments, so the lack of in-memory copies doesn’t buy you a lot of resources.
- Secondly, encryption and SSL/TLS (a must for all production deployments) already prohibit Kafka from using zero-copy due to modifying the message throughout its path. Despite this, Kafka still performs.

## 5. Fault tolerance

- An Apache Kafka cluster always has one broker who is the active Controller of the cluster. The Controller supports all kinds of administrative actions that require a single source of truth, like creating and deleting topics, adding partitions to topics, reassigning partition replicas.

## 6. Consensus

- Any distributed system requires **consensus** - the act of picking exactly one broker to be the controller at any given time is fundamentally a distributed consensus problem.
- Zookeeper:
  - Kafka historically outsourced consensus to ZooKeeper. When starting the cluster up, every broker would race to register the `/controller` zNode and the first one to do so would be crowned the controller. Similarly, when the current Controller died - the first broker to register the zNode subsequently would be the new controller.
  - Kafka used to persist all sorts of metadata in ZooKeeper, including the alive set of brokers, the topic names and their partition count, as well as the partition assignments.
  - Kafka also used to heavily leverage ZooKeeper’s watch mechanism, which would notify a subscriber whenever a certain zNode changed.
- For the last few years, Kafka has actively been moving away from ZooKeeper towards its own consensus mechanism called KRaft (“Kafka Raft”).
  - It is a dialect of Raft with a few differences, heavily influenced by Kafka’s existing replication protocol. Most basically said, it extends the Kafka replication protocol with a few Raft-related features.
  - A key realization is that the cluster's metadata can be easily expressed in a regular log through the ordered record of events that happened in the cluster. Brokers could then replay the event to build the latest state of the system.
  - In this new model, Kafka has a quorum of N controllers (usually 3). These brokers host a special topic called the metadata topic (“__cluster_metadata”). This topic has a single partition whose leader election is managed Raft. The leader of the partition becomes the currently active Controller. The other controllers act as hot standbys, storing the latest metadata in memory.

  ![](https://lh7-us.googleusercontent.com/rCWoO0Ha2O0SrdNx9oncgasZx3j3ZbvQ5dLdkFU6RPGR7Ef1EShjCDz_WcBzLccqhyWps7NMTzhcbIu4PehnzXkWbRrP1WnMU7SjQvrRE-d4a6AS3k0oTRuHCmT26YsmjacwcJeq4gPnCQ-9c8Yz6fA)

  - All regular brokers replicate this topic too. Instead of having to directly communicate to the controller, they asynchronously update their metadata simply by keeping up with the topic’s latest records.

## 7. Tiered storage

- Kafka brokers store all data on local disks, which creates challenges at scale:
  - Large data volumes (e.g., 10TB per broker) make recovery from failures and rebalancing slow and resource-intensive.
  - Historical reads compete for limited disk IOPS, impacting performance for both consumers and producers.
  - Disk failures or adding new brokers require massive data replication, further straining resources.
- **Tiered Storage** addresses these issues by introducing two storage layers: hot local storage for recent data and cold remote storage (e.g., object store) for older data. Brokers seamlessly move data between tiers, allowing efficient scaling and faster recovery, while serving historical reads from remote storage when needed.
