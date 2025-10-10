# How to Structure your ArgoCD repositories using Application Sets

Source: <https://codefresh.io/blog/how-to-structure-your-argo-cd-repositories-using-application-sets/>

Table of Contents

## 1. The different type of manifests

| Category | Description                    | Type                                      | Change Frequency | Target Users      |
| -------- | ------------------------------ | ----------------------------------------- | ---------------- | ----------------- |
| 1        | Developer Kubernetes manifests | Helm, Kustomize or plain manifests in Git | Very often       | Developers mostly |

|2 |Developer Argo CD manifests| Argo CD app and Application Set| Almost never |Operators/Developers|
|3 |Infrastructure Kubernetes manifests| Usually external Helm charts (in Git or Helm repo)| Sometimes |Operators|
|4 |Infrastructure |Argo CD manifests Argo CD app and Application Set |Almost never|Operators|

- The first category is the standard Kubernetes resources (deployment, service, ingress, config, secrets etc) that are defined by any Kubernetes cluster.
  - Change very often (update container image version, some kind of configuration in a configmap or secret)
- The second category is the ArgoCD application manifests.
  - These are essentially policy configurations referencing the source of truth for an application (the first type of manifests) and the destination and sync policies for that application.
- The third and fourth category is the same thing as the first and second, but this time we are talking about infrastructure applications (cert manager, nginx, coredns, prometheus etc) instead of in-house applications that your developers create.

## Anti-pattern 1 - Mixing different types of manifests

One of the crucial points of your manifests is to have a very clear separation between Kubernetes (category 1) and Argo CD resources (category 2). For convenience, Argo CD has several features that allow you to mix both categories. Even though this is needed in some corner cases, we advise AGAINST mixing different types of manifests.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-helm-override
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/example-org/example-repo.git
    targetRevision: HEAD
    path: my-chart

    helm:
      # DONT DO THIS
      parameters:
        - name: "my-example-setting-1"
          value: my-value1
        - name: "my-example-setting-2"
          value: "my-value2"
          forceString: true # ensures that value is treated as a string

      # DONT DO THIS
      values: |
        ingress:
          enabled: true
          path: /
          hosts:
            - mydomain.example.com

      # DONT DO THIS
      valuesObject:
        image:
          repository: docker.io/example/my-app
          tag: 0.1
          pullPolicy: IfNotPresent
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
```

This manifest is two things in one. The main file is about an Argo app (category 2) but the “helm” property actually contains values for the Kubernetes application (category 1).

This manifest can be easily corrected by putting all the parameters in a values file in the same Git repository as the chart like this.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-helm-override
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/example-org/example-repo.git
    targetRevision: HEAD
    path: my-chart
    helm:
      ## DO THIS (values in Git on their own)
      valueFiles:
        - values-production.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
```

Dividing the two types of manifests is a good practice as you see in the later sections, but it should be obvious from the table shown in the previous section that mixing things with different life cycles is always a recipe for trouble.

Mixing the different types of manifests has several different challenges:

- It makes manifests harder to understand for all involved parties
- If confuses the requirements for people that use manifests (e.g. devs) vs those that create manifests (i.e. admins/operators)
- It couples your manifests to specific Argo CD features
- It make separating security concerns more complex
- It results in more moving parts and difficult to debug scenarios
- It makes local testing for developers much more difficult.

## Anti-pattern 2 – Working at the wrong abstraction level

The purpose of Argo CD application CRDs is to work as a “wrapper” or “pointer” to the main Kubernetes manifests. The thing that matters is the Kubernetes manifests(category 1) and Argo CD manifests(category 2) should always have a supporting role.

In the ideal case, you should create an Application manifest once to define which Git repo goes to which cluster and then never touch this file again (this is why in the previous table the change frequency is “almost never”).

The classic example is where they use a CI process to automatically update the “targetRevision” (or “path”) field in an Application.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  ## DONT DO THIS
  name: my-ever-changing-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example-org/example-repo.git
    targetRevision: dev
    ## earlier it was "targetRevision: staging" and before that it was "targetRevision: 1.0.0",
    ## and even earlier it was "targetRevision: 1.0.0-rc"
    path: my-staging-app
    ## Previously it was "path: my-qa-app"
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
```
