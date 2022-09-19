# Helm vs Operator

Source: <https://www.reddit.com/r/kubernetes/comments/r1dj6i/what_are_the_differences_between_helm_and/>

The manual method of creating a YAML files for each deployment or configuration change is not a scalable option for most production environments. Helm Charts and Kubernetes Operators are two tools that aim to solve this problem.

## 1. What is Helm?

- Helm is a tool that enables users to manage Kubernetes applications. It allows users to package and share Kubernetes appications, facilitating easy deployment, update, and maintainance of K8s applications.
- The basic idea of Helm is to enable  reusability of Kubernetes YAMl artifacts through templatization.
- Charts are the packaging format used by Helm. A Helm chart contains configuration files and template files that define an application along with the correspoding Kubernetes resources.
- Helm project solves one of the key problems that enterprises face - creating custom YAMLs for deploying the same application workload with different settings, or deploying it in different environments (dev/test/prod).

## 2. What is Operator?

- Kubernetes operator is also a method sed to package, deploy and manage Kubernetes applications using the Kubernetes API and kubectl tooling.
- An operator is a custom controller that utilizes custom resources to manage applications. The custom resource (CR) is an API extension mechanism of K8s. It consists of all the configurations and settings provided by the user. The custom operator will take the custom resource and match the current state of the application to the desired state of the CR using the Kubernetes API.
- Operators can be implemented using any programming language and runtime supported by Kubernetes (client libraries).
- Operators can perform almost any kind of action.

## 3. Day-1 vs. Day-2 operations

- Helm's primary focus is on the day-1 operation of deploying Kubernetes artifacts in a cluster -> provide a simple application packaging, deployment, and management experience.
- Helm's ability to act as the package manager for Kubernetes.
- Operator is primarily focused on addressing day-2 management tasks of stateful/complex workfloads.
- Operator can also be used to automate application tasks beyond what is provided by default with Kubernetes to include application-specific automation to the Kubernetes cluster.
- Operator acts as the Kubernetes controller, they can manage the state of the applications and automatically carry out management tasks to preserve the application state.
- Best choice to manage applications when dealing with mature and complex Kubernetes clusters.

## 4. When to use Helm and Operators?

- Helm will be the better solution if you just want to install an application.
- Use Helm if you are starting up with Kubernetes and need to manage a simple application life cycle (install, update, remove).
- Use Helm to package and deploy if there are no special or complex configuration requirements. Go with Operators if there are Complex configurations.
- Operators provide a better solution when dealing with mature clusters as they can be deployed later but still manage some application configurations.
- Go with Operators if you need to automate mundane application-related tasks.
