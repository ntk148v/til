# Cadence

Source: <https://cadenceworkflow.io/>

- [Cadence](#cadence)
  - [1. Introduction](#1-introduction)
  - [2. Concepts](#2-concepts)
    - [2.1. Workflows](#21-workflows)
    - [2.2. Activities](#22-activities)
    - [2.3. Event handling](#23-event-handling)
    - [2.4. Task lists](#24-task-lists)

Fault-Tolerant Stateful Code Platform

## 1. Introduction

- Cadence is a highly scalable fault-oblivious stateful code platform. The fault-oblivious code is a next level of abstraction over commonly used techniques to achieve fault tolerance and durability.
- Deployment:

  ![](https://user-images.githubusercontent.com/14902200/160308507-2854a98a-0582-4748-87e4-e0695d3b6e86.jpg)

  - Frontend: which is a stateless service used to handle incoming requests from Workers.
  - History Service:  where the core logic of orchestrating workflow steps and activities is implemented.
  - Internal Worker Service: implements Cadence workflows and activities for internal requirements such as archiving.
  - Matching Service: matches workflow/activity tasks that need to be executed to workflow/activity workers that are able to execute them.
  - Workers: are effectively the client apps for Cadence. This is where user created workflow and activity logic is executed.
  - Persistent store: Apache Cassandra, MySQL, PostgreSQL, CockroachDB, TiDB.
  - Workflow worker: The workflow code is hosted by an external - workflow worker process. These processes receive decision tasks that contain events that the workflow is expected to handle from Cadence service, delivers them to the workflow code, and communicates workflow decisions back the the service.
  - Activity worker: Activities are pieces of code that can perform any application-specific action like calling a service, updating a database record, or downloading a file from S3. Activities are hosted by activity worker processes that receive activity tasks from the Cadence service, invoke correspondent activity implementations and report back task completion statuses.
  - External clients.

## 2. Concepts

### 2.1. Workflows

- Fault-oblivious stateful code is called workflow.
- Used to chain together activities.
- For more complex business logic, we can segregate this further into child workflows.

### 2.2. Activities

- Workflow fault-oblivious code is ummune to infrastructure failures. But we need to connect to other services where failures are common. Hence codes that do all these are called activities.
- All communication with external service should be using activities.
- Think of it as the building block of Cadence.
- Activities are invoked asynchronous through a task list.
  - A task list is essentially a queue used to store an activity task until it is picked up by an available worker.
  - The worker processes an activity by invoking its implementation function.
  - When function returns, the worker reports the result back to the Cadence service which in turn notifies the workflow about completion.

### 2.3. Event handling

- Fault-oblivious stateful workflows can be signalled about an external event. A signal is always point to point destined to a specific workflow instance. Signals are always processed in the order in which they are received.
- Signals allow us to provide data at a later stage, but it maintains the events and payloads in history for the rest of the workflow.

### 2.4. Task lists

- When a workflow invokes an activity, it sends the ScheduleActivityTask decision to the Cadence service.
- The service updates the workflow state and dispatches an activity task to an activity worker -> add to queue and a worker receives the task using a long poll request.
