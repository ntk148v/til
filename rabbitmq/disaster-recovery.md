# Disaster Recovery & High Availability

Source:

- <https://blog.rabbitmq.com/posts/2020/07/disaster-recovery-and-high-availability-101/>
- <https://www.rabbitmq.com/reliability.html>
- <https://www.rabbitmq.com/distributed.html>

TL;DR: RabbitMQ supports:

- clustering of multiple nodes
- synchronous replication - replicated queues
- asynchronous cluster-to-cluster message routing - exchange federation and shovels
- limited back-up support
- limited rack awareness support

## 1. High Availability

- [Clustering](https://www.rabbitmq.com/clustering.html) multiple RabbitMQ brokers within a single data center or cloud region.
  - Clustering requires highly reliable, low latency links between brokers.
  - Clusterring across a WAN is not recommended due to the effect of network partitions.
  - If an enterprise has its own fiber linking its data centers which is highly reliable and consistently low latency (like on-prem availability zones), then it might be an option.
- RabbitMQ offers two types of **replicated queue**:

  - Classic Mirrored Queue:

    - Classic queues can be mirrored and configured for either availability (AP) or consistency (CP).
    - Mirrored queues are based on a replication algorithm called Chained Replication. In the context of queues, chained replication forms a ring of queues where there is one leader (the master) and one or more secondaries (mirrors). All messages are published to and consumed from the leader, the leader then replicates those operations to its adjacent mirror which in turn replicates to its adjacent mirror. This continues until reaching the last mirror who then notifies the master that the operation if fully replicated.

    ![](https://blog.rabbitmq.com/assets/images/2020/04/ChainReplication3Nodes.png)

    - Due to some edge cases that produced message loss, this algorithm was modified so that the channel process would additionally send the message directly to each mirror -> double network load.

    ![](https://blog.rabbitmq.com/assets/images/2020/04/ChainReplication3NodesDoubleSend.png)

    - When a mirror has been out of communication with its peers beyond a certain time limit, it is removed from the ring and the queue continues to be available. The problem occur upon the mirror rejoining the ring again. First the mirror discards all its data and then, optionally, a process called synchronization begins. synchronization is where the master replicates its current messages to a mirror. This is a _stop the world_ process where the queue becomes frozen until synchronization is complete. This becomes a problem if the queue is very big as the period of unavailability can be long.

    ![](https://blog.rabbitmq.com/assets/images/2020/04/ChainReplication5NodesRejoin.png)

    - Another option is to not synchronize a rejoining mirror with the master. In this case we end up with lower redundancy but avoid potentially painful synchronization. Of course, if the queue is empty or has few messages then synchronization doesn’t pose a big problem.
    - Another important topic is how it handles network partitions. When a partition occurs that splits a cluster into two halves, we’ll end up with one or more mirrors that lose communications with the master. As an administrator we can choose availability or consistency at this point.

      - If we don't want to lose messages, then we’ll configure the cluster to use `pause-minority` mode. This basically stops all brokers on the minority side of a partition. On the majority side (if there is one) the queue continues to operate, just with reduced redundancy. Once the partition is resolved, the cluster returns to normality.

      ![](https://blog.rabbitmq.com/assets/images/2020/04/PauseMinority.png)

      - If we want continued availability on both sides of the partition then we can choose `ignore` or `auto-heal` mode. This will allow a mirror to be promoted to master, meaning we have a master on both sides. This allows the queue to continue to receive and deliver messages no matter which side of the partition a client is connected to. Unfortunately, on resolving the partition one side of the partition is chosen as the victim and restarted, losing any messages in the queue on that side.

      ![](https://blog.rabbitmq.com/assets/images/2020/04/NonPauseMinority.png)

    - Due to these issues, Mirror Queue is deprecated and scheduled for removal feature -> **Use Quorum Queue**.

  - Quorum Queue:

    - Quorum queues do not use chained replication but are based on the-well established and mathematically proven Raft protocol.
    - Just like with mirrored queues, all clients interact with a leader, whose job it is to then replicate the enqueues and acks to its followers.

    ![](https://blog.rabbitmq.com/assets/images/2020/04/QQ.png)

    - It does have higher end-to-end latencies and those latencies closely correspond to the throughput/latency of your disks. Quorum queues only confirm messages once written to disk on a majority and so disk performance plays a large role in quorum queue performance.
    - There is no _stop the world_ synchronization, no throwing away data on rejoining, no difficult decisions to make about automatic vs manual synchronization at all. There is no availability vs consistency choice to make; a quorum queue will only confirm a message once it has been replicated to a majority of nodes. If a majority is down then you lose availability.
    - Network partitions: Firstly they use a separate and much faster failure detector that can detect partitions rapidly and trigger fast leader elections meaning that availability is either not impacted or is quickly restored.

- Client Reconnection:
  - Clients also need to be able to reconnect automatically in the event of a connection failure or a broker going offline. Most RabbitMQ clients offer automatic reconnection features.
- Rack Awareness: RabbitMQ does not currently have rack awareness, you can achieve the same results via manually specifying the nodes that a replicated queue should be spread across.
  - With mirrored queues you can specify the [list of nodes](https://www.rabbitmq.com/ha.html#mirroring-arguments) it should be spread across
  - With quorum queues you must currently create the queue with an initial group size of 1 and then [add members](https://www.rabbitmq.com/rabbitmq-queues.8.html#Replication) on the nodes to achieve the desired spread.

## 2. Disaster Recovery

- Schema replication: RabbitMQ does have support for replication of schema (the exchanges, queues, bindings, users, permissions, policies etc) which allows for a secondary cluster in a different data center to be an empty mirror of the primary cluster.
  - [Definitions export/import](https://www.rabbitmq.com/definitions.html)
- Data:

  - RabbitMQ does not yet have an asynchronous data replication feature that is suitable for all multi-DC scenarios.
  - Partial solution: leverage exchange [federation](https://www.rabbitmq.com/federated-exchanges.html) or [shovels](https://www.rabbitmq.com/shovel.html) which are an asynchronous message routing feature that work across clusters.
    - Federation:
      - Allows an exchange or queue on one broker to receive messages published to an exchange or queue on another.
      - Communication: AMQP, for two exchanges or queues to federate they must be granted appropriate users and permissions.
      - Typically you would use federation to link brokers across the internet for pub/sub messaging and work queueing.
    - Shovel:
      - Typically you would use federation to link brokers across the internet for pub/sub messaging and work queueing.
      - Whereas federation aims to provide opinionated distribution of exchanges and queues, the shovel simply consumes messages from a queue on one broker, and forwards them to an exchange on another.
      - Typically you would use the shovel to link brokers across the internet when you need more control than federation provides.
  - These features were not built for an active-passive architecture:

    - The difference between replication and cross-cluster message routing is that replication involves replicating both enqueue and acknowledgement operations, whereas message routing is only about replicating the messages
    - For example:

    ![](https://blog.rabbitmq.com/assets/images/2020/07/replication-vs-message-routing1.png)

    - Now a consumer consumes and ackniowledges messages m1 and m2 on DC1, and new messages m3 and m4 are published. Federation routes the m3 and m4 messages to DC2 but not the acks (federation does message routing only). Now m1 and m2 only exist on DC2, having been consumed on DC1. If DC1 went down and we failed over to DC2, m1 and m2 would be consumed again.

    ![](https://blog.rabbitmq.com/assets/images/2020/07/replication-vs-message-routing2.png)

    - Queue will continue to grow as message accumulate + Message duplication.
    - In order to mitigate the problems of duplication, apply either [message TTL policies](https://www.rabbitmq.com/ttl.html#per-queue-message-ttl) or [queue length limits](https://www.rabbitmq.com/maxlength.html) -> _cause message loss_.
    - In order to mitigate the problems of duplication, your systems either need to tolerate duplication (by being _idempotent_) or have a _deduplication_ solution in place (like message ids being stored in Redis).
