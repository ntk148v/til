# RabbitMQ vs. Kafka

Source:

- <https://eranstiller.com/rabbitmq-vs-kafka-an-architects-dilemma-part-1>
- <https://eranstiller.com/rabbitmq-vs-kafka-an-architects-dilemma-part-2>
- <https://www.conduktor.io/blog/comparing-apache-kafka-activemq-and-rabbitmq/>

## 1. Asynchronous Messaging Patterns

### 1.1. Message Queueing

- Multiple producers can send messages to the same queue; however, when a consumer processes a message, it is locked or removed from the queue and is no longer available. Only a single consumer consumes a specific message.

![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Message-Queuing.svg)

### 1.2. Pub/Sub

- In the Publish/Subscribe (or Pub/Sub) communication pattern, a single message can be received and processed by multiple subscribers concurrently.

![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-PubSub.svg)

## 2. Introduce

### 2.1. RabbitMQ

- Message Broker
- It natively supports both messagnig patterns described above.
- Concepts:
  - Queue:RabbitMQ supports classic message queuing out of the box.
  - Message Exchange: RabbitMQ implements Pub/Sub via the use of message exchanges. It can also filter messages for some subscribers based on various routing rules.

  ![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-RabbitMQ-Message-Exchange.svg)
  - Consumer Group: group of consumers that work together processing messages in the form of competing consumers over a specific queue.

### 2.2. Kafka

- Distributed streaming platform.
- Kafka's storage layer is implemented using a partitioned transaction log.
- Concepts:
  - Kafka doesn't implement the notion of a queue. Kafka stores collections of reecords in categories called **topics**.
  - For each topic, Kafka maintains a partitioned log of messages.
  - Each **partition** is an ordered, immutable sequence of records where messages are continually appended.
  - By default, Kafka uses a round-robin partitioner to spread messages uniformly across partitions. Producers can modify this behavior to create logical streams of messages.

  ![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Kafka-Producers.svg)
  - Consumers consume messages by maintaining an **offset** (or index) to these partitions and reading them sequentially.
  - A single consumer can consume multiple topics, and consumers can scale-up to the number of partitions available
  - A group of consumers working together to consume a topic is called a **consumer group**.

  ![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Kafka-Consumers.svg)

## 3. Notable differences between Kafka and RabbitMQ

- RabbitMQ is a message broker, while Apache Kafka is a distributed streaming platform.

### 3.1. Message Ordering

- RabbitMQ provides few guarantees regarding the ordering of messages sent to queue or exchange.

```unknown
Messages published in one channel, passing through one exchange and one queue and one outgoing channel will be received in the same order that they were sent.

- RabbitMQ Broker Semantics -
```

- As long as we have a single message consumer, it receives messages in order. However, once we have multiple consumers reading messages from the same queue, we have no guarantee regarding the processing order of messages.
  - Use just 1 consumer? -> performance

![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Part-2-Message-Ordering-RabbitMQ.svg)

- Kafka provides a reliable ordering guarantee on message processing: all messages sent to the same topic partition are processed in-order.
  - A producer can set a partition key on each message to create logical streams of data. All messages from the same stream are then placed within the same partition, causing them to be processed in-order by consumer groups.
  - Within a consumer group, each partition is processed by a single thread of a single consumer -> Scale the number of partitions within a topic, causing each partition to receive fewer messages and add additional consumers for the additional partitions.

### 3.2. Message Routing

- RabbitMQ can route messages to subscribers of a message exchange based on subscriber defined routing rules.
  - A topic exchange can route messages based on a dedicated header named `routing_key`.
  - A headers exchange can route messages based on arbitrary message headers.
- Kafka doesn't allow consumer to filter messages in a topic before polling them.

### 3.3. Message Timing

- RabbitMQ provides various capabilities in regards to timing a message sent to a queue:
  - Message Time-To-Live (TTL)
  - Delayed/Scheduled Messages (plugin)
- Kafka provides no support for such features.

### 3.4. Message Retention

- RabbitMQ evicts messages from storage as soon as consumers successfully consume them.
- Kafka persists all messages by design up to a configured timeout per topic.

### 3.5. Fault Handling

- Two types of possible errors:
  - Transient failures: failures that occur due to a temporary issue such as network connectivity, CPU load, and a service crash.
  - Persistent failures: failures that occur due to a permanent issue that cannot be resolved via additional retries. Common causes of these failures are software bugs or an invalid message schema (i.e., a poison message).
- RabbitMQ provides tools such as delivery retries and dead-letter exchanges to handle message processing failures.
- Kafka doesn't provide any such mechanism out of the box. With Kafka, it is up to us to provide and implement message retry mechanisms at the application level.

### 3.6. Scale

- Both platforms can handle massive loads, Kafka typically scales better and can achieve higher throughput than RabbitMQ.

### 3.7. Consumer Complexity

- RabbitMQ uses a smart-broker & dumb-consumer approach.
  - Consumers register to consume queues, and RabbitMQ pushes them with messages to process as they come in
  - RabbitMQ manages the distribution of messages to consumers and the removal of messages from queues.

  ![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Part-2-Scaling-RabbitMQ.svg)

- Kafka, on the other hand, uses a dumb-broker & smart-consumer approach.
  - Consumers in a consumer group need to coordinate leases on topic parititions between them.
  - Consumers also need to manage and store their partitions’ offset index.
  - Kafka SDK takes care of these for us!

  ![](https://eranstiller.com/wp-content/uploads/2020/02/RabbitMQ-vs-Kafka-Part-2-Scaling-Kafka.svg)

## 4. Conclusion

- RabbitMQ is preferable when we need:
  - Advanced and flexible routing rules.
  - Message timing control (controlling either message expiry or message delay).
  - Advanced fault handling capabilities, in cases when consumers are more likely to fail to process messages (either temporarily or permanently).
  - Simpler consumer implementations.
- Kafka is preferable when we require:
  - Strict message ordering.
  - Message retention for extended periods, including the possibility of replaying past messages.
  - The ability to reach a high scale when traditional solutions do not suffice.
