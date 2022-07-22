# Terraform

Source: <https://www.terraform.io/docs>

## 1. Introduction

- An infrastructure as code (IaC) tool that allows you to build, change, and version infrastructure safely and efficiently.
  - Low-level components: compute instances, storage, and networking.
  - High-level components: DNS entries and SaaS features.
- Terraform creates and manages resources on cloud platforms and other services through their application programming interfaces (APIs).

![](https://content.hashicorp.com/api/assets?product=terraform&version=v1.2.5&asset=website%2Fimg%2Fdocs%2Fintro-terraform-apis.png&width=2048&height=644)

- The core Terraform workflow consists of three stages:

![](https://content.hashicorp.com/api/assets?product=terraform&version=v1.2.5&asset=website%2Fimg%2Fdocs%2Fintro-terraform-workflow.png&width=2048&height=1798)

- Use cases:
  - Multi-cloud deployment
  - Application infrastructure deployment, scaling, and monitoring tools
  - Self-service clusters
  - Policy compliance and management
  - PassS application setup
  - Software defined networking (SDN)
  - Kubernetes
  - Parallel environments
  - Software demos

## 2. Configuration

- The main purpose of the Terraform language is declaring resources, which represent infrastructure objects.

```terraform
resource "aws_vpc" "main" {
  cidr_block = var.base_cidr_block
}

# Declarative
# Blocks are containers for other content and usually represent
# the configuration of some kind of object, like resource
<BLOCK TYPE> "<BLOCK LABEL>" "<BLOCK LABEL>" {
  # Block body
  <IDENTIFIER> = <EXPRESSION> # Arguments assign a value to a name.
  # Expressions represent a value, either literally or by referencing and combining
  # other values.
}
```

## 3. Tools

- [Gaia](https://github.com/gaia-app/gaia) - a Terraform UI.
- [Stack-Lifecycle-deployment](https://github.com/D10S0VSkY-OSS/Stack-Lifecycle-Deployment)
- [Rover](https://github.com/im2nguyen/rover) - Interactive Terraform visualization. State and configuration explorer.
