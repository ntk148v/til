# Operators: Put Operational Knowledge into Software

Source: <https://coreos.com/blog/introducing-operators.html>

## What is Operator?

An Operator is an application-specific controller that extends the Kubernetes API to create, configure, and manage instance of complex stateful applications on behalf of a Kubernetes user. It builds upon the basic Kubernetes resource and controller concepts but includes domain or application-specific knowledge to automate common tasks.

## Stateless is Easy, Stateful is Hard

- Challenge is managing stateful applications, like database, cache and monitoring system (require application domain knowledge to correctly scale, upgrade, and reconfigure while protecting against data loss or unavalability).
- An Operator is software that encodes this domain knowledge and extends the Kubernetes API through the third party mechanism, enabling users to create, configure and manage applications.
- An Operator doesn't manage just a single instance of the application, but multiple instance across the cluster.

## How is an Operator Built?

- Operator build upon 2 central Kubernetes concepts: Resources and Controllers and adds a set of knowledge or configuration that allows the Operator to execute common application tasks. For example, when scaling an etcd cluster manually, a user has to perform a number of steps: create a DNS name for the new etcd member, launch the new etcd instance, and then use the etcd administrative tools (etcd member add) to tell the existing cluster about this new mebmber. Instead with the \*etcd Operator- a user can simply increase the etcd cluster size field by 1.

![backup-triggered-by-a-user](https://coreos.com/sites/default/files/inline-images/Operator-scale.png)

## How can you create an Operator?

- Operators, by their nature, are application-specific, so the hard work is going to be encoding all of the application operational domain knowledge into a reasonable configuration resource and control loop.
- Common patterns:
  - Operators should install as a single deployment.
  - Operators should create a new third party type when installed into Kubernetes. A user will create new application instance using this type.
  - Operators should leverage built-in Kubernetes primitives like Services and ReplicaSets when possible to leverage well-tested and well-understood code.
  - Operators should designed so application instances continue to run unaffected if the Operator is stopped or removed.
  - Operators should give users the ability to declare a desired version and orchestrate application upgrades based on the desired version.
  - Operators should be tested against a "Chaos Monkey" test suite that simulates potential failures of Pods, configuration, and networking.
