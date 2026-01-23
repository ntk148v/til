# Docker lazy loading works

Source: <https://engineering.grab.com/docker-lazy-loading>

## Container root filesystem (rootfs) and file organization

A container’s root filesystem, or rootfs, is the directory structure that the container sees as its root (/). It contains all the files and directories necessary for an application to run, including the application itself, its dependencies, system libraries, and configuration files. It’s an isolated filesystem, separate from the host machine’s filesystem.

The rootfs is built from a series of read-only layers that come from the container image. Each instruction in an image’s Dockerfile creates a new layer, representing a set of filesystem changes. When a container is launched, a new writable layer, often called the “container layer,” is added on top of the stack of read-only image layers. Any changes made to the running container, such as writing new files or modifying existing ones, are written to this writable layer. The underlying image layers remain untouched. This is known as a copy-on-write (CoW) mechanism.

In containerd, a snapshotter is a plugin responsible for managing container filesystems. Its primary job is to take the layers of an image and assemble them into a rootfs for a container. The default snapshotter in containerd is overlayFS, which uses the Linux kernel’s OverlayFS driver to efficiently stack layers. To assemble the rootfs, the overlayFS snapshotter creates a “merged” view of the read-only image layers:

![](https://engineering.grab.com/img/docker-lazy-loading/figure-4.png)

- lowerdir: The read-only image layers are used as the lowerdir in OverlayFS. These are the immutable layers from the container image.
- upperdir: A new, empty directory is created to be the upperdir. This is the writable layer for the container where any changes are stored.
- merged: The merged directory is the unified view of the lowerdir and upperdir. This is what is presented to the container as its rootfs.

When a container reads a file, it’s read from the merged view. When a container writes a file, it’s written to the upperdir using a copy-on-write mechanism. This is an efficient way to manage container filesystems, as it avoids duplicating files and allows for fast container startup.

## The problem: Traditional container image pull

To understand the benefits of lazy loading, we first need to understand the traditional container image pull process:

- **Download layers**: The container runtime downloads all layer tarballs that make up the image.
- **Unpack layers**: Each layer is unpacked and extracted onto the host’s disk.
- **Create snapshot**: The snapshotter combines these layers into a single, unified filesystem, known as the container’s rootfs.
- **Start container**: Only after all layers are downloaded and unpacked can the container start.

This process is slow, especially for large images, as the entire image must be present on the host before the container can launch.

## The solution: Remote snapshotter

To address the slow startup issue with large images, we use a **remote snapshotter** solution. A remote snapshotter is a special type of snapshotter that doesn’t require all image data to be locally present. Instead of downloading and unpacking all the layers, it creates a “snapshot” that points to the remote location of the data (like a container registry). The actual file content is then fetched on-demand when the container tries to read a file for the first time.

While a traditional snapshotter like overlayFS uses directories on the local disk as its lowerdir, a remote snapshotter creates a virtual lowerdir that is backed by the remote registry. This is typically done using FUSE (Filesystem in Userspace). The remote snapshotter creates a FUSE filesystem that presents the contents of the remote layer as if it were a local directory. This FUSE mount is then used as the lowerdir for the overlayFS driver. This allows the remote snapshotter to integrate with the existing overlayFS infrastructure while adding the capability of lazy-loading data from a remote source.

There are two main formats that enable remote snapshotters: **eStargz** and **SOCI**.

## eStargz

Check out [eStargz](./estargz-snapshotter.md).

## SOCI

SOCI is a technology open sourced by AWS that enables containers to launch faster by lazily loading the container image. SOCI works by creating an index (SOCI Index) of the files within an existing container image. SOCI borrows some of the design principles from stargz-snapshotter but takes a different approach:

- **Separate index**: A SOCI index is generated separately from the container image and is stored in the registry as an OCI Artifact, linked back to the container image by OCI Reference Types.
- **No image conversion**: This means that the container images do not need to be converted, image digests do not change, and image signatures remain valid.
- **Native Bottlerocket support**: SOCI is natively supported on Bottlerocket OS.
