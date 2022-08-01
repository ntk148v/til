# Kubernetes

- [Kubernetes](#kubernetes)
  - [1. Introduction](#1-introduction)
  - [2. Basic](#2-basic)
    - [2.1. Architecture](#21-architecture)
    - [2.2. Kubernetes API](#22-kubernetes-api)
    - [2.3. How Kubernetes runs an application](#23-how-kubernetes-runs-an-application)
    - [2.4. Concepts](#24-concepts)
      - [2.4.1. Pods](#241-pods)
      - [2.4.2. Replication controller](#242-replication-controller)
      - [2.4.3. Replica Sets](#243-replica-sets)
      - [2.4.4. Deployment](#244-deployment)
      - [2.4.5. Service](#245-service)
      - [2.4.6. Label & Selector](#246-label--selector)
      - [2.4.7. Persistent Volume](#247-persistent-volume)
      - [2.4.8. Secrets](#248-secrets)
      - [2.4.9. Namespaces](#249-namespaces)
      - [2.4.10. Ingress](#2410-ingress)
      - [2.4.11. ConfigMap](#2411-configmap)


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
  - [Kubernetes In Action 2nd Edition](https://www.manning.com/books/kubernetes-in-action-second-edition): This is a really good book for beginner. Access the MEAP [here](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition), I take a lot of pictures from this site.

## 2. Basic

### 2.1. Architecture

- Cluster: a set of work machines - called `nodes`, that run containerized applications.
  - Workload Plane: Node hosts the Pods that are the components of the application workload.
  - Control plane: manages the work nodes and the Pods in the cluster. In the production environments, the control plane usually run across multiple hosts.

![](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/1.11.png)

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

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/1.12.png)

- Node components:
  - Features: Maintaining running pods and providing the Kubernetes runtime environment.
  - `kubelet`: an agent that makes sure that containers are running a Pod.
  - `kube-proxy`: a network proxy, implementing part of the Kubernetes Service concept.
    - Maintain network rules on nodes. These network rules allow network communication to Pods from network sessions inside or outside of cluster.
    - Use the OS packet filtering layer if there is one and it's available (iptables...)
    - Forward traffic itself.
  - `Container runtime`: [containerd](https://containerd.io/docs/), [CRI-O](https://cri-o.io/#what-is-cri-o), and any other implementation of the [Kubernets CRI](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/1.13.png)

- Others:
  - Add-on components
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
  
### 2.2. Kubernetes API

- Both user and Kubernetes components interact with the cluster by manipulating objects through the Kubenetes APIs.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/4.1.png)

- HTTP-based RESTFul API where the state is represented by **resources** on which you perform CRUD operations.
- Each **resource** is assigned a URI that uniquely identifies.
- E.g. **deployment** resource. The collection of all deployments in the cluster is a REST resource exposed at `/api/v1/deployments`.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/4.2.png)

- An **object** can therefore be exposed through more than one resources.
- Objects are represented in structured text form (JSON/YAML).

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/4.3.png)

- Controllers manage the objects. Each controller is usually only responsible for one object type. For example, the Deployment controller manages Deployment objects.
  - The task of a controller is to read the desired object state from the the object's Spec section
  - Perform the actions required to achieve this state
  - Report back the actual state of the object by writing to its Status section

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/4.4.png)

- As controllers perform their task of reconciling the actual state of an object with the desired state, as specified in the object’s spec field, they generate events to reveal what they have done. Two types of events exist: Nomarl and Warning.
  - Events are represented by Event objects.
  - Each Event object is deleted one hour after its creation to reduce the burden on etcd.

```bash
# Listing events
kubectl get ev
# -o wide: display additional information
kubectl get ev -o wide
# Filter only Warning events
kubectl get ev --field-selector type=Warning
```

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/4.7.png)

### 2.3. How Kubernetes runs an application

- Define application: Everything in Kubernetes is represented by an object. These objects are usually defined in one or more manifest files in either YAML or JSON format.
- Actions:
  - Submit the application manifest to Kubernetes API. API Server writes the objects defined in the manifest to etd.
  - Controller notices the newly created objects and creates several new objects - one for each application instance.
  - Scheduler assigns a node to each instance.
  - Kubelet notices that an instance is assigned to the Kubelet's node. It runs the application instance via the Container runtime.
  - Kube-proxy notices that the application instances are ready to accept connections from clients and configures a LB for them.
  - Kublets and the Controllers monitor the system and keep the applications running.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/1.14.png)

### 2.4. Concepts

#### 2.4.1. Pods

- The **Pod** is a group of 1 or more containers and the smallest deployable unit
  in Kubernetes. Pods are always co-located and co-scheduled and run in a
  shared context. Each pod is isolated by the following Linux namespaces:
  - PID namespace
  - Network namespace
  - Interprocess Commnunication (IPC) namespace
  - Unix Time Sharing (UTS) namespace
- **Pod State**:
  - Pods have a status field (`kubectl get pods`).
  - Valid statuses:
    - **running**: pods has been bound to a node + all containers have been created +_ at least one container is still running/starting/restarting.
    - **pending**: pods has been accepted but is not running.
    - **succeeded**: all containers within this pod have been terminated successfully and will not be restarted.
    - **failed**: all containers within this pod have been Terminated + at least one container returned a failure code.
    - **unknown**: network error might have been occurred.
  - Check using `kubectl describe pod <podname>`.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/6.1.png)

- **Pod conditions**:

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/6.2.png)

- **Pod Lifecycle**:

![](imgs/pod-lifecycle.png)

#### 2.4.2. Replication controller

- A term for API objects in Kubernetes that refers to pod replicas.
- To be able to control a set of pod's behaviors.
- Ensures that the pods, in a user-specified number, are running all the time. If some pods in the replication controller crash and terminate, the system will recreate pods with the original configurations on healthy nodes automactically, and keep a certain amount of processes continously running.
- This concept is outdated. Kubernetes official documentation recommends: A **Deployment** that configures a ReplicaSet is now the recommended way to set up replication.

#### 2.4.3. Replica Sets

- **Replica Set** is the next-generation Replication Controller. The only between them right now is the selector support.
- It supports a new selector that can do selection based on **filtering** according a **set of values**, whereas a RC only supports equality-based selector requirements.
  - e.g "environment" either "dev" or "qa".
  - not only based on equality, like the Replication Controller
    - e.g. "environment" == "dev"
- This **Replica Set**, rather than the Replication Controller, is used by the Deployment object.

#### 2.4.4. Deployment

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

#### 2.4.5. Service

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

#### 2.4.6. Label & Selector

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

#### 2.4.7. Persistent Volume

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
- A **PersistentVolume** object represents a storage volume available in the clsuter that can be used to persist application data.
- A pod transitively references a persistent volume and its underlying storage by referring to a **PersistentVolumeClaim** object that references the **PersistentVolume** object, which then references the underlying storage. This allows the ownership of the persistent volume to be decoupled from the lifecyle of the pod.
  - A **PersistentVolumeClaim** represents a user's claim on the persistent volume.

  ![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/8.4.png)

- Benefits of using persistent volumes and claims:
  - The infrastructure-specific details are now decoupled from the application represents by the pod.
- Example:
  - Create PersistentVolume:

  ```yaml
  apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: mongodb-pv # The name of persistent volume
  spec:
    capacity: # The storage capacity of this volume
      storage: 1Gi
    accessModes: # Whether a single node or many nodes can access this volume in read/write or read-only mode.
      - ReadWriteOnce
      - ReadOnlyMany
    gcePersistentDisk: #This persistent volume uses the GCE Persistent Disk
      pdName: mongodb
      fsType: ext4
    # hostPath: # Local directory on the host node
    #   path: /tmp/mongodb
  ```

  ```bash
  kubectl get pv
  ```

  - Create PersistentVolumeClaim:

  ```yaml
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: mongodb-pvc # This name of this claim
  spec:
    resources:
      requests: # The volume must provide at least 1GiB of storage space
        storage: 1Gi
    accessModes: # The volume must support mounting by a single node for both reading and writing
      - ReadWriteOnce
    storageClassName: "" # Empty to disable dynamic provisioning
  ```

  ```bash
  kubectl get pvc
  ```
  
  - Use a persistent volume in a pod

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: mongodb
  spec:
    volumes:
      - name: mongodb-data # The internal name of the volume
        persistentVolumeClaim: # The volume points to a PersistentVolumeClaim named mongodb-pvc
          claimName: mongodb-pvc
    containers:
      - image: mongo
        name: mongodb
        volumeMounts: # The volume is mounted
          - name: mongodb-data
            mountPath: /data/db
  ```

- The lifecycle of manually provisioned persistent volumes and claims:

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/8.7.png)

- Dynamic provisioning of persistent volumes: instead of provisioning persistent volumes in advance (and manually), the cluster admin deploys a persistent volume provisioner to automate the just-in-time provisioning process.
  - A **StorageClass** object represents a class of storage that can be dynamically provisioned.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/8.8.png)

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/8.9.png)

```bash
kubectl get sc
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true" # This marks the storage class as default
  name: standard # The name of storage class
# ...
provisioner: rancher.io/local-path # The name of provisioner that gets called to provision persistent volumes of this class
reclaimPolicy: Delete # The reclaim policy for persistent volumes of this class
volumeBindingMode: WaitForFirstConsumer # How volumes of this class are provisioned and bound
```

#### 2.4.8. Secrets

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

#### 2.4.9. Namespaces

- The name of a resource is a unique identifier with a namespace in the Kubernetes cluster. Using a Kubernetes namepsace could isolate namespaces for different environments in the same cluster.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/10.1.png)

- Pods, services, replication controllers (replica sets) are contained in a certain namespace. Some resources, such as nodes and PVs, do not belong to any namespace.

![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/10.2.png)

- Some useful commands:

```bash
# Listing namespaces
kubectl get namespaces
# Listing objects in a specific namespace
kubectl get po --namespace kube-system
# Listing objects across all namespaces
kubectl get cm --all-namespaces
# Creating a namespace
kubectl create namespace ns-test1
# Creating a namespace from a manifest file
cat <<EOF > ns-test2.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns-test2
EOF
kubectl apply -f ns-test2.yaml
```

- Understanding the (lack of) isolation between namespaces:
  - When two pods created in different namespaces are scheduled to the same cluster node, they both run in the same OS kernel -> an application that break out of its container or consumes too much of the node's resources can ffect the operation of the other application.

  ![](https://wangwei1237.github.io/Kubernetes-in-Action-Second-Edition/images/10.3.png)

  - Kubernetes doesn't provide network isolation between applications running in pods in different namespaces (by default) -> Can use the NetworkPolicy object to configure which applications in which namespaces can connect to which applications in other namespaces.
  - Should not use namespaces to split a single physical cluster into production, staging, and development environments.

#### 2.4.10. Ingress

- Typically, services and pods have IPs only routable by the cluster network.

  ```
    internet
      |
  --------
  [ Services ]
  ```

- An Ingress is a collection of rules that allow **inbound connections** to reach
  the cluster services.

  ```
    internet
      |
  [ Ingress ]
  ---|---|---
  [ Services ]
  ```

- It's an alternative to the exernal **LoadBalancer** and **NodePort**:
  - Ingress allows you to **easily expose services** that need to be accessible from **outside** to the **cluster**.
- With ingress you can run **Ingress Controller** (basically a LoadBalancer) within the Kubernetes cluster.

![](imgs/ingress.png)

- It can be configured to give services externally-reachable URLs, load balance traffic, terminate SSL... User request ingress by POSTing the Ingress resource to the API server.
- Read [more](https://medium.com/@cashisclay/kubernetes-ingress-82aa960f658e).
- Example:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: helloworld-rules
spec:
  rules:
    - host: helloworld-v1.example.com
      http:
        paths:
          - path: /
            backend:
              serviceName: helloworld-v1
              servicePort: 80
    - host: helloworld-v2.example.com
      http:
        paths:
          - path: /
            backend:
              serviceName: helloworld-v2
              servicePort: 80
```

#### 2.4.11. ConfigMap

- Configuration parameters that are not secret -> put in **ConfigMap**.
- The **ConfigMap** key-value pairs can then be read by the app using:
  - **Environment** variables.
  - **Container commandline arguments** in the Pod configuration.
  - Using **volumes**.
- To generate configmap using files:

```bash
cat <<EOF > app.properties
driver=jdbc
database=postgres
lookandfeel=1
otherparams=xyz
param.with.hierarchy=xyz
EOF

kubectl create configmap app-config —from-file=app.properties
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
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config # /etc/config/driver /etc/config/param/with/hierachy
  volumes:
    - name: config-volume
      configMap:
        name: app-config
```
