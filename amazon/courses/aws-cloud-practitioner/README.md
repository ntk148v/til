# AWS Cloud Practitioner Essentials

- [AWS Cloud Practitioner Essentials](#aws-cloud-practitioner-essentials)
  - [1. Introduction](#1-introduction)
  - [2. Compute in the cloud](#2-compute-in-the-cloud)
  - [3. Global infrastructure and reliability](#3-global-infrastructure-and-reliability)
  - [4. Networking](#4-networking)
  - [5. Storage and database](#5-storage-and-database)
  - [6. Security](#6-security)
  - [7. Monitoring and analytics](#7-monitoring-and-analytics)
  - [8. Pricing and support](#8-pricing-and-support)
  - [9. Migration and innovation](#9-migration-and-innovation)

## 1. Introduction

## 2. Compute in the cloud

- Amazon Elastic Compute Cloud (Amazon EC2)
- Instance types.
- Pricing:
  - On-demand: short-term, irregular workloads that can't be interrupted.
  - EC2 savings plans: enables you to reduce compute costs by committing to a consistent amount of compute usage for a 1-year or 3-year term. 72% costs.
  - Reserved instances: billing discount applied to the use On-demand instances -> saving cost.
  - Spot instances: flexible start and end times, or that can withstand interruptions. Use unused EC2 computing capacity and offer you cost savings up to 90% off of On-demand prices.
  - Dedicated hosts: physical servers with EC2 instance capacity that is fully dedicated to your use. The most expensive
- Autoscaling
- Elastic Load Balancing.
- Simple Notification Service (SNS): Publish/subscribe service.
- Simple Queue Service (SQS): Send, store, and receive messages between software components, without losing messages or requiring other services to be available.
- Serverless computing - Lambda: a service that lets you run code without needing to provision or manage servers.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649329200/S8RVV63Y8dS-u7dGgx73pA/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/mJqf2HpZ33b0nHmJ_ssdAdxlZRBGG7c57.png)

- Container:
  - Elastic Container service
  - Elastic Kubernetes service
  - Fargate: serverless compute engine for containers

## 3. Global infrastructure and reliability

- Region.
  - Compliance with data governance and legal requirements
  - Proximity to your customers: Selecting a Region that is close to your customers will help to get content to them faster
  - Available services within a Region
  - Pricing
- Availability Zones
  - A single data center or a group of data centers within a Region.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/old4pJtvN7HvddhL_zBL1ijNGsMMu3-4j.png)

- Edge locations: a site that Amazon CloudFront (global content delivery service) uses to store cached copies of your content closer.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/X3WxHCXa0QwTmj_6_OvAnh0SdGr1YBIds.png)

- Ways to interact with AWS services:
  - AWS management console
  - AWS commandline interface
  - Software development kits
- AWS Elastic Beanstalk
  - Adjust capacity
  - Load balacing
  - Automatic scaling
  - Application health monitoring
- AWS CloudFormation
  - Infrastructure as code

## 4. Networking

- Amazon Virtual Private Cloud (Amazon VPC):
  - A networking service that you can use to establish boundaries around AWS resources
  - You can organize your resources into subnets.
- Internet gateway: a connection between a VPC and the internet.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/Q_HnMl_BAEsDZGxf_NEblbQjD0vn0-pPU.png)

- Virtual private gateway: the component that allows protected internet traffic to enter into the VPC.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/tthacSS-FyYNWwE3_s8U3lQzEONXm1FMX.png)

- AWS Direct connect: a service that enables you to establish a dedicated private connection between your data center and a VPC.
  - The private connection that AWS Direct connect provides helps you to reduce network costs and increase the amount of bandwidth that travel through your network.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/p53HDtoqu2euSy0Y_YdzRvczPABE_j-yV.png)

- Subnets are separate areas that are used to group together resources.
  - A subnet is a section of a VPC in which you can group resources based on security or operational needs. Subnets can be public or private.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/-HQN-9SqkWc5e-yv_pi4TpfvEYaalWuIu.png)

- Customer requests data from an application hosted in the AWS Cloud, this request is sent as a packet - a unit of data sent over the internet/a network.
- VPC component that checks packet permissions for subnets is a network access control list (ACL)
  - A network ACL is a virtul firewall that controls inbound and outbound traffic at the subnet level.
  - Allow all inbound by default
  - Network ACLs perform stateless packet filtering. They remember nothing and check packets that cross the subnet border each way: inbound and outbound.
- VPC component that checks packet permissions for EC2 instance is a security group.
  - A security group is a virtual firewall that controls inbound and outbound traffic for an EC2 instance.
  - Deny all inbound by default
  - Security groups perform stateful packet filtering. They remember previous decisions made for incoming packets.

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649394000/WP26ii189k60AcCIBa0Wvw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/QkcDe-SJB4lQAuyB_ha8um-1InZb0jryB.png)

- Amazon Route 53 is a DNS web service. It gives developers and businesses a reliable way to route end users to internet applications hosted in AWS.
  - Connects user requests to infrastructure running in AWS. It can route users to infrastructure oouside of AWS
  - Ability to manage the DNS records for existing domain names managed by other domain registrars
  - Can work with Amazon CloudFront.

## 5. Storage and database

- Instance stores and Amazon Elastic Block Store (Amazon EBS):
  - A service that provides block-level storage volumes that you can use with Amazon EC2 instances.
  - Instance stores -> terminate instance -> lose data
  - ESB volume -> available
  - Incremental backups of EBS volumes by creating EBS snapshots
  - Data stored in a single Availability zone

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649397600/pmnCF6L4ssjtw7Ws1RUpZw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/8PP53iK51gK7pU4Q_ruyKsXvVP8ZbeHC1.png)

- Amazon Simple Storage Service (Amazon S3):
  - A service that provides object-level storage. Amazon S3 stores data as objects in buckets
  - Ulimited storage space. The maximum file size for an object in S3 is 5TB
  - Storage classes: consider these two factors:
    - How often you plan to retrieve your data
    - How available you need your data to be
- Amazon Elastic File System (Amazon EFS)
  - A scalable file system used with AWS cloud services and on-premises resources
  - Data stored in and across multiple Availbility Zones
- Amazon Relational Database Service (Amazon RDS):
  - A service that enables you to run relational databases in the AWS Cloud
  - A managed service that automates tasks such as hardware provisioning, database setup, patching, and backups
  - Database engines:
    - Amazon Aurora: an enterprise-class relational database.
    - PostgreSQL
    - MySQL
    - MariaDB
    - Oracle Database
    - Microsoft SQL Server
- Amazon DynamicDB:
  - A key-value database service. It delivers single-digit millisecond performance at any scale
- Amazon Redshift:
  - A datawarehousing service that you can use for big data analytics
- Amazon Database Migration Service (Amazon DMS):
  - Migrate relational databases, nonrelational databases, and other types of data stores
  - Move data beween a source database and a target database
  - Development and test database migrations
  - Database consolidation
  - Continouus replication
- Additional database services:
  - Amazon DocumentDB: a document database service that supports MongoDB workloads. (MongoDB is a document database program.)
  - Amazon Neptune is a graph database service.
  - Amazon Quantum Ledger Database (Amazon QLDB) is a ledger database service.
  - Amazon Managed Blockchain is a service that you can use to create and manage blockchain networks with open-source frameworks.
  - Amazon ElastiCache is a service that adds caching layers on top of your databases to help improve the read times of common requests.
  - Amazon DynamoDB Accelerator (DAX) is an in-memory cache for DynamoDB.

## 6. Security

- AWS Shared responsibility model:
  - Divides into custom responsiblilities (commoly refered to as "security in the cloud") and AWS responsibilities (commonly referred to as "security of the cloud")

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649397600/pmnCF6L4ssjtw7Ws1RUpZw/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/sIlyltjk4kwKozZ1_eyqltDSWURM2V1xC.png)

