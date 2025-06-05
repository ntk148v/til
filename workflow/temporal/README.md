# Temporal

Source:

- <https://keithtenzer.com/temporal/Temporal_Fundamentals_Basics/>
- <https://sagikazarmark.github.io/temporal-intro-workshop/#>
- <https://manuel.bernhardt.io/2021/04/12/tour-of-temporal-welcome-to-the-workflow/>
- <https://thinhdanggroup.github.io/temporal-real-life/>
- <https://techdozo.dev/workflow-orchestration-with-temporal-and-spring-boot/>

Table of contents:

- [Temporal](#temporal)
  - [1. The problem](#1-the-problem)
  - [2. The basic](#2-the-basic)
    - [2.1. Temporal Platform](#21-temporal-platform)
    - [2.2. Temporal Application](#22-temporal-application)
    - [2.3. Temporal SDK](#23-temporal-sdk)
  - [3. Concepts](#3-concepts)
    - [3.1. Workflow](#31-workflow)
    - [3.2. Activity](#32-activity)
    - [3.3. Worker](#33-worker)
    - [3.4. Other notable concepts](#34-other-notable-concepts)

## 1. The problem

In just 20 years, software engineering has shifted from architecting monoliths with a single database and centralized state to microservices where everything is distributed across multiple containers, servers, data centers, and even continents. Distributing things solves scaling concerns, but introduces a whole new world of problems, many of which were previously solved by monoliths.

```unknown
Long running, complex interactions...
... in distributed systems...
... with transactional characteristrics
```

Let’s look at this problem in more detail, below is a very simple payment transaction involving just two APIs (withdraw and deposit).

```java
public void Payment(
    String fromAccountId, String toAccountId, String referenceId, int amountCents) {
    account.withdraw(fromAccountId, referenceId, amountCents);
    account.deposit(toAccountId, referenceId, amountCents);
}
```

- If the deposit API fails, an inconsistent state is reached as money is withdrawn, however no deposit can occur.
- To solve this problem, state must be maintained and persisted to a database. In addition retry and often timer mechanisms are required for handling failure recovery.
- The of course it all needs to scale, right? The result is a very complex architecture to handle what was a simple API orchestration.

![](https://keithtenzer.com/assets/2023-06-07/payment_wo_temporal.png)

Of course, we can develop these kind of mechanisms, combine with the exist solution like Kafka, Redis, to solve the problem. But, the question is "is it worth it?". It sounds like the reinvented wheels.

![](https://cdn.stackoverflow.co/images/jo7n4k8s/production/df945bd17e298523744411a7f4d4366771fcc139-1365x1600.png?auto=format)

We need a general solution, it's Temporal.

## 2. The basic

- Temporal provides the solution, which is **durable execution**. By enabling durability for every function or API call, Temporal is able to greatly reduce complexity, allowing developers to simply orchestrate their APIs and focus on business logic without worrying about durability.
- Developers can **write the business logic** (**workflow-as-code**) and have it be durable without building the durability themselves, or have to deal with the underlying infrastructure for distributed systems. This makes it easier to build applications that are resilient to failures, can scale horizontally, and are easy to test and debug.

![](https://keithtenzer.com/assets/2023-06-07/payment_with_temporal.png)

- The main components in the Temporal ecosystem are: Platform, SDK, tooling and application.
- ![](https://docs.temporal.io/diagrams/temporal-system-simple.svg)

### 2.1. Temporal Platform

- The **Temporal Platform** consists of a supervising software typically called a **Temporal Cluster** and application code bundled as **Worker Processes**. Together these components create a runtime for your application.

![](https://docs.temporal.io/diagrams/temporal-platform-simple.svg)

- **Temporal Cluster** is the group of services, known as the **Temporal Server**, combined with Persistence and Visibility stores, that together act as a component of the Temporal Platform.

![](https://docs.temporal.io/assets/images/temporal-cluster-30b133bd4034cd3226bf908ed3810e45.svg)

- **Worker Process** is responsible for polling a Task Queue, dequeueing a Task, executing your code in response to a Task, and responding to the Temporal Cluster with the results.
  - Worker Process is external to a Temporal Cluster.

[![](https://docs.temporal.io/diagrams/worker-and-server-component.svg)](https://docs.temporal.io/diagrams/temporal-platform-component-topology.svg)

### 2.2. Temporal Application

- Temporal Application is a set of **Temporal Workflow Executions**.
  - A Workflow Execution consumes few compute resources; in fact, if a Workflow Execution is suspended, such as when it is in a waiting state, the Workflow Execution consumes no compute resources at all.

### 2.3. Temporal SDK

- A Temporal SDK is a language-specific library that offers APIs to do the following:
  - Construct and use a Temporal Client
  - Develop Workflow Definitions
  - Develop Worker Programs

## 3. Concepts

Check out [the official documentation](https://docs.temporal.io/concepts) for more.

### 3.1. Workflow

- Workflow Definition:
  - aka. _Workflow Function_.
  - Encapsulates business logic.
  - Required to be **deterministic**.
    - Output is based entirely on the input.
  - Implemented in the _Worker_.
- Workflow Type:

  - Identities as _Workflow Definition_ (In the scope of a Task Queue)

  ![](https://docs.temporal.io/diagrams/workflow-type-cardinality.svg)

- Workflow Execution:
  - Durable and reliable execution of a _Workflow Definition_.
  - Runs once to completion.
  - Executed by the _Worker_.

### 3.2. Activity

- Activity Definition:
  - aka. _Activity Function_.
  - Building blocks for _Workflow (Definition)s_.
  - No restrictions on the code (ie. can be non-deterministic)
  - Asynchronously executed.
  - General **idempotent**.
    - Applying an operation multiple times does not change the result beyond the initial application.
- Activity Type:
  - Identities an _Actitivy Definition_ (in the scope of a Task Queue).
- Actitity Execution:
  - Execution of an _Activity Definition_
  - Can timeout
  - Can be retried
  - At least once execution guarantee
  - Runs to completion or exhausts timeouts/retries
  - Executed by the _Worker_

![](https://sagikazarmark.github.io/temporal-intro-workshop/assets/img/workflow-activity-relations.svg)

### 3.3. Worker

- Implemented and operated by the user
- Executes _Workflows_ and _Actitivies_.
- Listen to _Task Queues_.

![](https://sagikazarmark.github.io/temporal-intro-workshop/assets/img/temporal-high-level.svg)

### 3.4. Other notable concepts

- Namespace: unit of isolation and replication domain (analogous to a database)
- Task Queue: routing mechanism to different kinds of _Workers_.
