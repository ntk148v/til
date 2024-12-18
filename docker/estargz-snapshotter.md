# Startup Containers in Lighting Speed with Lazy Image Distribution on Containerd

Source:

- <https://medium.com/nttlabs/startup-containers-in-lightning-speed-with-lazy-image-distribution-on-containerd-243d94522361>
- <https://github.com/containerd/stargz-snapshotter>
- <https://www.reddit.com/r/devops/comments/1grfchd/lazy_pulling_docker_images_for_80_faster_startup/>

## 1. Overview

Pulling image is one of the time-consuming steps in the container lifecycle. Research shows that time to take for pull operation accounts for 76% of container startup time [FAST'16](https://www.usenix.org/node/194431). _Stargz Snapshotter_ is an implementation of snapshotter which aims to solve this problem by _lazy pulling_. _Lazy pulling_ here means a container can run without waiting for the pull completion of the image and necessary chunks of the image are fetched on-demand.

[_eStargz_](/docs/stargz-estargz.md) is a lazily-pullable image format proposed by this project.
This is compatible to [OCI](https://github.com/opencontainers/image-spec/)/[Docker](https://github.com/moby/moby/blob/master/image/spec/v1.2.md) images so this can be pushed to standard container registries (e.g. ghcr.io) as well as this is _still runnable_ even on eStargz-agnostic runtimes including Docker.
eStargz format is based on [stargz image format by CRFS](https://github.com/google/crfs) but comes with additional features like runtime optimization and content verification.

<img src="https://github.com/containerd/stargz-snapshotter/blob/main/docs/images/benchmarking-result-ecdb227.png" width="600" alt="The benchmarking result on ecdb227">

- `legacy` shows the startup performance when we use containerd's default snapshotter (`overlayfs`) with images copied from `docker.io/library` without optimization.
  For this configuration, containerd pulls entire image contents and `pull` operation takes accordingly.
- When we use stargz snapshotter with eStargz-converted images but without any optimization (`estargz-noopt`) we are seeing performance improvement on the `pull` operation because containerd can start the container without waiting for the `pull` completion and fetch necessary chunks of the image on-demand. But at the same time, we see the performance drawback for `run` operation because each access to files takes extra time for fetching them from the registry.
- When we use [eStargz with optimization](https://github.com/containerd/stargz-snapshotter/blob/main/docs/ctr-remote.md) (`estargz`), we can mitigate the performance drawback observed in `estargz-noopt` images.
  This is because [stargz snapshotter prefetches and caches _likely accessed files_ during running the container](https://github.com/containerd/stargz-snapshotter/blob/main/docs/stargz-estargz.md). On the first container creation, stargz snapshotter waits for the prefetch completion so `create` sometimes takes longer than other types of image. But it's still shorter than waiting for downloading all files of all layers.

  - Lazy pulling can cause runtime performance overhead by on-demand fetching of each file. eStargz mitigates this by supporting prefetching of important files called _prioritized files_. For example, you have workload-based image optimization in Stargz Snapshotter, the workload is the runtime configuration defined in Dockerfile -> including entrypoint command, environment variables and user.

## 2. Core technologies

### 2.1. Stargz archive format

- For lazy image distribution, container runtimes need to download and extract file entries from layer blob, selectively.
- OCI/Docker image specs define layer types as tar or tar.gz archives which require scanning the entire blob even for taking single file entry.
- [Stargz](https://github.com/google/crfs) is an archive format proposed by Google. Stargz stands for _Seekable tar.gz_ with which can seek the archive and extract file entries selectively, without scanning the entire blob.

![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*aba_56ZY6N-3Y-JuIwllpg.png)

- By combining this with HTTP Range Request supported by OCI/Docker registry specs, container runtimes can selectively fetch file entries from the registry.
- stargz archive is still valid gzip so any container runtimes can treat stargz archived layers in the way just same as legacy "tar.gz" layers.

### 2.2. Further optimization for stargz

- Stargz improves pull performance but it still has performance drawbacks for reading files which induce remotely fetching contents. For solving this, stargz snapshotter provides further optimization for images based on the _workload_.
- Container images are built with purpose and the _workloads_ are determined at the build. In many cases, a workload is defined in the Dockerfile using some parameters including entrypoint command, environment variables and user.

![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*mfr9bginI0ZenVqSgudlUw.png)

- During the optimization, the tool `ctr-remote images optimize` regards the workloads as likely accessed files, then it sorts the archive entries by the accessed order and put a landmark file at the end. Before running container, stargz snapshotter prefetches and precaches this range by singe HTTP Range Request -> increase the cache hit rate for the specified workload and mitigates runtime overheads.

### 2.3. Containerd remote snapshotter plugin

- Containerd has a clean and pluggable architecture and functionalities are implemented as plugins following the defined API. Snapshotter is one of these plugins, which is used for storing extracted layers.
- During pulling an image, containerd extracts layers in the image and overlays them for preparing rootfs views called "snapshots" in the snapshotter. When containerd starts a container, it queries a snapshot to snapshotter and uses it as the container’s rootfs.

## 3. Adoption status

Check out this [issue](https://github.com/containerd/stargz-snapshotter/issues/258).
