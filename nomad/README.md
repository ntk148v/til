# Nomad

## 1. Nomad vacabulary

### 1.1. Nomad cluster

![](https://learn.hashicorp.com/img/nomad/get-started/nomad-architecture-region.png)

- `agent`: process running in server or client mode. Agents are the basic building blocks of a Nomad cluster. `dev-agent` is for development and experimental use only.
- `server`: a Nomad agent running in server mode:
  - Manage all jobs and clients, run evaluations, create task allocations.
  - Servers replicate data between each other and perform leader election to ensure HA.
- `leader`: Nomad server that performs the builk of the cluster management.
  - Apply plans, deriving Vault tokens for the workloads, and maintaing the cluster state.
- `follower`: Non-leader Nomad servers.
- `client`: Nomad agent running in client mode.
  - Register with the servers, watch for any work to be assigned, and execute tasks.
  - Client <--mutlplexed connection--> server
  - Forward RPC calls.

### 1.2. Nomad objects

- `job`: define one or more task groups which contain >=1 tasks.
- `job specification` (jobspec): define the schema for Nomad jobs.
- `task group`: set of tasks that must be run together. A task group is the unit of scheduling, meaning the entire group must run on the same client node and cannot be split. A running instance of a task group is an `allocation`.
- `task driver`: represents the basic means of executing your tasks (Docker, QEMU, Java...).
- `task`: Tasks are executed by `task driver`, which allow Nomad to be flexible in the types of tasks it supports. Tasks specify their required task driver, configuration for the driver, constrains and resources required.
- `allocation`: a mapping between a task group in a job and a client node.
- `evaluation`: Allocations are created by the Nomad servers as part of scheduling decisions made during an `evalution`.

