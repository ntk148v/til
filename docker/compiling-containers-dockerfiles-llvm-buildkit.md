# Compiling Containers - Dockerfiles, LLVM and BuildKit

Source: https://blog.earthly.dev/compiling-containers-dockerfiles-llvm-and-buildkit/

- An image ~ an executable, a container ~ a process. Run multiple containers from 1 image, a running image isn't an image at all but a container.

![](https://blog.earthly.dev/content/images/2021/03/1-2.png)

- [BuildKit](https://github.com/moby/buildkit) is a compiler, just like [LLVM](https://en.wikipedia.org/wiki/LLVM).

![](https://blog.earthly.dev/content/images/2021/03/099.png)

- Docker build uses BuildKit, to turn a Dockerfile into a docker image, OCI image or another image format.

![](https://blog.earthly.dev/content/images/2021/03/buildctl-2.png)

- A traditional compiler takes code in a high-level language and lowers it to a lower-level language.

![](https://blog.earthly.dev/content/images/2021/03/compilingc.png)

- Creating an image from a dockerfile works a similar way.

![](https://blog.earthly.dev/content/images/2021/03/build-an-image.png)

- Computer hardware is not a singular thing (machine architecture) -> Split complication into phases (frontend, backend and middle - optimizer).

![](https://blog.earthly.dev/content/images/2021/03/3stagebuild.png)

- LLVM -> ARM, x86, and many other machine architectures using LLVM Intermediate Representation (IR) as a standard protocol. To create a new backend, write a translator from LLVM IR to target machine code. If you can write a translation from your language to LLVM IR, LLVM can translate that IR into machine code for all the backends it supports. This translation function is the primary job of a compiler frontend.

![](https://blog.earthly.dev/content/images/2021/03/backends.png)

![](https://blog.earthly.dev/content/images/2021/03/frontends-2.png)

- Images, unlike executables, have their own isolated filesystem.
  - The task of building an image can have varying syntax and the result must target several machine architectures.
  - BuildKit has its own IR, LLB. LLB is to Dockerfile what LLVM IR is to C.

![](https://blog.earthly.dev/content/images/2021/03/LLB-IR.png)

![](https://blog.earthly.dev/content/images/2021/03/Send-LLB.png)

- Dockerfile frontend:

![](https://blog.earthly.dev/content/images/2021/03/controlflow.png)
