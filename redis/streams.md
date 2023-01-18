# Redis streams

Source:

- <https://redis.io/topics/streams-intro>
- <https://www.infoworld.com/article/3320021/how-to-use-redis-streams.html>
- <https://media.trustradius.com/product-downloadables/Z4/F7/0H6ACUNFBHQJ.pdf>

- [Redis streams](#redis-streams)
  - [1. What is Redis streams?](#1-what-is-redis-streams)
  - [2. Understand data flow in Redis streams](#2-understand-data-flow-in-redis-streams)
  - [3. Commands](#3-commands)
  - [4. Consumer Groups](#4-consumer-groups)
  - [5. Usage](#5-usage)
    - [5.1. Add data to a stream](#51-add-data-to-a-stream)
    - [5.2. Consume data from a stream](#52-consume-data-from-a-stream)

## 1. What is Redis streams?

Redis Streams is a Redis data type that represents a log, so you can add new information and message in an append-only mode (Note: This is not 100% accurate, since you can remove messages from the log, but it’s close enough.)  Redis Streams lets you build “Kafka-like” applications, which can:

- Create applications that publish and consume messages. Nothing extraordinary here, you could already do that with Redis Pub/Sub.
- Consume messages that are published even when the client application (consumer) is not running. This is a big difference from Redis Pub/Sub.
- Consume messages starting from a specific point. For example, read the whole history or only new messages.
- Async: Producers and consumers don't need to be simultaneously connected to the stream. Consumers can subscribe to streams (push) or read periodically (pull).
- At-least Once Delivery.
- ...

## 2. Understand data flow in Redis streams

- "Append-only" data structure that appears similar to logs. It offers commands that allow you to add sources to streams, cosume streams, and monitor and manage how data is consumed. The Streams data structure is flexible, allowing you to connect producers and consumers in several ways.

![](https://images.idgesg.net/images/article/2018/11/redis-streams-figure-1-100779767-large.jpg?auto=webp)

![](https://images.idgesg.net/images/article/2018/11/redis-streams-figure-2-100779768-large.jpg?auto=webp)

![](https://images.idgesg.net/images/article/2018/11/redis-streams-figure-3-100779769-large.jpg?auto=webp)

## 3. Commands

All [commands of Redis streams](https://redis.io/commands#stream) are documented online:

- Adding: `XADD` is the only command for adding data to a stream. Each entry has a unique ID that enables ordering.
- Reading: `XREAD` and `XRANGE` read items in the order determined by the IDs. `XREVRANGE` returns items in reverse order. `XREAD` can read from multiple streams and can be called in a blocking manner
- Deleting: `XDEL` and `XTRIM` can remove data from the stream.
- Grouping: `XGROUP` is for managing consumer groups. `XREADROUP` is a special version of XREAD with support for consumer groups. `XACK`, `XCLAIM` and `XPENDING` are other commands associated with consumer groups.
- Information: `XINFO` shows details of streams and consumer groups. `XLEN` gives number of entries in a stream.

## 4. Consumer Groups

![](https://devopedia.org/images/article/229/8887.1571235190.png)

- A consumer group allows consumers of that group to share the task of consuming messages from a stream. Thus, a message in a stream can be consumed by only one consumer in that consumer group (When the task at hand is to consume the same stream from different clients, then XREAD already offers a way to fan-out to N clients, however in certain problems what we want to do is not to provide the same stream of messages to many clients, but to provide a different subset of messages from the same stream to many clients - that of messages which are slow to process -> create N different workers -> scale message processing)
- `XGROUP` creates a consumer group. A consumer is added to a group the first time it calls `XREADGROUP` (identify itself with a unique consumer name).
- A stream can have multiple groups. Each consumer group tracks the ID of the last consumed message which is shared by all consumers of the group.
- Once a consumer reads a message, its ID is added to *Pending Entries List (PEL)*. The consumer must *acknowledge* that it has processed the message, using `XACK` command. Once acknowledged, the PEL is updated. Another consumer can *claim* a pending message using `XCLAIM` command and begin processing it -> recovering from failures. Can use `XAUTOCLAIM` = `XPENDING` + `XCLAIM`.
- A consumer can choose to use the `NOACK` subcommand of `XREADGROUP` if high reliability is not important.

## 5. Usage

### 5.1. Add data to a stream

```
# Auto-gen ID
# * operator tells Redis to auto-gen the ID.
XADD mystream * name Anna
XADD mystream * name Bert
XADD mystream * name Cathy

# User-managed ID
XADD mystream 10000000 name Anna
XADD mystream 10000001 name Bert
XADD mystream 10000002 name Cathy
```

### 5.2. Consume data from a stream

```
# Read everything from the beginning of the stream
# Situation: The stream already has the data you need to process,
# and you want to process it all from the beginning.
# Read up to 100 entries from the beginning of the stream
XREAD COUNT 100 STREAMS mystream 0
# Assume 1518951481323-0 is the last ID of the item you received in the previous command
XREAD COUNT 100 STREAMS mystream 1518951481323-1

# Consume data asynchronously (via a blocking call)
# Situation: Your consumer consumes and processes data faster than the rate at
# which data is added to the stream.
# XREAD returns all of the data after 1518951123456-1, If there’s no data after
# that, the query will wait for N=60 seconds until fresh data arrives, and then time out.
XREAD BLOCK 60000 STREAMS mystream 1518951123456-1
# Block infinitely
XREAD BLOCK 0 STREAMS mystream 1518951123456-1

# Read only new data as it arrives
# Situation: You are interested in processing only the new set of data starting from
# the current point in time.
# $ sign tells the XREAD command to retrieve only new data
XREAD BLOCK 60000 STREAMS mystream $

# Iterate the stream to read past data
# Situation: Your data stream already has enough data, and you want to query it
# to analyze data collected so far.
# You could read the data between two entries either in forward or backward direction
# using XRANGE and XREVRANGE respectively. In this example, the command reads
# data between 1518951123450-0 and 1518951123460-0:
XRANGE mystream 1518951123450-0 1518951123460-0

# Partition data among more than one consumer
# Situation: Consumers consume your data far slower than producers produce it.
# When more than one consumer is part of a group, Redis Streams will ensure that
# every consumer receives an exclusive set of data.
XREADGROUP GROUP mygroup consumer1 COUNT 2 STREAMS mystream >
# More: https://www.infoworld.com/article/3320021/how-to-use-redis-streams.html
```
