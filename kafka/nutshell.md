# Kafka in a nutshell

Source: <https://sookocheff.com/post/kafka/kafka-in-a-nutshell/>

- Explain the various terms of Kafka in order to fully understand its characteristics:
  - Broker: The server processes messages in Kafka.
  - Topic: Each consumer needs to subscribe to one or more topics to obtain messages. The Producer needs to specify the topic for which the message occurs.
  - Partition: a topic will be split into multiple partitions and land on the disk. In the storage directory, files are stored in the folder created by the corresponding partition ID.
  - segment: a partition will have multiple segment files to actually store the content.
  - offset: each partition has its own independent sequence number, and the scope is only under the current partition, which is used to read the corresponding file content.
  - leader: each topic needs a leader to be responsible for the writing of the topic's information and data consistency.
  - controller: each kafka cluster will select a broker to act as the controller, responsible for deciding who the leader of each topic is, monitoring changes in cluster broker information, and maintaining the health of the cluster state.
