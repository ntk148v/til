A good first Kubernetes operator is deliberately small: define a custom resource called **`Greeting`**, then write a controller that ensures each `Greeting` has a corresponding `ConfigMap`.

This demonstrates the core Kubernetes pattern:

**CRD → Custom Resource → Watch → Reconcile → Managed Kubernetes resource → Status**

Kubernetes CRDs extend the API server with new resource types, while a custom controller turns that stored declarative data into actual behavior. ([Kubernetes](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/?utm_source=chatgpt.com "Custom Resources | Kubernetes"))

## 1. What we're building

A user will create:

    apiVersion: demo.example.com/v1alpha1
    kind: Greeting
    metadata:
      name: hello
    spec:
      message: "Hello Kubernetes"

Our controller will automatically create:

    apiVersion: v1 kind: ConfigMap
    metadata:
      name: hello-greeting
    data:
      message: "Hello Kubernetes"

And the CR will eventually report:

    status:
      ready: true
      configMapName: hello-greeting

The important part is that we aren't coding around individual create/update events. A Kubernetes reconciler should repeatedly compare **desired state** with **actual state** and make the latter converge on the former. controller-runtime explicitly describes reconciliation as level-based rather than event-driven business logic. ([Go Packages](https://pkg.go.dev/sigs.k8s.io/controller-runtime?utm_source=chatgpt.com "controllerruntime package - sigs.k8s.io/controller-runtime - Go Packages"))

---

## 2. Prerequisites

You need:

    Go
    Docker
    kubectl
    Kubebuilder
    a Kubernetes cluster

For local development, `kind` or `minikube` works well.

