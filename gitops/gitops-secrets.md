# The basics of GitOps secrets management (Kubernetes)

Source:

- <https://www.redhat.com/en/blog/a-guide-to-secrets-management-with-gitops-and-kubernetes>
- <https://www.harness.io/blog/gitops-secrets>

Kubernetes provides Secrets as objects to store confidential information without being visible in the application code. This mechanism makes it possible to use sensitive data with less risk of accidental exposure when managing the operations of Kubernetes itself. From a basic level, the process to create Kubernetes secrets is fairly straightforward:

- A trusted individual or source defines a Secret by creating a specific name for it and entering the confidential data. Kubernetes operators never see the actual data itself, only the name.
- Once a workload needs to access and use the confidential data, it will refer to that previously created specific name to retrieve it

Keeping sensitive data in Git in any capacity introduces a security risk, even if the repository is private with strict access controls. If a secret gets committed to a Git repository in plain text form, it must be revoked and no longer used. However, there are still ways to handle secrets in GitOps that mitigate security risks. Let's go over two of the popular methoddologies to manage secrets in GitOps:

## 1. Encrypted secrets:

> Store encrypted secrets in a Git repository and leverage automation to decrypt and render them as Kubernetes Secrets

[Bitnami Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets):

![](https://www.redhat.com/rhdc/managed-files/ohc/Copy%20of%20Secrets%20Management%20with%20GitOps-3.png)

- It takes advantage of public-key cryptography to encrypt secrets:
  - Using source control to store secrets.
  - Using a decryption key within a Kubernetes cluster to decrypt secrets.
- A CLI tool, Kubeseal, makes encrypting secrets simple because it has access to the cluster to retrieve encryption keys.

![](https://www.redhat.com/rhdc/managed-files/ohc/Copy%20of%20Secrets%20Management%20with%20GitOps-2.png)

- The main advantages are usability and eliminating the need to use a separate Secrets Manager, like Hashicorp Vault.
- You still need to manually encrypt each secret.
- The solution exclusively works with Kubernetes.

[Mozilla SOPs](https://github.com/mozilla/sops):

- A flexible CLI tool for encryption and decryption not limited to use cases with Kubernetes.
- Supports multiple input format.
- Supports integrations with Key Management Systems (KMS) like Hashicorp Vault, AWS KMS to provide encryption keys for securing secrets rather than storing secrets directly within with the KMS.
- Similar to how SealedSecrets work, secrets are manually encrypted by developers. It uses the SealedSecrets workflow but uses SOPS for encryption. It reads decryption keys from a key store and then decrypts secrets using a SOPS binary that a tool, such as Argo CD, can run with the SOPS plugin.

Disadvantages:

- Manually take secrets in plain text form, encrypt them, and store them in Git.
- The other downfall is that if any encrypted keys are compromised, it's difficult to retroactively find and revoke all of them.
- Scaling problem.

## 2. GitOps Secrets Reference

> Store references to the secrets in a Git repository Instead of storing encrypted secrets directly in Git. Then leverage automation to fetch the actual secrets based on their references before rendering them as Kubernetes Secrets.

To retrieve the secrets from the manager and get them into your cluster, you'll need an operator installed on your cluster to interact with secrets manager.

[External Secrets Operator](https://github.com/external-secrets/external-secrets) integrates external secret management systems like AWS Secrets Manager, hashicorp Vault, ... The operator reads information from external APIs and automatically injects the values into a Kubernetes Secret.

![](https://www.redhat.com/rhdc/managed-files/ohc/Copy%20of%20Secrets%20Management%20with%20GitOps-4.png)

Kubernetes Secrets Store CSI Driver is a solution to take secrets from an external secrets management tool and bring them into a Kubernetes cluster.

- More complex than External Secrets. Instead of retrieving external secrets and creating secret resources, this solution uses a separate volume attached to a pod to store secrets. A developer commits a SecretProviderClass with a reference to a secret. The GitOps operator deploys the change and the CSI Secret Store Operator Plugin then retrieves the secret from the secret management system. The operator plugin then creates a volume with the secret that is attached to a specified pod.

![](https://www.redhat.com/rhdc/managed-files/ohc/Copy%20of%20Secrets%20Management%20with%20GitOps.png)
