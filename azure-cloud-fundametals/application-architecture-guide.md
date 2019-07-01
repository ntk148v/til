# Architecture styles

[Source](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/)

An *architecture style* is a family of architectures that share certain characteristics.

An architecture style places constraints on the design, including the set of elements that can appear and the allowed relationships between those elements.

The following table summarizes how each style manages dependencies, and the types of domain that are best suited for each.

| Architecture style         | Dependency management                                        | Domain type                                                  |
| :------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| N-tier                     | Horizontal tiers divided by subnet                           | Traditional business domain. Frequency of updates is low.    |
| Web-Queue-Worker           | Front and backend jobs, decoupled by async messaging.        | Relatively simple domain with some resource intensive tasks. |
| Microservices              | Vertically (functionally) decomposed services that call each other through APIs. | Complicated domain. Frequent updates.                        |
| Event-driven architecture. | Producer/consumer. Independent view per sub-system.          | IoT and real-time systems                                    |
| Big data                   | Divide a huge dataset into small chunks. Parallel processing on local datasets. | Batch and real-time data analysis. Predictive analysis using ML. |
| Big compute                | Data allocation to thousands of cores.                       | Compute intensive domains such as simulation.                |

## N-tier

An N-tier architecture divides an application into *logical layers* and *physical tiers*.

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/n-tier-logical.svg)

Layers are a way to separate responsibilities and manage dependencies.

Tiers are physically separated, running on separate machines. A tier can call to another tier directly, or use asynchronous messaging (message queue).

When to use this architecture
* IaaS.
* Simple web applications.
* Unified development of on-premises and cloud applications.

Benefits
* Portability between cloud and on-premises, and between cloud platforms.
* Less learning curve for most developers.
* Natural evolution from the traditional application model.
* Open to heterogeneous environment (Windows/Linux)

Challenges
* It's easy to end up with a middle tier that just does CRUD operations on the database, adding extra latency without doing any useful work.
* Monolithic design prevents independent deployment of features.
* Managing an IaaS application is more work than an application that uses only managed services.
* It can be difficult to manage network security in a large system.

## Web-Queue-Worker

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/web-queue-worker-logical.svg)

A web front end that serves client requests, and a worker that performs resource-insentive tasks, long-running workflows, or batch jobs. The web front end communicates with the worker through a message queue.

The web and worker are both stateless. Session state can be stored in a distributed cache.

When to use this architecture
* Applications with a relatively simple domain.
* Applications with some long-running workflows or batch operations.
* When you want to use managed services, rather than infrastructure as a service (IaaS).

Benefits
* Relatively simple architecture that is easy to understand.
* Easy to deploy and manage.
* Clear separation of concerns.
* The front end is decoupled from the worker using asynchronous messaging.
* The front end and the worker can be scaled independently.

Challenges
* Without careful design, the front end and the worker can become large, monolithic components that are difficult to maintain and update.
* There may be hidden dependencies, if the front end and worker share data schemas or code modules.

## Microservices

A microservices architecture consists of a collection of small, autonomous services.Each service is self-contained and should implement a single business capability.

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/microservices-logical.svg)

Defining characteristics of a microservice:
* Services are small, independent and loosely coupled.
* Each service a separate codebase, which can be managed by a small development team.
* Service can be deployed independently.
* Service are responsible for persisting their own data or external state.
* Services communicates with each other by using well-defined APIs.
* Services don't need to share the same technology stack, libraries, or frameworks.

Typical components:
* Management.
* Service Discovery.
* API Gateway.

When to use this architecture
* Large applications that require a high release velocity.
* Complex applications that need to be highly scalable.
* Applications with rich domains or many subdomains.
* An organization that consists of small development teams.

Benefits
* Independent deployments.
* Independent devlopment.
* Small, focus teams.
* Fault isolation.
* Mixed technology stacks.
* Granular scaling.

Challenges
* Complexity.
* Development and test.
* Lack of governance.
* Network congestion and latency.
* Data integrity.
* Management.
* Versioning.
* Skillset.

## Event-driven architecture

An event-driven architecture consists of event producers that generates a stream of events, and event consumers that listen for the events.

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/event-driven.svg)

Models:
* Pub/sub.
* Event streaming.

When to use this architecture
* Multiple subsystems must process the same events.
* Real-time processing with minimum time lag.
* Complex event processing, such as pattern matching or aggregation over time windows.
* High volume and high velocity of data, such as IoT.

Benefits
* Producers and consumers are decoupled.
* No point-to point-integrations. It's easy to add new consumers to the system.
* Consumers can respond to events immediately as they arrive.
* Highly scalable and distributed.
* Subsystems have independent views of the event stream.

Challenges
* Guaranteed delivery.
* Processing events in order or exactly once.

### 1.5. Big data architecture

A big data architecture is designed to handle the ingestion, processing, and analysis of data that is too large or complex for traditional database systems.

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/big-data-logical.svg)

Types of workload:
* Batch processing of big data sources at rest.
* Real-time processing of big data in motion.
* Interactive exploration of big data.
* Predictive analytics and machine learning.

The common components:
* Data sources.
* Data storage.
* Batch processing.
* Real-time message ingestion.
* Stream processing.
* Analytical data store.
* Analysis and reporting.
* Orchestration.

When to use this architecture
* Store and process data in volumes too large for a traditional database.
* Transform unstructured data for analysis and reporting.
* Capture, process, and analyze unbounded streams of data in real time, or with low latency.

Benefits
* Technology choices.
* Performance through parallelism.
* Elastic scale.
* Interoperability with existing solutions.

Challenges
* Complexity.
* Skillset.
* Technology maturity.
* Security.

### Big compute architecture

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/big-compute-logical.png)

The term *big compute* describes large-scale workloads that require a large number of cores, often numbering in the hundreds or thousands.

![](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/images/big-compute-logical.png)

When to use this architecture
* Computationally intensive operations such as simulation and number crunching.
* Simulations that are computationally intensive and must be split across CPUs in multiple computers (10-1000s).
* Simulations that require too much memory for one computer, and must be split across multiple computers.
* Long-running computations that would take too long to complete on a single computer.
* Smaller computations that must be run 100s or 1000s of times, such as Monte Carlo simulations.

Benefits
* High performance with "embarrassingly parallel" processing.
* Can harness hundreds or thousands of computer cores to solve large problems faster.
* Access to specialized high-performance hardware, with dedicated high-speed InfiniBand networks.
* You can provision VMs as needed to do work, and then tear them down.

Challenges
* Managing the VM infrastructure.
* Managing the volume of number crunching
* Provisioning thousands of cores in a timely manner.
* For tightly coupled tasks, adding more cores can have diminishing returns. You may need to experiment to find the optimum number of cores.
