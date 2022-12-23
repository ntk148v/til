# Amazon Well-Architected Framework

Source:

- <https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html>
- <https://vticloud.io/aws-well-architected-framework-la-gi/> (VN)
- <https://www.romexsoft.com/blog/six-pillars-of-the-aws-well-architected-framework-the-impact-of-its-usage-when-building-saas-application/>

Table of Contents:

- [Amazon Well-Architected Framework](#amazon-well-architected-framework)
  - [1. Introduction](#1-introduction)
  - [2.General design principles](#2general-design-principles)
  - [3. Six pillars of AWS Well-Architected Framework](#3-six-pillars-of-aws-well-architected-framework)
  - [3.1 Operational excellence](#31-operational-excellence)
    - [3.2. Security](#32-security)
    - [3.3. Reliability](#33-reliability)
    - [3.4. Performance efficiency](#34-performance-efficiency)
    - [3.5. Cost optimization](#35-cost-optimization)
    - [3.6. Sustainability](#36-sustainability)
  - [4. AWS Well-Architected Tool](#4-aws-well-architected-tool)

## 1. Introduction

- AWS Well-Architected Framework helps you understand the pros and cons of decisions you make building systems on AWS. By using the Framework you will learn architectural best practices for designing and operating reliable, secure, efficient, cost-effective, and sustainable systems in the cloud.
- AWS provides a service for reviewing workloads at no charge - [AWS Well-Architected Tool](http://aws.amazon.com/well-architected-tool/?ref=wellarchitected-wp).
- Hands-on with [AWS Well-Architected Labs](https://www.wellarchitectedlabs.com/?ref=wellarchitected-wp).

## 2.General design principles

- Stop guessing your capacity needs.
- Test systems at production scale.
- Automate to make architectural experimentation easier.
- Allow for evolutionary architectures.
  - Design based on changing requirements
- Drive architectures using data.
- Improve through game days.
  - Simulate applications for flash sale days

## 3. Six pillars of AWS Well-Architected Framework

AWS Well-Architected Framework is based on six pillars.

![](https://cloudfront.romexsoft.com/wp-content/uploads/2022/08/aws-well-architected-pillars.svg)

## 3.1 Operational excellence

- Ability to support development and run workloads effectively, gain insight into their operations, and to continously improve supporting processes and procedures to deliver business value.
- Design principles:
  - Perform operations as code: Entire workload (applications, infrastructure) as code.
  - Make frequent, small, reversible changes (without affecting customers when possible).
  - Refine operations procedures frequently.
  - Anticipate failure: perform "pre-mortem" exercises to identify potential sources of failure.
  - Learn from all operational failures.
- Best practice areas:
  - Organization
  - Prepare
  - Operate
  - Evolve

### 3.2. Security

- The ability to protect data, systems, and assets to take advantage of cloud technologies to improve your security.
- Design principles:
  - Implement a strong identity foundation: the principle of least privilege.
  - Enable traceability.
  - Apply security at all layers.
  - Automate security best practices.
  - Protect data in transit and at rest.
  - Keep people away from data: reduce/eliminate the need for direct access or manual processing of data.
  - Prepare for security events.

![](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2019/03/11/aws-security-services-by-function.png)

- Best practice areas:
  - Securit
  - Identity and Access Managemen
  - Detectio
  - Infrastructure Protectio
  - Data Protectio
  - Incident Response

### 3.3. Reliability

- The ability of a workload to perform its intended function correctly and consistently when it's expected to. This includes the ability to operate and test the workload through its total lifecycle.
- Design principles:
  - Automatically recover from failure.
  - Test recovery procedures.'
  - Scale horizontally to increase aggregate workload availability.
  - Stop guessing capacity.
  - Manage change in automation.
- Best practice areas:
  - Foundations
  - Workload Architecture
  - Change Management
  - Failure Management

### 3.4. Performance efficiency

- The ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve.
- Design principles:
  - Democrative advanced technologies.
  - Go global in minutes: Deploy workloads in multiple AWS regions.
  - Use serverless architectures.
  - Experiment more often.
  - Consider mechainical sympathy: understand how cloud services are consumed and always use the technology approach that aligns best with your workload goals.
- Best practice areas:
  - Selection
  - Review
  - Monitoring
  - Tradeoffs

### 3.5. Cost optimization

- The ability to run systems to deliver business value at the lowest price point.
- Design principles:
  - Implement Cloud financial mangement.
  - Adopt a consumption model.
  - Measure overall efficiency.
  - Stop spending money on undifferentiated heavy lifting: AWS does the heavy lifting of data center operations like racking, stacking, and powering servers.
  - Analyze and attribute expenditure.
- Best practice areas:
  - Practice Cloud Financial Management
  - Expenditure and usage awareness
  - Cost-effective resources
  - Manage demand and supply resources
  - Optimize over time

### 3.6. Sustainability

- Environment impacts, especially energy consumption and efficiency.
- Design principles:
  - Understand your impact
  - Establish sustainability goals
  - Maximize utilization
  - Anticipate and adopt new, more efficient hardware and software offerings
  - Use managed services
  - Reduce the downstream impact of your cloud workloads
- Best practice areas:
  - Region selection
  - User behavior patterns
  - Software and architecture patterns
  - Data patterns
  - Hardware patterns
  - Development and deployment process

## 4. AWS Well-Architected Tool

- Free tool to review your architectures against the 6 pillars Well-architected framework and adopt architectural best practices.
- How does it works?
  - Select workload and answer questions
  - Review your answers against the 6 pillars
  - Obtain advice
