# Hashicorp Vault

Vault provides centralized, well-audited privileged access and secret management for mission-critical data whether you deploy systems on-premises, in the cloud, or in a hybrid environment.

With a modular design based around a growing plugin ecosystem, Vault lets you integrate with your existing systems and customize your application workflow.

## 1. Key concepts

### 1.1. Seal/Unseal

When you start a Vault server, it starts in a sealed state. In this state, Vault can access the physical storage, but it cannot decrypt any of the data on it. Unsealing is the process of obtaining the plaintext root key that is necessary to read the decryption key.

Vault encrypts most data using the encryption key in the keyring <- to get the keyring, Vault uses the root key to decrypt it <- the root key itself requires the unseal key to decrypt it.

**Shamir seals**

![](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/vault-shamir-seal.png)

Vault uses an algorithm known as Shamir's Secret Sharing to split the key into shares. Vault requires a certain threshold of shares to reconstruct the unseal key. Vault operators add shares one at a time in any order until Vault has enough shares to reconstruct the key. Then, Vault uses the unseal key to decrypt the root key.

Once you unseal a Vault node, it remains unsealed until one of the following happens:

1. You reseal it using the API.
2. You restart the server.
3. Vault's storage layer encounters an unrecoverable error.

## 2. Lease, renew, and revoke

With every dynamic secret and `service` type authentication token, Vault creates a _lease_: metadata containing information such as a time duration, renewability, and more.
