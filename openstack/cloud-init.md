# Deep dive into Cloud-init

Source:

- <https://firstcloud.pl/blog/deep-dive-into-cloud-init-in-openstack/>
- <https://docs.cloud-init.io/en/latest/>

> [!IMPORTANT]
> Read the original source first; it is a complete and detailed article. The content below omits the introduction and has been rewritten based on my understanding.

To turn a generic VM to a specialized component of your infrastructure, the solution is **metadata** and **cloud-init**.

- Cloud orchestrators like OpenStack, AWS, Azure, and others expose metadata to running instances (instance-specific information such as the hostname, network configuration, and SSH keys).
- The cloud-init service, embedded in cloud images, retrieves this metadata during boot and uses it to customize the VM before any user interaction.

> [!NOTE]
> Of course, you can also customize the VM using configuration management systems like Ansible or Puppet, but these tools require the instance to boot first, SSH to be available, and manual execution of playbooks or agent startup. Cloud-init runs automatically on first boot, configuring the instance before any external system connects to it.

## 1. Metadata in OpenStack

- Before a VM can configure itself, it needs to know who it is and what properties it should have. In OpenStack, this information flows from the cloud orchestrator to the instance as _instance_. When you launch an instance, OpenStack collects information from multiple sources and makes available to the running instance through the Nova metadata service.
  - the instance's own properties.
  - network configuration assigned by Neutron.
  - user-provided data like SSH keys.
- Not all metadata is consumed by cloud-init. Some metadata configures the hypervisor layer and affects how the VMs run on the physical host. These configurations happen at the hypervisor level and don't require any awareness from guest OS.
  - CPU pinning to dedicate specific CPU cores to an instance.
  - NUMA topology.
  - ...

### 1.1. Types of data

OpenStack Nova distinguishes between three key types of data passed to an instance:

1. **Metadata**: System-level information provided by the cloud platform. This is a JSON structure containing instance identity and environment information that cloud-init uses to configure the system.

- `uuid`: unique identifier for the instance.
- `hostname` and `name`: the hostname assigned to the instance.
- `availability_zone`: the availability zone where the instance runs.
- `public_keys`: SSH public keys for initial access.
- `project_id`: the OpenStack project (tenant) ID.

The instance queries this data from http://169.254.169.254/openstack/latest/meta_data.json. Network configuration is provided separately at http://169.254.169.254/openstack/latest/network_data.json and contains interface details, DHCP settings, MTU values, and DNS server addresses.

2. **User data**: The customization payload provided by the user when launching the instance. From the OpenStack API perpective, this is a base64-encoded string limited to 64KB in size. From the VM’s perspective, it’s the instruction manual for customization. User data can be:

- A bash script starting with `#!/bin/bash`
- A cloud-config YAML file starting with `#cloud-config`
- A MIME multi-part archive combining multiple formats
- Any other executable format cloud-init recognizes (Python, Perl, etc.)
  The instance retrieves this from http://169.254.169.254/openstack/latest/user_data.

3. **Vendor data**: Configuration injected by the cloud administrator into every instance automatically. This is configured on Nova API servers in `nova.conf` and allows cloud operators to provide baseline configuration that applies to all instances.

Some OpenStack deployments use vendor data to set a random root password and display it on the virtual console during first boot. This provides emergency access through the console (not SSH, as root SSH login is typically disabled) if something goes wrong with SSH key injection. However, this behavior depends on how your cloud is configured - many deployments don’t configure vendor data at all.

> [!NOTE]
> Users maintain ultimate control over vendor data. When both vendor data and user data provide cloud-config, user-supplied cloud-config is merged over vendor-supplied cloud-config, giving user configurations priority. Users can also disable vendor data execution entirely or selectively disable specific vendor data components through their user data configuration. For script-based vendor data (shell scripts), both vendor and user scripts execute, with vendor scripts running first during the first boot only.

- While vendor data follows the same format rules and processing logic as user data, its execution has several distinctive characteristics. By default, cloud-init processes vendor data only during the instance’s first boot, not on subsequent reboots. This differs from user data, which can be configured to run on every boot if needed.
- The separation between vendor-supplied and user-supplied configurations extends to script storage: `/var/lib/cloud/instance/scripts/vendor/` and `/var/lib/cloud/instance/scripts/`.
- There are two types of vendor data:
  - Static vendor data configured in nova.conf and identical for all instances
  - Dynamic vendor data fetched from an external REST API service, allowing per-instance or per-project customization.

### 1.2. How metadata reaches the VM

OpenStack provides two delivery mechanisms

#### 1.2.1. Config Drive

- An ISO9660 or VFAT filesystem containing all metadata, user data, and vendor data.
- Read-only and static. When rebuilding or resizing an instance, Nova generates a new config drive ISO with fresh metadata, completely replacing the previous one.
- Nova creates this small virtual disk and attaches it to the instance as a virtual CD-ROM or as an additional disk device. The filesystem has a label `config-2` which cloud-init uses to identify and automatically mount the drive during boot to read the configuration data.

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_OpenStack_Platform-17.0-Creating_and_Managing_Instances-en-US/images/217e854a4579afb1d57bc14d9eedd324/instance_storage_overview.png)

