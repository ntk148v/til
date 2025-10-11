# Kustomize

Source:

- <https://devopscube.com/kustomize-tutorial/>
- <https://codefresh.io/blog/applied-gitops-with-kustomize/>

Table of contents:

- [Kustomize](#kustomize)
  - [1. Introduction](#1-introduction)

## 1. Introduction

- Kustomize is a standalone tool to customize Kubernetes objects through kustomization file.
- Since 1.14, Kubectl also supports the management of Kubernetes objects using a kustomization file.
- It has the following features to manage application configuration files:
  - generating resources from other sources
  - setting cross-cutting fields for resources
  - composing and customizing collections of resources
- Kustomize settings are defined in a kustomization.yaml file. Kustomize is also integrated with kubectl. With Kustomize, you can configure raw, template-free YAML files, which allows you to modify settings between deployment and production easily. This enables troubleshooting misconfigurations and keeps use-case-specific customization overrides intact.
- Kustomize also allows you to scale easily by reusing a base file across all your environments (development, production, staging, etc.) and then overlay specifications for each.
  - **Base layer**: this layer specifies the most common resources and original configuration.
  - **Overlays layer**: this layer specifies use-case-specific resources by utilizing patches to override other kustomization files and Kubernetes manifests.

## 2. Benefits

- Reusability: you can reuse one of the base files across all environments and overlay specifications for each of those environments.
- Quick generation.
- Debug easily: using a YAML file allow easy debugging, along with patches that isolate configurations, allowing you to pinpoint the root cause of performance issues quickly.
- Kubernetes native configuration.

## 3. Sample

Checkout [demo](./demo).

![](https://codefresh.io/wp-content/uploads/2023/07/Screen-Shot-2021-12-01-at-10.32.44-AM-1.png)

- The base folder holds common resources, such as the deployment.yaml, service.yaml, configuration files. It contains the initial manifest and includes a namespace and label for the resources.
- The overlays folder: The overlays folder houses environment-specific overlays, which use patches to allow YAML files to be defined and overlaid on top of the base for any changes.
- kustomization.yaml: Each directory contains a kustomization file, which is essentially a list of resources or manifests that describes how to generate or transform Kubernetes objects. There are multiple fields that can be added, and when this list is injected, the kustomization action can be referenced as an overlay that refers to the base.

![](https://devopscube.com/content/images/2025/03/image-29-22.png)

./demo/base/kustomization.yaml

```yaml
commonLabels:
  app: demo

resources:
- deployment.yaml
- service.yaml
- configMap.yaml
```

./demo/overlays/staging/kustomization.yaml

```yaml
namePrefix: staging-
commonLabels:
 variant: staging
commonAnnotations:
  note: “Welcome to staging!”
bases:
- ../../base
patchesStrategicMerge:
- config-map.yaml
```

staging patch: add a configMap kustomization to change the server greeting from "Hello!" to "Kustomize rules!" (./demo/overlays/staging/config-map.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
 name: the-map
data:
 altGreeting: “Kustomize rules!”
 enableRisky: “true”
```

Overlays contain a kustomization.yaml, and can also include manifests as new or additional resources, or to patch resources. The kustomization file is what defines how the overlays should be applied to the base and this is what we refer to as a variant.
