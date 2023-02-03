# Cloudflare: Use Kafka to process 1 trillion inter-service messages

Source: <https://blog.cloudflare.com/using-apache-kafka-to-process-1-trillion-messages/>

Cloudflare uses Kafka to decouple microservices and communicate the creation, change or deletion of various resources via a common data format in a fault-tolerant manner.

This blog is focusing on inter-application communication use cases alone and not logging.

## Tooling

- General cluster - _Messagebus_:
  - Prevent data silos
  - Enable services to communicate more clearly with basically zero integration
  - Encourage the use of a self-documenting communication format and therefore removing the problem of out of data documentation

![](https://blog.cloudflare.com/content/images/2022/07/unnamed1-2.png)

- By providing a ready-to-go Kafka client, we ensured teams got up and running quickly, but we also abstracted some core concepts of Kafka a little too much, meaning that small unassuming configuration changes could have a big impact:

  - Example: partition skew (a large portion of messages being directed towards a single partition, meaning we were not processing messages in real time)
  - One drawback of Kafka is you can only have one consumer per partition, so when incidents do occur, you can't trivially scale your way to faster throughput.

  ![](https://blog.cloudflare.com/content/images/2022/07/image2-14.png)

## Connectors

- The connector framework is based on Kafka-connectors and allows our engineers to easily spin up a service that can read from a system of record and push it somewhere elase (Kafka/[Quicksilver](https://blog.cloudflare.com/introducing-quicksilver-configuration-distribution-at-internet-scale/)).

![](https://blog.cloudflare.com/content/images/2022/07/unnamed2-3.png)

- Example: Use connector to read from the Messagebus cluster and write to various other systems. This is orchestrated by a system the Application service team runs called Communication Preferences Service (CPS).

![](https://blog.cloudflare.com/content/images/2022/07/unnamed3-2.png)

## Strict Schemas

- Messagebus-Schema is a schema registry for all message types that will be sent over Messagebus cluster.
  - Message format: protobuf.
  - Store a mapping of proto mesages to a team, alongside that team's chat room in internal communication tool.

## Observability

- SaltStack: manage infrastructure configuration.
- Follow a Gitops style model, where repo holds the source of truth for the state of infrastructure.
  - To add a new Kafka topic, create pull request into this repo and add a couple of lines of YAML.
  - Upon merge, the topic and an alert for high lag will be created.
- Prometheus: metrics, Grafana: disaply.
- Metrics:
  - For producers:
    - Messages successfully delivered.
    - Message failed to deliver.
  - For consumer:
    - Messages successfully consumed.
    - Message consumption errors.
