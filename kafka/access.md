# Access Kafka

Source: <https://strimzi.io/blog/2019/04/17/accessing-kafka-part-1/>

![](https://strimzi.io/assets/images/posts/2019-04-17-connecting-to-leader.png)

- The client writing to or reading from a given partition have to connect directly to the leader broker which is hosting it. Thanks to the clients connecting directly to the individual brokers, the brokers don’t need to do any forwarding of data between the clients and other brokers. That helps to significantly reduce the amount of work the brokers have to do and the amount of traffic flowing around within the cluster. The only data traffic between the different brokers is due to replication, when the follower brokers are fetching data from the lead broker for a given partition. That makes the data shards independent of each other and that makes Kafka scale so well.

![](https://strimzi.io/assets/images/posts/2019-04-17-connection-flow.png)

- Discovery protocol:
  - Client is connecting to Kafka cluster -> connect to any broker which is member of the cluster and ask for metadata for topic(s). The _metadata_ contains the information about the topics, their partitions and brokers which host these partitions (all brokers should have this data).
  - The broker addresses used in the _metadata_ will be either created by the broker itself based on the hostname of the machine where the brokers runs. Or it can be configured by the user using `advertised.listeners` option.
  - Once received, the client will use the _metadata_ to figure out where to connect.
  - The client will use the address from the _metadata_ to open new connection(s) (always open new connection even when the _metadata_ would point to the same broker where the cclient already connected and received the _metadata_ from) to the addresses of the brokers which hosts the particular partitions it is interested in.
