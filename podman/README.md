# Podman

Source:

- <https://podman.io/>
- <https://developers.redhat.com/articles/podman-next-generation-linux-container-tools>

- [Podman](#podman)
  - [1. Introduction](#1-introduction)
  - [2. Docker vs Podman](#2-docker-vs-podman)
  - [3. Usage](#3-usage)

## 1. Introduction

- POD MANager.
- Daemonless.
- A tool for managing OCI containers and images, volumes mounted into those containers, and pods made from groups of containers.
- Based on libpod, a library for container lifecycle management that is also contained in this repository.
- Relies on an OCI compliant Container Runtime (runc, crun, runv, etc) to interface with the operating system and create the running containers.
- Able to run rootless containers. A rootless container is a concept of running and managing containers without root privileges. From a security standpoint, rootless containers add an additional layer of security by no allowing root access even if the containers gets compromised by an attacker. (FYI, Docker also supports rootless mode)
- Move from Docker CLI to Podman.

```shell
alias docker=podman
```

## 2. Docker vs Podman

![](https://media-exp1.licdn.com/dms/image/C4E22AQFwP9ecfBb81g/feedshare-shrink_800/0/1636952989088?e=1666828800&v=beta&t=2XsdsYOtJsWg3QzkKgq7Umq0V2hE6U03fT8xtPC1QNo)

| Podman                                                                                                                                                                                        | Docker                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Podman has a modular approach, relying on specialized tools for specific duties                                                                                                               | Docker is a monolithic, powerful, independent tool with all the benefits and drawbacks implied, handling all of the containerization takss throughout their entire cycle |
| Daemonless                                                                                                                                                                                    | Docker has a daemon (containerd). The Docker CLI interacts with the daemon to manage containers                                                                          |
| Interacts with the Linux kernel directly through OCI compliant Container runtime                                                                                                              | Docker daemon owns all the child processes of running containers                                                                                                         |
| Can deploy pods with multiple containers. The same pod manifest can be used in Kubernetes. Also, you can deploy Kubernetes pod manifest as a Pod pod                                          | There is no concept of a pod in Docker                                                                                                                                   |
| Can run rootless without any additional configurations                                                                                                                                        | Docker rootless mode requires additional configurations                                                                                                                  |
| Podman uses [buildah](https://buildah.io/) to build container images, and [skopeo](https://github.com/containers/skopeo) for moving container images between registries and container engines | Docker daemon can do all of these tasks                                                                                                                                  |
| Podman uses systemd to create control units for existing containers or to generate new ones.                                                                                                  | Docker uses its daemon                                                                                                                                                   |

## 3. Usage

- Check [here](https://docs.podman.io/en/latest/Commands.html).
- Some interesting commands:

```shell
# Create empty pod
podman pod create --name demo-pod
podman pod ls
# Add containers to the podman pod
podman run -dt --pod demo-pod nginx
podman pod ls
# For empty pod, there will be a `k8s.gcr.io/pause` container added to it
podman ps -a --pod
# Start, stop, remove containers
podman start <container-id>
podman stop <container-id>
podman rm <container-id>
# Create pod with containers
podman run -dt --pod new:frontend -p 8080:80 nginx
# Start, stop, delete pod
podman pod start <podname>
podman pod stop <podname>
podman pod rm -f <podname>
# Generate Kubernetes YAMLs from Podman pod definitions
podman generate kube frontend >> frontend.yaml
# Create Podman pod from YAML
podman play kube frontend.yaml
```
