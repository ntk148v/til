# Attach vs Exec

Source: <https://iximiuz.com/en/posts/containers-101-attach-vs-exec/>

![](https://iximiuz.com/containers-101-attach-vs-exec/docker-containerd-runc-2000-opt.png)

## 1. `attach`

- Docker came up with an idea of putting an extra process between the container and the rest of the system, called a container runtime shim. The container manager actually starts a shim process, that in turn, uses an OCI-compatible runtime (e.g.runc) to start the actual container.

```shell
$ docker run --name nginx  -d nginx
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
32ba157a56ed   nginx     "/docker-entrypoint.…"   12 seconds ago   Up 11 seconds   80/tcp    nginx
$ ps axfo pid,ppid,command
# ...
# Parent PID of shim is 1
 106086       1 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 32ba157a56eda526b4ce4214ea65ed5d1095154dfd04eaa5fd4daf539c758cf8 -address /run/containerd/containerd.sock
 106106  106086  \_ nginx: master process nginx -g daemon off;
 106165  106106      \_ nginx: worker process
 106166  106106      \_ nginx: worker process
 106167  106106      \_ nginx: worker process
 106168  106106      \_ nginx: worker process
 106169  106106      \_ nginx: worker process
 106170  106106      \_ nginx: worker process
```

- The shim process that becomes a daemon - it's reparented to PID 1, and its stdio streams are closed:
  - The shim takes control over the container's stdio streams.
  - The daemonized shim process reads from the container's stdout and stderr and dumps the read bytes to the log driver.
  - By default, the shim closes the container's stdin stream unless `-i` was passed to the corresponding `docker run` command.
  - Container runtime shim actually acts as a server, so when you run `docker attach <container>`

  ```unknown
  terminal <-> docker <-> dockerd <-> shim <-> container's stdio streams
  ```

![](https://iximiuz.com/containers-101-attach-vs-exec/docker-attach-2000-opt.png)

- Difference between `attach` and `logs`:
  - The `logs` command provides various options to filter the logs while `attach` in that regard acts as a simple `tail`.
  - The stream established by the `logs` command is always undirectional and connected to the container's logs.

## 2. `exec`

- You can `attach`-ing to an existing container (read, process). However, the `exec` command starts a totally new container. It is the form of the `run` command (create + start).
- The trick here is that the auxiliary container created by the `exec` command shares all the isolation boundaries of the target container (_net, pid, mount_,... namespaces, same cgroups hierarchy, etc) -> it feels like _running a command in a running container_ (`docker exec -h`).

```shell
Usage:  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

Execute a command in a running container
```

- When `exec`-ing, the relay looks quite similarly:

```unknown
terminal <-> docker-cli <-> dockerd <-> shim <-> command's stdio streams
```

![](https://iximiuz.com/containers-101-attach-vs-exec/docker-exec-2000-opt.png)
