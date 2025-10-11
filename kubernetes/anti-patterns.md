# Kubernetes anti-patterns

Source:
- <https://codefresh.io/blog/kubernetes-antipatterns-1/>

Table of contents:

- [Kubernetes anti-patterns](#kubernetes-anti-patterns)
  - [1. Anti-pattern 1 – Using containers with the latest tag in Kubernetes deployments](#1-anti-pattern-1--using-containers-with-the-latest-tag-in-kubernetes-deployments)
  - [2. Anti-pattern 2 – Baking the configuration inside container images](#2-anti-pattern-2--baking-the-configuration-inside-container-images)
  - [3. Anti-pattern 3 – Coupling applications with Kubernetes features/services for no reason](#3-anti-pattern-3--coupling-applications-with-kubernetes-featuresservices-for-no-reason)
  - [4. Anti-pattern 4 – Mixing application deployment with infrastructure deployment](#4-anti-pattern-4--mixing-application-deployment-with-infrastructure-deployment)
  - [5. Anti-pattern 5 – Performing ad-hoc deployments with kubectl edit/patch by hand](#5-anti-pattern-5--performing-ad-hoc-deployments-with-kubectl-editpatch-by-hand)
  - [6. Anti-pattern 6 – Misunderstanding Kubernetes network concepts](#6-anti-pattern-6--misunderstanding-kubernetes-network-concepts)
  - [7. Anti-pattern 7 - Using permanent staging environments instead of dynamic environments](#7-anti-pattern-7---using-permanent-staging-environments-instead-of-dynamic-environments)
  - [8. Anti-pattern 8 - Mixing production and non-production clusters](#8-anti-pattern-8---mixing-production-and-non-production-clusters)
  - [9. Anti-pattern 9 - Deploying without memory and cpu limits](#9-anti-pattern-9---deploying-without-memory-and-cpu-limits)
  - [10. Anti-pattern 10 - Misusing Health probes](#10-anti-pattern-10---misusing-health-probes)
  - [11. Anti-pattern 11 – Not using the Helm package manager](#11-anti-pattern-11--not-using-the-helm-package-manager)
  - [12. Anti-pattern 12 – Not having deployment metrics](#12-anti-pattern-12--not-having-deployment-metrics)
  - [13. Anti-pattern 13 - Not having a strategy for secrets](#13-anti-pattern-13---not-having-a-strategy-for-secrets)
  - [14. Anti-pattern 14 – Attempting to solve all problems with Kubernetes](#14-anti-pattern-14--attempting-to-solve-all-problems-with-kubernetes)
 

## 1. Anti-pattern 1 – Using containers with the latest tag in Kubernetes deployments

No surprise, instead of 'latest' use:
- Tags with Git hashes.
- Tags with application version.
- Tags that signify a consecutive number such as a build nimber of build date/time.

## 2. Anti-pattern 2 – Baking the configuration inside container images

Create “generic” container images that know nothing about the environment they are running on. For configuration, you can use any external method such as Kubernetes configmaps, Hashicorp Consul, Apache Zookeeper, etc.

## 3. Anti-pattern 3 – Coupling applications with Kubernetes features/services for no reason

Some classic examples are application that:
- expect a certain volume configuration for data sharing with other pods
- expect a certain naming of services/DNS that is set up by Kubernetes networking or assume the presence of specific open ports
- get information from Kubernetes labels and annotations
- query their own pod for information (e.g to see what IP address they have)
- need an init or sidecar container in order to function properly even in local workstations
- call other Kubernetes services directly (e.g. using the vault API to get secrets from a Vault installation that is assumed to also be present on the cluster)
- read data from a local kube config
- use directly the Kubernetes API from within the application

If your application is correctly designed you shouldn’t need Kubernetes for running integration tests locally. Just launch the application on its own (with Docker or Docker-compose) and hit it directly with the tests.

## 4. Anti-pattern 4 – Mixing application deployment with infrastructure deployment

The correct solution is of course to split deployment or infrastructure on their own pipelines. The infrastructure pipeline will be triggered less often than the application one, making application deployments faster (and cutting down on lead time).

![](https://codefresh.io/wp-content/uploads/2023/07/Flows-12-2.png)

## 5. Anti-pattern 5 – Performing ad-hoc deployments with kubectl edit/patch by hand

Kubectl should never be used for deployments by hand. All deployments should be taken care of by the deployment platform and ideally should also be recorded in Git following the GitOps paradigm.

If all your deployments happen via a Git commit:
- You have a complete history of what happened in your cluster in the form of Git commit history
- You know exactly what is contained on each cluster at any point in time and how environments differ among themselves
- You can easily recreate or clone an environment from scratch by reading the Git configuration.
- Rolling back configuration is trivial as you can simply point your cluster to a previous commit.

## 6. Anti-pattern 6 – Misunderstanding Kubernetes network concepts

Gone are the days, where a single load balancer was everything you needed for your application. Kubernetes introduces its own networking model and it is your duty to learn and understand the major concepts. At the very least you should be familiar with load balancers, clusterIPs, nodeports and ingress (and how they differ).

Understanding the different service options is one of the most confusing aspects for people starting with Kubernetes networking. ClusterIP services are internal to the cluster, NodePorts are both internal and external and Load balancers are external to the cluster, so make sure that you understand the implications of each service type.

![](https://codefresh.io/wp-content/uploads/2023/07/Flows-02-1.png)

And this is only for getting traffic inside your cluster. You should also pay attention to how traffic works within the cluster itself. DNS, security certificates, virtual services are all aspects that should be handled in detail for a production Kubernetes cluster.

## 7. Anti-pattern 7 - Using permanent staging environments instead of dynamic environments

One of the most common patterns is having at least 3 environments (QA/staging/production) and depending on the size of the company you might have more. The most important of these environments is the “integration” one (or whatever the company calls it) that gathers all features of developers after they are merged to the mainline branch.

![](https://codefresh.io/wp-content/uploads/2023/07/Flows-03-1.png)

If you use a single environment for integration then when multiple developers merge features and something breaks, it is not immediately which of the feature(s) caused the problem.

The solution of course, is to abandon the manual maintenance of static environments and move to dynamic environments that are created and destroyed on demand. With Kubernetes this is very easy to accomplish:

![](https://codefresh.io/wp-content/uploads/2023/07/Flows-06-1.png)

## 8. Anti-pattern 8 - Mixing production and non-production clusters

Mixing production and non-production is an obvious bad idea for resource starvation. You don’t want a rogue development version to overstep on the resource of the production version of something.

Note that depending on the size of your company you might have more clusters than two such as:

- Production
- Shadow/clone of production but with less resources
- Developer clusters for feature testing (see the previous section)
- Specialized cluster for load testing/security (see previous section)
- Cluster for internal tools

## 9. Anti-pattern 9 - Deploying without memory and cpu limits

## 10. Anti-pattern 10 - Misusing Health probes

In summary:

- Startup probe => Checks the initial boot of your applications. It runs only once
- Readiness probe => Checks if your application can respond to traffic. Runs all the time. If it fails Kubernetes will stop routing traffic to your app (and will try later)
- Liveness probe => Checks if your application is in a proper working state. Runs all the time. If it fails Kubernetes will assume that your app is stuck and will restart it.

## 11. Anti-pattern 11 – Not using the Helm package manager

## 12. Anti-pattern 12 – Not having deployment metrics

By "metrics" we actually mean the whole trilogy of:
- logging – to examine the events and details of requests (usually post-incident)
- tracing – to dive deep in the journey of a single request (usually post-incident)
- metrics – to detect an incident (or even better to predict it)


## 13. Anti-pattern 13 - Not having a strategy for secrets

Secrets should be passed during runtime to containers. There are many approaches to secret handling from simple storage to git (in an encrypted form) to a full secret solution like Hashicorp vault.

Some common pitfalls here are:
- Using multiple ways for secret handling
- Confusing runtime secrets with build secrets
- Using complex secret injection mechanisms that make local development and testing difficult or impossible.

Secret management should be handled in a flexible way that allows for easy testing and local deployment of your app. This means that the application should not really care about the source of the secrets and should only focus on their usage.

![](https://codefresh.io/wp-content/uploads/2023/07/Flows-01-1.png)

## 14. Anti-pattern 14 – Attempting to solve all problems with Kubernetes

As with all technologies before it, Kubernetes is a specific solution that solves a specific set of problems. If you already have those problems then you will find that adopting Kubernetes greatly simplifies your workflow and gives you access to a clustering solution that is well designed and maintained.

It is important however to understand the benefits and drawbacks of adopting Kubernetes. At least in the beginning it is much easier to use Kubernetes for stateless services that will exploit the elasticity and scalability of the cluster.

Even though technically Kubernetes supports stateful services as well, it is best to run such services outside the cluster as you begin your migration journey. It is ok if you keep databases, caching solutions, artifact repositories, and even Docker registries outside the cluster (either in Virtual machines or cloud-based services).
