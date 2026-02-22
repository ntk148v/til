# Zeebe

Source:

- <https://docs.camunda.io/docs/1.3/components/zeebe/technical-concepts/architecture/>
- <https://www.linkedin.com/pulse/zeebeio-horizontally-scalable-distributed-workflow-engine-ruecker/>

## 1. Introduction

- Zeebe is a workflow engine for microservices orchestration. Zeebe ensures that, once started, flows are always carried out fully, retrying steps in case of failures. Along the way, Zeebe maintains a complete audit log so that the progress of flows can be monitored. Zeebe is fault tolerant and scales seamlessly to handle growing transaction volumes.
- It leverages [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html), instead of database tables.
  - Traditional workflow engines capture the current state of a workflow instance in a database table.

  ![](https://media-exp1.licdn.com/dms/image/C4D12AQHhFrqzALwFwg/article-inline_image-shrink_1000_1488/0/1564999156954?e=1666224000&v=beta&t=OYeaNZjenFPQ5XWaNzgWW7H0nWHP8EPb3gpxRDeCVWM)
  - All changes to the workflow state are captured as _events_ and thse events are stored in an event log alongside commands.

  ![](https://media-exp1.licdn.com/dms/image/C4D12AQFZjsMSFbv4hA/article-inline_image-shrink_1000_1488/0/1564999185089?e=1666224000&v=beta&t=u86tsHpOHiTxbLAwgC-6olrjnKCowEfDFq6aFKZnt28)

## 2. Architecture

- In order to achieve performance, resilience and scalability we applied the following distributed computing concepts:
  - Peer-to-peer clusters [Gossip](https://en.wikipedia.org/wiki/Gossip_protocol).
  - [Raft consensus algorithm](https://raft.github.io/).
  - Partitions.
  - High-performance computing concepts and the [high-performance protocol gRPC](https://grpc.io/).
- Overview:

  ![](https://docs.camunda.io/assets/images/zeebe-architecture-67c608106ddc1c9eaa686a5a268887f9.png)
  - Clients: libraries that you embed in an application to connect to a Zeebe cluster (via gRPC), have 2 uses:
    - Carrying out business logic (starting workflow instances, publishing messages, working on tasks)
    - Handling operational issues (updating workflow instance variables, resolving incidents)
  - Gateway: proxies request to brokers.
  - Broker: the distributed workflow engine that keeps state of active workflow instances. Brokers can be partitioned for horizontal scalability and replicated for fault tolerance.
    - Storing and managing the state of active workflow instances.
    - Distributing work items to clients.
  - Exporter: provides an event stream of state changes within Zeebe.

## 3. Workflow

- Workflows are flowchart-like blueprints that define the orchestration of tasks. Every task represents a piece of business logic such that the ordered execution produces a meaningful result.
- Running a workflow then requires 2 steps:
  - submitting the workflow to Zeebe.
  - creating job workers that can request jobs from Zeebe and complete them.
- Zeebe uses **visual workflow definitions** in the ISO standard BPMN, which can be modeled graphically with Zeebe Modeler.
- A workflow can include so called _service tasks_. When an instance reaches these tasks some of your code needs to be executed. This is done by creating _Jobs_ which are fetched by _JobWorkers_ in your applications.
  - For example, Go:

  ```go
  func main() {
    client, err := zbc.NewZBClient("localhost:26500")
    jobWorker := client.NewJobWorker().JobType("my-service-task").Handler(handleJob).Open()
    defer jobWorker.Close()
    jobWorker.AwaitClose()
  }

  func handleJob(client worker.JobClient, job entities.Job) {
    // here: business logic that is executed with every job
    log.Println(job)
    // and let the workflow engine know we are done
    request, err := client.NewCompleteJobCommand().JobKey(jobKey)
    request.Send()
  }
  ```

![](https://media-exp1.licdn.com/dms/image/C4D12AQFVT8QEubFwtg/article-inline_image-shrink_1000_1488/0/1564999783959?e=1666224000&v=beta&t=ma5uqMZL8f8OPGzd4qybFjv0rbZ1VWX1m_bR9EsZsaQ)
