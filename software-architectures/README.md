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
    - [5.3. Best practices](#53-best-practices)
      - [5.3.1. Domain driven design](#531-domain-driven-design)
      - [5.3.2. Database per microservice](#532-database-per-microservice)
      - [5.3.3. Micro frontends](#533-micro-frontends)
      - [5.3.4. Continuous Delivery](#534-continuous-delivery)
      - [5.3.5. Observability](#535-observability)
      - [5.3.6. Unified Tech Stack](#536-unified-tech-stack)
      - [5.3.7. Asynchronous Communication](#537-asynchronous-communication)
      - [5.3.8. Microservice First](#538-microservice-first)
      - [5.3.9. Infrastructure over Libraries](#539-infrastructure-over-libraries)
      - [5.3.10. Organizational Considerations](#5310-organizational-considerations)
    - [5.4. Design Patterns](#54-design-patterns)
    - [5.5. Domain modeling for microservices](#55-domain-modeling-for-microservices)
      - [5.5.1. Introduction](#551-introduction)
      - [5.5.2. Analyze the domain](#552-analyze-the-domain)
    - [5.6. Concerns?](#56-concerns)

![](./overview.svg)

Source:

- <https://www.redhat.com/en/topics/cloud-native-apps/what-is-an-application-architecture>
- <https://docs.microsoft.com/vi-vn/dotnet/architecture/microservices/architect-microservice-container-applications/service-oriented-architecture>
- <https://www.redhat.com/en/topics/cloud-native-apps/what-is-service-oriented-architecture>
- <https://martinfowler.com/articles/microservices.html>
- <https://martinfowler.com/microservices/>
- <https://www.cio.com/article/2434865/top-10-reasons-why-people-are-making-soa-fail.html>
- <https://towardsdatascience.com/microservice-architecture-a-brief-overview-and-why-you-should-use-it-in-your-next-project-a17b6e19adfd>
- <https://johanlouwers.blogspot.com/2017/02/functional-decomposition-for.html>

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

- Microservice Architecture is about decomposing a Software System into autonomus Modules which are independently deployable and which communicates via lightweight, language agnostic way and together they fulfill the business goal.
- A variant of SOA structural style - arranges an application as a collection of loosely-coupled services.
  - Highly maintainable and testable
  - Loosely coupled
  - Independently deployable
  - Organized around business capabilities
  - Owned by a small team
- Advantages:
  - Application scaling.
  - Development speed.
  - Development scaling.
  - Release cycle.
  - Modularization.
  - Modernization.
- Disadvantages:
  - Design complexity.
  - Distributed systems complexity.
  - Operational complexity.
  - Security.
  - Data sharing and data consistency.
  - Communication complexities.

![](https://miro.medium.com/max/700/1*MrDMARKuvUCZliIvT5XtGg.png)

### 5.2. Decomposition

According to [microservices.io](https://microservices.io/patterns/microservices.html) and [amazon](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/decomposing-patterns.html), there are multiple patterns to decompose a monolith.

- Decompose by **business capability** and define services corresponding to business capabilities.
- Decompose by **domain-driven design subdomain**.
- Decompose by **verb or use case** and define services that are responsible for particular actions. e.g. a Shipping Service that’s responsible for shipping complete orders.
- Decompose by **by nouns or resource**s by defining a service that is responsible for all operations on entities/resources of a given type. e.g. an Account Service that is responsible for managing user accounts.

<https://docs.microsoft.com/en-us/learn/modules/microservices-architecture/5-analyze-decompose>

### 5.3. Best practices

Source: <https://towardsdatascience.com/effective-microservices-10-best-practices-c6e4ba0c6ee2>

#### 5.3.1. Domain driven design

- The foremost challenge to develop Microservices is to split a large, complex and application into small, autonomous, independently deployable Modules.
- Split wrong way -> tighly coupled Microservices (Monolith's disadavantages and Microserivces's complexities).
- Book [Domain Driven Design: Tackling Complexity in the Heart of Software](http://dddcommunity.org/book/evans_2003/):
  - The software development team should work in close co-operation with the Business department or Domain Experts.
  - The Architects/Developers and Domain Experts should first make the Strategic Design: Finding the Bounded Context and related Core Domain and Ubiquitous Language, Subdomains, Context Maps.
  - The Architects/Developers should then make the Tactical Design to decompose the Core Domain into fine-grained Building blocks: Entity, Value Object, Aggregate, Aggregate Root

#### 5.3.2. Database per microservice

- Shall we share database among Microservices or not?
- Sharing database among microservices -> strong coupling (changes -> synchronization among teams, manage transaction and locking of a database).
- Every microservice has own database/private tables -> exchaging data between microservices -> challenges.

#### 5.3.3. Micro frontends

- There are many ways to develop SPA based microfrontends: with iFrame, Web Components or via Elements.

#### 5.3.4. Continuous Delivery

- Each microservice can be deployed independently.
- To take full advantage of this Microservice feature, one needs CI/CD and DevOps.

#### 5.3.5. Observability

- Monitoring + Logging + Tracing

#### 5.3.6. Unified Tech Stack

- Using different programming languages/frameworks without any solid reason can lead to too many programming languages and frameworks without any real benefit.

#### 5.3.7. Asynchronous Communication

- How will the services communicate and share data among themselves?  (when each microservice has its own data storage).
- The easiest and most common way to communicate between microservices is via Synchronous REST API -> latency adds up + failure cascading + tight coupling between microservices.
- Microservices should communicate Asynchronous (Message Queue or asynchronous REST or CQRS).

#### 5.3.8. Microservice First

- Start with Microservices if there is a plan to use Microservice Architecture eventually.

#### 5.3.9. Infrastructure over Libraries

- Instead of investing heavily in a language-specific library (e.g. Java based Netflix OSS), it is wiser to use frameworks (e.g. Service Meshes, API gateway).

#### 5.3.10. Organizational Considerations

- Almost 50 years ago (1967), Melvin Conway gave an observation that the Software Architecture of a company is limited by Organizational Structure (Conway’s Law).
- If an organization plans to develop Microservice Architecture, then it should make the team size accordingly (two “American” Pizza team: 7±2 person).
- Also, the team should be cross-functional and ideally will have Frontend/Backend Developer, Ops Engineering and Tester.

### 5.4. Design Patterns

<table>
    <thead>
        <tr>
            <th>Pattern</th>
            <th>Diagram</th>
            <th>Pros</th>
            <th>Cons</th>
            <th>When to use</th>
            <th>When not to use</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Database per microservices</td>
            <td><img src="https://miro.medium.com/max/661/1*WWJQH50jxgrqh-ABFRQuzQ.jpeg"
                    srcset="https://miro.medium.com/max/276/1*WWJQH50jxgrqh-ABFRQuzQ.jpeg 276w, https://miro.medium.com/max/552/1*WWJQH50jxgrqh-ABFRQuzQ.jpeg 552w, https://miro.medium.com/max/640/1*WWJQH50jxgrqh-ABFRQuzQ.jpeg 640w, https://miro.medium.com/max/661/1*WWJQH50jxgrqh-ABFRQuzQ.jpeg 661w"
                    sizes="661px" width="661" height="410"></td>
            <td>Complete ownership of Data to a Service.Loose coupling among teams developing the services.</td>
            <td>Sharing data among services becomes challenging.Giving application-wide ACID transactional guarantee
                becomes a lot harder.Decomposing the Monolith database to smaller parts need careful design and is a
                challenging task.</td>
            <td>In large-scale enterprise applications.When the team needs complete ownership of their Microservices for
                development scaling and development velocity.</td>
            <td>In small-scale applications.If one team develops all the Microservices.</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Event sourcing</td>
            <td><img src="https://miro.medium.com/max/700/1*tRDaroNg_GnGdCZDFxLFKQ.jpeg"
                    srcset="https://miro.medium.com/max/276/1*tRDaroNg_GnGdCZDFxLFKQ.jpeg 276w, https://miro.medium.com/max/552/1*tRDaroNg_GnGdCZDFxLFKQ.jpeg 552w, https://miro.medium.com/max/640/1*tRDaroNg_GnGdCZDFxLFKQ.jpeg 640w, https://miro.medium.com/max/700/1*tRDaroNg_GnGdCZDFxLFKQ.jpeg 700w"
                    sizes="700px" width="700" height="180"></td>
            <td>Provide atomicity to highly scalable systems.Automatic history of the entities, including time travel
                functionality.Loosely coupled and event-driven Microservices.</td>
            <td>Reading entities from the Event store becomes challenging and usually need an additional data store
                (CQRS pattern)The overall complexity of the system increases and usually need Domain-Driven Design.The
                system needs to handle duplicate events (idempotent) or missing events.Migrating the Schema of events
                becomes challenging.</td>
            <td>Highly scalable transactional systems with SQL Databases.Transactional systems with NoSQL
                Databases.Highly scalable and resilient Microservice Architecture.Typical Message Driven or Event-Driven
                systems (e-commerce, booking, and reservation systems).</td>
            <td>Lowly scalable transactional systems with SQL Databases.In simple Microservice Architecture where
                Microservices can exchange data synchronously (e.g., via API).</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Command Query Responsibilityu Segregation (CQRS)</td>
            <td>
                <img src="https://miro.medium.com/max/341/1*l8GFDOUlyR_Km0dqg1VTgw.jpeg"
                    srcset="https://miro.medium.com/max/276/1*l8GFDOUlyR_Km0dqg1VTgw.jpeg 276w, https://miro.medium.com/max/341/1*l8GFDOUlyR_Km0dqg1VTgw.jpeg 341w"
                    sizes="341px" width="341" height="511">
                <img src="https://miro.medium.com/max/435/1*wCrXIQ7MD_20yKmZIBxHvQ.jpeg"
                    srcset="https://miro.medium.com/max/276/1*wCrXIQ7MD_20yKmZIBxHvQ.jpeg 276w, https://miro.medium.com/max/435/1*wCrXIQ7MD_20yKmZIBxHvQ.jpeg 435w"
                    sizes="435px" width="435" height="505">
            </td>
            <td>Faster reading of data in Event-driven Microservices.High availability of the data.Read and write
                systems can scale independently.</td>
            <td>Read data store is weakly consistent (eventual consistency)The overall complexity of the system
                increases. Cargo culting CQRS can significantly jeopardize the complete project.</td>
            <td>In highly scalable Microservice Architecture where event sourcing is used.In a complex domain model
                where reading data needs query into multiple Data Store.In systems where read and write operations have
                a different load.</td>
            <td>In Microservice Architecture, where the volume of events is insignificant, taking the Event Store
                snapshot to compute the Entity state is a better choice.In systems where read and write operations have
                a similar load.</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Saga</td>
            <td><img src="https://miro.medium.com/max/661/1*-Ro9jCnA7e0PnjnjEa0FWA.jpeg"
                    srcset="https://miro.medium.com/max/276/1*-Ro9jCnA7e0PnjnjEa0FWA.jpeg 276w, https://miro.medium.com/max/552/1*-Ro9jCnA7e0PnjnjEa0FWA.jpeg 552w, https://miro.medium.com/max/640/1*-Ro9jCnA7e0PnjnjEa0FWA.jpeg 640w, https://miro.medium.com/max/661/1*-Ro9jCnA7e0PnjnjEa0FWA.jpeg 661w"
                    sizes="661px" width="661" height="291"></td>
            <td>Provide consistency via transactions in a highly scalable or loosely coupled, event-driven Microservice
                Architecture.Provide consistency via transactions in Microservice Architecture where NoSQL databases
                without 2PC support are used.</td>
            <td>Need to handle transient failures and should provide idempotency.Hard to debug, and the complexity grows
                as the number of Microservices increase.</td>
            <td>In highly scalable, loosely coupled Microservice Architecture where event sourcing is used.In systems
                where distributed NoSQL databases are used.</td>
            <td>Lowly scalable transactional systems with SQL Databases.In systems where cyclic dependency exists among
                services.</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Backends for Frontends (BFF)</td>
            <td><img src="https://miro.medium.com/max/661/1*FCZRcAuSLhrNOjcq1zYXDw.jpeg"
                    srcset="https://miro.medium.com/max/276/1*FCZRcAuSLhrNOjcq1zYXDw.jpeg 276w, https://miro.medium.com/max/552/1*FCZRcAuSLhrNOjcq1zYXDw.jpeg 552w, https://miro.medium.com/max/640/1*FCZRcAuSLhrNOjcq1zYXDw.jpeg 640w, https://miro.medium.com/max/661/1*FCZRcAuSLhrNOjcq1zYXDw.jpeg 661w"
                    sizes="661px" width="661" height="704"></td>
            <td>Separation of Concern between the BFF’s. We can optimize them for a specific UI.Provide higher
                security.Provide less chatty communication between the UI’s and downstream Microservices.</td>
            <td>Code duplication among BFF’s.The proliferation of BFF’s in case many other UI’s are used (e.g., Smart
                TV, Web, Mobile, Desktop).Need careful design and implementation as BFF’s should not contain any
                business logic and should only contain client-specific logic and behavior.</td>
            <td>If the application has multiple UIs with different API requirements.If an extra layer is needed between
                the UI and Downstream Microservices for Security reasons.If Micro-frontends are used in UI development.
            </td>
            <td>If the application has multiple UI, but they consume the same API.If Core Microservices are not deployed
                in DMZ.</td>
        </tr>
        <tr>
            <td>6</td>
            <td>API Gateway</td>
            <td><img src="https://miro.medium.com/max/700/1*e3p0KRmyiqgEx9kYH1e0Hg.jpeg"
                    srcset="https://miro.medium.com/max/276/1*e3p0KRmyiqgEx9kYH1e0Hg.jpeg 276w, https://miro.medium.com/max/552/1*e3p0KRmyiqgEx9kYH1e0Hg.jpeg 552w, https://miro.medium.com/max/640/1*e3p0KRmyiqgEx9kYH1e0Hg.jpeg 640w, https://miro.medium.com/max/700/1*e3p0KRmyiqgEx9kYH1e0Hg.jpeg 700w"
                    sizes="700px" width="700" height="694"></td>
            <td>Offer loose coupling between Frontend and backend Microservices.Reduce the number of round trip calls
                between Client and Microservices.High security via SSL termination, Authentication, and
                Authorization.Centrally managed cross-cutting concerns, e.g., Logging and Monitoring, Throttling, Load
                balancing.</td>
            <td>Can lead to a single point of failure in Microservice Architecture.Increased latency due to the extra
                network call.If it is not scaled, they can easily become the bottleneck to the whole
                Enterprise.Additional maintenance and development cost.</td>
            <td>In complex Microservice Architecture, it is almost mandatory.In large Corporations, API Gateway is
                compulsory to centralize security and cross-cutting concerns.</td>
            <td>In private projects or small companies where security and central management is not the highest
                priority.If the number of Microservices is fairly small.</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Strangler</td>
            <td><img src="https://miro.medium.com/max/700/1*4cO7G9QFc9OjQgmSTwQP1Q.jpeg"
                    srcset="https://miro.medium.com/max/276/1*4cO7G9QFc9OjQgmSTwQP1Q.jpeg 276w, https://miro.medium.com/max/552/1*4cO7G9QFc9OjQgmSTwQP1Q.jpeg 552w, https://miro.medium.com/max/640/1*4cO7G9QFc9OjQgmSTwQP1Q.jpeg 640w, https://miro.medium.com/max/700/1*4cO7G9QFc9OjQgmSTwQP1Q.jpeg 700w"
                    sizes="700px" width="700" height="446"></td>
            <td>Safe migration of Monolithic application to Microservices.The migration and new functionality
                development can go in parallel.The migration process can have its own pace.</td>
            <td>Sharing Data Store between the existing Monolith and new Microservices becomes challenging.Adding a
                Facade (API Gateway) will increase the system latency.End-to-end testing becomes difficult.</td>
            <td>Incremental migration of a large Backend Monolithic application to Microservices.</td>
            <td>If the Backend Monolith is small, then wholesale replacement is a better option.If the client request to
                the legacy Monolithic application cannot be intercepted.</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Circuit Breaker</td>
            <td><img src="https://miro.medium.com/max/700/1*Olh9J1L3JSDi-PUa9CGa_A.jpeg"
                    srcset="https://miro.medium.com/max/276/1*Olh9J1L3JSDi-PUa9CGa_A.jpeg 276w, https://miro.medium.com/max/552/1*Olh9J1L3JSDi-PUa9CGa_A.jpeg 552w, https://miro.medium.com/max/640/1*Olh9J1L3JSDi-PUa9CGa_A.jpeg 640w, https://miro.medium.com/max/700/1*Olh9J1L3JSDi-PUa9CGa_A.jpeg 700w"
                    sizes="700px" width="700" height="395"></td>
            <td>Improve the fault-tolerance and resilience of the Microservice Architecture.Stops the cascading of
                failure to other Microservices.</td>
            <td>Need sophisticated Exception handling.Logging and Monitoring.Should support manual reset.</td>
            <td>In tightly coupled Microservice Architecture where Microservices communicates Synchronously.If one
                Microservice has a dependency on multiple other Microservices.</td>
            <td>Loosely coupled, event-driven Microservice Architecture.If a Microservice has no dependency on other
                Microservices.</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Externalizaed Configuration</td>
            <td></td>
            <td>Production configurations are not part of the Codebase and thus minimize security
                vulnerability.Configuration parameters can be changed without a new build.</td>
            <td>We need to choose a framework that supports the Externalized Configuration.</td>
            <td>Any serious production application must use Externalized Configuration.</td>
            <td>In proof of concept development.</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Consumer-Driven Contract Testing</td>
            <td></td>
            <td>If the Provider changes the API or Message unexpectedly, it is found autonomously in a short time.Less
                surprise and more robustness, especially an enterprise application containing lots of
                Microservices.Improved team autonomy.</td>
            <td>Need extra work to develop and integrate Contract tests in Provider Microservice as they may use
                completely different test tools.If the Contract test does not match real Service consumption, it may
                lead to production failure.</td>
            <td>In large-scale enterprise business applications, where typically, different teams develop different
                services.</td>
            <td>Relative simpler, smaller applications where one team develops all the Microservices.If the Provider
                Microservices are relatively stable and not under active development.</td>
        </tr>
    </tbody>
</table>

### 5.5. Domain modeling for microservices

#### 5.5.1. Introduction

- Domain-driven design (DDD) provides a framework that can get you most of the way to a set of well-designed microservices.
- DDD has 2 distinct phases:
  - Strategic: define the large-scale structure of the system.
  - Tatical: provide a set of design patterns (entities, aggregates, domain services) that you can use to create the domain model.

![](https://docs.microsoft.com/en-us/azure/architecture/microservices/images/ddd-process.png)

#### 5.5.2. Analyze the domain

### 5.6. Concerns?

- *How big is a microservice?* Or how do I scope my microservice?
- *How do I decompose our application?* Althought I have read multiple patterns, in the actual case, sometimes it isn't simple and clear as the guide.
- *SOA and Microservice*: You can check section 3.3. This is IBM's classification. But some others consider [SOA is just a concept, about arraging an application as a collection of sub services. And microservices is a one form of it as well as ESB](https://herbertograca.com/2017/11/09/service-oriented-architecture-soa/).
- *Microservice? Or Miniservices?*:
  - Check out this [article](https://thenewstack.io/miniservices-a-realistic-alternative-to-microservices/).
  - Miniservices is all about performing one function as a service.
- *Shared Database*: A shared database is considered an anti-pattern. Althought, it's debatable. The point is that when using a shared database, the microservices lose their core properties: scalability, resilience, and independence. Therefore, a shared database is rarely used with microservices.
