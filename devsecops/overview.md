# DevSecOps

Source:

- <https://www.redhat.com/en/topics/devops/what-is-devsecops>
- <https://www.synopsys.com/glossary/what-is-devsecops.html>
- <https://www.microfocus.com/en-us/what-is/devsecops>
- <https://www.infracloud.io/blogs/implement-devsecops-secure-ci-cd-pipeline/>
- <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/secure/devsecops-controls>

Table of contents:

- [DevSecOps](#devsecops)
  - [1. Overview](#1-overview)
  - [2. DevSecOps lifecycle and key components](#2-devsecops-lifecycle-and-key-components)
    - [2.1. Plan/Design](#21-plandesign)
    - [2.2. Develop](#22-develop)
    - [2.3. Build and code analysis](#23-build-and-code-analysis)
    - [2.4. Test](#24-test)
    - [2.5. Deploy](#25-deploy)
    - [2.6. Monitoring and Alerting](#26-monitoring-and-alerting)

## 1. Overview

- DevSecOps stands for _development, security, and operations_.
- DevSecOps automates the integration of security at every phase of the software development lifecycle (SDLC), from initial design through integration, testing, deployment, and software delivery.
- In the past, the role of security was isolated to a specific team in the final stage of development.

![](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/devsecops-linear-405x259.png?itok=1jsWGdOF)

- Now, in the collaborative framework of DevOps, secuirty is a shared responsibility integrated from end to end. It's a mindset that is so important, it led some to coin the term "DevSecOps" to emphasize the need to build a security foundation into DevOps initiatives.

![](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/devsecops-collab-405x308.png?itok=VsZ8waJV)

- DevSecOps enables seamless application security earlier in the SDLC, rather than at the end when vulnerability findings requiring mitigation are more difficult and costly to implement. It also means automating some security gates to keep the DevOps workflow from slowing down.
- DevSecOps is an extension of Devops, and is sometimes referred to as Secure DevOps, which means DevSecOps is about integrating Security into CI/CD pipeline.

![](https://snyk.io/wp-content/uploads/DevSecOps-Pipeline-1240x670.png)

- Benefits of the DevSecOps model:
  - Faster delivery.
  - Improved security posture.
  - Reduced costs.
  - Enhancing the value of DevOps.
  - Improving security integration and pace.
  - Enabling greater overall business success.

## 2. DevSecOps lifecycle and key components

DevSecOps requires planning application and infrastructure security from the start.

![](https://dlhr6gotgr9bx.cloudfront.net/2021-11/devsec.png)

![](https://d33wubrfki0l68.cloudfront.net/2d13f6c9c86cf550d671b50107181fdf3dc51c72/68c99/assets/img/blog/devsecops-pipeline/devsecops-pipeline-1600x350.svg)

### 2.1. Plan/Design

- Threat modeling: It effectively puts you in the mindset of an attacker and allow us to see the application through the attacker's eyes and block their attack before they get a chance to do anything about it.
  - Threat modeling is a simple concept, though it can be detailed and technical if need be. It reveals and documents a realistic security view of application that includes:
    - How attackers can abuse that application's design
    - How to fix vulnerabilities
    - How important it is to fix issues
  - There are published approaches for threat modeling that range from simple question and answer methods to detailed tool-based analysis. You can base your approach on methodologies like the [STRIDE model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats), the [DREAD model](<https://en.wikipedia.org/wiki/DREAD_(risk_assessment_model)>), or [OWASP threat modeling](https://owasp.org/www-community/Threat_Modeling).
- Secure SDLC: separate development, testing, and production environments and also have autorization processes that control the deployment promotion from one environment to another.

### 2.2. Develop

- IDE security plugins and [pre-commit](https://pre-commit.com/).
- Peer code review: It's good practice to have a security champion or knowledgeable security teammate who can guide the developer during the peer review process.
- [Secure coding practice guidelines](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/) help developers learn essential secure coding principles and how should applied.
- Code repository - Secret management

### 2.3. Build and code analysis

- Software composition analysis (SCA):
  - Open source software often times includes security vulnerabilities, so a complete security approach includes a solution that tracks OSS libraries, and reports vulnerabilities and license violations.
  - SCA automates the visibility into open source software for the purpose of risk management, security and license compliance.
  - [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- Static application security testing (SAST):
  - SAST scans the application source files, accurately identifies the root cause and helps remediate the underlying security flaws.
  - It analyzes the code based on predefined rule sets.
  - [SonarQube](https://github.com/SonarSource/sonarqube)

### 2.4. Test

- Dynamic application security testing (DAST): simulates controlled attacks on a running web apoplication or service to identify exploitable vulnerabilities in a running environment.
  - DAST is a web application security test that finds security issues in the running application.
  - [List of DAST scanning tools provided by OWASP](https://owasp.org/www-community/Vulnerability_Scanning_Tools)

### 2.5. Deploy

### 2.6. Monitoring and Alerting
