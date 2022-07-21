# NATS

Source:

- <https://docs.nats.io/nats-concepts/overview>

- [NATS](#nats)
  - [1. Overview](#1-overview)
  - [2. Subject-Based Messaging](#2-subject-based-messaging)
  - [3. Core NATS](#3-core-nats)
  - [4. JetStream](#4-jetstream)
  - [4. Choose between JetStream and Core NATS](#4-choose-between-jetstream-and-core-nats)

## 1. Overview

- NATS is a connective technology (addressing, discovery and exchanging of messages; asking and answering questions; making and processing statements, or stream processing) that powers modern distributed systems.
  - Message oriented middleware
- Advantages:
  - Effortless M:N connectivity: NATS manages addressing and discovery based on subjects and not hostname and ports.
  - Deploy anywhere
  - Secure: NATS is secure by default and makes no requirements on network perimeter security models.
  - Scalable, Future-Proof Deployments
  - Adaptability
- Use cases:
  - Cloud Messaging
    - Services (microservices, service mesh)
    - Event/Data Streaming (observability, analytics, ML/AI)
  - Command and Control
    - IoT and Edge
    - Telemetry/Sensor Data/Command and Control
  - Augmenting or Replacing Legacy Messaging Systems
- Connect NATS client applications to NATS servers:
  - [NATS URL](https://docs.nats.io/using-nats/developer/connecting#nats-url)
  - [Authentication](https://docs.nats.io/using-nats/developer/connecting#authentication-details): support multiple authentication schemes (username/password, decentralized JWT, token, TLS certificates and Nkey with challenge)
- Design:
  - Messages are addressed and identified by subject strings, and do not depend on network location
  - Data is encoded and framed as a message and sent by a publisher. The message is received, decoded, and processed by one or more subscribers.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-19a2ced7956b0b0681a8d97c2684d8669120eaec%2Fintro.svg?alt=media)

- Quality of service (QoS): NATS offers multiple qualities of service, depending on whether the application uses just the _Core NATS_ functionality or also leverages the added functionalities enabled by _NATS JetStream_
  - At most once QoS (Core NATS): If a subscriber is not listening on the subject, or is not active when the message is sent, the message is not received. This is the same level of guarantee that TCP/IP provides. Core NATS is a fire-and-forget messaging system.
  - At-least/exactly once QoS (NATS JetStream): Higher qualities of service, or functionalities such as persistent streaming, de-coupled flow control, and Key/Value Store.

## 2. Subject-Based Messaging

- Subject is just a string of characters that form a name which the publisher and subscriber can use to find each other. It helps scope messages into streams or topics.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-dc7b8771a8a77c9042d216ca3868ec0fa7b05fff%2Fsubjects1.svg?alt=media)

- Subject hierachies: the `.` character is used to create a subject hierarchy.

```
time.us
time.us.east
time.us.east.atlanta
```

- Wildcards: NATS provides two wildcards that can take the place of one or more elements in a dot-separated subject.
  - Matching a single token (`*` wildcard)

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-b70adb26feafc88e119d7455639c57bb82bba9a4%2Fsubjects2.svg?alt=media)

- Matching multiple tokens (`>` wildcard): match one or more tokens, and can only appear at the end of the subject.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-e73c731e2444069e3aedf8e14a6cd6bb8aced13d%2Fsubjects3.svg?alt=media)

## 3. Core NATS

- _Core NATS_ functionalities are publish/subscribe with subject-based-addressing and queuing.
- Publish-Subscribe:
  - One-to-many communications (fan-out).
  - A publisher sends a message on a subject and any active subscriber listening on that subject receives the message
  - Subscriber can also register interest in wildcard subjects.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-22d59af386038cc2717176561ffc95c63c295926%2Fpubsub.svg?alt=media)

- Request-Reply:
  - A request is published on a given subject using a reply subject (inbox). Responders listen on that subject and send responsess to the reply subject.
  - Multiple NATS responders can form dynamic queue groups.
  - NATS applications "drain before exiting" (processing buffered messages before closing the connection) -> scale down.
  - Allow multiple responses, when the 1st response is utilized and the system efficiently discards the additional ones.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-dc10798d4afca301adba55c1e85c599b25a2ae24%2Freqrepl.svg?alt=media)]

- Queue Groups:
  - NATS provides a built-in load balancing feature called distributed queues.
  - To create a queue subscription, subscribers register a queue name. All subscribers with the same queue name form the queue group (queue groups are defined by the application and their queue subscribers, not on the server configuration)
  - Although queue groups have multiple subscribers, each message is consumed by only one.
  - "No responder": When a request is made to a service (request/reply) and the NATS server knows there are no services avaiable (there are no client applications currently subscribing the subject in a queue-group) the server will short circuit the request -> send a "no responder" protocol message to the requesting client.

## 4. JetStream

- Built-in distributed system called **JetStream**.
- Functionalities:

  - **Streaming**: temporal decoupling between publishers and subscribers.
    - Streams capture and store messages published on one (or more) subject and allow client applications to create 'subscribers' (JetStream consumers) at any time to 'replay' (or consume) all or some of the messages stored in the stream.
    - Replay policies: _all_ (_instant_, _original_), _last_, _sequence number_, and _start time_.
    - Limits:Maximum message age, maximum total stream size, maximum number of messages in the stream,...
    - Retention policy: _limits_, _interest_ and _work queue_.

  ![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-dedcc17f082fa1e39497c54ed8191b6424ee7792%2Fstreams-and-consumers-75p.png?alt=media)

  - **Persistent distributed storage**:
    - Memory storage
    - File storage
    - Replication (1 (none), 2, 3) between nats servers for Fault Tolerance
  - **De-coupled flow control**: Flow control is not 'end-to-end' where the publisher(s) are limited to publish no faster than the slowest of all the consumers can receive, but is instead happening individually between each client application and nats server.
  - **Exactly once message delivery**:
    - For publishing side it relies on the publishing application attaching a unique message or publication id in a message header and on the server keeping track of those ids for a configurable rolling period of time in order to detect the publisher publishing the same message twice.
    - For the subscribers a _double ack_ mechanism is used to avoid a message being erroneouslyh re-sent to a subscriber by the server after some kinds of failures.
  - **Consumers**:
    - 'Views' on a stream, subscribe to (or pulled) by client applications to receive copies of (or to consume) messages stored in the stream.
    - Client applications can choose to use un-ack `push` (ordered) consumers to receive messages as fast as possible (for the selected replay policy) on a specified delivery subject or to an inbox.
    - Horizontally scalable pull consumers with batching.
    - Consumer ack.
  - **K/V store**: the ability to store, retrieve and delete value messages associated with a key, to watch (listen) for changes happening to that key and even to retrieve a history of the values (and deletions) that have happened on a particular key.

- With JetStream a stream can also used as a queue, check out example [here](https://github.com/ntk148v/testing/tree/master/golang/nats/nats-jetstream).
  - Set the retention policy to `WorkQueuePolicy` and leveraging `pull consumers` to get easy horizontal scalability of the processing.
  - Use an explicit ack `push consumer` with a queue group of subscribers.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-62652b3e6dd556e3cb1c3bb474ec10038334c600%2Fqueue.svg?alt=media)

## 4. Choose between JetStream and Core NATS

- When to use streaming: Streaming is ideal when:
  - A historical record of a stream is required. This is when a replay of data is required by consumer.
  - The last message produced on a stream is required for initalization and the producer may be offline.
  - A-priori knowledge of consumers is not available, but consumers must receive messages. This is often a false assumption.
  - **Data producers and consumers are high decoupled**. They may be online at different times and consumers must receive messages.
  - The data in messages being sent have a lifespan beyond that of the intended application lifespan.
  - Applications need to consume data at their own pace.
  - You want de-coupled flow control between the publishers and the consumers of the stream.
  - You need `exactly-once` quality of service with de-duplication of publications and double-acknowledged consumption.
- When to use Core: Core is ideal for the fast request path for scalable services where there is toleranace for message loss or when applications them selves handle message delivery guarantees.
  - Service patterns where there is tightly coupled request-reply.
  - Where only the last message received is important and new messages will be received frequently enough for applications to tolerate a lost message.
  - Message TTL is low, where the value of the data being transmitted degrades or expires quickly.
  - The exptected consumer set for a message is available a-priori and consumers are expected to be live. The request-reply pattern works well here or consumers can send an application level acknowledgement.
  - Control plane messages.
