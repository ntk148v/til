# ArgoCD best practices

Source: <https://codefresh.io/blog/argo-cd-best-practices/>

## 1. Separate your Git repositories

![](https://codefresh.io/wp-content/uploads/2023/07/word-image-20220330-174003-1.png)

## 2. Create a directory structure to enable a multi-application system for your Argo CD deployments

Tips:

- Do: We suggest modeling your environments or clusters using different folders instead of branches in your configuration repository (e.g., prod, staging, testing, etc.).
- Do: Make sure your cluster and environment configurations repositories are separated (i.e., separate your prod configuration in a different repository from staging).
- Do: Utilize some sort of manifest management, such as a raw Kubernetes YAML file, Kustomize, or Helm for your environment definitions for your apps.
- Do: Create an ‘argocd’ folder in your configuration repository for each cluster and create an Argo CD Application manifest for each app in the cluster’s repository.
  - By creating the separate ‘argocd’ folder, you can also implement role-based access control for different clusters if you wish with Git repository permissions.
- Do: Leverage a multi-folder or a multi-repo structure instead of a multi-branch approach. You should NOT have permanent branches for your clusters or environments.
- Don’t: Never put any independent applications or applications managed by different teams in the same repository.

[ArgoCD Autopilot](https://argocd-autopilot.readthedocs.io/en/stable/) provides an opinionated directory structure that also installs Argo CD and allows it to manage itself.

## 3. Determine a promotion strategy

**Group your applications**

- ApplicationSets:
  - ApplicationSet is a Kubernetes controller/CRD that enables automation and allows flexibility when managing multiple applications across several clusters.
  - The ApplicationSet consists of two main components:
    - Generators.
    - Application template.

![](https://codefresh.io/wp-content/uploads/2023/07/word-image-20220330-174007-1.png)

- Apps of Apps:
  - <=10 applications -> Apps of Apps.
  - You are leveraging the actual app itself, aka a “Root App,” to contain the other applications instead of individual Kubernetes objects. This, in turn, allows you to manage a group of applications that you can deploy declaratively. Essentially this pattern supports the declaration of children apps in a recursive way.

**Which to choose?**

One does not “need” a promotion strategy when beginning to deploy with Argo CD. The strategies listed above are needed when trying to solve “too many apps.” This problem dramatically depends on the number of Argo CD applications you are managing and whether or not you already have a deployment process in place or not.

## 4. Manage your secrets securely

**Encrypt your secrets directly in your Git repository**

- [Bitnami Sealed Secrets](https://engineering.bitnami.com/).
- [SOPS](https://github.com/mozilla/sops).

**Externalizing your secrets from your Git repository**

- [ArgoCD Vault plugin](https://github.com/argoproj-labs/argocd-vault-plugin).
- Cloud provider secrets.

## 5. Confirm how your team accesses Argo CD

- Developers require access to Argo CD, so you need to set security measures and role-based access control (RBAC).
- No one within your organization requires access to Argo CD.

So, whichever approach you choose above – as long as it benefits you and your team, you’re making the right choice.

## 6. Increase automation for your system with the other Argo projects

> NOTE(kiennt26): Hmm it's nice but seems too much for me at this moment. Check out the post.