- Doesn't require any network connectivity.

#### 1.2.2. The Metadata service (169.254.169.254)

- The metadata service provides instance-specific data through HTTP requests to the link-local address 169.254.169.254. Unlike config drive, this method requires network connectivity but allows dynamic updates and doesn’t consume virtual hardware resources.
- When an instance makes an HTTP request to http://169.254.169.254/openstack/latest/meta_data.json, the metadata service receives this request, identifies which instance is making the call, and returns the appropriate metadata from Nova’s database. This approach is more flexible than config drive because the metadata can be updated while the instance is running (though cloud-init typically only reads it during boot stages).

#### 1.2.3. Choosing between Config Drive and Metadata Service

Use **Config Drive** when:

- Deploy network appliances (routers, firewalls, load balancers) that need to configure their own network interfaces before they can reach the metadata service.
- Using PCI passthrough for network devices, which bypasses the virtual network infrastructure (OVS bridge, OpenFLow rules) required for metadata service routing.
- Working in environments where the metadata service is unreliable or not available.
- Building images for bare metal deployments where no metadata service exists.
- Requiring guaranteed metadata availability even if networking fails during boot.

Use **Metadata Service** when:

- Deploying standard workloads.
- Needing to update instance metadata after launch without recreating the instance.
- Working in large-scale deployments where attaching an additional virtual device to thousands of instances adds overhead.
- Preferring the standard cloud-native approach that works consistently across OpenStack, AWS, Azure, and GCP.

In most production OpenStack environments, the metadata service is the default and recommended approach. Config drive is typically enabled only when explicitly needed for specific use cases.

### 1.3. The metadata service architecture in ML2/OVN

In OpenStack deployments using ML2 plugin with OVN (Open Virtual Network), the metadata service architecture is distributed and runs locally on each compute node.

#### 1.3.1. Network namespace isolation

Each Neutron network that has instances running on a compute node gets its own dedicated metadata service namespace (`ovnmeta-<network-uuid>`). This means a single compute node can run multiple metadata service instances, one per network. Each namespace is isolated from the host and contains:

- A virtual interface with an IP address from the subnet's allocation pool.
- The magic metadata address 169.254.169.254 configured on the same interface.
- An HAProxy instance listening on port 80. It acts as a reverse proxy, forwarding metadata requests along with network context headers (such as the source IP address via `X-Forwarded-For` and network/router identifiers) to the Neutron Metadata Agent through a Unix socket.

The Neutron Metadata Agent identifies the requesting instance by correlating the source IP address and network ID with its database, then adds critical authentication headers including X-Instance-ID and X-Tenant-ID (project ID). The agent also signs the request with an HMAC signature using a shared secret (`metadata_proxy_shared_secret`) before forwarding it to the Nova Metadata API service. These authentication mechanisms are critical for security: Nova Metadata API verifies the signature and headers to ensure that the request is authorized for the specific instance, preventing instances from accessing metadata belonging to other instances or projects.

![](https://firstcloud.pl/assets/images/posts/2026/2026-02-openstack-metadata-architecture.svg)

#### 1.3.2. Traffic flow with OpenFlow

```mermaid
flowchart TD
    A[Instance sends HTTP request<br/>169.254.169.254:80] --> B[Tap device (vNIC)]
    B --> C[OVS Integration Bridge (br-int)]

    C --> D[OpenFlow rules match<br/>metadata IP]
    D --> E[Redirect to metadata tap interface]

    E --> F[Metadata service network namespace]

    F --> G[HAProxy<br/>adds X-Forwarded-For + network headers]
    G --> H[Neutron Metadata Agent<br/>(via Unix socket)]

    H --> I[Identify instance<br/>add X-Instance-ID, X-Tenant-ID, HMAC]
    I --> J[Nova Metadata API]

    J --> K[Verify signature<br/>return instance metadata]

    K --> L[Response path (reverse flow)]
```

This architecture ensures that metadata requests are handled locally on the compute node without requiring traffic to traverse the physical network. The network namespace isolation guarantees that instances from different projects or networks cannot access each other’s metadata, even though they all use the same destination IP address.

## 2. What is Cloud-init?

The cloud-init package includes a daemon process, configuration files stored in `/etc/cloud/`, and runtime data cached in `/var/lib/cloud/`. Its modular architecture allows cloud operators and users to customize which configuration tasks run and when they execute during the boot sequence.

- Cloud-init’s portability comes from datasources. A datasource is a plugin that knows how to retrieve metadata and user data from a specific cloud platform or environment. When cloud-init starts, it probes available datasources in order of preference to determine where it’s running and how to fetch configuration data.
  - OpenStack (reads from the metadata service at 169.254.169.254 or from config drive).
  - EC2 (Amazon Web Services metadata service).
  - Azure (Microsoft Azure’s instance metadata).
  - ...
