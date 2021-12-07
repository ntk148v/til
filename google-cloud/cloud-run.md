# Cloud Run

- [Cloud Run](#cloud-run)
  - [1. What is Cloud Run?](#1-what-is-cloud-run)
  - [2. Cloud Run platforms](#2-cloud-run-platforms)
  - [3. Knative](#3-knative)
  - [4. Migrate/develope service - notes](#4-migratedevelope-service---notes)

## 1. What is Cloud Run?

- A managed compute platform that enables you to run stateless containers that are invocable via web requests or Pub/Sub events.
- It is built from [Knative](https://cloud.google.com/knative)

## 2. Cloud Run platforms

![](https://cloud.google.com/anthos/run/docs/images/choose-platform.svg)

- Cloud Run (full managed) platform you to deploy stateless containers without having to worry about the underlying infrastructure.
- Cloud Run for Anthos abstracts away complex Kubernetes concepts, allowing developers to easily eleverage the benefits of Kubernetes and serverless together.

## 3. Knative

- [Knative](https://knative.dev) is a serverless framework that is based on Kubernetes. One important goal of Knative is to establish a cloud-native and cross-platform orchestration standard.
- Knative implements this serverless standard through integrating the creation of container or function, workload management and auto scaling, and event models

![](https://knative.dev/community/contributing/images/knative-audience.svg)

- Core components:
  - Build component: Build container images.
  - Eventing component: Eventing provides a whole set of event management functions including connecting and trigger events.
  - Serving component: Serving manages serverless workfloads. It provides request-based auto-scaling and supports scale-to-zero when no services need to be processed.

## 4. Migrate/develope service - notes

- Service requirements:
  - The service must listen for requests.
  - The service must be **stateless**. It cannot rely on a persistent _local_ state.
  - The service must not perform background activities outside the scope of request handling: When an application running on Cloud Run finishes handling a request, the container instance's access to CPU will be disabled or severely limited.
- Using a web server.
- Responses: Your container instance must send a response within the time specified in the request timeout settings (1-900 seconds), including the container instance startup time/504 error. >20 5xx sequential responses -> container instance is terminated.
- Filesystem access: In-memory filesystem -> container's memory -> potential leak memory -> not persist.
- Container resources limit: 1 vCPU, 256MB memory (default, maximum 8GB).
- Container memory usage:
  - Running the application executable.
  - Allocating memory in your application process.
  - Writing files to the filesystem.

```
(Standing Memory) + (Memory per Request) * (Service Concurrency)
```
