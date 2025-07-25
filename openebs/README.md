# OpenEBS

Source: <https://openebs.io/docs/>

## 1. Introduction

- OpenEBS turns any storage available to Kubernetes worker nodes into Local or Replicated Kubernetes Persistent Volumes. OpenEBS helps application and platform teams easily deploy Kubernetes stateful workloads that require fast and highly durable, reliable, and scalable _Container Native Storage_.
- OpenEBS manages the storage available on each of the Kuberenetes nodes and uses that storage to provide Local or Replicated Persistent Volumes to Stateful workloads.
  - **Local Volumes**:
    - OpenEBS can create persistent volumes or use sub-directories on Hostpaths or use locally attached storage or sparse files or over existing LVM or ZFS stack.
    - The local volumes are directly mounted into the Stateful Pod, without any added overhead from OpenEBS in the data path, decreasing latency.
    - OpenEBS provides additional tooling for local volumes for monitoring, backup/restore, disaster recovery, snapshots when backed by LVM or ZFS stack, capacity-based scheduling, and more.
  - **Replicated Volumes**:
    - OpenEBS Replicated Storage creates an NVMe target accessible over TCP, for each persistent volume.
    - The Stateful Pod writes the data to the NVME-TCP target that synchronously replicates the data to multiple nodes in the cluster. The OpenEBS engine itself is deployed as a pod and orchestrated by Kubernetes. When the node running the Stateful pod fails, the pod will be rescheduled to another node in the cluster and OpenEBS provides access to the data using the available data copies on other nodes.
    - OpenEBS Replicated Storage is developed with durability and performance as design goals. It efficiently manages the compute (hugepages and cores) and storage (NVME Drives) to provide fast block storage.

![](https://openebs.io/docs/assets/images/data-engines-comparision-c92dc7f1053b2ba59697c8d7769d3308.svg)
