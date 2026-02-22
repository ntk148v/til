# Kafka Multi-Data Center - One Data Center is not enough

Source:

- <https://docs.confluent.io/platform/current/multi-dc-deployments/multi-region-architectures.html>
- <http://mbukowicz.github.io/kafka/2020/08/31/kafka-in-multiple-datacenters.html>
- <https://kafka.apache.org/documentation/#datacenters>
- <https://www.confluent.io/blog/multi-geo-replication-in-apache-kafka/>
- <https://www.confluent.io/kafka-summit-sf17/scaling-apache-kafka-across-multiple-data-centers/>

Table of contents:

- [Kafka Multi-Data Center - One Data Center is not enough](#kafka-multi-data-center---one-data-center-is-not-enough)
  - [0. Intro](#0-intro)
  - [1. Stretched Cluster](#1-stretched-cluster)
  - [2. Connected clusters](#2-connected-clusters)
    - [2.1. Active/Passive](#21-activepassive)
    - [2.2. Active/Active](#22-activeactive)

## 0. Intro

- Why Multi-Data Center?
  - Data center failure [disaster recovery](../disaster-recovery/).
  - Global operations with minimized latency.
  - Data sovereignty.
  - Data governance.
  - Network isolation.
- Why not Multi-Data Center?
  - Not all applications require a multi-region architecture. For exmaple, many startups don't have SLAs that require low RPO/RTO during full region failure.
  - Further, single-region arcitectures are simpler and easier to operate and maintain.

## 1. Stretched Cluster

- Take 3 nearby data center:
  - Low latency (sub-100ms)
  - Stable (veriy tight p99s)
  - Install at least 1 Zookeeper in each
  - Install at least 1 Kafka broker in each
  - Configure each DC as "rack"
  - Configure [acks](https://kafka.apache.org/documentation/#producerconfigs_acks)=all, [min.insync.replicas](https://kafka.apache.org/documentation/#brokerconfigs_min.insync.replicas)=2

![](http://mbukowicz.github.io/images/kafka-in-multiple-dcs/stretched-cluster.png)

> **NOTE**: Yes, I know these are two DCs in picture. But I'm too lazy to draw the new one.

- Rack-awareness:
  - Each partition in one DC has a repliac in the other DC:

  ![](http://mbukowicz.github.io/images/kafka-in-multiple-dcs/stretched-cluster-replica-assignment.png)
  - It is necessary because when disaster strikes then all partitions will need to be handled by the remaining data center:

  ![](http://mbukowicz.github.io/images/kafka-in-multiple-dcs/stretched-cluster-disaster.png)
  - By default Kafka is not aware that our brokers are running from different data centers and it could potentially put replicas of the same partition inside one DC. But if we take advantage of the [rack-awareness](https://cwiki.apache.org/confluence/display/KAFKA/KIP-36+Rack+aware+replica+assignment) feature and [assign Kafka brokers to their corresponding data centers](https://kafka.apache.org/documentation/#basic_ops_rackst) then Kafka will try to evenly distribute replicas over available DCs.

- With [KIP-392, Apache Kafka supports “Fetch From Followers”](https://cwiki.apache.org/confluence/display/KAFKA/KIP-392%3A+Allow+consumers+to+fetch+from+closest+replica) which allows consumers to read from the closest replica, whether that’s the leader or follower replica.
- **Pros**:
  - Easy to setup
  - Failover is "business as usual"
  - Sync replication - only method to guarantee no loss of data
- **Cons**:
  - Need 3 datacenters nearby
  - Higher latency, lower throughput.
  - Traffic betwene DCs can be bottleneck
  - Costly infrastructure.
- **RPO=0 and RTO~0**
- **When to use**:
  - You have 3 DCs, stable and low-latency network.
  - Need **RPO=0, RTO~0**
- **When not to use**:
  - Network performance is poor or unknown.
  - Don't have a strict RPO=0 requirement.

## 2. Connected clusters

- Basic async replication:
  - You have 2 (or more) clusters.
  - [MirrorMaker](https://kafka.apache.org/documentation/#basic_ops_mirror_maker)/[Confluent Replicator](https://docs.confluent.io/current/multi-dc-deployments/replicator/index.html) to sync between clusters.
  - Async -> Replication Lag!

### 2.1. Active/Passive

- 2 separate Kafka clusters in 2 DCs and _asynchronuos replicate messaegs from one cluser to the other_.
- Producers and consumers actively _use only one cluster_ at a time.

![](http://mbukowicz.github.io/images/kafka-in-multiple-dcs/active-passive.png)

- _A message could get lost_ if the first data center crashed before the message gets replicated.
- Requrire a _human intervention_: swicth to healthy cluster running.
- Deal with _aligining offsets_. Because clusters are totally independent the same message in the active cluster can get an entirely different offset in the passive one. And this can become a problem when you switch to the passive cluster because now consumers will need to somehow figure out where they have ended up reading. If done incorrectly the same messages will be read more than once, or worse - they will not be read at all.
- **RPO>0 and RTO>0**
- **When to use**:
  - You have >= 2 DCs.
  - High/Unpredictable ntework latency.
- **When no to use**:
  - Do not use this architecture when a small amount of data loss in the event of a data center failure would lead to a catastrophic cost (such as a breach of regulation).

### 2.2. Active/Active

- For details, please check [Linkedin blog post](https://engineering.linkedin.com/kafka/running-kafka-scale).

![](http://mbukowicz.github.io/images/kafka-in-multiple-dcs/active-active.png)

- Producers 1 an d2 publish messages to local clusters (represented by brokre A1 and A2) which are then propagated to aggregaet clusters (to which brokers B1 and B2 belong).
- Consumer 1 and 2 process only local messages; consumer 3 and 4 read messages from both local DCs (from Aggregate cluster).
  - For applications that need a global view of all data you can use mirroring to provide clusters which have aggregate data mirrored from the local clusters in all datacenters. These aggregate clusters are used for reads by applications that require the full data set.
- Depends on a scenario, you may choose read local or wait for aggregate clusters.
- It could also make sense to allow consumption only from the aggregate clusters (then only consumers 3 and 4 could read messages) which can potentially make reasoning easier and help achieve a more straightforward disaster-recovery procedure (at the cost of increased latency).
- The replication is still _async_.
- **RPO>0 and RTO either >0 or near 0**.
- **When to use**:
  - You have >= 2 DCs.
  - There is a business advantage from running applications in multiple data centers at the same time.
  - High/Unpredictable ntework latency.
- **When no to use**:
  - Do not use this architecture when a small amount of data loss in the event of a data center failure would lead to a catastrophic cost (for example, breach of regulation).
  - Do not use this architecture if an active/passive one would work just as well.
