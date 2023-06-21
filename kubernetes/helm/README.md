# Helm

Source:

- <https://www.baeldung.com/ops/kubernetes-helm>

Table of contents:

- [Helm](#helm)
  - [1. Introduction](#1-introduction)
  - [2. Key concepts](#2-key-concepts)
  - [3. First Chart](#3-first-chart)
  - [3. Manage Charts](#3-manage-charts)

## 1. Introduction

- Helm is a package manager for Kubernetes applications.
- Architecture:

  - Helm 2:

    - Primaryly on a client-server architecture that comprises of a client and an in-cluster server.
    - Tiller server: Helm manages the Kubernetes application through Tiller server installed within a Kubernetes cluster. Tiller interacts with the Kubernetes API server to install.
    - Helm client: Helm provides a command-line interface for users to work with Helm Charts.

    ![](https://www.baeldung.com/wp-content/uploads/2019/03/Helm-2-Architecture.jpg)

  - Helm 3:

    - Has moved onto a completely client-only architecture, where the in-clusterserver has been removed.
    - Helm client interacts directly with the Kubernetes API server.

    ![](https://www.baeldung.com/wp-content/uploads/2019/03/Helm-3-Architecture.jpg)

## 2. Key concepts

- Helm manages Kubernetes resource packages through **Charts**:
  - Charts are basically packaging format of Helm.
  - A chart is a collection of files organized in a specific directory structure.
  - Chart is a bundle of information necessary to create an instance of a Kuberntes configuration.
  - The **config** contains config info to create a releasable object.
  - The **release** is a running instance of a chart, combined with a specific config.
- Helm tracks an installed charts in the Kubernetes cluster using releases.
- Share charts as archives through **repositories**.

## 3. First Chart

- Create new chart:

```shell
helm create hello-world
```

- Directory structure:

```shell
tree hello-world

hello-world
├── charts # An optional directory that may contain sub-charts
├── Chart.yaml # main file that contains the description of chart
├── templates # Directory where Kubernete resources are defined as templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml # the file that contains the default values for our chart

3 directories, 10 files
```

- A few templates for common Kubernetes resources have already been created. Helm makes use of the Go template language and extends that to something called Helm template language. During the evaluation, every file inside the template directory is submitted to the template rendering engine. This is where the template directive injects actual values into the templates.

## 3. Manage Charts

- Helm lint: run a battery of tests to ensure that the chart is well-formed.

```shell
helm lint hello-world
```

- Helm template: render template locally for quick feedback.

```shell
helm template hello-world
```

- Helm install: install the chart into the Kubernetes cluster.

```shell
helm install --name hello-world ./hello-world
# Uninstall
helm uninstall hello-world
```

- Helm list: get the installed charts.

```shell
helm ls
```

- Helm upgrade: install the updated version.

```shell
helm upgrade hello-world ./hello-world
# Rollback
helm rollback hello-world 1
```

## 4. Helm Charts Best practices

- Document your chart by adding comment and a README file as documenation is essential for ensuring maintainable Helm charts.
- Should name the Kubernetes manifest files after the Kind of object (deployment, service, secret,...)
- Put the chart name in lowercase onlyand if it has more than a word then separate out with hyphens (-).
- In values.yaml file field name should be in lowercase.
- Always wrap the string values between quote signs.
