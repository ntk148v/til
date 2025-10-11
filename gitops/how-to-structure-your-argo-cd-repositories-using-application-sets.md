# How to Structure your ArgoCD repositories using Application Sets

Source: <https://codefresh.io/blog/how-to-structure-your-argo-cd-repositories-using-application-sets/>

Table of Contents

- [How to Structure your ArgoCD repositories using Application Sets](#how-to-structure-your-argocd-repositories-using-application-sets)
  - [1. The different type of manifests](#1-the-different-type-of-manifests)
  - [Anti-pattern 1 - Mixing different types of manifests](#anti-pattern-1---mixing-different-types-of-manifests)
  - [Anti-pattern 2 – Working at the wrong abstraction level](#anti-pattern-2--working-at-the-wrong-abstraction-level)
  - [Anti-pattern 3 - Using templating at different/multiple levels](#anti-pattern-3---using-templating-at-differentmultiple-levels)
  - [Anti-pattern 4 - Not using Application Sets](#anti-pattern-4---not-using-application-sets)
  - [Best practice - Use three-level structure](#best-practice---use-three-level-structure)
  - [Best practice - use a Git repository per team](#best-practice---use-a-git-repository-per-team)
  - [What about infrastructure applications (categories 3 and 4)?](#what-about-infrastructure-applications-categories-3-and-4)

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

An ArgoCD application is NOT a reusable box that can be used to run arbitrary applications. The whole point of GitOps is to have a clear history of events for what an application did. But if you treat the application CRD as a generic unit of work that you can point to completely different manifests you lose one of the main benefits of GitOps.

Also in most cases, you should change the underlying Kubernetes manifests themselves instead of the CRD. For example, instead of changing the targetRevision field to a branch that has a newer image of the application, you should instead change the application image directly on the Kubernetes deployment resource that is pointed by the Argo CRD.

## Anti-pattern 3 - Using templating at different/multiple levels

A close relative of the previous anti-pattern is to apply templating facilities at the Application CRDs (category 2). Helm and Kustomize are already very powerful tools and can cover most cases with templating the main Kubernetes manifests (category 1).

The problem starts when people try to template Application CRDs, as they try to solve the issues created by the previous anti-pattern. The classic example here is when a team creates a Helm chart containing Application CRDs which themselves point to the Helm charts of the Kubernetes manifests. So now you are trying to apply Helm templates into two different levels at the same time. And as your Argo CD footprint grows, it is very difficult for newcomers to understand how your manifests are structured.

## Anti-pattern 4 - Not using Application Sets

Ideally, you shouldn’t need to create Application CRDs at all.

Application Sets can take care of the creation of all your application manifests (category 2) for you. For example, if you have 20 applications and 5 clusters, you can have a SINGLE application set file that will autogenerate the 100 combinations for your Argo CD applications.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-git
spec:
  generators:
    # matrix 'parent' generator
    - matrix:
        generators:
          # Git generator, 'child' #1
          - git:
              repoURL: https://github.com/codefresh-contrib/gitops-cert-level-2-examples.git
              revision: HEAD
              directories:
                - path: application-sets/example-apps/*
          # cluster generator, 'child' #2
          - clusters: {}
  template:
    metadata:
      name: '{{path.basename}}-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/codefresh-contrib/gitops-cert-level-2-examples.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: '{{server}}'
        namespace: '{{path.basename}}'
```

This generator says “take all the apps under application-sets/example-apps and deploy them to all clusters currently defined in Argo CD”.  It doesn’t matter how many clusters are currently connected or how many applications exist in the Git repo. The Application Set generator will automatically create all the possible combinations and also continuously redeploy as you add new clusters or new applications.

## Best practice - Use three-level structure

![](https://codefresh.io/wp-content/uploads/2024/05/hierarchy-of-manifests-1024x732.png)

- At the lowest level we have the Kubernetes manifests that define how the application runs (category 1).
- One level above, we have the ApplicationSet. These wrap the main Kubernetes manifests into ArgoCD applications (category 2).
- Last, as an optional component you can group all your application sets in an App-of-App that will help you bootstrap a completely empty cluster with all apps.

An example repo: <https://github.com/kostis-codefresh/many-appsets-demo>

![](https://codefresh.io/wp-content/uploads/2024/05/levels-.png)

The “apps” directory holds the standard Kubernetes manifests. We are using Kustomize for this example. For each application, there is an overlay ONLY for the applicable environments.

![](https://codefresh.io/wp-content/uploads/2024/05/apps.png)

It is important to note that if you look at the overall structure each environment is placed on the directory “`apps/<name-of-app>/envs/<name-of-env>`”

In the appsets folder, we keep all our application sets. Each application set simply mentions the overlays defined in the Kubernetes manifest. This application set says the following:

> Go to the apps folder. Search all folders that contain an application and if they have a subfolder envs/qa then create an Argo CD application.
> This appset will only deploy to the QA cluster applications with "qa" overlays. Applications without this overlay will not be deployed.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-qa-appset
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
    repoURL: https://github.com/kostis-codefresh/many-appsets-demo.git
    revision: HEAD
    directories:
    - path: apps/*/envs/qa
  template:
  metadata:
    name: '{{index .path.segments 1}}-{{index .path.segments 3}}'
  spec:
    # The project the application belongs to.
    project: default

    # Source of the application manifests
    source:
      repoURL: https://github.com/kostis-codefresh/many-appsets-demo.git
      targetRevision: HEAD
      path: '{{.path.path}}'

    # Destination cluster and namespace to deploy the application
    destination:
      server: https://kubernetes.default.svc
      namespace: '{{index .path.segments 1}}-{{index .path.segments 3}}'
```

## Best practice - use a Git repository per team

> Have multiple Git repositories. Ideally one for each team or each department. Again the basic question you should always asks yourself is if the applications contained in the Git repository are related in some way.

![](https://codefresh.io/wp-content/uploads/2024/05/team-topology-1024x808.png)

## What about infrastructure applications (categories 3 and 4)?

You can store infrastructure manifests in the same way as developer applications using the 3-level structure mentioned in the previous sections. It is imperative however that you don’t mix those manifests with those that developers need. And the best way to separate them is to have another Git repository.

Don’t mix infrastructure applications and developer applications in the same Git repo.

![](https://codefresh.io/wp-content/uploads/2024/05/all-teams-topology-1020x1024.png)
