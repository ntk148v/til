# Pulumi

Source: <https://www.pulumi.com/docs/get-started/>

- [Pulumi](#pulumi)
  - [1. How it works](#1-how-it-works)
  - [2. Program, project and stack](#2-program-project-and-stack)
  - [3. Pulumi vs. X](#3-pulumi-vs-x)
    - [3.1. Terraform](#31-terraform)

> Modern infrastructure as Code platform that allows you to use familiar programming languages (TypeScript, JavaScript, Python, Go, .NET, Java), markup languages (YAML) , and tools to build, deploy, and manage cloud infrastructure.

## 1. How it works

- Pulumi uses a desired state model for managing infrastructure.
  - A Pulumi program is executed by a **language host** to compute a desired state for a stack's infrastructure.
  - The **deployment engine** compares this desired state with the stack's current state and determines what resources need to be created, updated or deleted.
  - The engine uses a set of resource providers in order to manage the **individual resources**. As it operates, the engine updates the state of your infrastructure with information about all resources that have been provisioned as well as any pending operations.

![](https://www.pulumi.com/images/docs/reference/engine-block-diagram.png)

- Pulumi executes resource operations in parallel whenever possible, but understands that some resources may have dependencies on other resources.
- By default, if a resource must be replaced, Pulumi will attempt to create a new copy of the resource before destroying the old one.

## 2. Program, project and stack

- Pulumi programs are structured as projects and stacks. The distinction between them is:
  - **Program**: a collection of files written in your chosen programming langugage.
  - **Project**: a directory containing a program, with metadata, so Pulumi knows how to run it.
  - **Stack**: an instance of your project, each often corresponding to a different cloud environment.
- Code structure & useful commands:

```bash
# To use Pulumi without Pulumi services
$ pulumi login --local
# List all templates
$ pulumi new -l
# Create new project from template
$ pulumi new openstack-go
$ tree
├── go.mod # Golang module
├── go.sum
├── main.go # Golang main program
├── Pulumi.dev.yaml # Pulumi stack definition
└── Pulumi.yaml # Pulumi project config
# Create a new stack
$ pulumi stack init staging
$ pulumi stack ls
$ pulumi stack select dev
# Destroy a stack
$ pulumi destroy
# Delete a stack with no resources
$ pulumi stack rm --force
```

- Stack outputs:

  - A stack can export values as stack outputs. For example:

  ```go
  ctx.Export("url", resource.Url)
  ```

  ```bash
  pulumi stack output url
  ```

- Stack references: allow you to access the outputs of one stack from another stack. For example:

```go
other, err := pulumi.NewStackReference(ctx, "acmecorp/infra/other", nil)
if err != nil {
    return err
}
otherOutput := other.GetOutput(pulumi.String("x"))
```

- State and backend:
  - Pulumi stores metadata (_state_) about infrastructure so that it can manage cloud resources. Each stack hash its own state.
  - Pulumi stores state in a _backend_. A backend is an API and storage endpoint used by the CLI to coordinate updates, and read and write stack stack state whenever appropriate.
  - Backend:
    - Service: a managed cloud experience using the online or self-hosted Pulumi service application.
    - Self-managed: AWS S3 (and compatible server such as Minio, Ceph), Microsoft Azure Blob Storage, Google Cloud Storage, or a local filesystem.

## 3. Pulumi vs. X

### 3.1. Terraform

- <https://phoenixnap.com/blog/pulumi-vs-terraform>
- <https://www.pulumi.com/docs/intro/vs/terraform/>

|                        | Pulumi                                                                     | Terraform                                                                           |
| ---------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Language support       | No DSL                                                                     | Has a DSL (HCL). Can extend with Terraform Cloud Development Kit.                   |
| IaC approach           | Declarative                                                                | Declarative                                                                         |
| State Management       | Managed through Pulumi Service by default, self-managed options available. | Self-managed b default, managed SaaS offering available.                            |
| User                   | Suitable for Developers                                                    | Suitable for many roles: Developers, DevOps Engineers, System Admin                 |
| Resource support       | 1945 provides, 8673 modules & counting support                             | 82 providers                                                                        |
| Documentation          | Limited, with best resources found on Pulumi slack and Github              | Excellent official documentation                                                    |
| Testing and validation | Unit, property, and integration testing. Supports popular test frameworks  | Intergration testing only                                                           |
| Secrets management     | Yes, secrets are encrypted in transit and in the state file.               | No, secrets are stored in Vault. There is no way to encrypt them in the state file. |
| Deploying to the cloud | Can be done from a local service                                           | Must be done through the SaaS platform                                              |
| Modularity             | Problematic with higher-level Pulumi extensions                            | Ideal due to reusable components                                                    |