- Amazon Identity and Access Management (IAM):
  - Enables you to manage access to AWS services and resources securely
- AWS account root user: The root user is accessed by signing in with the email address and password that you used to create your AWS account.
  - Do not use the root user for everyday tasks. Instead, use the root user to create 1st IAM user and assign it permissions to create other users
- IAM users:
  - An IAM user is an identity that you create in AWS, represents the person or application that interacts with AWS services and resources. (name + credentials)
- IAM policies:
  - An IAM policy is a document that allows or denies permissions to AWS services and resources
  - Follow the security principle of least privilege when granting permissions
  - Example:

![](https://assets.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1649419200/Eg2lO02vy-5QqmhWJupcbg/tincan/31d9c0cca79c54bdceaf3e938fd424e97c98c7e8/assets/4PUOpE714WIQyBUs_wwEWNhiDL7wyp00S.png)

- IAM groups:
  - An IAM group is a collection of IAM users.
  - Assign an IAM policy to a group, all users in the group are granted permissions specified by the policy
- IAM roles:
  - An IAM role is an identity that you can assume to gain temporary access to permissions
  - IAM roles are ideal for situations in which access to services or resources needs to be granted temporarily, instead of long-term
- Multi-factor authentication:
- AWS Organizations:
  - When create an organization, AWS Organizations automatically creates a root, which is the parent container for all the accounts in organization
  - Control permissions for the accounts in organization by using service control policies (SCPs)
- Organizational units (OU):
  - When apply a policy to an OU, all the accounts in the OU automatically inherit the permisions specified in the policy
- AWS Artifact: A service that provides on-demand access to AWS security and compliance reports and select online agreements
- Denial-of-service attacks - AWS Shield
- AWS Key Management Service (AWS KMS): Enables user to perform encryption operations through the use of cryptographic keys
- AWS WAF:
  - Web application firewall that lets you monitor network requests that come into web applications
  - Works together with Amazon CloudFront and an Application Load Balancer
- Amazon Inspector: helps to improve the security and compliance of applications by running automated security assessments. It checks applications for security vulnerabilities and deviations from security best practices, such as open access to Amazon EC2 instances and installations of vulnerable software versions
- Amazon GuardDuty: a service that provides intelligent threat detection for your AWS infrastructure and resources. It identifies threats by continuously monitoring the network activity and account behavior within your AWS environment.

## 7. Monitoring and analytics

- Amazon CloudWatch: a web service that enables you to monitor and manage various metrics and configure alarm actions based on data from those metrics
- Amazon CloudTrail: records API calls for your account. The recorded information includes the identity of the APi caller, the time of the API call, the source IP address of the APi caller, and more.
  - CloudTrail Insights: allow CloudTrail to automatically detect unusual API activities
- AWS Trusted Advisor: a web service that inspects AWS environment and provides real-time recommendations in accordance with AWS best practices (cost optimization, performance, security, fault tolerance, and service limits)

## 8. Pricing and support

- AWS Free tier: 3 types of offers are available:
  - Always free
  - 12 months free
  - Trials
- AWS Pricing concepts:
  - Pay for what you use
  - Pay less when you reserve
  - Pay less with volume-based discounts when you use more
- AWS Pricing calculator
- AWS Budgets: create budgets to plan service usage, service costs, and instance reservations
- AWS Cost exploxer: a tool that enables you to visualize, understand, and manage AWS costs and usage over time
- AWS Support offers 4 different Support plan:
  - Basic
  - Developer
  - Business
  - Enterprise
- AWS Marketplace: a digital catalog that includes thousands of software listings from independent software vendors

## 9. Migration and innovation

- AWS Cloud adoption framework (AWS CAF):
