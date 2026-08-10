# Understanding Kubernetes Multi-Tenancy

Source: <https://www.vcluster.com/blog/understanding-kubernetes-multi-tenancy-models-challenges-and-solutions>

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3c7500fc35e2b60653_67e5fd9a6ac740a1972019a2_007.png)

## 1. Kubernetes as a Shared System

To understand multi-tenancy, we must first understand how Kubernetes processes a request.

- When a user runs `kubectl apply` to create a Deployment, the API Server takes control.
- It validates the request, runs authentication and authorization checks, and commits the Deployment manifest into etcd.
- The Deployment controller inside the `kube-controller-manager` picks up the change, creates a corresponding ReplicaSet, and ensures the desired number of pods exist.
- The ReplicaSet controller watches for changes, spawns pods accordingly, and registers them in etcd.
- The kube-scheduler steps in, scanning for unscheduled pods. It evaluates available nodes, selects the best fit, and assigns the pod.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3c7500fc35e2b60658_67e5fe0b7111e48bbcdb9270_108.svg)

- No workloads are running; only metadata exists. The real action begins when the kubelet, running on each worker node, detects a new pod scheduled to its node. It pulls the pod specification from the API Server, preps the runtime, and finally launches the containers.

At no point does Kubernetes distinguish between teams or users. Every request passes through the same API server, every resource lands in the same etcd, and every kubelet treats pods the same way.

The reason is Kubernetes is _a shared system_.

In a multi-tenant cluster, the challenge of this shared infrastructure is that every team's workloads flow through the same control plane.

## 2. Introducing Multi-Tenancy in Kubernetes

One approach would be hardcoding tenancy into the API itself, defining scoped endpoints like `/api/team-a` and `/api/team-b`, where each team only sees their resources. Kubernetes achieves this dynamically with Namespaces and RBAC (Role-Based Access Control).

- Namespaces create logical boundaries at the API level. When a user in Team A runs `kubectl get pods`, they only see their namespace's pods.
- RBAC defines who can access what.
- ResourceQuotas prevent noisy neighbors from over-consuming shared infrastructure
- LimitRanges enfore per-tenant resource constraints.
- NetworkPolicies segment traffic.
- Pod Security Admission restricts unsafe workloads.

But even with all that, Namespaces doesn't isolate workloads. They are just a control mechanism for permissions and API scoping.

## 3. Building True multi-tenant platfor

When running a multi-tenant Kubernetes platform, you need all these components working together. You need a framework that expresses tenancy as a single specification like Capsule. Instead of manually configuring quotas, roles, and network policies for every team, Capsule lets you define tenancy in one place.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3e7500fc35e2b6069f_67e5fe9e52fe6f6d263e6b49_702.svg)

However, namespaces have limitations. Some objects like PersistentVolumes, nodes, Custom Resource Definitions (CRDs), even namespaces themselves aren't bound to a single namespace.

How do you scope them to a specific team? RBAC grants access, but it doesn't partition resources dynamically.

The solution is API proxies.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3d7500fc35e2b60661_67e5fec63fd619de2c3f9ee5_807.svg)

Tools like Capsule Proxy and KCP sit in front of the real API server as a proxy layer, impersonate users, and filter responses. The control plane remains shared, but tenants only see their own resources.

Even this approach doesn't solve the CRD Isolation problem. CRDs are tricky; they live in etcd, and etcd is shared. You can't install two versions of the same CRD in a single cluster.

Similarly, you can't create CRD-level isolation without splitting etcd.

Then, there's the problem of node isolation. You can restrict CPU and memory and enforce network policies, but you can't isolate I/O. If a database runs on a node with noisy neighbors, they compete for disk throughput. You can't isolate network bandwidth at the node level, either.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3e7500fc35e2b60675_67e5ff0866d2e2b02f4c6d95_1106.svg)

If isolating the database is too complex, isolate the control plane instead.

Instead of running a single control plane for every team, give each tenant a dedicated API server and an isolated etcd instance.

Teams can run different CRD versions without conflicts, workloads are decoupled, and tenancy becomes a first-class concept. The challenge isn't in the idea—it's in the execution.

## 2. Achieving Hard isolation: Control Plane Strategies

There are three major approaches to hard separation at the control plane level, each with its own trade-offs.

- Dedicated clusters for each team. Every team gets its own cluster, fully isolated, with separate control and data planes. However, managing these clusters at scale is a different challenge. You need a way to orchestrate deployments across them, distribute workloads efficiently, and interconnect networking, storage, and I/O.
  - Tools like KubeAdmiral, Karmada, Sveltos, Kubesphere, and Kubeslice come in here.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3e7500fc35e2b6067e_67e5ff77be93b234fcabfdb5_1407.svg)

- Nested control plane inside a single manager cluster. Instead of running separate clusters, you package the entire Kubernetes control plane as a pod inside an existing cluster.
  - Like managed Kubernetes services on AWS, GKE, or AKS, you attach worker nodes directly to the control plane.
  - If a node breaks, it's the tenant's problem, as they own the infrastructure they attach.

![](https://cdn.prod.website-files.com/68ad5281556da93bd7179b0e/68b79f3f7500fc35e2b606db_67e5ff9727c1f7766c1f376c_1702.svg)

- A single-cluster control planes without external nodes. Instead of spinning up control plane as pods in an external management cluster, everything stays inside one cluster. The control planes don't have their own nodes; instead, they synchronize resources back to the main cluster.

## 3. Evaluating Multi-Tenancy Approaches

Multi-tenancy in Kubernetes isn't just about picking a tool but understanding the trade-offs. Every approach has its limits, and the landscape isn't balanced.

- Dedicated clusters are the cleanest solution, primarily when operating across multiple clouds or regions. Full isolation, no shared resources, no tenant conflicts. But not every team needs that level of separation, and managing fleets of clusters adds complexity.
- Control plane as a service works well for managed Kubernetes providers. Spinning up dedicated control planes per tenant makes sense if you're offering Kubernetes as a service. But unless that's your business model, the use case is limited.
