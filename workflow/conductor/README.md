# Conductor

Source: <https://conductor.netflix.com/>

- [Conductor](#conductor)
  - [1. Setup](#1-setup)
  - [2. Basic](#2-basic)
    - [2.1. Concepts](#21-concepts)
    - [2.2. Client](#22-client)
  - [2.3. Architecture](#23-architecture)

> Conductor is a platform created by Netflix to orchestrate workflows that span across microservices.

## 1. Setup

- Follow [Getting stared guide](https://conductor.netflix.com/gettingstarted/docker.html) and [Docker images and compose files here](https://github.com/ntk148v/dockerfiles/tree/master/conductor).
- Conductor server url: <http://localhost:8080/>
- Conductor UI url: <http://localhost:5000/>

## 2. Basic

### 2.1. Concepts

- Definitions (Metadata/Blueprints): Like definition in OOP paradigm.

```bash
Definitions 1->N Excutions
```

- Tasks: Building blocks of Workflows.
  - System tasks: Executed by Conductor server (within JVM).
  - Worker tasks: Executed by workers.

  ```bash
  Worker tasks <---gRPC---> Conductor server
  ```

- Workflow: the container of process flow, includes several different types of Tasks, Sub-Workflows, inputs and outpus connected to each other.
- Task definition: define Task level parameters like inputs and outputs, timeouts, retries...

### 2.2. Client

- Conductor tasks that are executed by remote workers communicate over HTTP endpoints/gRPC to poll for the task and update the status of the execution.
  - Metadata client: Register/Update workflow and task definitions
  - Workflow client: Start a new workflow/get execution status a workflow.
  - Task client: Poll for task/Update task result after execution/Get status of a task.

## 2.3. Architecture

![](https://conductor.netflix.com/img/conductor-architecture.png)

- Runtime Model:
  - RPC based communication model.
  - Workers are running on a separrate machine from the server.
  - Workers communicate with server over HTTP based endpoints and employs polling model for managing work queues.

![](https://conductor.netflix.com/img/overview.png)

- Worker is responsible for executing a task. Each worker embodies Microservice design pattern and follows certain basic principles:
  - Stateless.
  - Each worker executes a very specific task and produces well defined output given specific inputs.
  - Workers are meant to be idempotent.
  - Workers do not implement the logic to handle retries etc, that is taken care by the Conductor server.
