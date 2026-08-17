# MicroVM

## 1. Micro-vs-container

Source: <https://vercel.com/i/microvm-vs-container>

Agents now write files and run commands faster than any review process can keep up with, making the isolation boundary a design decision rather than an ops detail. Containers partition host processes using Linux primitives and share a single kernel, whereas microVMs provide each workload with its own guest kernel via hardware virtualization.

Here is how the split plays out across the dimensions that change an architecture decision:

|                         |                                                                                     |                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Dimension               | Containers                                                                          | MicroVMs                                                                          |
| Isolation boundary      | Namespaces, cgroups, capabilities, and seccomp-bpf, all enforced by the host kernel | Hardware virtualization around a guest kernel, plus host-side controls on the VMM |
| Kernel                  | One shared kernel for the host and every container on it                            | One guest kernel per workload, reducible to what the workload needs               |
| Startup time            | No guest boot step when the image is present                                        | VMM start plus guest boot, or a snapshot restore                                  |
| Memory overhead         | Low, because kernel memory is shared                                                | VMM process plus configured guest RAM per instance                                |
| Density                 | High for homogeneous workloads sharing a trust model                                | Bounded by guest RAM allocated per isolated execution                             |
| Blast radius if hostile | A permitted syscall reaching a kernel bug crosses into shared territory             | Guest OS and CPU-enforced privilege separation sit in front of the host kernel    |

---

A microVM stack is smaller than a general-purpose hypervisor because it removes devices and machine features that server workloads never touch. Four pieces carry the isolation:

- **Minimal device model:** Firecracker exposes only the block, network, and control paths its target workloads need, keeping the host-facing surface narrow.
- **Purpose-built VMM:** One monitor process runs per microVM, so the relationship between workload, monitor, and boundary stays direct and auditable.
- **Dedicated guest kernel:** Each instance boots its own kernel, limited to the drivers and subsystems the workload requires.
- **Host-side jailer:** The VMM process runs under cgroups, namespaces, a minimal chroot, dropped privileges, and per-thread seccomp filters.

The advantages concentrate on workloads whose behavior cannot be predicted:

- **Per-workload kernel:** A guest kernel per execution means the boundary no longer rests solely on the host kernel's process isolation.
- **Auditable containment story:** Hardware virtualization, a minimal VMM, and jailer controls map to mechanisms security reviewers already recognize.
- **Tenant fault isolation:** A kernel panic or runaway resource spike stays inside that guest instead of becoming a shared-host incident.
- **Serverless-shaped footprint:** Firecracker targets ephemeral workloads rather than general-purpose virtualization, so the boundary arrives without a full hypervisor stack.

The limitations are mostly operational:

- **Virtualization expertise required:** KVM hosts, guest kernel images, network setup, and snapshot management need an on-call owner.
- **Observability across a VM boundary:** Debugging inside a microVM differs from attaching to a container, and container-native tracing often needs adaptation.
- **Per-instance memory floor:** Configured guest RAM is allocated per execution, which caps density against processes sharing a kernel.
- **Narrower workload fit:** Firecracker stacks are Linux-guest environments, and accelerator-heavy workloads can call for a different approach.

---

Container isolation is built from Linux primitives rather than provided by a single mechanism. Four pieces do the work:

- **Namespaces:** clone(2) and unshare(2) create separate views of process IDs, mounts, IPC, hostname, users, and networking.
- **Cgroups:** Hierarchical groups that cap and monitor CPU, memory, and I/O consumption via `/sys/fs/cgroup`.
- **The shared kernel:** Every permitted syscall executes kernel code shared with the host, which keeps overhead low and defines the boundary's limit.
- **Image and runtime:** The OCI specifications package the filesystem and process configuration into a repeatable unit.

The advantages are concrete:

- **No boot step:** Containers start without a guest kernel boot, which suits interactive latency budgets.
- **Shared kernel memory:** Per-instance overhead stays low, so a host packs many workloads at once.
- **Existing toolchain:** Registries, build pipelines, logging, and orchestration already speak this model.
- **Runtime selection per pod:** Kubernetes RuntimeClass, stable since v1.20, lets one cluster schedule hardened and virtualized handlers side by side.

The limitations follow from the shared kernel:

- **A shared escape surface:** A permitted syscall that reaches a kernel bug executes code shared with the host and every neighbor. Hence, a single kernel vulnerability is a multi-tenant vulnerability.
- **Hardening reduces without relocating:** seccomp-bpf, AppArmor, and dropping capabilities such as `CAP_SYS_ADMIN` shrink the reachable surface, and the kernel still belongs to the host.
- **Privileged workloads undo the boundary:** Container-in-container builds need elevated privileges, which removes much of the isolation the setup provided.
- **Security depends on two things at once:** the boundary holds only when both configuration and kernel correctness hold.

## 2. microvm 2026

Source: <https://emirb.github.io/blog/microvm-2026/>
