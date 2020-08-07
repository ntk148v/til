# Overview

- [Overview](#overview)
  - [1. What is OKD?](#1-what-is-okd)
  - [2. Features](#2-features)
  - [3. Lifecycle](#3-lifecycle)

## 1. What is OKD?

OKD is a **distribution of Kubernetes** optimized for continuous application development and multi-tenant deployment. OKD adds **developer and operations-centric** tools on top of Kubernetes to enable rapid application development, easy deployment and scaling, and long-term lifecycle maintenance for small and large teams. OKD is the upstream Kubernetes distribution embedded in Red Hat OpenShift.

```
Kubernetes <-----> Linux Kernel
OKD        <-----> Fedora
OpenShift  <-----> RHOS
```

## 2. Features

- Hybrid cloud deployments.
- Custom operating system - Fedora CoreOS (FCOS):
  - CoreOS + [Red Hat Atomic Host](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/installation_and_configuration_guide/introduction_to_atomic_host)
  - Includes: Ignition (firstboot system configuratin) + CRI-O (Kubernetes native container runtime) + Kubelet (Kuberenetes node agent)

- Simplified installation and update process.
- Operators, Operator Lifecycle Manager and the OperatorHub.
- Include improvements in software defined networking (SDN), authentication, log aggregation, monitoring, and routing.

## 3. Lifecycle

The following figure illustrates the basic OKD lifecycle:

- Creating an OKD cluster
- Managing the cluster
- Developing and deploying applications
- Scaling up applications
