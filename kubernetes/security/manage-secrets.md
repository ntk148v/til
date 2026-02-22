# Manage secrets in K8s using GitOps without compromising security

Source:

- <https://platformengineering.org/talks-library/manage-secrets-in-k8s-using-gitops-without-compromising-security>
- <https://kubernetes.io/docs/concepts/configuration/secret/>

You're probably well aware that storing sensitive data in a cluster is extremely foolhardy. This is true even if you follow best practices for Kubernetes Secrets.

![](https://cdn.prod.website-files.com/6489e23dd070ba71d41a33b2/6491625a4bc89d9efb8b8169_6426c10b65f015747b4e9e74_cYNOvjj4gQzz3j3YzdPzDGx0qDdfJ3XfEty2xDHBd2awDNdXKMpwUP7YGI03FHNoj6K16qdda0Xcd5EDoYf_i_elwbRc0UyI9jFJpKi7d3eevadw2jqY5XrWALDsQP2Oa45PW6YrDpXUyZF8odiwOuk.png)

- For starters, K8s stores secrets as base64-encoded, encrypted strings -> anyone can easily reverse the encryption.
- Storing secrets in Git is a common vulnerability that ultimately lengthens your to-do list.
- K8s supports encrypting secret data at rest, which you should take advantage of. For this to succeed, you'll need to enable etcd and define a config specifying encryption resource targets by name.
- Unfortunately, encrypt-at-rest has its weaknesses too. Many organizations forget to limit cluster admin roles properly or remove secrets, making it pretty simple to peek behind the curtain. If you go this route, it's essential to implement the correct role-based access controls to manage who can access what.

The nice thing about the GitOps way is that you still get to be flexible, which enables you to use what suits your organization. Rajith shared two major options: Storing the encrypted secret and storing a reference to a secret.

![](https://cdn.prod.website-files.com/6489e23dd070ba71d41a33b2/6491625a4bc89d9efb8b8165_6426c10b23073ddbffdd964b_byIvlqIh-EegGE_1cahzZrLAoO-1To-YO5FVC8yBSUNVM_8-xmpMGGjpxqKajFUHbrM-dMbmNlcUMpWzYN-vNCzY8y1Y8cVXa_rdetWHrJGw6d_6_ZdgASRN-NvHKw_5CC_27CVI71HM3kHDX8UKTTM.png)

- Storing an encrypted secret:
  - Create a secret that only a few people can decrypt using an automation tool like [Bitnami Sealed Secret](https://github.com/bitnami-labs/sealed-secrets) or [Mozilla SOPS](https://github.com/mozilla/sops).
  - Your automation tool encrypts the secret as you store it in Git. When it's time to decrypt and create a Kubernetes Secret, the tooling steps up to the plate again to handle the details.
- Storing a reference to a secret:
  - When storing a reference to a secret, you store the secrets in some kind of backend such as HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, etc.
  - use a tool like the [External Secrets Operator](https://external-secrets.io/) to declaratively specify which secrets you need and where they need to be stored in your Git repo.

With the encrypted secret method, it doesn't matter if someone gets into your repo, the key isn't there. Yes, you do need to worry about key rotation and other security practices, but it's a sound technique if you're just getting started.

Storing a reference achieves a few important goals. It lets developers clearly communicate to the platform engineering or SRA teams what to provision in the secret store. The reference option also appeals from the management point of view since storing secrets in a purpose-built tool grants you audit logs and other features that promote security and scalability.

Again, this is one area where it's OK to explore. Do what suits your organization best from a maintainability and sustainability perspective.
