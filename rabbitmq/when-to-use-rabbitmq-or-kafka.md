# When to use RabbitMQ or Apache Kafka

Source: <https://www.cloudamqp.com/blog/when-to-use-rabbitmq-or-apache-kafka.html>

> [!IMPORTANT]
> A **message queue** is a queue in RabbitMQ, and this “queue” in Kafka is referred to as a log, but to simplify the information in the article, I will refer to queues instead of switching to ‘log’ all the time.
>
> A message in Kafka is often called a **record**, but again, I will refer to messages in order to simplify the information here.
>
> When I write about a **topic** in Kafka, you can think of it as a categorization inside a message queue. Kafka topics are divided into partitions which contain records in an unchangeable sequence.

Both systems pass messages between producers and consumers through queues or topics. A message can include any kind of information. This kind of system is ideal for connecting different components, building microservices, real-time streaming of data or when passing work to remote workers.

![](https://www.cloudamqp.com/img/blog/kafka-vs-rabbitmq/message-broker.png)

![](https://www.cloudamqp.com/img/blog/kafka-vs-rabbitmq/kafka-setup.png)

## The big question; when to use Kafka, and when to use RabbitMQ?

**RabbitMQ and Kafka solve different problems**, and neither is universally "better." The right choice depends on your system requirements.

### RabbitMQ in a nutshell

RabbitMQ is presented as a **general-purpose message broker** designed for reliable message delivery between applications. It excels when you need:

- Task queues and background job processing
- Communication between microservices
- Complex message routing
- Multiple messaging protocols (AMQP, MQTT, STOMP, etc.)
- Features such as message priorities and flexible routing rules
- A simpler learning curve and operational model for many application-integration scenarios

Typical examples:

- Processing uploads, emails, PDF generation
- Event-driven microservices
- Service-to-service communication

### Kafka in a nutshell

Kafka is described as a **distributed event-streaming platform** optimized for:

- Very high-throughput data ingestion
- Long-term storage of event streams
- Replaying historical data
- Real-time analytics
- Log aggregation, auditing, and tracking systems

Kafka stores events as an append-only log and allows consumers to reread data from any point in time.

Typical examples:

- User activity tracking
- Security and audit logs
- Data pipelines
- Real-time analytics
- Financial market data streams

### The impact of RabbitMQ Streams

A major point in the article is that the comparison has changed since RabbitMQ introduced **Streams**.

Historically:

- RabbitMQ queues removed messages after consumption.
- Kafka retained data for replay.

With RabbitMQ Streams:

- Messages can be retained and replayed.
- Consumers can reread data multiple times.
- RabbitMQ now supports some use cases that previously pointed almost exclusively to Kafka.

However, Kafka remains more naturally centered around large-scale event streaming and analytics workloads.

### Key differences

| Area             | RabbitMQ                                      | Kafka                               |
| ---------------- | --------------------------------------------- | ----------------------------------- |
| Primary role     | Message broker                                | Event streaming platform            |
| Routing          | Rich routing (direct, topic, fanout, headers) | Minimal built-in routing            |
| Protocols        | Supports multiple standards                   | Uses Kafka-specific protocol        |
| Replay           | Available via Streams                         | Core feature                        |
| Message priority | Supported                                     | Not supported                       |
| Best for         | Work queues, microservices, integration       | Streaming, analytics, event storage |
| Learning curve   | Generally easier                              | Typically more complex ecosystem    |

### CloudAMQP's practical guidance

Choose **RabbitMQ** when:

- Building microservices
- Running asynchronous jobs
- Handling request/response workflows
- Needing sophisticated routing
- Wanting a traditional pub/sub message broker

Choose **Kafka** when:

- Building event-driven data platforms
- Storing and replaying large event streams
- Running analytics pipelines
- Handling massive ingestion rates
- Requiring long-term event retention and auditing

### One-sentence decision rule

**If you're primarily moving work between services, start with RabbitMQ; if you're primarily storing and processing streams of events at scale, start with Kafka.** RabbitMQ Streams narrows the gap, but Kafka remains the stronger fit for large-scale event streaming and analytics workloads.
