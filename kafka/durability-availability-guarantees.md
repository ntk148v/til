# Data Durability and Availability Guarantees

Source: <https://developer.confluent.io/learn-kafka/architecture/guarantees/>

- Consumers only see committed records. Producers on the other hand have some choices as to when receive acknowledment for the success or failure of a produce request from the broker.
- Producer acks = 0.
  - The producer doesn't wait for a response from the broker.
  - No strong durability guarantee.

![](https://images.ctfassets.net/gt6dp23g0g38/6pfzwjpx5YWvwFENsCLMC4/5556aeccc621f4a71f638c9a5cf0b1b0/producer-acks-0.png)

- Producer acks = 1.
  - Better durability (data was written to the leader replica), a little higher latency.

![](https://images.ctfassets.net/gt6dp23g0g38/3p6EMq0jqOYJbabjyCPqWO/9f2b16737c49aeb98f557dade9ae7331/producer-acks-1.png)

- Producer acks = all (-1).
  - Default.
  - Highest level of durability, higher latency.

![](https://images.ctfassets.net/gt6dp23g0g38/2PE3eY4NoxDiz5zBCrideK/3989ab3a9dcf9a517fb4ffc42842845e/producer-acks-all.png)

- Topic `min.insync.replicas`.
  - The broker doesn't allow an event to be written to a topic unless there are N replicas in the ISR.
  - `min.insync.replicas = 2` and replication factor is 3 -> 2 nodes down, an exception!

![](https://images.ctfassets.net/gt6dp23g0g38/1w80a15fjW6XiLuZvZORxn/1f7ad75c445fa7b4a0a00e30646d79a3/topic-min-insync-replicas.png)

- Producer idempotence.
  - Kafka also has ordering guarantees which are handled mainly by Kafka’s partitioning and the fact that partitions are append-only immutable logs.
  - Events are written to a particular partition in the order they were sent, and consumers read those events in the same order (unless failure happens -> duplicate events).
  - Default: `event.idempotence = true`.

![](https://images.ctfassets.net/gt6dp23g0g38/5NH8JBhOQWlZNiki8Ff5iE/7c62e7ac73a8d1d610af622e3420dffb/producer-idempotency.png)

- End-to-end ordering guarantee.
  - `acks=all` + `event.idempotence=true`

![](https://images.ctfassets.net/gt6dp23g0g38/2oppFb3lGVX2jDxxSaR7rq/e86bc58bfcc4d65522f8c9939869c732/end-to-end-ordering.png)
