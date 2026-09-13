# Kubernetes Controller and Custom Resources

Source: <https://github.com/gianlucam76/kubernetes-controller-tutorial/>

## 1. Kubernetes APIs and Custom Resources

### 1.1. Kubernetes APIs

Kubernetes provides a robust API for managing your cluster. API uses a RESTful design, allowing to perform common actions like creating, retrieving, updating, deleting, listing, patching, and watching various resources within your cluster.

Kubernetes APIs are divided into groups:

1. **core** group: this includes _Nodes_, _Pods_, _Namespaces_, _Services_, _ConfigMaps_ and _Secrets_.
2. **named** groups: These groups categorize related functionalities. For example, the `apps` group contains resources for managing _deployments_, _stateful sets_, _daemon sets_, and _replica sets_, while the `batch` group handles _jobs_ and _cron jobs_.

Each group may have one or more versions that evolve independent of other API groups, and each version within the group has one or more resources.

version within the group has one or more resources.

[![Kubernetes REST Paths](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/kubernetes_rest_paths.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/kubernetes_rest_paths.png)

To summarize:

1. **Group**: Categorizes resources based on functionality or origin. This allows for easy API extension by adding new groups for specific features.
2. **Version**: Represent specific API versions within a group. New features or modifications to existing resources might be introduced in different versions. Versioning ensures compatibility and smoother upgrades.
3. **Resource** type is the name used in the URL (e.g., pods, namespaces, services).
4. **Kind**: defines the concrete representation (object schema) of a resource type.
5. **Collection**: refers to a list of instances for a specific resource type. There are distinct collection kinds with "List" appended (e.g., _PodList_, _ServiceList_).
6. **Resource**: an individual instance of a resource type, typically representing an object in your cluster.
7. **Sub-resources:**: for specific resource types, additional functionalities are exposed as sub-resources within the resource URI path.

To see all the available API resources in your cluster: `kubectl api-resources`

```notranslate
$ kubectl api-resources
NAME                                SHORTNAMES   APIVERSION                                NAMESPACED   KIND
bindings                                         v1                                        true         Binding
configmaps                          cm           v1                                        true         ConfigMap
endpoints                           ep           v1                                        true         Endpoints
events                              ev           v1                                        true         Event
limitranges                         limits       v1                                        true         LimitRange
namespaces                          ns           v1                                        false        Namespace
nodes                               no           v1                                        false        Node
persistentvolumeclaims              pvc          v1                                        true         PersistentVolumeClaim
persistentvolumes                   pv           v1                                        false        PersistentVolume
pods                                po           v1                                        true         Pod
...
```

The API server handles all requests.

[![REST post](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/request_resource.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/request_resource.png)

When we create a deployment for instance, the kube-apiserver validates the content of our deployment to ensure it meets the required format and follows the rules. Once validated, it stores the deployment information in the cluster's data store, typically etcd.

[![Deployment controller](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/deployment_controller.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/deployment_controller.png)

Much of the behavior of Kubernetes is implemented by programs called controllers, that are clients of the API server. Kubernetes comes already with a set of built-in controllers. For instance we can look at the `kube-controller-manager` pod's log to see which controllers are started. The _deployment controller_ is one of those.

```notranslate
kubectl logs -n kube-system                         kube-controller-manager-sveltos-management-control-plane
...
I0531 15:34:16.026590       1 controllermanager.go:759] "Started controller" controller="deployment-controller"
```

The deployment controller is constantly watching for deployment instances. In our case, when we created a new deployment, the deployment controller became aware of this change and it took action to achieve the desired state we specified. In this case, it created a ReplicaSet resource. The deployment controller also updated the deployment status section. This section keeps track of the progress towards achieving the desired state.

### 1.2. Objects

Every object must have the following data.

`TypeMeta` contains the kind and API version.

A nested field `metadata` contains:

1. **namespace**: the default namespace is 'default'. Cluster wide resources do not have this field set.
2. **name**: a string that uniquely identifies this object within the current namespace. This value is used in the path when retrieving an individual object.
3. **uid**: a unique in time and space value used to distinguish between objects with the same name that have been deleted and recreated.
4. **resourceVersion**: a string that identifies the internal version of this object that can be used by clients to determine when objects have changed;
5. **creationTimestamp**: a string representing the date and time an object was created.
6. **deletionTimestamp**: a string representing the date and time after which this resource will be deleted.
7. **labels**: a map of string keys and values that can be used to organize and categorize objects.
8. **annotations**: a map of string keys and values that can be used by external tooling to store and retrieve arbitrary metadata about this object.

[![Kubernetes Object](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/kubernetes_object.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/kubernetes_object.png)

A nested object field called `spec` represents the desired state of an object.

A nested object field called `status` summarizes the current state of the object in the system. The Kubernetes declarative API enforces a separation of responsibilities. You declare the desired state of your resource (spec). The Kubernetes controller keeps the current state of Kubernetes objects in sync with your declared desired state.

### 1.3. Extending the Kubernetes API

Any system that is successful needs to grow and change as new use cases emerge or existing ones change. Therefore, Kubernetes has designed the Kubernetes API to continuously change and grow. There are two ways to extend Kubernetes APIs:

- The `CustomResourceDefinition` (CRD) mechanism allows you to declaratively define a new custom API with an API group, kind, and schema that you specify. CRDs allow you to create new types of resources for your cluster without writing and running a custom API server. When you create a new CustomResourceDefinition, the Kubernetes API Server creates a new RESTful resource path for each version specified.

- The `aggregation layer` sits behind the primary API server, which acts as a proxy. This arrangement is called API Aggregation (AA), which allows you to provide specialized implementations for your custom resources by writing and deploying your own API server. The main API server delegates requests to your API server for the custom APIs that you specify.

[![Kube-aggregator](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/extension_apiserver.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/extension_apiserver.png)

You can register an `extension API server` by creating an _APIService_ claiming a URL path in the Kubernetes API. From that point on, `kube-aggregator` will forward any request sent to that API path will be forwarded to the registered APIService.

### 1.4. Custom Resource Definition

To introduce new resources, you can use CustomResourceDefinitions. CRDs extends Kubernetes capabilities by allowing users to create new types of resources beyond the built-in set.

A CustomResourceDefinition is a Kubernetes resource itself. So you can create a CustomResourceDefinition like you would create any other Kubernetes resources.

Most validation can be specified in the CRD using OpenAPI v3.0 validation and the Common Expression Language. Any other validations is supported by addition of a Validating Webhook.

## 1.5. Kubebuilder

[Kubebuilder](https://github.com/kubernetes-sigs/kubebuilder), a framework by Kubernetes SIGs, simplifies creating Kubernetes APIs using Custom Resource Definitions.

With Kubebuilder installed, you can create a new project.

```sh
mkdir my-project
cd my-project
kubebuilder init --domain viettel.com.vn --repo viettel.com.vn/my-project
kubebuilder create api --group app --version v1alpha1 --kind MyKind
```

- **Group**: This acts as a unique identifier for your set of custom resources. It's recommended to use a subdomain you control (e.g., yourcompany.com) to prevent conflicts with existing Kubernetes groups.
- **Version**: Kubernetes versions follow a specific format: vX.Y (optionally with alpha or beta) and potentially additional numbers. alpha indicates a feature under development, while beta suggests more stability.
- **Kind**: This defines the specific type of resource within your API (e.g., Database, ConfigMap). It essentially names the individual resources you'll be managing.

```sh
tree api
api
└── v1alpha1
    ├── groupversion_info.go
    ├── mykind_types.go
    └── zz_generated.deepcopy.go

1 directory, 3 files
```

In Kubebuilder projects, two key files play specific roles:

- **groupversion_info.go**: This file, as its name suggests, holds information about the API group and version for your CRD. It typically defines a variable named GroupVersion with the group (e.g., app.projectsveltos.io) and version (e.g., v1alpha1). This establishes the unique identifier for your CRD within the Kubernetes API.
- **mykind_types.go**: This file is where you define the actual resource itself. It contains the structure of your CRD, including its fields and any validation rules. This file essentially describes the data your CRD will manage within your Kubernetes cluster.

Now, you are ready to customize the API behavior by defining the **MyKindSpec** and **MyKindStatus** structs in mykind_types.go. Once you've completed these definitions, running `make manifests` will generate the CustomResourceDefinition file in _config/crd/bases/app.viettel.com.vn_mykinds.yaml_.

### 1.6.. Example: Cleaner CRD

#### 1.6..1. Choosing the scope

A key design decision involved the scope. Since the primary users are platform administrators who manage the entire cluster, I opted for a **cluster-wide** scope. This allows admins to identify unused resources (e.g., ConfigMaps) across all namespaces efficiently. This eliminates the need to deploy separate cleaners for each namespace, streamlining their workflow.

However, while a cluster-wide scope offers clear benefits for platform admins, I also acknowledged the potential need for users to focus on specific namespaces. To address this flexibility, I incorporated namespace filtering as a configuration option. This allows users to customize the cleaner's operation to their specific requirements. As a configuration option, it's exposed within the **Spec** field.

The marker comment used to define a cluster-wide scope for the Cleaner controller is:

    //+kubebuilder:resource:path=cleaners,scope=Cluster

If you decide your resources should be scoped to namespace:

    //+kubebuilder:resource:path=cleaners,scope=Namespaced

#### 1.6..2. Spec

The Spec represents the desired state, including user-defined settings and system defaults. So expose in the Spec all that the user might need to specify.

My vision was to empower users with the ability to:

1. _Define Criteria_: Clearly specify what constitutes an unused or unhealthy resource in their specific context.
2. _Schedule Scans_: Determine how often the Cleaner controller should scan the cluster for resources meeting your cleanup criteria.
3. _Automate Actions_: Choose the desired action (removal or update) to be taken on identified resources.

Remember some fields might be optional and have a default value. Use the `// +kubebuilder:default:=` marker to specify the default value.

    // +kubebuilder:default:=Delete
    Action Action `json:"action,omitempty"`

Here, `Delete` is the default action if not explicitly defined by the user.

Add the `optional` marker along to the json struct `omitempty` tag of the field you want to make optional.

    // +optional
    Transform string `json:"transform,omitempty"`

Full list of [validation markers](https://book.kubebuilder.io/reference/markers/crd-validation.html?highlight=%2F%2F%20%2Bkubebuilder%3Avalidation%3AEnum#crd-validation).

#### 1.6..3. Status Subresource

The status subresource is enabled via `//+kubebuilder:subresource:status`. This subresource exposes an additional endpoint specifically for the status of your cleaner instance.

In Kubernetes, as already explained, a `resource` represents a logical entity like a Pod or a Deployment. Each resource has an associated API endpoint. The status subresource provides a dedicated endpoint for monitoring the current state and progress of your cleaner instance.

It's important to note that updates made to the main cleaner resource won't directly affect its status. Likewise, changes to the status subresource only influence the status information, not the main configuration. This separation allows for focused updates.

Since the status subresource has its own endpoint, you can leverage RBAC (Role-Based Access Control) to manage access to the cleaner resource and its status independently. This enables you to define who can view or modify the cleaner's configuration and who can monitor its progress through the status subresource.

[![Status subresource: different endpoints](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/status_subresource.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/status_subresource.png)

Understanding who defines the Spec and who utilizes the Status is crucial when designing a CRD. These sections play distinct roles in managing your Cleaner resource.

The Spec section acts as a blueprint for the desired state of your Cleaner resource. In this scenario, the platform administrator defines the Spec by outlining the cleaning criteria, scan schedule, and desired actions. Essentially, the Spec tells the Cleaner controller what to do.

The Status section, automatically updated by the Cleaner controller, reflects the current state of your resource. It provides valuable information for the platform administrator, such as:

1. _lastRunTime_: The timestamp of the most recent Cleaner execution.
2. _failureMessage_ (optional): A human-readable error message if the last run failed.
3. _nextScheduleTime_: The scheduled time for the next Cleaner execution.

By monitoring the Status subresource, the platform administrator gains insights into the Cleaner's performance and can identify any potential cleaning errors.

#### 1.6..4. Make generate

Once done defining Spec and Status, just run `make generate` target. That will simply properly invoke controller-gen behind the scene.

This will generate the [Cleaner CustomResourceDefinition](https://github.com/gianlucam76/k8s-cleaner/blob/main/config/crd/bases/apps.projectsveltos.io_cleaners.yaml). Use _kubectl_ to apply it to your cluster.

#### 1.6..5. Apiextension-apiserver

After posting a CustomResourceDefinition object, the `apiextensions-apiserver` inside of kube-apiserver will check whether there is a conflict and whether the resource is valid. It will then report the result in the status of the CRD, for example:

```notranslate
kubectl get customresourcedefinitions cleaners.apps.projectsveltos.io -o yaml
```

    apiVersion: apiextensions.k8s.io/v1
    kind: CustomResourceDefinition
    metadata:
      name: cleaners.apps.projectsveltos.io
    ...
    status:
      acceptedNames:
        kind: Cleaner
        listKind: CleanerList
        plural: cleaners
        singular: cleaner
      conditions:
      - lastTransitionTime: "2024-05-31T12:32:39Z"
        message: no conflicts found
        reason: NoConflicts
        status: "True"
        type: NamesAccepted
      - lastTransitionTime: "2024-05-31T12:32:39Z"
        message: the initial names have been accepted
        reason: InitialNamesAccepted
        status: "True"
        type: Established
      storedVersions:
      - v1alpha1

### 1.7. Common Expression Language (CEL)

For ensuring your CRD configurations are well-defined, you can leverage marker comments with `Common Expression Language` (`CEL`). Since Kubernetes v1.25 introduced CEL support for validation in beta, you can now write expressions to validate your custom resources.

Marker `//+kubebuilder:validation:XValidation:rule` can be used for this scope.

#### 1.7.1. Immutability

One common example is immutability. For instance if I wanted to make Cleaner.Spec.Schedule string immutable

    //+kubebuilder:validation:XValidation:rule="self == oldSelf",message="Value is immutable"
    Schedule string `json:"schedule"`

With that, If I tried to update a Cleaner instance changing the _schedule_ field, the update would fail

```notranslate
The Cleaner "list-pods-with-outdated-secret-data" is invalid: spec.schedule: Invalid value: "string": Value is immutable
```

self is a special keyword in CEL which refers to the object whose type contains the rule. In the above example, self refers to Schedule field. So I am only forcing the Schedule field to be immutable.

#### 1.7.2. Append-only list

Another common example is a list which is append only. As a hypothetical example, if ResourceSelectors were designed this way

    //+kubebuilder:validation:XValidation:rule="size(self) >= size(oldSelf)",message="this list is append only"
    ResourceSelectors []ResourceSelector `json:"resourceSelectors"`

any update reducing that list would fail

```notranslate
The Cleaner "list-pods-with-outdated-secret-data" is invalid: spec.resourcePolicySet.resourceSelectors: Invalid value: "array": this list is append only
```

#### 1.7.3. Name format

To enforce that cleaner instance starts with "my-prefix" (remember the meaning of _self_ )

    // Cleaner is the Schema for the cleaners API
    type Cleaner struct { //+kubebuilder:validation:XValidation:rule=self.metadata.name.startsWith("my-prefix")

creating any Cleaner instance with an incorre name will fail

```notranslate
The Cleaner "list-pods-with-outdated-secret-data-2" is invalid: <nil>: Invalid value: "object": failed rule: self.metadata.name.startsWith("my-prefix")
```

When dealing with string fields in your CRD, you can leverage the `+kubebuilder:validation:Pattern` annotation to enforce a specific format using regular expressions. For example, to ensure a string field named description starts with a letter or underscore and only contains letters, numbers, and underscores, you can use the following YAML snippet:

    // +kubebuilder:validation:Pattern=`^[A-Za-z_][A-Za-z0-9_]*$`
    Description string `json:"description"`

If you have a string field that requires a valid date and time format, typically following RFC 3339, you can use the `+kubebuilder:validation:Format="date-time"` annotation. For instance, to validate a field named TimeOfX, the following YAML snippet would ensure it adheres to RFC 3339:

    //+kubebuilder:validation:Format="date-time"
    TimeOfX string `json:"timeOfX"`

then _"2024-06-03T15:29:48Z"_ would be a valid value, while "2024" would not be.

#### 1.7.4. Comparing different fields

Imagine having a Spec with

    // +kubebuilder:validation:XValidation:rule=self.minReplicas <= self.replicas
    type MyResourceSpec struct {
      Replicas int `json:"replicas"`

      MinReplicas int `json:"minReplicas"`

above marker enforces that minReplicas is always less than or equal to replicas.

## 2. Kubernetes Controller

Behind the scenes in Kubernetes, controllers constantly monitor the cluster's state, comparing it to your desired configuration. Whenever there's a gap between the two, they spring into action.

[![Reconciler Queue](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/reconcile_loop.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/reconcile_loop.png)

Each controller focuses on a specific type of resource in Kubernetes, like pods or deployments. Remember how we talked about resources having a ["spec"](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/custom-resources.md#objects) field? This spec defines your desired state for that resource. The controller's job is to make the actual state (what's currently running) match that spec.

In other words, the controller makes adjustments to bring things in line with your desired state. It then updates the status with the latest information. Other controllers might potentially take their own actions based on the new information.

Let's what happens behind the scene when we create a deployment:

1. Imagine you have a file named deployment.yaml that contains instructions for your deployment (like the one shown below). This file describes how many Nginx pods you want to run and their configuration. To deploy your application based on this configuration, you can run the following command: `kubectl apply -f deployment.yaml -n test`

<!-- end list -->

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx-deployment
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:latest
            ports:
            - containerPort: 80

2. Behind the scenes, Kubernetes has a special a [Deployment controller](https://github.com/kubernetes/kubernetes/blob/e67f889edc4ab278028f6cffd2501bc90a0defcf/pkg/controller/deployment/deployment_controller.go#L101). This controller constantly monitors the cluster for deployments instances. When it detects the newly created deployment (like nginx-deployment), it takes action by creating a [ReplicaSet instance](https://github.com/kubernetes/kubernetes/blob/e67f889edc4ab278028f6cffd2501bc90a0defcf/pkg/controller/deployment/sync.go#L195) and by [updating](https://github.com/kubernetes/kubernetes/blob/e67f889edc4ab278028f6cffd2501bc90a0defcf/pkg/controller/deployment/sync.go#L476) the Deployment Status field.

[![Deployment Controller](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/deployment_controller.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/deployment_controller.png)

The ReplicaSet instance created has the ownerReferences field in the metadata section set. This essentially indicates the ReplicaSet is _owned_ by the Deployment instance specified.

The ReplicaSet instance created has the ownerReferences field in the metadata section set. This essentially indicates the ReplicaSet is _owned_ by the Deployment instance specified

```
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: Deployment
      name: nginx-deployment
      uid: df02a54a-cf4b-4543-870a-523c2da36bbd
```

3. Kubernetes relies on the [ReplicaSet controller](https://github.com/kubernetes/kubernetes/blob/e67f889edc4ab278028f6cffd2501bc90a0defcf/pkg/controller/replicaset/replica_set.go#L118) to maintain a set number of identical pods for your deployments. The ReplicaSet controller constantly watches the cluster for ReplicaSets.

[![ReplicaSet Controller](https://github.com/gianlucam76/kubernetes-controller-tutorial/raw/main/docs/assets/replicaset_controller.png)](https://github.com/gianlucam76/kubernetes-controller-tutorial/blob/main/docs/assets/replicaset_controller.png)

```notranslate
kubectl get pods -n test
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-576c6b7b6-wzc6l   1/1     Running   0          24m
nginx-deployment-576c6b7b6-xwsc2   1/1     Running   0          24m
```

And each Pod instance has the ownerReferences field in the metadata field set. This indicates that these pods are created and managed by a specific ReplicaSet instance.

```
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: nginx-deployment-576c6b7b6
    uid: 9a749240-6b63-4c29-ad7e-ba8dcd9a16bc
```

If a pod is deleted unexpectedly (due to crash or other reasons), the ReplicaSet controller will notice the change. It then springs into action to maintain the desired number of pods. In this case, it would create a new pod to bring the total back to the expected count.
