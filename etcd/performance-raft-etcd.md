# Understanding performance aspects of etcd and raft

Source: <https://www.slideshare.net/slideshow/understanding-performance-aspects-of-etcd-and-raft/76576115>

## 1. Background of Raft and state machine replication (SMR) techniques

Assume you have a Key Value Store (KVS) -> want it to work in a HA and consistent manner.

- Method 1: use mainframe (hardware).
- Method 2: replicate the KVS -> achieve with software.

Our goal of availability:

- Even f node fail at once, the entire system must survive if enough node are alive.
- The failure includes temporal failure (e.g. power outage, network disconnection) and permanent failure.

Out goal of consistency:

- Linearizability: replicated systems behaves as a non replicated system. e.g. Clients must not see stale state of the servers.

SMR: replicate a service as a state machine.

- Model KVS as a deterministic state machine.
- Wrap the state machine with a SMR framework.
- Every inputs that change the state must be supplied by the framework.
- Replicate the framework. The consensus module decides which inputs should be supplied and an order of the inputs.
- If the state machines are deterministic, every state machine should be identical.
  - If one server goes down, others can be an alternative.
- The inputs must be persisted on a non volatile media.

When should the consensus module issue append and apply?

- If a quorum of nodes can agree, the module can issue apply.
- If a cluster has 2f + 1 nodes, it can tolerate f faults.

Raft is a methodology for SMR based systems.
