# Monitor Kafka

## 1. Kafka consumer group lag

- **Consumer**: An application - read messages from a Kafka topic, run some validations against them, and write the results to another store --> Create a consumer object, subscribe to the appropriate topic, and start receiving messages, validating them and writing results.
- **Consumer group**: a set of consumers which cooperate to consume data from some topics. The partitions of all the topics are divived among the consumers in the group. As new group members arrive and old members leave, the partitions are re-assigned so that each member receives a proportional share of the partitions (rebalance).

![](https://www.oreilly.com/library/view/Kafka-the-definitive/9781491936153/assets/ktdg_04in01.png)

- **Consumer group lag**: the difference between the last produced message (the latest message available) and the last committed message (the last processed or read message) of a partition. For example, if there are 130 total messages in a parition and we've commited up to 100, then the consumer group lag for that partition is 30 messages/offsets.

![](https://downloads.lightbend.com/website/blog/monitor-Kafka-consumer-group-latency-with-Kafka-lag-exporter/consumer-lag.png)

- Having a large consumer group lag -> how far behind your application is in processing up-to-date information.

