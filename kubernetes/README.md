# Kubernetes

- [Kubernetes](#kubernetes)
  - [1. Introduction](#1-introduction)
  - [2. Basic](#2-basic)
    - [2.1. Architecture](#21-architecture)
    - [2.2. Concepts](#22-concepts)
      - [2.2.1. Pods](#221-pods)
      - [2.2.2. Replication controller](#222-replication-controller)
      - [2.2.3. Replica Sets](#223-replica-sets)
      - [2.2.4. Deployment](#224-deployment)
      - [2.2.5. Service](#225-service)
      - [2.2.6. Label & Selector](#226-label--selector)
      - [2.2.7. Volume](#227-volume)
      - [2.2.8. Secrets](#228-secrets)
      - [2.2.9. Namespaces](#229-namespaces)
      - [2.2.10. Ingress](#2210-ingress)
      - [2.2.11. ConfigMap](#2211-configmap)


## 1. Introduction

- Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.
- Features:
  - Service discovery and load balancing
  - Storage orchestration
  - Automated rollouts and rollbacks
  - Automatic bin packing
  - Self-healing
  - Secret and configuration management
- Refs:
  - [100DaysOfKubernetes](https://devops.anaisurl.com/kubernetes)

## 2. Basic

### 2.1. Architecture

- Cluster: a set of work machines - called `nodes`, that run containerized applications.
  - Node hosts the Pods that are the components of the application workload.
  - Control plane manages the work nodes and the Pods in the cluster. In the production environments, the control plane usually run across multiple hosts.

![](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)

![overview](./imgs/kubernetes_overview.png)
  
- Check check:
  - **Kubernetes master/control plane** connect to **etd** via HTTP/HTTPS to store data and connect to **flannel** to access the container application.
  - **Kubernetes nodes** connect to the **Kubernetes master** via HTTP/HTTPS to get a command and report the status.
  - **Kubernetes nodes** use an overlay network (**flannel**) to make a connection of their container applications.

- Control plane components:
  - Features:
    - Authorization and authetication
    - RESTful API entry point
    - Container deployment scheduler to the Kubernetes nodes
    - Scaling and replicating the controller
    - Read and store the configuration
    - Command line interface
  - `kube-api-server`: exposes the Kubernetes API. The API is the front end for the Kubernetes control plane.
  - `etcd`: Consistent and highly-available key-value store used as Kubernetes's backing store for all cluster data.
    - Explore the Kubernetes configuration and status in etcd:

    ```bash
    curl -L "http://10.0.0.1:2379/v2/keys/registry"
    ```

  - `kube-scheduler`: watches for newly created Pods with no assigned node, and selects a node for them to run on.
  - `kube-controller-manager`: runs controller processes.
    - A controller is a control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired state.
    - Each controller is a separate process (logically).
    - Some types of these controller: Node controller, Job controller, Endpoints controller, Service account & token controllers.
  - `cloud-controller-manager:` embeds cloud-specific control logic, links cluster into cloud provider's API, and separates out the components that interact with that cloud platform from components that only interact with cluster.
- Node components:
  - Features: Maintaining running pods and providing the Kubernetes runtime environment.
  - `kubelet`: an agent that makes sure that containers are running a Pod.
  - `kube-proxy`: a network proxy, implementing part of the Kubernetes Service concept.
    - Maintain network rules on nodes. These network rules allow network communication to Pods from network sessions inside or outside of cluster.
    - Use the OS packet filtering layer if there is one and it's available (iptables...)
    - Forward traffic itself.
  - `Container runtime`: [containerd](https://containerd.io/docs/), [CRI-O](https://cri-o.io/#what-is-cri-o), and any other implementation of the [Kubernets CRI](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).
- Others:
  - overlay network (Flannel):
    - Read more [here](https://chunqi.li/2015/10/10/Flannel-for-Docker-Overlay-Network/)
    - Network communicate - multihost.
    - Flannel also uses etcd to configure the settings and store the status.

    ```bash
    curl -L "http://10.0.0.1:2379/v2/keys/coreos.com/network/config"
    ```

![](https://chunqi.li/images/flannel-01.png)

- Communications:
  - Node to control plane:
    - "hub-and-spoke" API pattern.
    - All API usage from nodes (or the pods they run) terminates at the API server.
    - Secure.
  - Control plane to node:
    - API server to kubelet:
      - Connections: fetching logs, attaching to running pods, providing the kubelet's port-fowarding.
      - HTTPS - unsafe, API server doesn't verify kubelet's serving certificate.
    - API server to nodes, pods, and services:
      - Plain HTTP connections.
    - SSH tunnels: to protect the control plane to nodes communication paths.

### 2.2. Concepts

#### 2.2.1. Pods

- The **Pod** is a group of 1 or more containers and the smallest deployable unit
  in Kubernetes. Pods are always co-located and co-scheduled and run in a
  shared context. Each pod is isolated by the following Linux namespaces:
  - PID namespace
  - Network namespace
  - Interprocess Commnunication (IPC) namespace
  - Unix Time Sharing (UTS) namespace
- **Pod State**

#### 2.2.2. Replication controller

- A term for API objects in Kubernetes that refers to pod replicas.
- To be able to control a set of pod's behaviors.
- Ensures that the pods, in a user-specified number, are running all the time. If some pods in the replication controller crash and terminate, the system will recreate pods with the original configurations on healthy nodes automactically, and keep a certain amount of processes continously running.
- This concept is outdated. Kubernetes official documentation recommends: A **Deployment** that configures a ReplicaSet is now the recommended way to set up replication.

#### 2.2.3. Replica Sets

- **Replica Set** is the next-generation Replication Controller. The only between them right now is the selector support.
- It supports a new selector that can do selection based on **filtering** according a **set of values**, whereas a RC only supports equality-based selector requirements.
  - e.g "environment" either "dev" or "qa".
  - not only based on equality, like the Replication Controller
    - e.g. "environment" == "dev"
- This **Replica Set**, rather than the Replication Controller, is used by the Deployment object.

#### 2.2.4. Deployment

- A deployment declaration allows you to do app **deployments** and **updates**.
- Deployments are intented to replace Replication Controllers.
- When using the deployment object, define the **state** of your application.
  - Kubernetes will then make sure the clusters matches your **desired** state.
- With a deployment object:
  - **Create** a deployment
  - **Update** a deployment
  - Do **rolling updates**: `rolling-update` command works with Replication Controllers, but won't work with Replica Set. This is because RS are meant to be used as the backend for Deployments.
  - **Roll back** to a previous version
  - **Pause/Resume** a deployment
- Example:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: helloworld-deployment
spec:
  replicas: 3
  template:
  metadata:
  labels:
  app: helloworld
  spec:
  containers:
    - name: k8s-demo
  image: wardviaene/k8s-demo
  ports:
    - containerPort: 3000
```

#### 2.2.5. Service

- **Pods** are very **dynamic**, they come and go on the Kubernetes cluster.
  - When using a **Replication Controller**, pods are **terminated** and created during scaling operations.
  - When using **Deployments**, when **updating** the image version, pods are **terminated** and new pods take the place of older posts.
- That's why Pods should never be accessed directly, but always through a **Service**.
- It is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service. A service is the **logical service** between the "mortal" pods  and other **services** or **end-users**.
- Use `kubectl expose` command.
- The set of Pods targeted by a **Service** is (usually) determined by Label Selector.
  - **ClusterIP**: Exposes the service on a cluster-internal IP. A virtual IP address only reachable from within the cluster (*default*).
  - **NodePort**: Exposes the service on each Node's IP at a static port. A porta that is the same on each node that is also reachable externally.
  - **LoadBalancer**: Exposes the service externally using a cloud provider's load balancer. A LoadBalancer created by the cloud provider that route external traffic to every node on the NodePort (ELB on AWS for example)
  - **ExternalName**: Maps the service to the contents of the externalName. This only works when **DNS add-on** is enabled.

![Services](./imgs/Services.png)

- Example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: helloworld-service
spec:
  ports:
    - port: 31001 # By default service can only run between ports 30000-32767 -> change by adding the --service-node-port-range= argument to the kube-apiserver
      nodePort: 31001
      targetPort: nodejs-port
  protocol: TCP
  selector:
  app: helloworld
  type: NodePort
```

#### 2.2.6. Label & Selector

- Labels are a set of key/value pairs, which are attached to object metadata.
  - Labels are like **tags** in AWS or other cloud providers, used to tag resources.
- Use **labels** to select, organize and group **objects**, for instance your pod, following an organizational structure:
  - Key: environment - Value: dev/staging/qa/prod
  - Key: department - Value: engineering/marketing

```yaml
metadata:
  name: nodehelloworld.example.com
  labels:
    environment: staging
```

- Unlike name and UIDs, labels don't provide identify a set of objects. Via a **label selector**, the client/user can identify a set of objects. The label selector is the core grouping primitive in Kubernetes.
- 2 types of selector: equality-based and set-based.
- You can also use labels to tag **nodes** -> use **label selectors** to let pods only run on specific nodes.
  - **Tag** the node.
  - Add a **nodeSelector** to your pod configuration.

```bash
kubectl label nodes node1 hardware=high-spec
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nodehelloworld.example.com
  labels:
    app: helloworld
spec:
  containers:
    - name: k8s-demo
      image: wardviaene/k8s-demo
      ports:
        - containerPort: 3000
  nodeSelector:
  hardware: high-spec
```

#### 2.2.7. Volume

- Volume lives with a pod across container restarts.
- It supports the following different types of network disks:
  - emptyDir
  - hostPath
  - nfs
  - iscsi
  - flocker
  - glusterfs
  - rbd
  - gitRepo
  - awsElasticBlockStore
  - gcePersistentDisk
  - secret
  - downwardAPI

#### 2.2.8. Secrets

- Secrets provides a way in Kubernetes to distribute **sensitive data** to the pods.
- There are still other ways container  can get its secrets: using an external vault services.
- Secrets can be used:
  - As environment variables.
  - As a file in a pod (via volumes).
  - External image to pull secrets.
- Generate  secrets:
  - Using files.

```bash
echo -n "root" > ./username.txt
echo -n "password" > ./password.txt
kubectl create secret generic db-user-pass --from-file=./username.txt —from-file=./password.txt secret "db-user-pass" created
# SSH key
kubectl create secret generic ssl-certificate --from-file=ssh-privatekey=~/.ssh/id_rsa --ssl-cert-=ssl-cert=mysslcert.crt
```

  - Using yaml definitions.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  password: cm9vdA== # echo -n 'root' | base64
  username: cGFzc3dvcmQ= # echo -n "password" | base64
```

```bash
kubectl create -f secrets-db-secret.yml
```

#### 2.2.9. Namespaces

- The name of a resource is a unique identifier with a namespace in the
  Kubernetes cluster. Using a Kubernetes namepsace could isolate namespaces
  for different environments in the same cluster.
- Pods, services, replication controllers (replica sets) are contained in a
  certain namespace. Some resources, such as nodes and PVs, do not belong to
  any namespace.

#### 2.2.10. Ingress

- Typically, services and pods have IPs only routable by the cluster network.

  ```
    internet
      |
  --------
  [ Services ]
  ```

- An Ingress is a collection of rules that allow inbound connections to reach
  the cluster services.

  ```
    internet
      |
  [ Ingress ]
  ---|---|---
  [ Services ]
  ```

- It can be configured to give services externally-reachable URLs, load
  balance traffic, terminate SSL... User request ingress by POSTing the
  Ingress resource to the API server.
- Read [more](https://medium.com/@cashisclay/kubernetes-ingress-82aa960f658e).

#### 2.2.11. ConfigMap
