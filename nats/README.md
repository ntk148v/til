# NATS

Source:
- <https://docs.nats.io/nats-concepts/overview>

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

- Quality of service (QoS): NATS offers multiple qualities of service, depending on whether the application uses just the *Core NATS* functionality or also leverages the added functionalities enabled by *NATS JetStream*
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

- *Core NATS* functionalities are publish/subscribe with subject-based-addressing and queuing.
- Publish-Subscribe:
  - One-to-many communications (fan-out).
  - A publisher sends a message on a subject and any active subscriber listening on that subject receives the message
  - Subscriber can also register interest in wildcard subjects.

![](https://683899388-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LqMYcZML1bsXrN3Ezg0%2Fuploads%2Fgit-blob-22d59af386038cc2717176561ffc95c63c295926%2Fpubsub.svg?alt=media)

- Request-Reply:
  - A request is published on a given subject using a reply subject.
  - Responers listen on that subject and send responsess to the reply subject.
- Queue Groups
