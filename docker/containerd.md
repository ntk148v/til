# Containerd

Source:

- <https://github.com/containerd/containerd>

Table of contents:

- [Containerd](#containerd)
  - [1. Introduction](#1-introduction)
  - [2. Playground](#2-playground)
    - [2.1. Command line](#21-command-line)
    - [2.2. containerd library](#22-containerd-library)

## 1. Introduction

- containerd is an industry-standard container runtime with an emphasis on simplicity, robustness, and portability.
- It is available as a daemon for Linux and Windows, which can manage the complete container lifecycle of its host system: image transfer and storage, container execution and supervision, low-level storage and network attachments, etc.
- containerd is designed to be embedded into a larger system, rather than being used directly by developers or end-users.

![](https://github.com/containerd/containerd/raw/main/docs/historical/design/architecture.png)

- containerd began as part of Docker and was donated to CNCF. containerd remains in use today by Docker/moby/buildkit etc., and has many other [adopters](https://github.com/containerd/containerd/blob/main/ADOPTERS.md).

![](https://www.docker.com/wp-content/uploads/974cd631-b57e-470e-a944-78530aaa1a23-1.jpg)

## 2. Playground

### 2.1. Command line

- You can play with container using [ctr](https://github.com/containerd/containerd/tree/e1ad7791077916aac9c1f4981ad350f0e3fce719/cmd/ctr) which is a command-line client shipped as part of the containerd project.

```shell
$ ctr

NAME:
   ctr -
        __
  _____/ /______
 / ___/ __/ ___/
/ /__/ /_/ /
\___/\__/_/

containerd CLI


USAGE:
   ctr [global options] command [command options] [arguments...]

VERSION:
   1.6.20

DESCRIPTION:

ctr is an unsupported debug and administrative client for interacting
with the containerd daemon. Because it is unsupported, the commands,
options, and operations are not guaranteed to be backward compatible or
stable from release to release of the containerd project.

COMMANDS:
   plugins, plugin            provides information about containerd plugins
   version                    print the client and server versions
   containers, c, container   manage containers
   content                    manage content
   events, event              display containerd events
   images, image, i           manage images
   leases                     manage leases
   namespaces, namespace, ns  manage namespaces
   pprof                      provide golang pprof outputs for containerd
   run                        run a container
   snapshots, snapshot        manage snapshots
   tasks, t, task             manage tasks
   install                    install a new package
   oci                        OCI tools
   shim                       interact with a shim directly
   help, h                    Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug                      enable debug output in logs
   --address value, -a value    address for containerd's GRPC server (default: "/run/containerd/containerd.sock") [$CONTAINERD_ADDRESS]
   --timeout value              total timeout for ctr commands (default: 0s)
   --connect-timeout value      timeout for connecting to containerd (default: 0s)
   --namespace value, -n value  namespace to use with commands (default: "default") [$CONTAINERD_NAMESPACE]
   --help, -h                   show help
   --version, -v                print the version
```

- Working with images using ctr:

```shell
# Don't forget image's tag
$ ctr images pull docker.io/library/nginx:latest

docker.io/library/nginx:latest:                                                   resolved       |++++++++++++++++++++++++++++++++++++++|
index-sha256:2ab30d6ac53580a6db8b657abf0f68d75360ff5cc1670a85acb5bd85ba1b19c0:    done           |++++++++++++++++++++++++++++++++++++++|
manifest-sha256:bfb112db4075460ec042ce13e0b9c3ebd982f93ae0be155496d050bb70006750: done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:9862f2ee2e8cd9dab487d7dc2152a3f76cb503772dfb8e830973264340d6233e:    done           |++++++++++++++++++++++++++++++++++++++|
config-sha256:080ed0ed8312deca92e9a769b518cdfa20f5278359bd156f3469dd8fa532db6b:   done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:7f7f30930c6b1fa9e421ba5d234c3030a838740a22a42899d3df5f87e00ea94f:    done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:2836b727df80c28853d6c505a2c3a5959316e48b1cff42d98e70cb905b166c82:    done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:f1f26f5702560b7e591bef5c4d840f76a232bf13fd5aefc4e22077a1ae4440c7:    done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:e1eeb0f1c06b25695a5b9df587edf4bf12a5af9432696811dd8d5fcfd01d7949:    done           |++++++++++++++++++++++++++++++++++++++|
layer-sha256:86b2457cc2b0d68200061e3420623c010de5e6fb184e18328a46ef22dbba490a:    done           |++++++++++++++++++++++++++++++++++++++|
elapsed: 9.1 s                                                                    total:  53.4 M (5.9 MiB/s)
unpacking linux/amd64 sha256:2ab30d6ac53580a6db8b657abf0f68d75360ff5cc1670a85acb5bd85ba1b19c0...
done: 2.099057206s

$ ctr images ls

REF                            TYPE                                                      DIGEST                                                                  SIZE     PLATFORMS                                                                                               LABELS
docker.io/library/nginx:latest application/vnd.docker.distribution.manifest.list.v2+json sha256:2ab30d6ac53580a6db8b657abf0f68d75360ff5cc1670a85acb5bd85ba1b19c0 54.4 MiB linux/386,linux/amd64,linux/arm/v5,linux/arm/v7,linux/arm64/v8,linux/mips64le,linux/ppc64le,linux/s390x -

# Import existing images built with docker build
$ docker build -t app .

$ docker save -o app.tar app

$ ctr images import app.tar

# Mount images
$ mkdir /tmp/nginx

$ ctr images mount docker.io/library/nginx:latest /tmp/nginx

sha256:d78ffa8b3ff6145eb277087027ab2f07317ef3c8155dea0c68aba0be0dc9e357
/tmp/nginx

$ mount | grep nginx

overlay on /tmp/nginx type overlay (ro,relatime,lowerdir=/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/6/fs:/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/5/fs:/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/4/fs:/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/3/fs:/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/2/fs:/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/1/fs)

$ ls -la /tmp/nginx

# Or umount /tmp/nginx directly
$ ctr images unmount /tmp/nginx

# Remove image
$ ctr images remove docker.io/library/nginx:latest
```

- Working with containers using ctr:

```shell
$ ctr images pull docker.io/library/alpine:latest

$ ctr run --rm -t docker.io/library/alpine:latest alpine
/ #

# Open another terminal
$ ctr containers ls
CONTAINER    IMAGE                              RUNTIME
alpine       docker.io/library/alpine:latest    io.containerd.runc.v2

# or using the following command:
$ ctr containers create -t docker.io/library/alpine:latest alpine

$ ctr containers ls

$ ctr tasks ls
# empty

$ ctr tasks start alpine
/ #

# Open another terminal
$ ctr tasks ls
TASK      PID       STATUS
alpine    181772    RUNNING

# Stop container
$ ctr tasks kill -s 9 alpine

# Alternatively, remove running using:
$ ctr tasks rm -f alpine

$ ctr containers rm alpine
```

### 2.2. containerd library

Checkout [my testing repository](https://github.com/ntk148v/testing/blob/master/golang/containerd/main.go).
