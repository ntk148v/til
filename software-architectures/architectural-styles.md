# Architectural styles and patterns

- [Architectural pattern](https://en.wikipedia.org/wiki/Architectural_pattern) is a general, reusable solution to a commonly occurring problem in software architecture within a given context.

## 1. Service-oriented architecture (SOA)

Source:

- <https://medium.com/@SoftwareDevelopmentCommunity/what-is-service-oriented-architecture-fa894d11a7ec>
- <https://avinetworks.com/glossary/service-oriented-architecture/>
- <https://www.ibm.com/cloud/blog/soa-vs-microservices>

### 1.1. What is SOA?

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

### 1.2. How it works?

- Typically, Service-Oriented Architecture is implemented with web services, which makes the “functional building blocks accessible over standard internet protocols.”
- Example: [SOAP](https://en.wikipedia.org/wiki/SOAP) - a messaging protocol specification for exchaging structured information in the implementation of web services in computer networks.
- It’s important to note that architectures can “operate independently of specific technologies,” which means they can be implemented in a variety of ways, including messaging, such as ActiveMQ; Apache Thrift; and SORCER.

![](https://avinetworks.com/wp-content/uploads/2018/10/service-oriented-architecture-diagram.png)

### 1.3. SOA vs Microservices

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

## 2. Microservices
