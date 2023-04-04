# Architecting Containers Part 1: Why Understanding User Space vs. Kernel Space Matters

Source: <https://www.redhat.com/en/blog/architecting-containers-part-1-why-understanding-user-space-vs-kernel-space-matters>

- All applications, inclusive of containerd applications, rely on the underlying kernel.
- The kernel provides an API to these applications via system calls.
- Versioning of this API matters as it's the 'glue' that ensures deterministic communication between the user space and kernel space.

Containers are processes, they make system calls.

![](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/2015/07/user-space-vs-kernel-space-simple-container.png?itok=ptougYzT)

These files and programs make up what is known as `user space`. When a container is started, a program is loaded into memory from the container image. Once the program in the container is runnning, it still needs to make system calls into kernel space. The ability for the user space and kernel space to communicate in a deterministic fashion is critical.

## User space

- User space refers to all of the code in an operating system that lives outside of the kernel.
- All user programs function by manipulating data, but where does this data live? This data can come from registers in the CPU and external devices, but most commonly it is stored in memory and on disk. User programs get access to data by making special requests to the kernel called `system calls`.

## Kernel space

- The kernel provides abstraction for security, hardware and internal data structures.
