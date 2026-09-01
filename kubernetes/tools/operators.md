# Operators: Put Operational Knowledge into Software

Source: [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) | [CNCF Operator White Paper v1](https://github.com/cncf/tag-app-delivery/blob/163962c4b1cd70d085107fc579e3e04c2e14d59c/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## What is an Operator?

An Operator is a **Kubernetes controller** that extends the Kubernetes API with domain-specific knowledge to manage the full lifecycle of complex stateful applications. It encodes human operational expertise in software, enabling automated deployment, scaling, upgrades, backup/restore, and self-healing for applications that go beyond what native Kubernetes resources support.

> _The operator pattern aims to capture the key aim of a human operator managing a service: deep knowledge of how the system ought to behave, how to deploy it, and how to react if there are problems._ — Kubernetes Docs

## Operator Design Pattern

The Operator pattern consists of three components working together:

| Component                                | Description                                                                                                                                                                                               |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Application/infrastructure to manage** | The stateful application (database, cache, monitoring system, etc.) running in the cluster.                                                                                                               |
| **Custom Resource (CR)**                 | A declarative API (via CRD) that describes the desired state of the application. Users create, update, or delete CR instances to manage the application.                                                  |
| **Control loop (controller)**            | A long-running process that continuously watches CRs, compares desired vs. current state, and takes action to reconcile them. It runs the reconciliation loop to transition objects to the desired state. |

> _By using the operator pattern, the user only describes the desired state; the operator implementation makes the necessary changes to achieve that state._ — CNCF White Paper

## Operator Characteristics

Operators provide capabilities across three overarching categories:

### Dynamic Configuration

- Operators define **custom resource types** (CRDs) to express application configuration more precisely than generic Kubernetes objects.
- Enable **better validation and data structuring**, reducing configuration errors and allowing teams to self-serve.
- Support **progressive defaults** — a few high-level settings populate best-practices-driven configuration.
- Adaptive configuration: adjust resource usage based on available hardware or expected load.

### Operational Automation

- Include **custom controllers** that automate common or repetitive tasks (backups, restores, scaling, upgrades).
- Tasks become **repeatable, testable, and upgradable** in a standardized fashion.
- Keep humans out of the loop on frequent tasks, preventing missed steps and drift.
- Reduce hours spent on upkeep like application backups.

### Domain Knowledge

- Encode **specialized knowledge** about particular software or processes (e.g., multi-step database upgrades).
- Handle **error remediation** with specific behavior — monitor and react to errors, or escalate if auto-resolution fails.
- Reduce **MTTR** (mean time to recovery) and **operator fatigue** from recurring issues.

> _An operator can monitor its application and react to errors with specific behavior to resolve the error or escalate the issue if it can't be automatically resolved._ — CNCF White Paper

## Operator Components in Kubernetes

### Custom Resources and CRDs

Custom resources extend the default Kubernetes API, allowing operators to define new object types. A CRD defines the schema (fields, names, versions) of the custom resource.

**Example CRD instance:**

```yaml
apiVersion: example-app.appdelivery.cncf.io/v1alpha1
kind: ExampleApp
metadata:
  name: appdelivery-example-app
spec:
  appVersion: "0.0.1"
  features:
    exampleFeature1: true
    exampleFeature2: false
  backup:
    enabled: true
    storageType: "s3"
    host: "my-backup.example.com"
    bucketName: "example-backup"
status:
  currentVersion: "0.0.1"
  url: "https://myloadbalancer/exampleapp/"
  authSecretName: "appdelivery-example-app-auth"
  backup:
    lastBackupTime: "12:00"
```

- **`spec`**: Declares the desired state — version, features, backup configuration, etc.
- **`status`**: Operator communicates current state — deployed version, connection details, health, last backup time, etc.

### Control Loop (Reconciliation Loop)

The control loop continuously:

1. **Watches** for changes to the custom resource and other relevant Kubernetes objects.
2. **Compares** the desired state (from CR `spec`) with the current state (actual running resources).
3. **Reconciles** by taking action to move the current state toward the desired state.
4. Can be **event-triggered** (CRUD on CR) or **time-based** (scheduled backups, periodic checks).

> _The controller will constantly compare the desired state with the current state using the reconciliation loop which ensures that the watched objects get transitioned to the desired state in a defined way._ — CNCF White Paper

### Kubernetes Controllers

- A **Kubernetes controller** takes care of routine tasks to ensure the desired state of a resource type matches the current state (e.g., Deployment controller managing pod replicas).
- **Technically, there is no difference** between a typical controller and an operator. The distinction is the **operational knowledge** embedded in the operator.
- A controller that simply spins up a pod when a CR is created is a **simple controller**. If it has operational knowledge (upgrades, error remediation), it is an **operator**.

## Operator Frameworks

Several frameworks exist to scaffold and build operators. Choose based on language, abstraction level, and needs:

| Framework                                         | Language   | Abstraction                                                           |
| ------------------------------------------------- | ---------- | --------------------------------------------------------------------- |
| **Operator Framework**                            | Go         | High-level SDK with `operator-sdk`                                    |
| **Kubebuilder**                                   | Go         | Framework for CRD/controller generation (based on Operator Framework) |
| **kopf**                                          | Python     | Pythonic framework, concise syntax                                    |
| **Metacontroller**                                | Any        | Lightweight controllers as a service using webhooks                   |
| **kopf (Kubernetes Operator Pythonic Framework)** | Python     | Fluent API, excellent for simple operators                            |
| **kube-rs**                                       | Rust       | Rust-based operator library                                           |
| **Java Operator SDK**                             | Java       | Java ecosystem operator development                                   |
| **Charmed Operator Framework**                    | Go/Charmed | Model-driven operators for complex applications                       |
| **shell-operator**                                | Bash/Shell | Shell scripts as operators                                            |

> _Choose the right tool for your needs. The framework handles boilerplate; you provide the operational logic._ — CNCF White Paper

## Operator Lifecycle Management

### Upgrading the Operator

- Operators should support **in-place upgrades** without disrupting managed applications.
- New version of the operator Deployment runs alongside the old one during transition.
- CRD changes require careful handling — old CR versions must remain readable.

### Upgrading the Declarative State

- Operators can orchestrate **application upgrades** (code, database schemas, configuration) based on the user-specified desired version.
- The control loop handles sequential steps: backup → migrate → restart → verify.

### Managing Relations of CRDs

- One CRD per controller is the simplest pattern.
- For related applications, consider the **Operator of Operators** pattern or using **annotations/labels** to relate multiple CRDs.

## Use Cases

| Use Case                 | Description                                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **Prometheus Operator**  | Extends Kubernetes to manage Prometheus monitoring instances, ServiceMonitors, alert rules, and storage configuration. |
| **Operator for GitOps**  | Encodes GitOps workflows: operator watches Git state and reconciles cluster to match.                                  |
| **Database Operators**   | Manages lifecycle of databases: deployment, backup, restore, upgrade, failover.                                        |
| **Cache Operators**      | Manages Redis, Memcached clusters with proper clustering, failover, and data persistence.                              |
| **Middleware Operators** | Message queues (Kafka, RabbitMQ), streaming platforms, search engines.                                                 |

> _Operators can manage any application whose lifecycle can be expressed as a sequence of well-defined steps._ — CNCF White Paper

## Successful Patterns

### Management of a Single Type of Application

- Focus the operator on **one application type** per controller/CRD pair. Simpler, more maintainable, and easier to reason about.

### Operator of Operators

- An operator that manages other operators. Useful for platform teams managing a portfolio of application operators.

### One CRD per Controller

- Each controller watches and manages **one custom resource type**. Avoids complexity from a single controller managing multiple unrelated CRDs.

### Where to Publish and Find Operators

- **OperatorHub.io**: Discover and install operators for popular applications.
- Publish your operator to make it available to the community.

### Further Reading

- CNCF Operator White Paper (this document)
- Kubernetes: [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- Google Cloud: [Best practices for building Kubernetes operators](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps)

## Designing Operators

### Requirement Analysis

1. Identify the **application** to manage and its lifecycle steps (deploy, scale, upgrade, backup, restore).
2. Determine what **domain knowledge** needs encoding (upgrade sequences, error handling, resource requirements).
3. Decide on the **custom resource schema** — what does the user need to configure?

### Custom or Third-Party Operator

- If an existing operator meets your needs, **install it** rather than building your own.
- If building custom, select a framework that matches your team's language and expertise.

### Use the Right Tool

- **Go teams**: Operator Framework / Kubebuilder
- **Python teams**: kopf
- **Rust teams**: kube-rs
- **Java teams**: Java Operator SDK

### Use the Right Programming Language

- Consider existing team skills, runtime requirements (e.g., need for binary compilation vs. scripting), and ecosystem support.

### Design Your Operator According to Your Needs

1. **Start small**: Implement the core reconciliation loop first, then add features.
2. **Test thoroughly**: Use chaos testing (Pod deletions, network partitions) to verify resilience.
3. **Observe everything**: Export metrics, logs, and health signals for observability.
4. **Plan for upgrades**: Design the operator and CRD schema to support future version transitions.

### References

- [Kubernetes Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [Operator Framework](https://operatorframework.io)
- [Kubebuilder](https://book.kubebuilder.io)
- [kopf operator framework](https://github.com/nolar/kopf)
- [CNCF Operator White Paper](https://github.com/cncf/tag-app-delivery/blob/163962c4b1cd70d085107fc579e3e04c2e14d59c/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## Emerging Patterns of the Future

### Operator Lifecycle Management (OLM)

- **OLM** (Operator Lifecycle Management) provides a standardized way to package, install, and upgrade operators.
- Manages operator dependencies, channels, and subscription-based installation.
- Part of the [Operator Framework](https://operatorframework.io).

### Policy-Aware Operators

- Operators that understand and enforce organizational policies (resource quotas, security policies, compliance requirements).
- Can automatically remediate policy violations or reject operations that violate policy.

### Conclusion

Operators encode domain-specific operational knowledge into software, enabling automated management of complex stateful applications on Kubernetes. By extending the Kubernetes API through custom resources and controllers, operators reduce manual imperative work, improve reliability, and empower teams to self-serve application infrastructure.

The key to a successful operator is **starting small**, **testing thoroughly**, and **encoding only the operational knowledge that provides real value**. As the CNCF White Paper concludes: _Operators provide a way to encapsulate the required activities, checks, and state management of an application — turning manual runbooks into autonomous, testable, upgradable software._

## What's Next

- [Read the CNCF Operator White Paper](https://github.com/cncf/tag-app-delivery/blob/163962c4b1cd70d085107fc579e3e04c2e14d59c/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)
- [Learn about Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [Discover operators on OperatorHub.io](https://operatorhub.io/)
- [Google Cloud best practices for building operators](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps)
