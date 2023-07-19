# Exit Status

The exit code from `docker run` gives information about why the container failed to run or why it exited. When `docker run` exits with a non-zero code, the exit codes follow the [chroot](../linux/exit-code.md) standard.

**_125_** if the error is with Docker daemon **_itself_**

```console
$ docker run --foo busybox; echo $?

flag provided but not defined: --foo
See 'docker run --help'.
125
```

**_126_** if the **_contained command_** cannot be invoked

```console
$ docker run busybox /etc; echo $?

docker: Error response from daemon: Container command '/etc' could not be invoked.
126
```

**_127_** if the **_contained command_** cannot be found

```console
$ docker run busybox foo; echo $?

docker: Error response from daemon: Container command 'foo' not found or does not exist.
127
```

**_Exit code_** of **_contained command_** otherwise

```console
$ docker run busybox /bin/sh -c 'exit 3'
$ echo $?
3
```
