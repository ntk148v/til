# Podman

Source:

- <https://podman.io/>
- <https://developers.redhat.com/articles/podman-next-generation-linux-container-tools>
- <https://www.redhat.com/en/topics/containers/what-is-podman>
- <https://linuxhandbook.com/docker-vs-podman/>

Table of contents:

- [Podman](#podman)
  - [1. Overview](#1-overview)
  - [2. What are Pods?](#2-what-are-pods)
  - [3. Rootless and systemd integration](#3-rootless-and-systemd-integration)
  - [4. Docker vs. Podman](#4-docker-vs-podman)
    - [4.1. daemon-based vs. daemon-less](#41-daemon-based-vs-daemon-less)
    - [4.2. Security](#42-security)
    - [4.3. All in one vs. segregated](#43-all-in-one-vs-segregated)
  - [5. Usage](#5-usage)

## 1. Overview

- POD MANager.
- Daemonless.
- A tool for managing OCI containers and images, volumes mounted into those containers, and pods made from groups of containers.
- Based on libpod, a library for container lifecycle management that is also contained in this repository.
- Relies on an OCI compliant Container Runtime (runc, crun, runv, etc) to interface with the operating system and create the running containers.
- Able to run rootless containers. A rootless container is a concept of running and managing containers without root privileges. From a security standpoint, rootless containers add an additional layer of security by no allowing root access even if the containers gets compromised by an attacker. (FYI, Docker also supports rootless mode).

## 2. What are Pods?

- Pods are groups of containers that run together and share the same resources, similar to Kubernetes pods.
  - Each pod is composed of 1 infra container and any number of regular containers.

  ![](https://phoenixnap.com/kb/wp-content/uploads/2022/03/podman-pod-visualisation.png)
  - The purpose of the infra container, which by default runs the `k8s.gcr.io/pause` image, is to keep the pod alive and maintain the namespaces associated with the pod.
  - Each container has a dedicated container monitor, a service that monitors container processes and logs exit codes if the containers die.

- Podman manages these pods via a simple CLI and the libpod library, which provides application programming interfaces (APIs) for manage containers, pods, container images, and volumes.

## 3. Rootless and systemd integration

- Podman stands out from other container engines because it’s **daemonless**, meaning it doesn't rely on a process with root privileges to run containers (**rootless**).
- The benefits of rootless containers are:
  - The orchestrator, runtime, or container engine can become compromised. Rootless containers ensure that even in those circumstances, attackers cannot gain root privileges for the host.
  - Multiple unprivileged users can run containers on the same system.
  - Inside a rootless container, code can utilize root privileges without running as the root user of the host system.
- Systemd integration:
  - The integration with systemd makes Podman a practical solution for Linux container management.
  - Podman integrates with systemd in two ways:
    - systemd can run inside a Podman container. This feature makes it much easier to run containers whose packages require systemd for service and dependencies management.
    - Podman can run as part of the systemd services. The traditional Linux fork-exec architecture implemented by Podman integrates well with Linux systems and allows Podman to communicate with systemd efficiently.

## 4. Docker vs. Podman

| Podman                                                                                                                                                                                        | Docker                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Podman has a modular approach, relying on specialized tools for specific duties                                                                                                               | Docker is a monolithic, powerful, independent tool with all the benefits and drawbacks implied, handling all of the containerization takss throughout their entire cycle |
| Daemonless                                                                                                                                                                                    | Docker has a daemon (containerd). The Docker CLI interacts with the daemon to manage containers                                                                          |
| Interacts with the Linux kernel directly through OCI compliant Container runtime                                                                                                              | Docker daemon owns all the child processes of running containers                                                                                                         |
| Can deploy pods with multiple containers. The same pod manifest can be used in Kubernetes. Also, you can deploy Kubernetes pod manifest as a Pod pod                                          | There is no concept of a pod in Docker                                                                                                                                   |
| Can run rootless without any additional configurations                                                                                                                                        | Docker rootless mode requires additional configurations                                                                                                                  |
| Podman uses [buildah](https://buildah.io/) to build container images, and [skopeo](https://github.com/containers/skopeo) for moving container images between registries and container engines | Docker daemon can do all of these tasks                                                                                                                                  |
| Podman uses systemd to create control units for existing containers or to generate new ones.                                                                                                  | Docker uses its daemon                                                                                                                                                   |

### 4.1. daemon-based vs. daemon-less

- Docker's core runs as a daemon `dockerd`. Meaning, it's always running in the background, managing the containers.
- Meanwhile, Podman is like your average program; once you perform an action (start/stop a container) using Podman, it exits.
- Podman can be used with systemd to achieve the same thing, and it has its own benefits:
  - If the Docker daemon crashes, the containers are in an uncertain state. This is prevented by making Podman daemon-less.
  - Hooking Podman with systemd allows you to also update running containers with minimal downtime. You can also recover from any bad updates.

### 4.2. Security

- Podman is pitched as a more secure alternative to Docker.
- With Podman, you have the ability to run a container without requiring any root privileges. That means, even if a container image has a security vulnerability, only the user who owns that container is compromised.
- Docker recently got support for [rootless execution of containers](https://linuxhandbook.com/rootless-docker/), but it has a few missing features. Namely, AppArmor support is absent. AppArmor is Debian's and Ubuntu's default Mandatory Access Control (MAC) system.

### 4.3. All in one vs. segregated

- Docker has an "all in one" approach and Podman is different, you have three separate binaries.
- To build images -> `buildah`.
- To publish image to a registry -> `skopeo`.
- To manage containers -> `podman`.

## 5. Usage

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

# Autostarting Podman containers with systemd
# podman generate systemd --new --name CONTAINER_NAME
$ podman generate systemd --new --name chitragupta-db -f
/home/pratham/container-chitragupta-db.service

$ ls *.service
container-chitragupta-db.service

# Move the systemd service file to a specific location
$ mv -v container-chitragupta-db.service ~/.config/systemd/user/
renamed 'container-chitragupta-db.service' -> '/home/pratham/.config/systemd/user/container-chitragupta-db.service'
# Enable the container's systemd service
sudo systemctl daemon-reload
# or
systemctl --user daemon-reload
sudo systemctl enable SERVICE_NAME.service
systemctl --user enable SERVICE_NAME.service
# Enable podman restart service
systemctl --user enable podman-restart.service
```
