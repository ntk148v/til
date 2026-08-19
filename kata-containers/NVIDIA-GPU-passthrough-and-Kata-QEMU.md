# Enabling NVIDIA GPU workloads using GPU passthrough with Kata Containers

This guide describes how to run GPU workloads with Kata Containers using
the NVIDIA TEE (Trusted Execution Environment) and non-TEE GPU runtime
classes. It covers:

1. The components involved when running GPU workloads with Kata Containers
   using the NVIDIA GPU runtime classes.
1. The orchestration flow on a Kubernetes node for this scenario.
1. A step-by-step deployment guide to utilize these runtime classes.

It follows NVIDIA's reference implementation for running GPU workloads with
Kata Containers.

We assume the reader is familiar with Kubernetes, Kata Containers, and
Confidential Containers.

> **Note:**
>
> The currently supported modes for enabling GPU workloads in the TEE
> scenario are: (1) single‑GPU passthrough (one physical GPU per pod) and
> (2) multi-GPU passthrough on NVSwitch (NVLink) based HGX systems
> (for example, HGX Hopper (SXM) and HGX Blackwell / HGX B200).

## Component Overview

Before providing deployment guidance, we describe the components involved to
support running GPU workloads. We start from a top to bottom perspective
from the NVIDIA GPU Operator via the Kata runtime to the components within
the NVIDIA GPU Utility Virtual Machine (UVM) root filesystem.

### NVIDIA GPU Operator

