# Infrastructure as Code

Source: <https://www.ibm.com/cloud/learn/infrastructure-as-code>

- [Infrastructure as Code](#infrastructure-as-code)
  - [1. What is Infrastructure as Code (IaC)?](#1-what-is-infrastructure-as-code-iac)
  - [2. Benefits](#2-benefits)
  - [3. Immutable infrastructure vs mutable infrastructure](#3-immutable-infrastructure-vs-mutable-infrastructure)
  - [4. Declarative vs imperative approach](#4-declarative-vs-imperative-approach)
  - [5. Tools](#5-tools)
    - [5.1. Potential tools](#51-potential-tools)
    - [5.2. Choose the right one](#52-choose-the-right-one)

## 1. What is Infrastructure as Code (IaC)?

- IaC uses a high-level descriptive coding language to automate the provisioning of IT infrastructure, enabling your organization to develop, deploy and scale cloud applications with greater speed, less risk and reduced cost.

## 2. Benefits

- Faster time to production/market.
- Improved consistency-less 'configuration drift'.
- Faster, more efficient development.
- Protection against churn.
- Lower costs and improved ROI.

## 3. Immutable infrastructure vs mutable infrastructure

- Mutable infrastructure:

  - Can be modified or updated after it is originally provisioned.
  - Flexibile customization.
  - Hard to maintain consistency between deployment or within versions - and can make infrastructure version tracking much more difficult.

- Immutable infrastructure:
  - Cannot be modified once originally provisioned. Change -> replace with new infrastructure.
  - Easy to maintain consistency between test and deployment environment.
  - Easy to maintain and track infrastructure versions and to confidently roll back to any version when necessary.

## 4. Declarative vs imperative approach

- Declarative - the functional approach.

  - Specify the desired final state of the infrastructure you want to provision and the IaC software handles the rest.
  - Requires a skilled administrator to set up and manage, and these administrators often specialize in their prefered solution.

- Imperative - the procedural approach.
  - Prepare automation scripts that provision your infrastructure one specific step at a time.
  - Easier for existing administrative staff to understand and can leverage configuration scripts you already have in place.

## 5. Tools

### 5.1. Potential tools

- [Ansible](https://www.ansible.com/).
- [Terraform](https://www.terraform.io/).
- [Chef](https://www.chef.io/).
- [Puppet](https://puppet.com/).
- [SaltStack](https://www.saltstack.com/).

### 5.2. Choose the right one

- Choosing the most appropriate tool requires a way of understanding the many tasks involved in app and infrastructure provisioning.
- Tasks are generally divided into the domains of _configuration management_ and _configuration orchestration_.
  - Configuration management: install and manage software on existing server instances.
  - Configuration orchestration: provision the server instances themselves, leaving the job of configuring those servers to other tools.

![](https://1.cms.s81c.com/sites/default/files/2018-11-19/Screen%20Shot%202018-11-19%20at%205.03.18%20PM.png)
