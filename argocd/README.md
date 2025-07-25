# ArgoCD

Source:

- <https://argo-cd.readthedocs.io/en/stable/>
- <https://spacelift.io/blog/argocd>

Table of contents:

- [ArgoCD](#argocd)
  - [1. Overview](#1-overview)
  - [2. Architecture:](#2-architecture)
  - [3. Core concepts](#3-core-concepts)

## 1. Overview

- Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.
- Argo CD follows the **GitOps** pattern of using Git repositories as the source of truth for defining the desired application state. Kubernetes manifests can be specified in several ways:
  - kustomize applications
  - helm charts
  - jsonnet files
  - Plain directory of YAML/json manifests
  - Any custom config management tool configured as a config management plugin
- ArgoCD automates the deployment of the desired application states in the specified target environments. Application deployments can track updates to branches, tags, or be pinned to a specific version of manifests at a Git commit.

![](https://spacelift.io/_next/image?url=https%3A%2F%2Fspaceliftio.wpcomstaging.com%2Fwp-content%2Fuploads%2F2023%2F03%2Fhow-does-argo-cd-work.png&w=1920&q=75)

## 2. Architecture:

![](https://argo-cd.readthedocs.io/en/stable/assets/argocd_architecture.png)

- ArgoCD is implemented as a Kubernetes controller which continuously monitors running applications and compares the current, live state against the desired target state.
- A deployed application whose live state deviates from the target state is considered `OutofSync`.
- Any modifications made to the desired target state in the Git repo can be automatically applied and reflected in the specified target environments.
- Components:
  - API Server: A gRPC/REST server which exposes the API consumed by the Web UI, CLI, and CI/CD systems.
  - Repository Server: An internal service which maintains a local cache of the Git repository holding the application manifests. It is responsible for generating and returning the Kubernetes mainfests.
  - Application controller: a Kubernetes controller which continuously monitors running applications and compares the current, live state against the desired target state (as specified in the repo). It detects `OutOfSync` application state and optionally takes corrective action. It is responsible for invoking any user-defined hooks for lifecycle events.

## 3. Core concepts

- Application: A group of Kubernetes resources as defined by a manifest. This is a Custom Resource Definition (CRD).
- Application source type: Which Tool is used to build the application.
- Target state: The desired state of an application, as represented by files in a Git repository.
- Live state: The live state of that application. What pods etc are deployed.
- Sync status: Whether or not the live state matches the target state. Is the deployed application the same as Git says it should be?
- Sync: The process of making an application move to its target state. E.g. by applying changes to a Kubernetes cluster.
- Sync operation status: Whether or not a sync succeeded.
- Refresh: Compare the latest code in Git with the live state. Figure out what is different.
- Health: The health of the application, is it running correctly? Can it serve requests?
- Tool: A tool to create manifests from a directory of files. E.g. Kustomize. See Application Source Type.
- Configuration management tool.
- Configuration management plugin: A custom tool.

## 4. Best practices

- **Use ApplicationSets for dynamic app management**: Leverage ApplicationSets to automate the deployment of multiple similar apps (e.g., per tenant or per cluster) from templates, reducing boilerplate and manual updates.
- **Pin ArgoCD versions and CRDs**: Avoid auto-upgrading ArgoCD or its custom resource definitions; pin versions explicitly to prevent breaking changes or unexpected behaviors in production.
- **Use the app-of-apps pattern for hierarchical management**: Manage large-scale deployments using an "app of apps" model, where a root application defines and manages multiple child applicationns for better modularity.
- **Apply resource exclusions and ignore differences**: Configure resource exclusions or diff settings (e.g., ignore `status` fields or ephemeral annotations) to prevent false-positive drift detections.
- **Tag and label applications for automation and auditing**: Use consistent metadata (labels/annotations) on ArgoCD apps to enable automated filtering, reporting, or lifecycle management.
- **Run ArgoCD in a dedicated namespace or cluster**: Isolate ArgoCD to a specific namespace or cluster to simplify access control, avoid conflicts, and improve operational clarity.
