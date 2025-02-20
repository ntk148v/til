# Queues in Apache Kafka

Source: <https://www.confluent.io/blog/queues-on-kafka/>

## 1. What are message queues?

- Key characteristics of a queue:
  - Asynchronous communication: message queues allow producers to send message via the queue without needing the consumers to be ready at the same time.
  - First in, First out (FIFO): Just like the order in which you place your orders matters, message queues typically follow a FIFO pattern. There are shared queues where the ordering is not guaranteed.
  - Durability: Most message queues ensure that messages are stored reliably.
  - Message deletion: Messages are stored in the queue until a consumer processes them.
- Queues are especially beneficial in scenarios where parallel processing is needed, as they enable multiple consumers to read and process messages concurrently, and help in scalability of the system -> load balancing and managing tasks that can be processed independently of the order in which they were received.

## 2. What about streaming messages?

- Key characteristics of streaming messages:
  - Real-time processing: Streaming messages are designed for immediate consumption.
  - Event-driven architecture: Streaming is all about reacting to events as they happen.
  - Scalability: Streaming systems can handle a massive volume of data, processing thousands of messages per second.
  - Message retention: Messages are stored and can be consumed by multiple consumers, enabling both real-time and batch processing. Consumers track their progress (via offsets), allowing flexible replay of messages. Messages can be deleted based on retention policies, such as time-based (e.g., retain for 7 days) or size-based limits (e.g., retain up to 1GB per partition). Consumers do not trigger message deletion; rather, data is retained for historical access or reprocessing.

## 3. Apache Kafka and message queues

- Kafka stores messages in an append-only log format, where each message is assigned an offset. Consumers read these messages sequentially from these offsets, making it easy to replay messages and ensure fault tolerance. Messages can stick around for a set period of time, allowing for reprocessing or recovery if something goes wrong.

![](https://images.ctfassets.net/8vofjvai1hpv/5TVmeTBoRyO4EzgmvWJ9wP/0a3d4ae20131231a5bed9d380595387e/queues-1.png)

- **Consumer groups and share group**:

  - A **consumer group** is a set of consumers that cooperate to consume data from some topics. You establish the group for a consumer by setting its group.id in the properties for the consumer. The partitions of all the topics are divided among the consumers in the group.
  - This design offers both order and scalability, but it also ties the number of consumers directly to the number of partitions. To handle peak loads, many Kafka users create more partitions than they actually need, which can be inefficient and frustrating -> **share group**.
  - In some cases, consumers need to work together without being tied to specific partitions. Share groups introduce a more flexible way for consumers to cooperate, especially in use cases that feel more like a traditional queue system. Share groups act like a "durable shared subscription", allowing multiple consumers to process records from the same partitions.
    - Consumers in a share group can read from the same partition, unlike in consumer groups where partitions are exclusively assigned.
    - You can have more consumers in a share group than there are partitions.
    - Records are acknowledged one by one, though Kafka still optimizes for batch processing.
    - Kafka tracks delivery attempts and allows consumers to return unprocessed messages back to the queue, enabling other consumers to process them automatically.

![](https://images.ctfassets.net/8vofjvai1hpv/63ihAhdizxWnm9REoqBohY/57ce04a811db21b47856940513d8f0a3/queues-2.png)

- A share group doesn't guarantee ordering. Within a batch of records from a particular share-partition, the records are guaranteed to be in order by increasing offset. But when it comes to ordering between between different batches, there's no such guarantee.
