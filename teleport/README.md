# Teleport

Source: <https://goteleport.com/how-it-works/>

Teleport provides secure access to SSH or Windows servers, Windows desktops, Kubernetes clusters, database and web applications.

## 1. Architecture

- **cluster**: A Teleport cluster consists of the:
  - **Teleport Auth service**: The certificate authority of the cluster. It issues certificate to clients and maintain the audit log.
  - **Teleport Proxy service**: The proxy allows access to cluster resources from the outside. Typically it is the only service available from the public network.
  - **Teleport agents**: A Teleport agent runs in the same network as a target resource and speaks its native protocol.
  - And resource that you want to connect to such as Linux or Windows servers, databases, Kubernetes clusters, Windows desktops, and internal web apps.

## 2. How a Teleport cluster works

- The concept of a cluster is the foundation of the Teleport security model.
  - Users and servers must all join the same cluster before access can be granted.
  - To join a cluster, both users and servers must authenticate and receive certificates.
  - The Teleport Auth Service is the CA of the cluster, which issues certificates for both users and servers with all supported protocols.

### 2.1. Certificate-based authentication

- How authentication works:
  - Teleport Proxy service serves the login secreen on the `https://proxy.example.com:443`, where users are asked for their username, password, and second factor. If a third-party identity provider such as Github is used, the Proxy service forwards the user to Github using OAuth2.
  - Proxy Service sends the user's identity to the Teleport Auth service. In turn, the Auth service issues _certificates_ for SSH, Kubernetes, and other resources in a cluster, and sends them back to the client via the Proxy service.
  - That is called Certificate-based authentication. You have to run a Certificate Authority (CA) and distribute server and client certificates which impedes its adoption at scale.
- Teleport supports all the necessary certificate management operations to enable certificate-based authentication. Teleport operates two internal CA as a function of the **Teleport Auth service**. One is used to sign **User** certificates, and the other signs **Node** certificates. Each certificate is used to prove identity, cluster membership, and manage access.
- By default, all user certificates have an expiration date, also known as _the time to live_ (TTL). This TTL can be configured by a Teleport administrator. However, the node certificates issued by the Teleport Auth Service are valid indefinitely by default. Teleport supports certificate rotation, i.e. the process of invalidating all previously-issued certificates for nodes and users regardless of their TTL.

### 2.2. Authentication flow for SSH

- Teleport comes with its own `ssh` client - `tsh`. When a user types `ssh host` command, Teleport will check if a user has a valid SSH certificate in the `~/.tsh` directory or loaded into an `ssh-agent`. If no certificate is found, it will trigger the login sequence.

![](https://goteleport.com/_next/image/?url=%2F_next%2Fstatic%2Fmedia%2Fteleport-proxy.ddb384e1.png&w=640&q=75)

- Upon successful authentication, an SSH certificate will be stored in the user's `~/.tsh/keys` directory and loaded into an ssh-agent, if there is one running. If Kubernetes support is enabled, an x509 certificate for Kubernetes will be stored there as well, and `~/.kube/config` will be updated with it.
- The Teleport client stores the Teleport Proxy Service URL in `~/.tsh/profile`. The user does not need to use the `--proxy` flag again. They can edit the profile file when connecting to multiple Teleport clusters.

### 2.3. Connecting to Nodes

- When a user is authenticated, they can establish SSH and Kubernetes connections to a cluster.

```shell
# using SSH
$ tsh ssh hostname

# using K8s
$ kubectl get pods
```

![](https://goteleport.com/_next/image/?url=%2F_next%2Fstatic%2Fmedia%2Fteleport-connection.2160e2a0.png&w=640&q=75)

- Flow:
  - The client dials to the Teleport Proxy Service specified in ~/.tsh/profile file and relays to it the hostname of the destination hostname.
  - Teleport Proxy Service does not perform any decryption or authentication\*, it simply performs a name resolution for the given hostname and tries to relay the SSH connection to it. The user connection is shown in green.
  - The destination host validates the user's certificate and begins logging user actions to the Teleport Auth Service using its audit connection. The connection between a host and the Teleport Auth Service is also authenticated via the host's certificate and encrypted. The audit connection is shown in red.
  - If the destination host is a remote host, such as an IoT node (self-driving vehicle or a smart device) the connection is established using the reverse tunnel that remote nodes always maintain.