A central component is the
[NVIDIA GPU Operator](https://github.com/NVIDIA/gpu-operator) which can be
deployed onto your cluster as a helm chart. Installing the GPU Operator
delivers various operands on your nodes in the form of Kubernetes DaemonSets.
These operands are vital to support the flow of orchestrating pod manifests
using NVIDIA GPU runtime classes with GPU passthrough on your nodes. Without
getting into the details, the most important operands and their
responsibilities are:

- **nvidia-vfio-manager:** Binding discovered NVIDIA GPUs and nvswitches to
  the `vfio-pci` driver for VFIO passthrough.
- **nvidia-cc-manager:** Transitioning GPUs into confidential computing (CC)
  and non-CC mode (see the
  [NVIDIA/k8s-cc-manager](https://github.com/NVIDIA/k8s-cc-manager)
  repository).
- **nvidia-sandbox-device-plugin** (see the
  [NVIDIA/sandbox-device-plugin](https://github.com/NVIDIA/sandbox-device-plugin)
  repository):
  - Creating host-side CDI specifications for GPU passthrough,
    resulting in the file `/var/run/cdi/nvidia.yaml`, containing
    `kind: nvidia.com/pgpu`
  - Allocating GPUs during pod deployment.
  - Discovering NVIDIA GPUs, their capabilities, and advertising these to
    the Kubernetes control plane (allocatable resources as type
    `nvidia.com/pgpu` resources will appear for the node and GPU Device IDs
    will be registered with Kubelet). These GPUs can thus be allocated as
    container resources in your pod manifests. See below GPU Operator
    deployment instructions for the use of the key `pgpu`, controlled via a
    variable.

To summarize, the GPU Operator manages the GPUs on each node, allowing for
simple orchestration of pod manifests using Kata Containers. Once the cluster
with GPU Operator and Kata bits is up and running, the end user can schedule
Kata NVIDIA GPU workloads, using resource limits and the
`kata-qemu-nvidia-gpu`, `kata-qemu-nvidia-gpu-tdx` or
`kata-qemu-nvidia-gpu-snp` runtime classes, for example:

```yaml
apiVersion: v1
kind: Pod
...
spec:
  ...
  runtimeClassName: kata-qemu-nvidia-gpu-snp
  ...
    resources:
      limits:
        "nvidia.com/pgpu": 1
...
```

When this happens, the Kubelet calls into the sandbox device plugin to
allocate a GPU. The sandbox device plugin returns `DeviceSpec` entries to the
Kubelet for the allocated GPU. The Kubelet uses internal device IDs for
tracking of allocated GPUs and includes the device specifications in the CRI
request when scheduling the pod through containerd. Containerd processes the
device specifications and includes the device configuration in the OCI
runtime spec used to invoke the Kata runtime during the create container
request.

### Kata runtime

The Kata runtime for the NVIDIA GPU handlers is configured to cold-plug VFIO
devices (`cold_plug_vfio` is set to `root-port` while
`hot_plug_vfio` is set to `no-port`). Cold-plug is by design the only
supported mode for NVIDIA GPU passthrough of the NVIDIA reference stack.

With cold-plug, the Kata runtime attaches the GPU at VM launch time, when
creating the pod sandbox. This happens _before_ the create container request,
i.e., before the Kata runtime receives the OCI spec including device
configurations from containerd. Thus, a mechanism to acquire the device
information is required. This is done by the runtime calling the
`coldPlugDevices()` function during sandbox creation. In this function,
the runtime queries Kubelet's Pod Resources API to discover allocated GPU
device IDs (e.g., `nvidia.com/pgpu = [vfio0]`). The runtime formats these as
CDI device identifiers and injects them into the OCI spec using
`config.InjectCDIDevices()`. The runtime then consults the host CDI
specifications and determines the device path the GPU is backed by
(e.g., `/dev/vfio/devices/vfio0`). Finally, the runtime resolves the device's
PCI BDF (e.g., `0000:21:00`) and cold-plugs the GPU by launching QEMU with
relevant parameters for device passthrough (e.g.,
`-device vfio-pci,host=0000:21:00.0,x-pci-vendor-id=0x10de,x-pci-device-id=0x2321,bus=rp0,iommufd=iommufdvfio-faf829f2ea7aec330`).

The runtime also creates _inner runtime_ CDI annotations
which map host VFIO devices to guest GPU devices. These are annotations
intended for the kata-agent, here referred to as the inner runtime (inside the
UVM), to properly handle GPU passthrough into containers. These annotations
serve as metadata providing the kata-agent with the information needed to
attach the passthrough devices to the correct container.
The annotations are key-value pairs consisting of `cdi.k8s.io/vfio<num>` keys
(derived from the host VFIO device path, e.g., `/dev/vfio/devices/vfio1`) and
`nvidia.com/gpu=<index>` values (referencing the corresponding device in the
guest CDI spec). These annotations are injected by the runtime during
container creation via the `annotateContainerWithVFIOMetadata` function (see
the Kata Containers
[`container.go`](https://github.com/kata-containers/kata-containers/blob/main/src/runtime/virtcontainers/container.go)).

We continue describing the orchestration flow inside the UVM in the next
section.

### Kata NVIDIA GPU UVM

#### UVM composition

To better understand the orchestration flow inside the NVIDIA GPU UVM, we
first look at the components its root filesystem contains. Should you decide
to use your own root filesystem to enable NVIDIA GPU scenarios, this should
give you a good idea on what ingredients you need.

From a file system perspective, the UVM is composed of two files: a standard
Kata kernel image and the NVIDIA GPU rootfs in initrd or disk image format.
These two files are being utilized for the QEMU launch command when the UVM
is created.

The two most important pieces in Kata Container's build recipes for the
NVIDIA GPU root filesystem are the `nvidia_chroot.sh` and `nvidia_rootfs.sh`
files. The build follows a two-stage process. In the first stage, a
full-fledged Ubuntu-based root filesystem is composed within a chroot
environment. In this stage, NVIDIA kernel modules are built and signed
against the current Kata kernel and relevant NVIDIA packages are installed.
In the second stage, a chiseled build is performed: Only relevant contents
from the first stage are copied and compressed into a new distro-less root
filesystem folder. Kata's build infrastructure then turns this root
filesystem into the NVIDIA initrd and image files.

The resulting root filesystem contains the following software components:

- NVRC - the
  [NVIDIA Runtime Container init system](https://github.com/NVIDIA/nvrc/tree/main)
- NVIDIA drivers (kernel modules)
- NVIDIA user space driver libraries
- NVIDIA user space tools
- kata-agent
- confidential computing guest components: the attestation agent,
  confidential data hub and api-server-rest binaries
- CRI-O pause container (for the guest image-pull method)
- BusyBox utilities (provides a base set of libraries and binaries, and a
  linker)
- some supporting files, such as file containing a list of supported GPU
  device IDs which NVRC reads

#### UVM orchestration flow

When the Kata runtime asks QEMU to launch the VM, the UVM's Linux kernel
boots and mounts the root filesystem. After this, NVRC starts as the initial
process.

NVRC scans for NVIDIA GPUs on the PCI bus, loads the
NVIDIA kernel modules, waits for driver initialization, creates the device nodes,
and initializes the GPU hardware (using the `nvidia-smi` binary). NVRC also
creates the guest-side CDI specification file (using the
`nvidia-ctk cdi generate` command). This file specifies devices of
`kind: nvidia.com/gpu`, i.e., GPUs appearing to be physical GPUs on regular
bare metal systems. The guest CDI specification also contains `containerEdits`
for each device, specifying device nodes (e.g., `/dev/nvidia0`,
`/dev/nvidiactl`), library mounts, and environment variables to be mounted
into the container which receives the passthrough GPU.

Then, NVRC forks the Kata agent while continuing to run as the
init system. This allows NVRC to handle ongoing GPU management tasks
while kata-agent focuses on container lifecycle management. See the
[NVRC sources](https://github.com/NVIDIA/nvrc/blob/main/src/main.rs) for an
overview on the steps carried out by NVRC.

When the Kata runtime sends the create container request, the Kata agent
parses the inner runtime CDI annotation. For example, for the inner runtime
annotation `"cdi.k8s.io/vfio1": "nvidia.com/gpu=0"`, the agent looks up device
`0` in the guest CDI specification with `kind: nvidia.com/gpu`.

The Kata agent also reads the guest CDI specification's `containerEdits`
section and injects relevant contents into the OCI spec of the respective
container. The kata agent then creates and starts a `rustjail` container
based on the final OCI spec. The container now has relevant device nodes,
binaries and low-level libraries available, and can start a user application
linked against the CUDA runtime API (e.g., `libcudart.so` and other
libraries). When used, the CUDA runtime API in turn calls the CUDA driver
API and kernel drivers, interacting with the pass-through GPU device.

An additional step is exercised when using images from an authenticated
registry: the guest-pull mechanism triggers attestation using Trustee's Key
Broker Service (KBS) for secure release of the NGC API authentication key
used to access the NVCR container registry. In this flow the CPU and all
additional devices are attested. GPUs will automatically be set to ready by
NVRC per the NVRC configuration flag in the default kernel command line.

## Deployment Guidance

This guidance assumes you use bare-metal machines with proper support for
Kata's non-TEE and TEE GPU workload deployment scenarios for your Kubernetes
nodes. Note that this setup:

- uses the nydus snapshotter to pull container image layers in the guest
- uses the genpolicy tool to attach Kata agent security policies to the pod
  manifest
- supports composite attestation, a CUDA vectorAdd test, and secure API key
  release using sealed secrets.

A similar deployment guide and scenario description can be found in NVIDIA resources
under
[NVIDIA Confidential Containers Overview (Early Access)](https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/latest/overview.html).

### Feature Set

The NVIDIA stack for Kata Containers leverages features for the confidential
computing scenario from both the confidential containers open source project
and from the Kata Containers source tree, such as:

- composite attestation using Trustee and the NVIDIA Remote Attestation
  Service NRAS
- generating kata agent security policies using the genpolicy tool
- use of signed sealed secrets
- access to authenticated registries for container image guest-pull
- container image signature verification and encrypted container images
- ephemeral container data and image layer storage

For the use of these features, we refer to separate documentation in the
kata-containers and confidential-containers documentation resources.
For example, see a
[list of features](https://confidentialcontainers.org/docs/features/) along
with their documentation in the confidential-containers documentation.

> **Note:**
>
> Image signature verification for signed multi-arch images is currently not
> supported.

### Requirements

The requirements for the TEE scenario are:

- Ubuntu 26.04 as host OS
- CPU with AMD SEV-SNP or Intel TDX support with proper BIOS/UEFI version
  and settings
- CC-capable Hopper/Blackwell GPU with proper VBIOS version.

BIOS and VBIOS configuration is out of scope for this guide. Other resources,
such as the documentation found on the
[NVIDIA Trusted Computing Solutions](https://docs.nvidia.com/nvtrust/index.html)
page, on the
[Secure AI Compatibility Matrix](https://www.nvidia.com/en-us/data-center/solutions/confidential-computing/secure-ai-compatibility-matrix/)
page, and on the above linked NVIDIA documentation, provide guidance on
selecting proper hardware and on properly configuring its firmware and OS.

### Installation

#### Containerd and Kubernetes

First, set up your Kubernetes cluster. For instance, a single-node vanilla
Kubernetes cluster with containerd v2.3 works well for this scenario. You can
set this up manually or with any cluster provisioning tool of your choice,
as long as containerd and its `cri` plugins are enabled.

> **Note:**
>
> We recommend to configure your Kubelet with a higher
> `runtimeRequestTimeout` timeout value than the two minute default timeout.
> Using the guest-pull mechanism, pulling large images may take a significant
> amount of time and may delay container start, possibly leading your Kubelet
> to de-allocate your pod before it transitions from the _container creating_
> to the _container running_ state. The NVIDIA shim configurations use a
> `create_container_timeout` of 1200s, which is the equivalent value on shim
> side, controlling the time the shim allows for a container to remain in
> _container creating_ state.
> If you need a timeout of more than 1200s, you will also need to adjust the
> agent's `image_pull_timeout`, which in turn sets the confidential data
> hub's image pull API timeout in seconds. For this, add the
> `agent.image_pull_timeout=<seconds>` kernel parameter to your shim
> configuration's `kernel_params` field, or pass the parameter explicitly
> via the `io.katacontainers.config.hypervisor.kernel_params: "..."` pod
> annotation. The default value for this timeout is 1200s.

> **Note:**
>
> The NVIDIA GPU runtime classes use VFIO cold-plug which, as
> described above, requires the Kata runtime to query Kubelet's Pod Resources
> API to discover allocated GPU devices during sandbox creation. For
> Kubernetes versions **older than 1.34**, you must explicitly enable the
> `KubeletPodResourcesGet` feature gate in your Kubelet configuration. For
> Kubernetes 1.34 and later, this feature is enabled by default.

#### GPU Operator

Assuming you have the helm tools installed, deploy the latest version of the
GPU Operator as a helm chart (minimum version: `v26.3.0`):

```bash
$ helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
$ helm install --wait --generate-name \
    -n gpu-operator --create-namespace \
    nvidia/gpu-operator \
    --set sandboxWorkloads.enabled=true \
    --set sandboxWorkloads.defaultWorkload=vm-passthrough \
    --set sandboxWorkloads.mode=kata \
    --set nfd.enabled=true \
    --set nfd.nodefeaturerules=true
```

> **Note:**
>
> For heterogeneous clusters with different GPU types, you can specify an
> empty `P_GPU_ALIAS` environment variable for the sandbox device plugin:
> `-    --set 'kataSandboxDevicePlugin.env[0].name=P_GPU_ALIAS' \`
> `-    --set 'kataSandboxDevicePlugin.env[0].value=""' \`
> This will cause the sandbox device plugin to create GPU model-specific
> resource types (e.g., `nvidia.com/GH100_H100L_94GB`) instead of the
> default `pgpu` type, which usually results in advertising a resource of
> type `nvidia.com/pgpu`
> The exposed device resource types can be used for pods by specifying
> respective resource limits.
> Your node's nvswitches are exposed as resources of type
> `nvidia.com/nvswitch` by default. Using the variable `NVSWITCH_ALIAS`
> allows to control the advertising behavior similar to the `P_GPU_ALIAS`
> variable.

> **Note:**
>
> Using `--set sandboxWorkloads.defaultWorkload=vm-passthrough` causes all
> your nodes to be labeled for GPU VM passthrough. Remove this parameter if
> you intend to only use selected nodes for this scenario, and label these
> nodes by hand, using:
> `kubectl label node <node-name> nvidia.com/gpu.workload.config=vm-passthrough`.

#### Kata Containers

Install the latest Kata Containers helm chart, similar to
[existing documentation](https://github.com/kata-containers/kata-containers/blob/main/tools/packaging/kata-deploy/helm-chart/README.md)
(minimum version: `3.29.0`).

```bash
$ export VERSION=$(curl -sSL https://api.github.com/repos/kata-containers/kata-containers/releases/latest | jq .tag_name | tr -d '"')
$ export CHART="oci://ghcr.io/kata-containers/kata-deploy-charts/kata-deploy"

$ helm install kata-deploy \
    --namespace kata-system \
    --create-namespace \
    -f "https://raw.githubusercontent.com/kata-containers/kata-containers/refs/tags/${VERSION}/tools/packaging/kata-deploy/helm-chart/kata-deploy/try-kata-nvidia-gpu.values.yaml" \
    --set nfd.enabled=false \
    --wait --timeout 10m \
    "${CHART}" --version "${VERSION}"
```

> **Note:**
>
> For node lifecycle management, see the
> [lifecycle-manager](https://github.com/kata-containers/lifecycle-manager)
> repository which enables Argo Workflows-based lifecycle management for your
> node's Kata deployments.

#### Trustee's KBS for remote attestation

Trustee's KBS is used for composite attestation for secure key release, for
instance, for test scenarios which use authenticated container images. In
such scenarios, the credentials to access the authenticated container
registry are only released to the confidential guest after successful
attestation. Please see the "Deploy pods using attestation" section below
for more information about this.

Deploy Trustee via any of the mechanisms documented by the
[confidential-containers repository](https://github.com/confidential-containers/trustee).
For this architecture it is important to set up KBS in the remote verifier
mode, which requires entering a licensing agreement with NVIDIA; see the
[notes in the confidential-containers repository](https://github.com/confidential-containers/trustee/blob/main/deps/verifier/src/nvidia/README.md).

### Cluster validation and preparation

If you did not use the `sandboxWorkloads.defaultWorkload=vm-passthrough`
parameter during GPU Operator deployment, label your nodes for GPU VM
passthrough, for the example of using all nodes for GPU passthrough, run:

```bash
$ kubectl label nodes --all nvidia.com/gpu.workload.config=vm-passthrough --overwrite
```

With the suggested parameters for GPU Operator deployment, the
`nvidia-cc-manager` operand will automatically transition the GPU into CC
mode.

After deployment, you can transition your node(s) to the desired CC state,
using either the `on`, `ppcie`, or `off` value, depending on your scenario.
For the non-CC scenario, transition to the `off` state via:
`kubectl label nodes --all nvidia.com/cc.mode=off --overwrite` and wait
until all pods are back running. When an actual change is exercised, various
GPU Operator operands will be restarted.

Ensure all pods are running:

```bash
$ kubectl get pods -A
```

On your node(s), ensure for correct driver binding. Your GPU device should be
bound to the VFIO driver, i.e., showing `Kernel driver in use: vfio-pci`
when running:

```bash
$ lspci -nnk -d 10de:
```

### Run the CUDA vectorAdd sample

Create the pod manifest with:

```bash
$ cat > cuda-vectoradd-kata.yaml.in << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd-kata
  namespace: default
spec:
  runtimeClassName: ${GPU_RUNTIME_CLASS_NAME}
  restartPolicy: Never
  containers:
  - name: cuda-vectoradd
    image: "nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0-ubuntu22.04"
    resources:
      limits:
        nvidia.com/pgpu: "1"
        memory: 16Gi
EOF
```

Depending on your scenario and on the CC state, define the environment
variable with your desired runtime class name:

```bash
$ export GPU_RUNTIME_CLASS_NAME="kata-qemu-nvidia-gpu-snp"
```

Then, deploy the sample Kubernetes pod manifest and observe the pod logs:

```bash
$ envsubst < ./cuda-vectoradd-kata.yaml.in | kubectl apply -f -
$ kubectl wait --for=jsonpath='{.status.phase}'=Succeeded pod/cuda-vectoradd-kata --timeout=60s
$ kubectl logs -n default cuda-vectoradd-kata
```

Expect the following output:

```
[Vector addition of 50000 elements]
Copy input data from the host memory to the CUDA device
CUDA kernel launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```

To stop the pod, run: `kubectl delete pod cuda-vectoradd-kata`.

### Next steps

#### NUMA topology for GPU locality

On multi-NUMA hosts, enabling NUMA support ensures GPU memory accesses stay
local to the NUMA node where the GPU is physically attached, avoiding
cross-NUMA latency. The NVIDIA GPU configuration templates ship with
`enable_numa = true` by default.

For details on NUMA configuration, topology verification, and
troubleshooting, see the Kata Containers
[NUMA support guide](https://github.com/kata-containers/kata-containers/blob/main/docs/how-to/how-to-use-numa-with-kata.md).

#### Use multi-GPU passthrough

If you have machines supporting multi-GPU passthrough, use a pod deployment
manifest which uses 8 pgpu and 4 nvswitch resources.
On the NVIDIA Hopper architecture multi-GPU passthrough uses protected PCIe
(PPCIE) which claims exclusive use of the nvswitches for a single CVM. In
this case, transition your relevant node(s) GPU mode to `ppcie` mode.
The NVIDIA Blackwell architecture uses NVLink encryption which places the
switches outside of the Trusted Computing Base (TCB) and so does not
require a separate switch setting.

#### Transition between CC and non-CC mode

Use the previously described node labeling approach to transition between
the CC and non-CC mode. In case of the non-CC mode, you can use the
`kata-qemu-nvidia-gpu` value for the `GPU_RUNTIME_CLASS_NAME` runtime class
variable in the above CUDA vectorAdd sample. The `kata-qemu-nvidia-gpu-snp`
runtime class will **NOT** work in this mode - and vice versa.

#### Worker node as a virtual machine (nested GPU passthrough)

So far this guide assumed the physical GPU is passed directly from a
bare-metal host into the Kata guest VM. The same scenario also works when the
Kubernetes worker node is itself a virtual machine that receives the physical
GPU through VFIO passthrough — for example, when your Kubernetes nodes run
as VMs of a private or public cloud. In this case the Kata guest VM does not
receive the physical host device directly, but the virtual device exposed by
the worker VM. This is a _nested_ device assignment (L1 guest / worker VM → L2
guest / Kata VM).

QEMU documents this as
[Use Case 3: Nested Guest Device Assignment](https://wiki.qemu.org/Features/VT-d#Use_Case_3:_Nested_Guest_Device_Assignment)
in its VT-d feature description. The underlying principle: for a device to be
assigned to a nested guest, its DMA traffic must be remapped through the
virtual IOMMU (vIOMMU) of the intermediate guest. When the physical GPU is
passed into the worker VM, it is exposed against the worker VM's emulated
IOMMU. That vIOMMU must in turn be visible to the Kata guest so the Kata
guest can remap the device. In QEMU terms this means announcing an Intel
IOMMU device inside the Kata guest and attaching the VFIO device with
`iommu_platform=on`.

In the Kata Containers QEMU configuration, the equivalent is controlled by
two `[hypervisor.qemu]` settings:

- `enable_iommu = true` — enables an emulated IOMMU device inside the Kata
  guest, providing the (virtual) DMA remapping that a nested assignment
  relies on.
- `enable_iommu_platform = true` — attaches the `iommu_platform=on`
  attribute to VFIO devices, so the guest treats the passthrough device as
  IOMMU-aware and routes its DMA through the vIOMMU.

> **Note:**
>
> These settings are required for the nested scenario described here. On a
> bare-metal host that passes the GPU directly into the Kata guest, vIOMMU
> mapping might not be strictly required, but enabling it is still valid and
> matches NVIDIA's reference configuration. Either way, the worker VM itself
> must already receive the GPU via `vfio-pci` (check with
> `lspci -nnk -d 10de:`), and the hypervisor hosting the worker VM (L0) as
> well as the worker VM must expose an IOMMU to the layers below.

##### Configuring via the kata-deploy Helm chart

Kata's deployment artifacts ship NVIDIA GPU configuration templates that you
can customize per runtime class without editing files on the node by passing
Helm values to the
[kata-deploy chart](https://github.com/kata-containers/kata-containers/blob/main/tools/packaging/kata-deploy/helm-chart/README.md).
The chart's top-level `shims` section controls which runtime classes are
installed and how each is configured:

- `disableAll` disables every shim that is not explicitly listed, so only the
  runtime class(es) you configure are installed.
- The per-shim key, here `qemu-nvidia-gpu`, corresponds to the
  `kata-qemu-nvidia-gpu` runtime class (repeat or adjust the key for the
  `-snp` / `-tdx` variants you use).
- `dropIn` is an arbitrary snippet that gets appended to the generated
  `configuration.toml` for that shim, which is exactly where the
  `[hypervisor.qemu]` settings above go.
- `allowedHypervisorAnnotations` controls which `io.katacontainers.config.hypervisor.*`
  pod annotations are honored. An empty list disables annotation-based
  overrides, keeping the configuration fixed to the drop-in below. To allow
  overrides, either enumerate the annotation keys or set `allowAll: true`.

To enable the vIOMMU for the `kata-qemu-nvidia-gpu` runtime class, install the
chart with the following values:

```yaml
# kata-nvidia-gpu-values.yaml
shims:
  disableAll: true
  qemu-nvidia-gpu:
    allowedHypervisorAnnotations: []
    containerd:
      snapshotter: ''
    dropIn: |
      [hypervisor.qemu]
      enable_iommu = true
      enable_iommu_platform = true
```

Deploy the chart with these values:

```bash
$ export VERSION=$(curl -sSL https://api.github.com/repos/kata-containers/kata-containers/releases/latest | jq .tag_name | tr -d '"')
$ export CHART="oci://ghcr.io/kata-containers/kata-deploy-charts/kata-deploy"

$ helm install kata-deploy \
    --namespace kata-system \
    --create-namespace \
    -f kata-nvidia-gpu-values.yaml \
    --set nfd.enabled=false \
    --wait --timeout 10m \
    "${CHART}" --version "${VERSION}"
```

After the chart is deployed, the `kata-qemu-nvidia-gpu` runtime class runs
with the vIOMMU enabled, and the CUDA vectorAdd sample from above can be run
against the worker VM without further changes.

> **Note:**
>
> Make sure the hypervisor that hosts the worker VM (L0) and the worker VM
> itself hand the GPU down to the Kata guest with proper IOMMU support. If
> that outer layer does not expose an IOMMU to the worker VM, the vIOMMU
> setup inside Kata will not be able to remap DMA and device assignment will
> fail. Adjust the L0 configuration (for example, enable VT-d/AMD IOMMU and
> attach `iommu_platform=on` to the outer `vfio-pci` device) before relying on
> the settings above.

#### Deploy pods with Kata agent security policies

With GPU passthrough being supported by the
[genpolicy tool](https://github.com/kata-containers/kata-containers/tree/main/src/tools/genpolicy),
you can use the tool to create a Kata agent security policy.

The `genpolicy` binary is shipped in the separate Kata tools archive and is
not installed by the Kata Containers Helm chart. Install the Kata tools
archive matching the Kata release selected by `VERSION`. For example, run
the following commands from the root of the Kata Containers source tree
(checked out at the tag matching `VERSION`):

```bash
$ mkdir -p kata-tools-artifacts
$ curl -fsSL \
    "https://github.com/kata-containers/kata-containers/releases/download/${VERSION}/kata-tools-static-${VERSION}-amd64.tar.zst" \
    --output kata-tools-artifacts/kata-tools-static.tar.zst
$ tar --zstd -xf kata-tools-artifacts/kata-tools-static.tar.zst -C /opt/kata
$ test -x /opt/kata/bin/genpolicy
$ rm -rf kata-tools-artifacts
```

These commands install `genpolicy` and its settings under `/opt/kata` on the
host that runs this single-node Kubernetes instance.

You may need to modify the genpolicy default settings, for example to adjust
the OCI version. This can be done via snippets such as the following applied
through a genpolicy drop-in configuration file (e.g.,
`src/tools/genpolicy/drop-in-examples/20-oci-1.3.0-drop-in.json` in the Kata
Containers source tree):

```bash
[
  {
    "op": "replace",
    "path": "/kata_config/oci_version",
    "value": "1.3.0"
  }
]
```

When using a newer (or older) containerd version, the OCI version field
may need to be adjusted accordingly.

#### Deploy pods using attestation

Attestation is a fundamental piece of the confidential containers solution.
It is used, for example, to leverage the authenticated container image pull
mechanism where container images reside in the authenticated NVCR registry,
and to request secrets from KBS. KBS will release the image pull secret to a
confidential guest only after the guest has been successfully attested. To
get the authentication credentials from inside the guest, KBS must already
be deployed and configured. Configure KBS with the guest image pull secret
and a resource policy, and launch the pod with the following kernel command
line parameters:
`"agent.image_registry_auth=kbs:///default/credentials/nvcr agent.aa_kbc_params=cc_kbc::${CC_KBS_ADDR}"`.

The `agent.aa_kbc_params` option is a general configuration for attestation.
For your use case, you need to set the IP address and port under which KBS
is reachable through the `CC_KBS_ADDR` variable. This tells the guest how to
reach KBS. Something like this must be set whenever attestation is used, but
on its own this parameter does not trigger attestation. The
`agent.image_registry_auth` option tells the guest to ask for a resource from
KBS and use it as the authentication configuration. When this is set, the
guest will request this resource at boot (and trigger attestation)
regardless of which image is being pulled.

To deploy your own pods using authenticated container images, or secure key
release for attestation, follow steps similar to those described above.

#### Deploy pods using your own containers and manifests

You can author pod manifests leveraging your own containers, for instance,
containers built using the CUDA container toolkit. We recommend to start
with a CUDA base container.

When using the GPU runtime classes, the GPUs will automatically be set to ready.

> **Notes:**
>
> - musl-based container images (e.g., using Alpine), or distro-less
>   containers are not supported.
