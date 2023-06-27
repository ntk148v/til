# DevSecOps

Source:

- <https://github.com/OWASP/DevSecOpsGuideline>
- <https://www.linkedin.com/posts/practical-devsecops_which-security-testing-methodology-is-right-ugcPost-7068533553487052800-4ZTq>

Table of contents:

- [DevSecOps](#devsecops)
  - [0. Threat modeling (Design)](#0-threat-modeling-design)
  - [1. Pre-commit](#1-pre-commit)
  - [2. Vulnerability Scanning](#2-vulnerability-scanning)
    - [2.1. Static Application Security Test - SAST](#21-static-application-security-test---sast)
    - [2.2. Dynamic Application Security Testing (DAST)](#22-dynamic-application-security-testing-dast)
    - [2.3. Interactive Application Security Testing (IAST)](#23-interactive-application-security-testing-iast)
    - [2.4. Software Component/Composition Analysis (SCA)](#24-software-componentcomposition-analysis-sca)
    - [2.5. Infrastructure Vulnerability Scanning](#25-infrastructure-vulnerability-scanning)
    - [2.6. Container Vulnerability Scanning](#26-container-vulnerability-scanning)
    - [2.7. Privacy](#27-privacy)
  - [3. Compliance Auditing](#3-compliance-auditing)

```shell
The purpose and intent of DevSecOps is to build on the mindset that “everyone is responsible for security” with the goal of safely distributing security decisions at speed and scale to those who hold the highest level of context without sacrificing the safety required.”

-- Shannon Lietz - founder at DevSecOps foundation --
```

- DevSecOps culture: introducing security earlier in the process instead of having it in the final steps. Considering security in design by threat modeling and break down huge security tests in smaller security testing and integrating them in the development pipeline.

![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/DevOps%20vs%20DevSecOps.png)

- DevSecOps is about injecting security in software writing and testing, so let's talk about testing.

  - Testing strategies:
    - Positive testing: Positive testing assumes that, under normal conditions and inputs, everything will _behave as expected_.
    - Negative testing: Negative testing checks the system behavior _under unexpected conditions_.
  - Methods of testing:

    - Static testing (Static application security testing - SAST):

      - Checks software defects without executing the application code.
      - Performed in the early stage of development to avoid errors, as it is easier to find souces of failures and it can be fixed easily.
      - Issues: hard coded credentials, deprecated encryption algorithms, 2nd order injections, weak random,...
      - Scope: 1 component at time.

      ![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/sast_scanning.png)

    - Dynamic testing (Dynamic application security testing - DAST):

      - Analyzes the behavior of the application code at runtime.
      - Scanners specially crafted requests to the target application. Request parameters are constantly modified during testing to try and expose a range of vulnerabilities. Based on the response of the application the tool can then identify potential vulnerabilities and report back.
      - Issues: cliend side vulnerabilities like authentication & session issues, sensitive data sent in plain text,...
      - Scope: mutiple components at once.

      ![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/dast_scanning.png)

    - Interactive analysis (Interactive Application Security Testig (IAST) ):

      - Monitors the application (using sensors/agents deploy with the application) while other systems interact with it and observe vulnerabilities.
      - Scope: 1 component/multiple components (agents/sensors are deployed on all components) at once.

      ![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/iast_analysis.png)

## 0. Threat modeling (Design)

- What: A systematically listing all the potential ways one can attack an application - a process for looking at attacks actively.
  - Output:
    - Diagrams
    - Security requirements
    - Non-requirements
    - List of threats / vulnerabilties
- Why:
  - Pro-active approach to finding threats
  - Increasing efficiency by reducing costs
  - A better prioritization based on bugs and mitigation plan
  - A better understanding of the system
- Who: It depends on the organization.
  - Artitect.
  - Developer
  - Tester
  - Security expert
- When: Threat Modeling should be as early as possible in the software design process.
- How:

  - Approaches:
    - Attacker-centric approach: producing steps:
      - Create a list of assets
      - Draw assets, components and data flows
      - For each element, check for threats
    - Asset-centric approach: producing steps:
      - Create a list of threat actors: motive, means, opportunity
      - Create a list of threats
    - Application-centric approach: producing steps:
      - Draw a diagram of the application
      - List threats for each element: STRIDE, OWASP Top 10
      - Rank threats using a classification model\
  - Methodology: according to the approaches, there is a list of methodology:
    - PASTA
    - Microsoft Threat Modeling
    - OCTAVE
    - TRIKE
      - VAST

- Pipeline:

  ![](https://github.com/OWASP/DevSecOpsGuideline/raw/master/assets/images/DevSecOps-pipeline.png)

  - Pipeline with tools:

  ![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/Pipeline-view.png)

## 1. Pre-commit

- Pre-commit phase is important because it can prevent security issues before they are submitted to a central Git repository.
- Different types of pre-commit actions:
  - **Secrets management**: make sure that there are no secrets in the code.
    - Approach: scanning the repo for sensitive information, and then remove them; note that when a credential is leaked, it is already compromised and should be invalidated.
    - Detecting secrets in several locations:
      - Detecing existing secrets by searching in a repository for existing secrets
      - Using Pre-commit hooks in order to prevent secrets for entering code base
      - Detecting secrets in pipeline
    - The best location is the _pre-commit_ location. Another locatiotn is the build server or the _build_ process.
    - Tools: [gittyleaks](https://github.com/kootenpv/gittyleaks), [git-secrets](https://github.com/awslabs/git-secrets), [repo-supervisor](https://github.com/auth0/repo-supervisor),...
  - **Linting code**:
    - The automated checking of source code for _programmatic and stylistic errors_ - using lint tool (linter)
      - Detect _errors_ in a code and errors that can lead to a security vulnerabilities
      - Detect _formatting or styling issues_
      - Suggest _best practices_
      - Increase _overall quality of code_
      - Make _maintenance of code_ easier.
    - Issues with linters:
      - Not every language has "quality" standard linter tools available, each framework usually has one or several linters
      - Different versions or configurations can lead to different results
      - Since some linters are very verbose and information overload can lead to focusing on "unimportant" issues
    - Perform it in the _pre-commit_ phase. Another phase: _build_ phase.

![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/pre-commit.png)

- Tools: [Pre-commit](https://pre-commit.com/) - A framework for managing and maintaining multi-language pre-commit hooks.

## 2. Vulnerability Scanning

- Vulnerability scanning is an inspection of the potential points of exploit on a computer, application, endpoints, and IT infrastructure (including network) to identify security holes.
- Different types of vulnerability scanning:
  - Static Application Security Test - SAST
  - Dynamic Application Security Test - DAST
  - Interactive Application Security Testing - IAST
  - Software Composition Analysis - SCA
  - Infrastructure Vulnerability Scanning
  - Container Vulnerability Scanning

### 2.1. Static Application Security Test - SAST

![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/Static%20scanning.png)

- _Static Code Analysis_ or _Source Code Analysis_ is usually part of Code Review (_white-box testing_) and it is a method of computer program debugging that is done by examining the code without executing the program.
  - Syntax violations
  - Security vulnerabilities
  - Programming errors
  - Coding standard violations
  - Undefined values
- To achieve a better result, combine static security scanning, 3rd party code (open-source libraries) scanning, IaC (Infrastructure as Code) security scan.
  - Static Code Analysis (known as SAST):
    - [SonarQube](https://www.sonarqube.org/): An open-source web-based tool, extending its coverage to more than 20 languages, and also allows a number of plugins.
    - [Veracode](https://www.veracode.com/security/static-analysis-tool): A static analysis tool that is built on the SaaS model. This tool is mainly used to analyze the code from a security point of view
    - [Checkmarx SAST](https://checkmarx.com/cxsast-source-code-scanning/): A static analysis security vulnerability scanner
  - Open-source libraries (3rd party / dependency) scanning (known as SCA):
  - IaC Security scanning:
    - [Checkov](https://github.com/bridgecrewio/checkov): Prevent cloud misconfigurations during build-time for Terraform, Cloudformation, Kubernetes, Serverless framework and other infrastructure-as-code-languages.
    - [ansible-lint](https://github.com/ansible-community/ansible-lint): Best practices checker for Ansible.
- When to use: During development
- Advantages: able to find security issues before application deployment. Easy integration with development toolchain.
- Disadvantages:
  - Generate a high number of false positives
  - Not suitable for identifying runtime issues or vulnerabilities that arise during the execution
- Cost: Moderate to high
- Use case scenario:
  - Detecting common coding errors
  - Finding vulnerabilities within your codebase
  - Ensuring code adherence to security standards

### 2.2. Dynamic Application Security Testing (DAST)

- DAST is a _black-box testing_, can find vulnerabilities and weaknesses in a running application by injecting malicious payloads to identify potential flaws that allow for attacks like SQL injections or cross-site scripting (XSS),...
  - Input or output validation
  - Authentication issues
  - Server configuration mistakes
- DAST tools allow for sophisticated scans on the client side and server side without needing the source code or the framework the application is built on.
- Tools:
  - [ZED Attack Proxy](https://www.zaproxy.org/): It is an open source tool which is offered by OWASP for performing security testing
  - [Acunetix](https://www.acunetix.com/): An automatic web security testing scanner that accurately scans and audits all web applications, including HTML5, JavaScript and Single Page applications (SPAs)
  - [Netsparker](https://www.netsparker.com/): It can identify vulnerabilities in all types of modern web applications, regardless of the underlying architecture or platform
  - [Veracode Dynamic Analysis](https://www.veracode.com/products/dynamic-analysis-dast): Veracode Dynamic Analysis helps companies scan their web applications for exploitable vulnerabilities at scale
  - [Checkmarx DAST](https://checkmarx.com/checkmarx-dast/)
- When to use: Post-development, during testing or production
- Advantages: Identifies vulnerabilities in the running applications
- Disadvantages:
  - May miss some vulnerables
  - Can generate false positives
  - Slows down the application during testing
- Cost: Moderate to high
- Use case scenario:
  - Identifying vulnerabilities in web applications, web services, and APIs.
  - Simulating real-world attacks

### 2.3. Interactive Application Security Testing (IAST)

- IAST is an application security testing method that tests the application while the app is run by an automated test, human tester, or any activity "interacting" with the application functionality.
- The core is sensor modules, software libraries included in the application code.
- Tools:
  - [Checkmarx Interactive Application Security Testing(CxIAST)](https://www.checkmarx.com/products/interactive-application-security-testing/)
  - [Contrast Community Edition](https://www.contrastsecurity.com/contrast-community-edition)

### 2.4. Software Component/Composition Analysis (SCA)

- _Component Analysis_ is the process of automating application security for managing third-party and open source components of codebase. SCA will find any potential vulnerable components in our codebase to prevent high security risks like Supply-Chain Attack, not only that but also provide licensing about each components
- Should put the SCA earlier, before security testing like SAST, DAST to prevent any vulnerable libraries pushed to production.
- Tools:
  - [OWASP Dependency-check](https://owasp.org/www-project-dependency-check)
  - [Safety](https://github.com/pyupio/safety)
  - [Synopsys BlackDuck](https://www.blackducksoftware.com/)
  - [Snyk](https://snyk.io/)
- When to use: During development and throughout the software development life cycle.
- Advantages: Identifies vulnerable third-party software.
- Disadvantages:
  - Doesn't identify issues inside the code
  - Limited scope around third-party software
- Cost: Low to moderate
- Use case scenario:
  - Promoting license and policy compliance
  - Identifying open-source component risks
  - Protecting against supply chain attacks
  - Checking dependencies for vulnerabilities

### 2.5. Infrastructure Vulnerability Scanning

- To make sure the infrastructure where deploy code is safe, incorporate vulnerability scanning into your pipeline.
- A vulnerability scanner is a computer program designed to assess computers, networks or applications for known weaknesses.
- Modern vulnerability scanners:
  - Allow for both authenticated and unauthenticated scans.
    - Authenticated scans allow for the scanner to directly access network based assets using remote administrative protocols such as secure shell (SSH) or remote desktop protocol (RDP) and authenticate using provided system credentials.
    - Unauthenticated scans is a method that can result in a high number of false positives and is unable to provide detailed information about the assets OS and installed software.
  - Typically available as SaaS
  - Able to customize vulnerability reports as well as the installed software, open ports, certificates and other host information that can be queried as part of its workflow.
- Tools:
  - [Nessus](https://www.tenable.com/products/nessus/nessus-professional)
  - [SAINT](https://www.carson-saint.com/)
  - [Nikto](http://www.cirt.net/nikto2)

### 2.6. Container Vulnerability Scanning

- As containers become an almost ubiquitous method of packaging and deploying applications, the instances of malware have increased. Securing containers is now a top priority for DevOps engineers. Fortunately, a number of open source programs are available that scan containers and container images.
  - Detect secure containers: outdated libraries, incorrectly configured containers, outdated OS
  - Detect compliance validations
  - Suggest best practices
- Use it at the _build_ phase when you're actually building for instance a Dockerfile and looking the resulting image that you're creating. Another location to perform would be when you _push_ an image to the registry or when you _pull_ an image from a registry. However, a good approach is scanning before pushing into a trusted container registry.

![](https://owasp.org/www-project-devsecops-guideline/latest/assets/images/container-security-pipeline.png)

- Tools:
  - [Clair](https://github.com/quay/clair)
  - [Falco](https://falco.org/)
  - [Harbor](https://goharbor.io/)
  - [Trivy](https://aquasecurity.github.io/trivy/)

### 2.7. Privacy

- Privacy has become an important aspect of application security.
  - GDPR, LGPD, CCPA and other laws and regulations have impose several controls over processing _PII (Personally Identifiable Information)_. What is considered PII?
    - First and last name
    - Identifiable email (name.lastname@domain.com)
    - Identify card numbers
    - Location data (mobile)
    - IP address
    - Racial or ethnic origin
    - Political opinions
    - ...
  - To comply with those regulations, DevSecOps have to be sure to use PII accordingly and protect data agains leaking.
  - Create a PII data flow to make sure you apply the required protection to the data thru its lifecycle.
  - All PII data processing requirements have to be specified. you have to create an inventory of all PII and evaluate the processing activity to make sure it follows all requirementes, such as:
    - Lawfulness, fairness and transparency
    - Purpose limitation
    - Data minimization
    - Accuracy
    - Storage limitation
    - Integrity and confidentiality (security)
    - Accountability

## 3. Compliance Auditing
