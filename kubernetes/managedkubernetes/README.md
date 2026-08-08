# Managed Kubernetes or Kubernetes-as-a-service

## 1. Kamaji

### 1.1. etcd performance

Kubernetes setups can be staggering in size for multiple reasons: it can be thousands of Kubernetes clusters or thousands of Kubernetes worker nodes. When these conditions are `AND`, technology must be on the rescue.

Kubernetes with many nodes requires fine-tuning and optimisation: from metrics retrieval to etcd performance. One of the most useful and powerful settings in the Kubernetes API Server is the `--etcd-server-overrides` flag.

It allows overriding the etcd endpoints for specific Kubernetes resources: imagine it as a sort of built-in sharding to distribute the retrieval and storing of heavy group objects. In the context of huge clusters, each Kubelet is sending a `Lease` object update, which is a write operation (thus, with thousands of nodes, you have thousands of writes every 10 seconds): this interval can be customised (`--node-lease-renew-interval`), although with some considerations in the velocity of detecting down nodes.

The two heaviest resources in a Kubernetes cluster made of thousands of nodes are Leases and Events: the latter due to the high amount of Pods, strictly related to the number of worker nodes, where a rollout of a fleet of Pods can put pressure on the API Server, eventually on etcd.

One of the key suggestions to handle these scenarios is to have separate etcd clusters for such objects, and keep the main etcd storage cluster just for the "critical" state by reducing the storage pressure.

Kamaji has been designed to make Kubernetes at scale effortless, such as hosting thousands of Kubernetes clusters. By working together, we've enhanced the project to manage Kubernetes clusters running thousands of worker nodes.

```yaml
apiVersion: kamaji.clastix.io/v1alpha1
kind: TenantControlPlane
metadata:
  name: my-cluster
  namespace: default
spec:
  dataStore: etcd-primary-kamaji-etcd
  dataStoreOverrides:
    - resource: "/events" # Store events in the secondary ETCD
      dataStore: etcd-secondary-kamaji-etcd
  controlPlane:
    deployment:
      replicas: 2
    service:
      serviceType: LoadBalancer
  kubernetes:
    version: "v1.35.0"
  addons:
    coreDNS: {}
    kubeProxy: {}
    konnectivity: {}
```

The basic idea of Kamaji is hosting Control Planes as Pods in a management cluster, and treating cluster components as Custom Resource Definitions to leverage several methodologies: GitOps, Cluster API, and the Operator pattern.

- Don't run `etcd` on a node with other roles. A general rule of thumb is to never have the worker role on the same node as etcd. However many environments have etcd and controlplane roles on the same node and run just fine. If this is the case for your environment then you should consider separating etcd and controlplane nodes.

- If you have separated `etcd` and the controlplane node and are still having issues, you can mount a separate volume for `etcd` so that read write operations for everything else on the node do not impact `etcd` performance. This is mostly applicable to Cloud hosted nodes since each volume mounted has its own allocated set of resources.

- If you are on a dedicated server and would like to separate `etcd` read write operations from the rest of the server, you should install a new storage device for `etcd` mounts.

- Always use SSDs for your `etcd` nodes, whether it is metal, virtual, or in the Cloud.

- Set the priority of the `etcd` container so that it is higher than other processes but not too high that it overwhelms the server.

  ionice -c2 -n0 -p `pgrep -x etcd`

> [!NOTE]
> or sharding proxy for etcd: <https://github.com/Azure/metaetcd>

## 2. Kubernetes multi-tenancy

<https://www.vcluster.com/blog/understanding-kubernetes-multi-tenancy-models-challenges-and-solutions>
