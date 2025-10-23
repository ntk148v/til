# Hashicorp Vault

Vault provides centralized, well-audited privileged access and secret management for mission-critical data whether you deploy systems on-premises, in the cloud, or in a hybrid environment.

With a modular design based around a growing plugin ecosystem, Vault lets you integrate with your existing systems and customize your application workflow.

## 1. Key concepts

### 1.1. Seal/Unseal

When you start a Vault server, it starts in a sealed state. In this state, Vault can access the physical storage, but it cannot decrypt any of the data on it. Unsealing is the process of obtaining the plaintext root key that is necessary to read the decryption key.
