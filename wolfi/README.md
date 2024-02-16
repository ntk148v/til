# Wolfi

Source: <https://edu.chainguard.dev/open-source/wolfi/wolfi-with-dockerfiles/>

## 1. Introduction

- Wolfi is a minimal open source Linux distribution created specially for cloud workloads, with an emphasis on software supply chain security.
- Use [apk](https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper) for package management. The apk format was introduced by Alpine Linux to address specific design requirements that could not met by existing package managers such as `apt` and `dnf`.
  - Manipulating the Desired State:
    - In traditional package managers like `apt` and `dnf`, requesting the installation or removal of packages causes those packages to be dreictly installed or removed.
    - In `apk`, when you run `apk add package1/apk del package2`, `package1` and `package2` are added/removed as a dependency constraint in `/etc/apk/world`, which describes the desired system state.
    - Package installation or removal is done as a side effect of modifying this system state.
    - You can edit `/etc/apk/world/` with text editor of your choice and then use `apk fix` to synchronize the installed packages with the desired state.
  - Verification and unpacking in Parallel to package fetching
    - `apk` is completely driven by the package fetching I/O when installing or upgrading packages. When the package data is fetched, it is verified and unpacked on the fly.
  - Constainted Solver:
  - Fast and Safe package management.
- Doesn't have a kernel as it is intended to be used with a container runtime.
- An ideal base for both _distroless_ images and fully-featured builder images.
  - A _distroless_ image is a minimal container image that typically doesn’t include a shell or package manager. The extra tightness improves security in several aspects, but it requires a more sophisticated strategy for image composition since you can’t install packages so easily.
- There are currently two main strategies for building distroless images with Wolfi:
  - **With a Dockerfile**: use `-dev` variants or the `wolfi-base` image to build the application, and copy the artifacts to a distroless runtime image. This option is typically more accessible for people who are already used to a Dockerfile workflow.
  - **With apko**: Use [apko] to build a distroless image with only the packages you need, fully customized. This option requires a steeper learning curve to get used to how apko works, but it will give you smaller images with better SBOM coverage.

### 2. apko

- apko is a command-line tool that allows users to build container images using a declarative language based on YAML.

![](https://edu.chainguard.dev/open-source/apko/overview/apko_melange_ecosystem_hu6466fa4d3ca2be1551c385d0a0b84b16_214353_500x0_resize_box_3.png)
