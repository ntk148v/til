# Inside the Apache Kafka Broker

Source: <https://developer.confluent.io/learn-kafka/architecture/broker/>

- The functions within a Kafka cluster are broken up into a data plane and a control plane:
  - The control plane handles managements of all the metadata in the cluster.
  - The data plane deals with the actual data that is written to and read from Kafka.

![](https://images.ctfassets.net/gt6dp23g0g38/6dIHZmyFufygLqoOZl9NK8/8f9c1a72e4d9f627847563d89bbe5afa/kafka-manages-data-and-metadata-separately.png)

- Client requests fall into 2 categories: produce requests and fetch requests.
- The Produce request:
  - Partition assignment: when a producer is ready to send an event record, it will use a configurable partitioner to determine the topic partition to assign to the record. If the record has a key, then the default partitioner will use a hash of the key to determine the correct partition -> any records with the same key will always be assigned to the same partition. If the record has no key then a partition strategy is used to balance the data in the partitions.
  - Record batching: the producer will accumulate the records assigned to a given partition into batches (+ compression). The producer has 2 main configurations that is uses to determine when to send batches to the broker: `batch.size` determines the minimum size of the batch, `linger.ms` specifies the maximum amount of time to wait for the batch to reach tat size. When either the batch size requirement is met, or the wait time has been reached, the batch is sent to the broker.

  ![](https://images.ctfassets.net/gt6dp23g0g38/4QinkT7rPaVuBNxl7hDjgq/056fd480245db3f5eb9cc54579914c3b/records-accumulated-into-record-batches.png)
  - Network thread adds request to queue: the request first lands in socket receive buffer where it will be picked up by a network thread from the pool. That network thread will handle that particular client request through the rest of its lifecycle. The network thread will read data from the socket buffer, form it into a produce request object, and add it to the request queue.

  ![](https://images.ctfassets.net/gt6dp23g0g38/7at83emsdcw5xzqGabaWjw/42b9b4f12a823cb85d21bed088d06561/network-thread-adds-request-to-queue.png)
  - I/O thread verifies and stores the batch: a thread from the I/O thread pool will pick up the request from the queue -> perform some validation, including a CRC check of the data in the request -> append the data to the physical data structure of the partition, which is called a commit log.

  ![](https://images.ctfassets.net/gt6dp23g0g38/5yYOWLCfh5E9ozctlPTxoc/e75266c8fb84ea8c4731edd2e9eb7cb8/io-thread-verifies-record-batch-and-stores.png)
  - Kafka physical storage: On disk, the commit log is organized as a collection of segments (each is made up of several files). One of these, a `.log` file, contain the event data. A `index` file contains an index structure, which maps from a record offset to the position of that record in the `.log` file.

  ![](https://images.ctfassets.net/gt6dp23g0g38/6BStOsjiQRncUJUEXIeo1s/1ca01b9ed05975582355502c18c671c6/kafka-physical-storage.png)
  - Purgatory holds reuqests until replicated: The log data is not flushed from the Pagecache to disk synchronously. Kafka relies on replication to multiple broker nodes, in order to provide durability. Check [./durability-availability-guarantees.md]. To avoid tying up the I/O threads while waiting for the replication step complete, the request object will be stored in a map-like data structure called purgatory. Once the request has been fully replicated, the broker will take the request object out of purgatory, genrate a response object, and place it on the response queue.

  ![](https://images.ctfassets.net/gt6dp23g0g38/50DNQZvomT50ZIrqo31F9I/b095631bc24b288459d712d517b70086/purgatory-holds-requests-being-replicated.png)
  - Response added to socket: Network thread will pick up the generated response, and send its data to the socket send buffer.

  ![](https://images.ctfassets.net/gt6dp23g0g38/23uvk4KmFEHuMAHcgxHCj5/6ac6107345c297851ad995f552c0b5cb/response-added-to-socket-send-buffer.png)

- The Fetch request:

  ![](https://images.ctfassets.net/gt6dp23g0g38/130jkNPNKOm2I6QizpNtu7/9c278568be8ec5e8886468acd01aeaa6/fetch-requests.png)
  - A consumer client sends a fetch request to the borker, specifying the topic, partition, and offset it wants to consume.
  - The fetch request is handled by network thread as same as the produce request.
  - I/O thread will take the offset that is included in the fetch request and compare it with `.index` file that is part of the partition segment. That will tell it exactly the range of bytes that need to be read from the corresponding `.log` file to add to the response object.
  - Consumers can be configured to wait for a minimum number of bytes of data, or to wait for a maximum amount of time before returning a response to a fetch request. While waiting for these criteria to be met, the fetch request is send to purgatory.
