# Use cases

Source: ByteByteGo

Kafka was originally built for massive log processing. It retains messages until expiration and lets consumers pull messages at their own pace.

Unlike its predecessors, Kafka is more than a message queue, it is an open-source event streaming platform for various cases.

Let’s review the popular Kafka use cases.

1. Log processing and analysis
The diagram below shows a typical ELK (Elastic-Logstash-Kibana) stack. Kafka efficiently collects log streams from each instance. ElasticSearch consumes the logs from Kafka and indexes them. Kibana provides a search and visualization UI on top of ElasticSearch.

2. Data streaming in recommendations
E-commerce sites like Amazon use past behaviors and similar users to calculate product recommendations. The diagram below shows how the recommendation system works. Kafka streams the raw clickstream data, Flink processes it, and model training consumes the aggregated data from the data lake. This allows continuous improvement of the relevance of recommendations for each user.

3. System monitoring and alerting
Similar to the log analysis system, we need to collect system metrics for monitoring and troubleshooting. The difference is that metrics are structured data while logs are unstructured text. Metrics data is sent to Kafka and aggregated in Flink. The aggregated data is consumed by a real-time monitoring dashboard and alerting system (for example, PagerDuty).

4. CDC (Change data capture)
Change Data Capture (CDC) streams database changes to other systems for replication or cache/index updates. For example, in the diagram below, the transaction log is sent to Kafka and ingested by ElasticSearch, Redis, and secondary databases.

5. System migration
Upgrading legacy services is challenging - old languages, complex logic, and lack of tests. We can mitigate the risk by leveraging a messaging middleware. In the diagram below, to upgrade the order service in the diagram below, we update the legacy order service to consume input from Kafka and write the result to ORDER topic. The new order service consumes the same input and writes the result to ORDERNEW topic. A reconciliation service compares ORDER and ORDERNEW. If they are identical, the new service passes testing.

![](https://media.licdn.com/dms/image/D4E22AQHsiU3E1pybWA/feedshare-shrink_1280/0/1694100936831?e=1698278400&v=beta&t=jH_G4C-OsMvyxTtKEpcCPHR9uRd90vj80BHLWR6G95I)
