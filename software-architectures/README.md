# Architecture

- [Architecture](#architecture)
  - [1. Layered or N-tier architecture](#1-layered-or-n-tier-architecture)
  - [2. Monolithic architecture](#2-monolithic-architecture)
  - [3. Service-oriented architecture (SOA)](#3-service-oriented-architecture-soa)
    - [3.1. What is SOA?](#31-what-is-soa)
    - [3.2. How it works?](#32-how-it-works)
    - [3.3. SOA vs Microservices](#33-soa-vs-microservices)
  - [4. Event-driven architecture](#4-event-driven-architecture)
    - [4.1. Overview](#41-overview)
    - [4.2. Models](#42-models)
    - [4.3. Benefits of event-driven architecture](#43-benefits-of-event-driven-architecture)
  - [5. Microservices](#5-microservices)
    - [5.1. Overview](#51-overview)
    - [5.2. Decomposition](#52-decomposition)
    - [5.3. Problems/Concerns](#53-problemsconcerns)

Source:

- <https://www.redhat.com/en/topics/cloud-native-apps/what-is-an-application-architecture>
- <https://docs.microsoft.com/vi-vn/dotnet/architecture/microservices/architect-microservice-container-applications/service-oriented-architecture>
- <https://www.redhat.com/en/topics/cloud-native-apps/what-is-service-oriented-architecture>
- <https://martinfowler.com/articles/microservices.html>
- <https://martinfowler.com/microservices/>
- <https://www.cio.com/article/2434865/top-10-reasons-why-people-are-making-soa-fail.html>

- An application architecture describes the patterns and techniques used to design and build an application. The architecture gives you a roadmap and best practices to follow when building an application, so that you end up with a well-structured app.
- Choosing an application
  - Determine your strategic goals.
  - Design the architecture your goals.
  - Consider how frequently you want to relase updates to meet customer or operational needs, as well as functionality is required by either business objectives or development needs.
  - There are many different types of application architectures, but the most prominent today, based on the relationships between the services are: **monoliths and N-tier architecture** (tightly coupled), **microservices** (decoupled), and **event-driven architecture** and **service-oriented architecture** (loosely coupled).

## 1. Layered or N-tier architecture

- Traditional architecture.
- There are several layers or tiers, often 3. Layers help to manage dependencies and perform logical functions.
- Layers are arranged horizontally, so they are only able to call into layers bellow.

## 2. Monolithic architecture

- A single application stack that contains all functionality within that 1 application. This is tightly coupled, both in the interaction between the services and how they are developed and delivered.
- A single change to the application code requires the whole application to be released.

## 3. Service-oriented architecture (SOA)

Source:

- <https://medium.com/@SoftwareDevelopmentCommunity/what-is-service-oriented-architecture-fa894d11a7ec>
- <https://avinetworks.com/glossary/service-oriented-architecture/>
- <https://www.ibm.com/cloud/blog/soa-vs-microservices>

### 3.1. What is SOA?

- Defines a way to make software components reusable and interoperable via service interfaces - a communication protocol over a network.
- **9 main elements**:
  - *Standardized Service* Contract where services are defined making it easier for client applications to understand the purpose of the service.
  - *Loose Coupling* is a way to interconnecting components within the system or network so that the components can depend on one another to the least extent acceptable.
  - *Service Abstraction* hides the logic behind what the application is doing.
  - *Service Reusability* divides the services with the intent of reusing as much as possible to avoid spending resources on building the same code and configurations.
  - *Service Autonomy* ensures the logic of a task or a request is completed within the code.
  - *Service Statelessness* whereby services do not withhold information from one state to another in the client application.
  - *Service Discoverability* allows services to be discovered via a service registry.
  - *Service Composability* breaks down larger problems into smaller elements, segmenting the service into modules, making it more manageable.
  - *Service Interoperability* governs the use of standards (e.g. XML) to ensure larger usability and compatibility.
- There are **3 roles** in each of the SOA building blocks.
  - *Service provider* works in conjunction with the service registry, debating the whys and hows of the services being offered, such as security, availability, what to charge, and more. This role also determines the service category and if there need to be any trading agreements.
  - *Service registry/broker/repository* makes information regarding the service available to those requesting it. The scope of the broker is determined by whoever implements it.
  - *Service consumer* locates entries in the broker registry and then binds them to the service provider. They may or may not be able to access multiple services; that depends on the capability of the service requester.
- SOA was an overused term and has meant different things to different people. But as a common denominator, SOA means that *you structure your application by decomposing it into multiple services (most commonly as HTTP services) that can be classified as different types like subsystems or tiers*. Those services can now be deployed as Docker containers, which solves deployment issues, because all the dependencies are included in the container image --> scale up issue if you're deploying based on single Docker host --> Docker clustering software/an orchestrator.
- Microservices derive from SOA, but SOA is different from microservices architecture. Features like large central broker, central orchestrators at the organization level, and the Enterprise Service Bus are typical in SOA but in most cases, there are anti-patterns in the microservice community.

### 3.2. How it works?

- Typically, Service-Oriented Architecture is implemented with web services, which makes the “functional building blocks accessible over standard internet protocols.”
- Example: [SOAP](https://en.wikipedia.org/wiki/SOAP) - a messaging protocol specification for exchaging structured information in the implementation of web services in computer networks.
- It’s important to note that architectures can “operate independently of specific technologies,” which means they can be implemented in a variety of ways, including messaging, such as ActiveMQ; Apache Thrift; and SORCER.

![](https://avinetworks.com/wp-content/uploads/2018/10/service-oriented-architecture-diagram.png)

### 3.3. SOA vs Microservices

![](https://miro.medium.com/max/672/1*qAFyYAQSE3e-flZSqprHlg.jpeg)

- [Microservices](#2-microservices) and SOA are similar in some ways, the key differences come in their functionality.

  - **Scope**: SOA has an enterprise scope, while the microservices architecture has an application scope.

    ![](https://1.cms.s81c.com/sites/default/files/2020-09-02/SOA_microservices%20%281%29.png)

  - **Communication**: In a micoservices architecture, each service is developed independently, with its own communication protocol. With SOA, each service much sahre a common communication mechanism called an enterprise service bus (ESB).
  - **Interoperability**: In the interest of keeping things simple, microservices use lightweight messaging protocols like HTTP/REST (Representational State Transfers) and JMS (Java Messaging Service). SOAs are more open to heterogeneous messaging protocols such as SOAP (Simple Object Access Protocol), AMQP (Advanced Messaging Queuing Protocol) and MSMQ (Microsoft Messaging Queuing).
  - **Service granularity**: Microservices architectures are made up of highly specialized services, each of which is designed to do one thing very well. The services that make up SOAs, on the other hand, can range from small, specialized services to enterprise-wide services.
  - **Speed**: By leveraging the advantages of sharing a common architecture, SOAs simplify development and troubleshooting. However, this also tends to make SOAs operate more slowly than microservices architectures, which minimize sharing in favor of duplication.
  - **Governance**: The nature of SOA, involving shared resources, enable the implementation of common data governance standards across all services. The independent nature of microservices does not enable consistent data governance. This provides greater flexibility for each service, which can encourage greater collaboration across the organization.
  - **Storage**: SOA and microservices also differ in terms of how storage resources are allocated. SOA architecture typically includes a single data storage layer shared by all services within a given application, whereas microservices will dedicate a server or database for data storage for any service that needs it.

- SOA vs. microservices: which is best for you?: Larger, more diverse environments tend to lean towards service-oriented architecture (SOA), which supports integration between heterogenous applications and messaging protocols via an enterprise-service bus (ESB). Smaller environments, including web and mobile applications, do not require such a robust communication layer and are easier to develop using a microservices architecture.

## 4. Event-driven architecture

### 4.1. Overview

- With an event-driven system, the capture, communication, processing, and persistence of events are the core structure of the solution. This differs from a traditional request-driven model.
- Event-driven architecture enables minimal coupling, which makes it a good option for modern, distributed application architectures.

![](https://hazelcast.com/wp-content/uploads/2020/02/20_EventDrivenArchitecture.png)

- Event-driven architecture is made up of event producers and event consumers. An event producer detects or senses an event and represents the event as a message. It does not know the consumer of the event, or the outcome of an event.

### 4.2. Models

- **Pub/Sub** model.
  - This is a messaging infrastructure based on subscriptions to an event stream. With this model, after an event occurs, or is published, it is sent to subscribers that need to be informed.
- **Event streaming** model.
  - With an event streaming model, events are written to a log. Event consumers don’t subscribe to an event stream. Instead, they can read from any part of the stream and can join the stream at any time.
    - *Event stream processing* uses a data streaming platform, like Apache Kafka, to ingest events and process or transform the event stream. Event stream processing can be used to detect meaningful patterns in event streams.
    - *Simple event processing* is when an event immediately triggers an action in the event consumer.
    - *Complex event processing* requires an event consumer to process a series of events in order to detect patterns.

### 4.3. Benefits of event-driven architecture

## 5. Microservices

### 5.1. Overview

- A variant of SOA structural style - arranges an application as a collection of loosely-coupled services.
  - Highly maintainable and testable
  - Loosely coupled
  - Independently deployable
  - Organized around business capabilities
  - Owned by a small team
- Advantages:
  - Strong module boundaries.
  - Independent deployment.
  - Technology diveristy.
- Disadvantages:
  - Distribution.
  - Eventual consistency.
  - Operational complexity.

### 5.2. Decomposition

According to [microservices.io](https://microservices.io/patterns/microservices.html) and [amazon](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/decomposing-patterns.html), there are multiple patterns to decompose a monolith.

- Decompose by **business capability** and define services corresponding to business capabilities.
- Decompose by **domain-driven design subdomain**.
- Decompose by **verb or use case** and define services that are responsible for particular actions. e.g. a Shipping Service that’s responsible for shipping complete orders.
- Decompose by **by nouns or resource**s by defining a service that is responsible for all operations on entities/resources of a given type. e.g. an Account Service that is responsible for managing user accounts.

### 5.3. Problems/Concerns

- *How big is a microservice?* Or how do I scope my microservice?
- *How do I decompose our application?* Althought I have read multiple patterns, in the actual case, sometimes it isn't simple and clear as the guide.
- *SOA and Microservice*: You can check section 3.3. This is IBM's classification. But some others consider [SOA is just a concept, about arraging an application as a collection of sub services. And microservices is a one form of it as well as ESB](https://herbertograca.com/2017/11/09/service-oriented-architecture-soa/).
- *Microservice? Or Miniservices?*:
  - Check out this [article](https://thenewstack.io/miniservices-a-realistic-alternative-to-microservices/).
  - Miniservices is all about performing one function as a service.
- *Shared Database*: A shared database is considered an anti-pattern. Althought, it's debatable. The point is that when using a shared database, the microservices lose their core properties: scalability, resilience, and independence. Therefore, a shared database is rarely used with microservices.
