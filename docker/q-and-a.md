# Q & A

## Q: How can Docker run distros with different kernels?

Source: https://stackoverflow.com/questions/32841982/how-can-docker-run-distros-with-different-kernels

A: Because the kernel is the same and will support the Docker engine to run all those container images: the host kernel should be 3.10 or more, but its [list of system call](https://stackoverflow.com/questions/32841982/how-can-docker-run-distros-with-different-kernels) is fairly stable.

If your host kernel is "compatible enough" with the software in the container you want to run it will work; otherwise it won't. So what does "compatible enough" mean? It depends on what requests the program makes of the kernel (system calls) and what features it expects the kernel to support. Some programs make requests that will break things; others don't. For example, on an Ubuntu 18.04 (kernel 4.19) or similar host:

- `docker run centos:7 bash` - ok.
- `docker run centos:6 bash` - fails with exit code 139, meaning it terminated with a segmentation violation signal; this is because the 4.19 kernel doesn't support something that build of bash tried to do.
- `docker run centos:6 ls` - works fine, because it's not making a request the kernel can't handle, as bash was.

## Q: Why kernel version doesn't match Ubuntu version in a Docker container?

A: There's no kernel inside a container. Even if you install a kernel, it won't be loaded when the container starts. The very purpose of a container is to isolate processes without the need to run a new kernel.