The current Kubebuilder quick start uses the standard workflow of `kubebuilder init`, `kubebuilder create api`, `make install`, and `make run`. ([Kubebuilder Book](https://book.kubebuilder.io/quick-start.html?utm_source=chatgpt.com "Quick Start - The Kubebuilder Book"))

Install Kubebuilder:

    curl -L -o kubebuilder \
      "https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)"

    chmod +x kubebuilder
    sudo mv kubebuilder /usr/local/bin/

Verify:

    kubebuilder version
    go version
    kubectl version --client

For a throwaway local cluster:

    kind create cluster --name operator-dev

Check it:

    kubectl cluster-info
    kubectl get nodes

---

## 3. Create the operator project

Create a directory:

    mkdir greeting-operator
    cd greeting-operator

Initialize the Go/Kubebuilder project:

    kubebuilder init \
      --domain example.com \
      --repo example.com/greeting-operator

Kubebuilder creates the manager, Makefile, Dockerfile, RBAC configuration, Kustomize configuration, and other operator scaffolding.

Now create the API:

    kubebuilder create api \
      --group demo \
      --version v1alpha1 \
      --kind Greeting

Answer:

    Create Resource [y/n]
    y

    Create Controller [y/n]
    y

This should give you files roughly like:

    greeting-operator/
    ├── api/
    │   └── v1alpha1/
    │       ├── greeting_types.go
    │       ├── groupversion_info.go
    │       └── zz_generated.deepcopy.go
    │
    ├── internal/
    │   └── controller/
    │       ├── greeting_controller.go
    │       └── greeting_controller_test.go
    │
    ├── config/
    │   ├── crd/
    │   ├── rbac/
    │   ├── manager/
    │   └── samples/
    │
    ├── cmd/
    │   └── main.go
    ├── Dockerfile
    ├── Makefile
    └── go.mod

Current Kubebuilder scaffolding likewise puts API definitions under `api/...` and reconciliation code under `internal/controller`. ([Kubebuilder Book](https://book.kubebuilder.io/quick-start.html?utm_source=chatgpt.com "Quick Start - The Kubebuilder Book"))

---

## 4. Define the CRD API

Open:

    api/v1alpha1/greeting_types.go

Replace the generated spec/status definitions with:

    package v1alpha1

    import (
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    )

    // GreetingSpec defines the desired state of Greeting.
    type GreetingSpec struct {
        // Message is the text that should be stored in the generated ConfigMap.
        //
        // +kubebuilder:validation:MinLength=1
        Message string `json:"message"`
    }

    // GreetingStatus defines the observed state of Greeting.
    type GreetingStatus struct {
        // Ready indicates whether the managed ConfigMap exists.
        Ready bool `json:"ready,omitempty"`

        // ConfigMapName is the ConfigMap managed by this Greeting.
        ConfigMapName string `json:"configMapName,omitempty"`
    }

    // +kubebuilder:object:root=true
    // +kubebuilder:subresource:status
    // +kubebuilder:printcolumn:name="Ready",type="boolean",JSONPath=".status.ready"
    // +kubebuilder:printcolumn:name="ConfigMap",type="string",JSONPath=".status.configMapName"

    // Greeting is the Schema for the greetings API.
    type Greeting struct {
        metav1.TypeMeta   `json:",inline"`
        metav1.ObjectMeta `json:"metadata,omitempty"`

        Spec   GreetingSpec   `json:"spec,omitempty"`
        Status GreetingStatus `json:"status,omitempty"`
    }

    // +kubebuilder:object:root=true

    // GreetingList contains a list of Greeting.
    type GreetingList struct {
        metav1.TypeMeta `json:",inline"`
        metav1.ListMeta `json:"metadata,omitempty"`

        Items []Greeting `json:"items"`
    }

    func init() {
        SchemeBuilder.Register(&Greeting{}, &GreetingList{})
    }

The important API design distinction is:

    spec   = desired state supplied by the user
    status = observed state supplied by the controller

For our resource:

    spec:
      message: Hello

means:

> I want a greeting containing `"Hello"`.

Whereas:

    status:
      ready: true
      configMapName: hello-greeting

means:

> The controller observed that it successfully realized that request.

---

## 5. Generate the CRD

Run:

    make generate
    make manifests

`make manifests` converts Kubebuilder markers into CRDs, RBAC manifests, and related generated configuration. This is the standard Kubebuilder workflow after changing API definitions or RBAC markers. ([Kubebuilder Book](https://book.kubebuilder.io/quick-start.html?utm_source=chatgpt.com "Quick Start - The Kubebuilder Book"))

You'll now have a generated CRD under something similar to:

    config/crd/bases/demo.example.com_greetings.yaml

The resulting CRD is conceptually equivalent to:

    apiVersion: apiextensions.k8s.io/v1
    kind: CustomResourceDefinition
    metadata:
      name: greetings.demo.example.com
    spec:
      group: demo.example.com

      scope: Namespaced

      names:
        plural: greetings
        singular: greeting
        kind: Greeting

      versions:
        - name: v1alpha1
          served: true
          storage: true

          schema:
            openAPIV3Schema:
              type: object
              properties:
                spec:
                  type: object
                  required:
                    - message
                  properties:
                    message:
                      type: string
                      minLength: 1

                status:
                  type: object
                  properties:
                    ready:
                      type: boolean
                    configMapName:
                      type: string

          subresources:
            status: {}

Modern CRDs use:

    apiVersion: apiextensions.k8s.io/v1

and contain an OpenAPI schema for the custom resource. ([Kubernetes](https://kubernetes.io/docs/reference/kubernetes-api/apiextensions/custom-resource-definition-v1/?utm_source=chatgpt.com "CustomResourceDefinition | Kubernetes"))

---

## 6. Implement the controller

Now edit:

    internal/controller/greeting_controller.go

The controller's responsibility will be:

    Greeting exists
          ↓
    Reconcile()
          ↓
    ConfigMap exists?
       /       \
     no         yes
     ↓           ↓
    create      update if necessary
          ↓
    update Greeting.status

Use this implementation:

    // RBAC markers must be package-scoped for controller-tools v0.21+.
    // +kubebuilder:rbac:groups=demo.example.com,resources=greetings,verbs=get;list;watch;create;update;patch;delete
    // +kubebuilder:rbac:groups=demo.example.com,resources=greetings/status,verbs=get;update;patch
    // +kubebuilder:rbac:groups=demo.example.com,resources=greetings/finalizers,verbs=update
    // `core` generates the empty API group ("") for ConfigMaps.
    // +kubebuilder:rbac:groups=core,resources=configmaps,verbs=get;list;watch;create;update;patch;delete

    package controller

    import (
        "context"

        corev1 "k8s.io/api/core/v1"
        "k8s.io/apimachinery/pkg/runtime"

        ctrl "sigs.k8s.io/controller-runtime"
        "sigs.k8s.io/controller-runtime/pkg/client"
        "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
        "sigs.k8s.io/controller-runtime/pkg/log"

        demov1alpha1 "example.com/greeting-operator/api/v1alpha1"
    )

    // GreetingReconciler reconciles a Greeting object.
    type GreetingReconciler struct {
        client.Client
        Scheme *runtime.Scheme
    }

    func (r *GreetingReconciler) Reconcile(
        ctx context.Context,
        req ctrl.Request,
    ) (ctrl.Result, error) {

        logger := log.FromContext(ctx)

        // ------------------------------------------------------------
        // 1. Fetch the Greeting
        // ------------------------------------------------------------

        var greeting demov1alpha1.Greeting

        if err := r.Get(ctx, req.NamespacedName, &greeting); err != nil {
            // A reconcile may happen after the resource was deleted.
            // Ignore NotFound because there is nothing left to reconcile.
            return ctrl.Result{}, client.IgnoreNotFound(err)
        }

        logger.Info(
            "reconciling Greeting",
            "name", greeting.Name,
            "namespace", greeting.Namespace,
        )

        // ------------------------------------------------------------
        // 2. Describe the ConfigMap we want
        // ------------------------------------------------------------

        configMap := &corev1.ConfigMap{}

        configMap.Name = greeting.Name + "-greeting"
        configMap.Namespace = greeting.Namespace

        // ------------------------------------------------------------
        // 3. Create or update it
        // ------------------------------------------------------------

        _, err := controllerutil.CreateOrUpdate(
            ctx,
            r.Client,
            configMap,
            func() error {

                if configMap.Data == nil {
                    configMap.Data = map[string]string{}
                }

                configMap.Data["message"] = greeting.Spec.Message

                // Make Greeting the owner of this ConfigMap.
                return controllerutil.SetControllerReference(
                    &greeting,
                    configMap,
                    r.Scheme,
                )
            },
        )

        if err != nil {
            logger.Error(err, "unable to reconcile ConfigMap")
            return ctrl.Result{}, err
        }

        // ------------------------------------------------------------
        // 4. Update status if necessary
        // ------------------------------------------------------------

        if !greeting.Status.Ready ||
            greeting.Status.ConfigMapName != configMap.Name {

            greeting.Status.Ready = true
            greeting.Status.ConfigMapName = configMap.Name

            if err := r.Status().Update(ctx, &greeting); err != nil {
                return ctrl.Result{}, err
            }
        }

        logger.Info(
            "Greeting reconciled",
            "configMap", configMap.Name,
        )

        return ctrl.Result{}, nil
    }

The central operation is:

    controllerutil.CreateOrUpdate(...)

This makes the operation **idempotent**.

That property is critical.

Don't design reconciliation as:

    CREATE event → create ConfigMap
    UPDATE event → update ConfigMap
    DELETE event → delete ConfigMap

Instead design it as:

    read desired state
    read actual state
    make actual state equal desired state

The reconcile request generally contains only the resource's namespace/name; the reconciler examines current state to determine what action is required. ([Go Packages](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile?utm_source=chatgpt.com "reconcile package - sigs.k8s.io/controller-runtime/pkg/reconcile - Go Packages"))

---

## 7. Register the watch

At the bottom of `greeting_controller.go`, add or replace `SetupWithManager`:

    func (r *GreetingReconciler) SetupWithManager(mgr ctrl.Manager) error {
        return ctrl.NewControllerManagedBy(mgr).
            For(&demov1alpha1.Greeting{}).
            Owns(&corev1.ConfigMap{}).
            Complete(r)
    }

This part:

    For(&demov1alpha1.Greeting{})

means:

> Reconcile `Greeting` resources.

And:

    Owns(&corev1.ConfigMap{})

means:

> Also reconcile the parent `Greeting` when a ConfigMap owned by it changes.

Kubebuilder/controller-runtime supports precisely this owner-resource relationship through the controller builder's `Owns` mechanism. ([Kubebuilder Book](https://book-v3.book.kubebuilder.io/reference/watching-resources/externally-managed?utm_source=chatgpt.com "Externally Managed Resources - The Kubebuilder Book"))

So your controller reacts both to:

    Greeting changed
           ↓
     Reconcile Greeting

and:

    owned ConfigMap changed/deleted
           ↓
    find owning Greeting
           ↓
     Reconcile Greeting

That second behavior gives us an important self-healing property.

---

## 8. Why `SetControllerReference` matters

This line:

    controllerutil.SetControllerReference(
        &greeting,
        configMap,
        r.Scheme,
    )

creates an `ownerReferences` relationship.

The ConfigMap will look roughly like:

    metadata:
      ownerReferences:
        - apiVersion: demo.example.com/v1alpha1
          kind: Greeting
          name: hello
          controller: true

This gives us two useful behaviors.

First, controller-runtime can determine:

    ConfigMap → owning Greeting

which supports:

    Owns(&corev1.ConfigMap{})

Second, Kubernetes garbage collection can delete the ConfigMap when its owner is deleted.

Therefore, in this example, we don't need custom ConfigMap deletion code.

---

## 9. Regenerate RBAC

Because the controller watches owned ConfigMaps, it needs this package-scoped RBAC marker:

    // +kubebuilder:rbac:groups=core,resources=configmaps,verbs=get;list;watch;create;update;patch;delete

`core` generates Kubernetes's empty API group (`""`). With controller-tools v0.21+, place RBAC markers before the `package` declaration; markers attached to `Reconcile` are ignored.

Regenerate and check the manifest:

    make manifests
    grep -A8 configmaps config/rbac/role.yaml

Kubebuilder generates the appropriate RBAC rules under `config/rbac/`.

Without `list` and `watch`, `.Owns(&corev1.ConfigMap{})` makes the controller fail with:

    configmaps is forbidden:
    User "system:serviceaccount:..." cannot list resource "configmaps" in API group "" at the cluster scope

---

## 10. Install the CRD

Install the CRD into your current Kubernetes cluster:

    make install

Check it:

    kubectl get crd greetings.demo.example.com

You should see:

    NAME                         CREATED AT
    greetings.demo.example.com   ...

You can now ask Kubernetes about your new resource:

    kubectl api-resources | grep Greeting

or:

    kubectl api-resources | grep greeting

And:

    kubectl explain greeting

Try:

    kubectl explain greeting.spec

and:

    kubectl explain greeting.spec.message

At this point the **CRD exists**, but the controller isn't running yet.

---

## 11. Run the controller locally

Kubebuilder supports running the controller on your workstation while it communicates with the cluster selected by your current kubeconfig. ([Kubebuilder Book](https://book.kubebuilder.io/quick-start.html?utm_source=chatgpt.com "Quick Start - The Kubebuilder Book"))

Run:

    make run

You'll see controller-manager logs.

Leave this terminal running.

---

## 12. Create a custom resource

Open another terminal.

Create:

    config/samples/demo_v1alpha1_greeting.yaml

with:

    apiVersion: demo.example.com/v1alpha1
    kind: Greeting
    metadata:
      name: hello
    spec:
      message: "Hello from my Kubernetes controller"

Apply it:

    kubectl apply -f config/samples/demo_v1alpha1_greeting.yaml

Check:

    kubectl get greetings

Because of our printer columns you should eventually get something similar to:

    NAME    READY   CONFIGMAP
    hello   true    hello-greeting

Inspect it:

    kubectl get greeting hello -o yaml

Look for:

    spec:
      message: Hello from my Kubernetes controller

    status:
      configMapName: hello-greeting
      ready: true

---

## 13. Verify the generated ConfigMap

Run:

    kubectl get configmap hello-greeting -o yaml

You should find:

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: hello-greeting
    data:
      message: Hello from my Kubernetes controller

So the complete process was:

    kubectl apply Greeting
            │
            ▼
     Kubernetes API
            │
            ▼
    controller-runtime watch
            │
            ▼
     Reconcile("hello")
            │
            ├── read Greeting
            │
            ├── create ConfigMap
            │
            └── update Greeting.status

---

## 14. Test reconciliation on update

Change the custom resource:

    kubectl patch greeting hello \
      --type merge \
      -p '{"spec":{"message":"Greeting updated!"}}'

Check the ConfigMap:

    kubectl get configmap hello-greeting \
      -o jsonpath='{.data.message}'

Result:

    Greeting updated!

No special "update handler" exists.

Instead:

    Greeting changes
          ↓
    watch queues reconcile request
          ↓
    Reconcile reads Greeting
          ↓
    CreateOrUpdate compares ConfigMap
          ↓
    ConfigMap converges to desired state

---

## 15. Test self-healing

This is the more interesting experiment.

Delete the ConfigMap manually:

    kubectl delete configmap hello-greeting

Then:

    kubectl get configmap hello-greeting

The controller should recreate it.

Why?

Because:

    .Owns(&corev1.ConfigMap{})

observes the change, associates the deleted object with its owner, and queues the corresponding `Greeting` reconciliation.

The controller sees:

    desired:
      hello-greeting should exist

    actual:
      hello-greeting doesn't exist

Therefore:

    create hello-greeting

This is the fundamental Kubernetes controller model.

---

## 16. Test garbage collection

Now delete the custom resource itself:

    kubectl delete greeting hello

Then:

    kubectl get configmap hello-greeting

The ConfigMap should disappear as well because it has an owner reference pointing to the `Greeting`.

That means our controller didn't need this kind of imperative cleanup:

    if greetingDeleted {
        deleteConfigMap()
    }

Kubernetes garbage collection handles the owned resource.

---

## 17. Understand the complete architecture

The architecture now looks like this:

```
                      Kubernetes API Server
                               │
                ┌──────────────┴──────────────┐
                │                             │
          Greeting CR                    ConfigMap
                │                             ▲
                │ watch                       │
                ▼                             │
        controller-runtime                    │
                │                             │
                ▼                             │
        workqueue request                     │
       namespace/default                      │
            name/hello                        │
                │                             │
                ▼                             │
          Reconcile()                         │
                │                             │
                ├── GET Greeting              │
                │                             │
                ├── calculate desired CM      │
                │                             │
                ├── CreateOrUpdate ───────────┘
                │
                └── Status().Update()
```

There are effectively three layers:

    API
    │
    ├── GreetingSpec
    ├── GreetingStatus
    └── CRD schema

    Controller
    │
    ├── Watches
    ├── Work queue
    └── Reconcile()

    Managed resources
    │
    └── ConfigMap

The manager supplied by controller-runtime handles shared facilities such as caches, Kubernetes clients, controllers, and graceful shutdown. ([Go Packages](https://pkg.go.dev/sigs.k8s.io/controller-runtime?utm_source=chatgpt.com "controllerruntime package - sigs.k8s.io/controller-runtime - Go Packages"))

---

## 18. The most important controller rule: idempotency

Suppose Kubernetes invokes:

    Reconcile(default/hello)

twenty times.

You shouldn't end up with:

    20 ConfigMaps
    20 Deployments
    20 external API calls

Your reconciliation should converge to:

    exactly the state described by spec

That's why code such as:

    controllerutil.CreateOrUpdate(...)

is preferable to unconditional:

    r.Create(...)

A useful mental model is:

    Reconcile(desiredState, actualState)
        -> newActualState

rather than:

    HandleCreateEvent()
    HandleUpdateEvent()
    HandleDeleteEvent()

---

## 19. Deploy the controller inside Kubernetes

So far:

    make run

runs the controller on your computer.

For a real operator, build its container image.

For example, assuming a registry:

    export IMG=ghcr.io/YOUR_USER/greeting-operator:v0.1.0

Build:

    make docker-build IMG=$IMG

Push:

    make docker-push IMG=$IMG

Deploy:

    make deploy IMG=$IMG

Kubebuilder's generated deployment includes the manager, RBAC, service account, CRD/Kustomize configuration, and related resources. The current official workflow likewise uses `make docker-build docker-push` followed by `make deploy`. ([Kubebuilder Book](https://book.kubebuilder.io/quick-start.html?utm_source=chatgpt.com "Quick Start - The Kubebuilder Book"))

Check:

    kubectl get pods -A | grep greeting

Then you no longer need:

    make run

because the controller runs as a Pod.

---

## 20. Useful debugging commands

List CRDs:

    kubectl get crd

Inspect our CRD:

    kubectl describe crd greetings.demo.example.com

List custom resources:

    kubectl get greetings -A

Watch changes:

    kubectl get greetings -w

Inspect one:

    kubectl describe greeting hello

View ConfigMaps:

    kubectl get configmap

Check owner references:

    kubectl get configmap hello-greeting \
      -o jsonpath='{.metadata.ownerReferences}'

Controller logs when deployed:

    kubectl logs -n greeting-operator-system \
      deployment/greeting-operator-controller-manager \
      -c manager

Exact generated namespace/deployment names can vary with project configuration.

---

## 21. The files that matter most

Once you're comfortable with the scaffold, most operator development boils down to two files:

    api/v1alpha1/greeting_types.go

defines:

    What should users be allowed to ask for?

And:

    internal/controller/greeting_controller.go

defines:

    How should Kubernetes make that request true?

Everything else largely supports those two concepts.

---

## 22. Where to go from here

Once this simple version makes sense, the natural progression is:

    1. CRD + ConfigMap
           ↓
    2. CRD + Deployment
           ↓
    3. Deployment + Service
           ↓
    4. Conditions in Status
           ↓
    5. validation/defaulting
           ↓
    6. finalizers
           ↓
    7. retries/requeue
           ↓
    8. events
           ↓
    9. webhooks
           ↓
    10. controller tests

A particularly useful next exercise is changing `Greeting` into something like:

    apiVersion: apps.example.com/v1alpha1
    kind: WebApp
    metadata:
      name: nginx-demo
    spec:
      image: nginx:1.29
      replicas: 3
      port: 80

and having the controller manage:

    WebApp
      │
      ├── Deployment
      │      └── Pods
      │
      └── Service

That moves from a teaching CRD to the core structure used by real Kubernetes operators.

The key concept to retain is:

```
                 spec
                  │
                  ▼
           desired state
                  │
                  ▼
             Controller
             Reconcile()
                  │
                  ▼
            actual state
                  │
                  ▼
                status
```

**`spec` says what should be true. The reconciler makes it true. `status` reports what is true.** That's the foundation of CRD/controller development in Kubernetes. ([Kubernetes](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/?utm_source=chatgpt.com "Custom Resources | Kubernetes"))
