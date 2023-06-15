# Kafka Producer Acks Deep Dive

Source: <https://www.conduktor.io/kafka/kafka-producer-acks-deep-dive/>

## 1. Kafka producers acks settings

- Kafka producers only write data to the current leader broker for a partition.
- Kafka producers must also specify a level of acknowledgement `acks` to specifyif the message must be written to a minimum number of replicas before being considered a successful write.

```unknown
The default value of acks has changed with Kafka 3.0

The producer has stronger delivery guarantees by default: idempotence is enabled and acks is set to all instead of 1. See KIP-679 for details. In 3.0.0 and 3.1.0, a bug prevented the idempotence default from being applied which meant that it remained disabled unless the user had explicitly set enable.idempotence to true. Note that the bug did not affect the acks=all change. See KAFKA-13598 for more details. This issue was fixed and the default is properly applied in 3.0.1, 3.1.1, and 3.2.0.
```

- Check [documentation](https://kafka.apache.org/documentation/#producerconfigs_acks).

- `acks=0`

  - Producers consider messages as "written succesfully" the moment the message was sent without waiting for the broker to accept it all.
  - If the broker goes offline, we won't know will lose data.

  ![](https://www.conduktor.io/kafka/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fo12xgu4mepom%2FSSa6dWceX7LtTjtVI92Bs%2Fabab84f7d8fd2429dfe9c99e4d29527f%2FAdv_Producer_Acks_DD_1.png)

- `acks=1`

  - Producers consider messages as "written successfully" when the message was acknowledged by only the leader.
  - Leader response is requested, but replication is not a guarantee as it happens in the background. If an ack is not received, the producer may retry the request. If leader broker goes offline unexpectedly but replicas haven't replicated the data yet, we have data loss.

  ![](https://www.conduktor.io/kafka/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fo12xgu4mepom%2F2FXXu7gdxEpADV0SuixTCH%2F8cac72693d6cb459f45230ac59f73433%2FAdv_Producer_Acks_DD_2.png)

  - `acks=all`

    - Producers consider messages as "written successfully" when the message is accepted by all in-sync replicas (ISR).
    - The lead replica for a partition checks to see if there are enough in-sync replicas for safely writing the message (controlled by the broker settings `min.insync.replicas`). The request will be stored in a buffer until the leader observes that the follower replicas replicated the message, at which point at successful acknowledgement is sent back to the client.

    ![](https://www.conduktor.io/kafka/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fo12xgu4mepom%2FYeG6HfAi9e8pWslz9rmQl%2Faaa8432f79c247d9fee37b4d7da598d0%2FAdv_Producer_Acks_DD_3.png)

    - The `min.insync.replicas` can be configured both at the topic and the broker-level.

      - `min.insync.replicas=2`: at least 2 brokers that are ISR (including leader) must respond that they have the data.
      - If a topic has three replicas and `min.insync.replicas=2` -> can only write to a partition in the topic if at least 2/3 replicas are in-sync. If 2/3 replicas are not available, the brokers will no longer accept produce reequests.

      ![](https://www.conduktor.io/kafka/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fo12xgu4mepom%2F3hv820JRmEOuuMELP6molP%2F8d7e04853ae37999fee673dd8df8c63f%2FAdv_Producer_Acks_DD_4.png)

## 2. Kafka Topic Durability & Availability

- General rule:
  - For a replica factor of `N`, you can permanently lose up to `N-1` brokers and still recover your data.
  - `acks=all` & `replication.factor=N` & `min.insync.replicas=M`, we can tolerate `N-M` brokers going down for topic availability purposes.
- Read: as long as one partition is up and considered an ISR, the topic will be available for reads.
- Write:
  - `acks=0` & `acks=1`: as long as one partition is up and considered an ISR, the topic will be available for writes.
  - `acks=all` & `min.insync.replicas=1` (default): the topic must have at least 1 partition up as an ISR and so we can tolerate two brokers being down.
  - `acks=all` & `min.insync.replicas=2`: the topic must have at least 2 ISR up, and therefore we can tolerate at most one broker being down (in the case of replication factor of 3), and we have the guarantee that for every write, the data will be at least written twice.
  - `acks=all` & `min.insync.replicas=3`: this wouldn't make much sense for a corresponding replication factor of 3 and we couldn't tolerate any broker going down.
