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

### 1.2. Lease, renew, and revoke

With every dynamic secret and `service` type authentication token, Vault creates a _lease_: metadata containing information such as a time duration, renewability, and more. Vault promises that the data will be valid for the given duration, or TTL. Once the lease is expired, Vault can automatically revoke the data, and the consumer of the secret can no longer be certain that it is valid.

The benefit should be clear: consumers of secrets need to check in with Vault routinely to either renew the lease (if allowed) or request a replacement secret.

### 1.3. Tokens

Tokens are the core method for authentication within Vault.
Token map to information:

- A set of one or more  attached policies. These policies control what the token holder is allowed to do within Vault.
- Metadata that can be viewed and is added to the audit log, such as creation time, last renewal time, and more.

There are three types of token:
- `service`: what users will generally think of as "normal" Vault tokens. Full features, but heavyweight to create and track.
- `batch` tokens are encrypted blobs that carry enough information for them to be used for Vault actions, but they require no storage on disk to track them. Extremely lightweight and scalable, but lack of features.
- `recovery`.

| Token Type      | Vault 1.9.x or earlier | Vault 1.10 and later |
| --------------- | ---------------------- | -------------------- |
| Service tokens  | s.<random>             | hvs.<random>         |
| Batch tokens    | b.<random>             | hvb.<random>         |
| Recovery tokens | r.<random>             | hvr.<random>         |

Root tokens are tokens that have the `root` policy attached to them. Root tokens can do _anything_ in Vault (never expired).

Normally, when a token holder creates new tokens, these tokens will be created as children of the original token; tokens they created will be children of them; and so on.

When tokens are created, a token accessor is also created and returned. This accessor is a value that acts as a reference to a token and can only be used to perform limited actions:
- Look up a token's properties.
- Look up a token's capabilities on a path.
- Renew the token.
- Revoke the token.

The token _making the call, not the token associated with the accessor, must have appropriate permissions for these functions.
