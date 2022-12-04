# AWS SAA-C03

Table of contents:

- [AWS SAA-C03](#aws-saa-c03)
  - [1. Getting started with AWS](#1-getting-started-with-aws)
  - [2. IAM](#2-iam)
  - [3. EC2](#3-ec2)
  - [4. EC2 Instance storage](#4-ec2-instance-storage)
  - [5. High availability and Scalability: ELB & AS](#5-high-availability-and-scalability-elb--as)

## 1. Getting started with AWS

- AZ: physical data centers of AWS.
- Region: a collection of AZs that are geographically located close to one other.

![](https://cloudacademy.com/wp-content/uploads/2017/07/Screen-Shot-2017-07-05-at-13.13.38.png)

- Edge location: AWS site deployed in major cities and highly popular ares across the globe. Not used to deploy main infrastructure such as EC2 instances, EBS storage,... resources like AZs, they are used by AWS services such as AWS CloudFront and AWS Lambda@Edge -> used to end users who are accessing and using your services.
- Checkout [detail](https://cloudacademy.com/blog/aws-global-infrastructure/).
- Global services: IAM, Route 53 (DNS), CloudFront, WAF.
- Region-scoped services: EC2 (IaaS), Beanstalk (PaaS), Lambda (FaaS), Rekognition (SaaS)

## 2. IAM

- IAM = Identity and Access management, Global service.
- Root account (default) -> Users (can be grouped, multiple groups, no subgroup).
- Permissions: JSON policies -> least privilege principle.
- Policies inheritance.
- Policies structure: check [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html).

![](https://docs.aws.amazon.com/images/IAM/latest/UserGuide/images/AccessPolicyLanguage_General_Policy_Structure.diagram.png)

```JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FirstStatement",
      "Effect": "Allow",
      "Action": ["iam:ChangePassword"],
      "Resource": "*"
    },
    {
      "Sid": "SecondStatement",
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    },
    {
      "Sid": "ThirdStatement",
      "Effect": "Allow",
      "Action": [
        "s3:List*",
        "s3:Get*"
      ],
      "Resource": [
        "arn:aws:s3:::confidential-data",
        "arn:aws:s3:::confidential-data/*"
      ],
      "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}
    }
  ]
}
```

- How the decision is made as AWS authenticates the principal that makes the request:

[](https://osamaoraclecom.files.wordpress.com/2021/08/2021-08-15_18-50-58.png)

- To access AWS:
  - AWS management console (password + MFA)
  - AWS CLI (access keys): https://github.com/aws/aws-cli
    - Install with pip: `pip install awscli`.
  - AWS SDK (access keys): Language-specific APIs.
- Access keys are generated through the AWS Console:
  - Access key id: username
  - Secret access key: password
- IAM Roles for Services:
  - Some AWS service will need to perform actions on your behalf. (An IAM role is an IAM identity that you can create in your account that has specific permissions. An IAM role is similar to an IAM user, in that it is an AWS identity with permission policies that determine what the identity can and cannot do in AWS.)
  - Assign permissions to AWS services with IAM roles.
- IAM Security Tool: Credentials report (account-level) & Access advisor (user-level).
- Guidelines & Best practices:
  - Don't use the root account except for AWS account setup.
  - One physical user = One AWS user.
  - Assign users to groups and assign permissions to groups.
  - Create a strong password policy.
  - User and enforce the use of MFA.
  - Create and use Roles for giving permissions to AWS services.
  - Use Access keys for CLI/SDK.
  - Audit permissions of your account with the IAM credentials report.
  - Never share IAM users & access keys.

## 3. EC2

- Elastic Compute Cloud (IaaS)
- Sizing & configuration options:
  - OS
  - CPU
  - RAM
  - Storage:
    - Network-attached (EBS & EFS)
    - Hardware (EC2 Instance store)
  - Network
  - Security group (firewall)
  - Bootstrap script: EC2 User data
    - Launch commands when a command start (run once - first start)
    - Run with root user
- Instance types:
  - Convention:

  ```shell
  m5.2xlarge

  - m: instance class
  - 5: generation
  - 2xlarge: size within the instance class
  ```

  - General purpose: Great for a diversity of workloads.
  - Compute optimized: Great for compute intensive tasks that require high performance processors.
  - Memory optimized: Fast performance for workloads that process large data sets in memory.
  - Storage optimized: Great for storage-intensive tasks that require high, sequential read and write access to large data sets on local storage.
- Security groups:
  - Control how traffic is allowed in/or EC2 instance.
  - Contain allow rules.
  - Can be attached to multiple instances.
  - Can refer to other security groups.
  - Locked down to a region/VPC combination.
  - Good to maintain 1 separate security group for SSH access.
  - Application is not accessible (time out) -> security group issue.
  - Connection refused error -> application error.
  - All inboud traffic is blocked by default.
  - All outbound traffic is authorised by default.

![](https://sysdig.com/wp-content/uploads/Blog_Images-AWS_Security_Groups-diagram.png)

- Instances purchasing options:
  - On-demand instances: short workload, predictable pricing, pay by second.
  - Reserved (1 & 3 years):
    - Up to 72% discount compared to On-demand.
    - Recommended for steady-state usage applications (think database).
    - Reserved instances: long workloads.
    - Convertible reserverd instances: long workloads with flexible instances (can change EC2 instance type, family, OS, tenancy).
  - Saving plans (1 & 3 years):
    - Commitment to an amount of usage (for example $10/hour for 1/3 years), long workload.
    - Loked to a specific instance family & AWS region.
    - Flexible across: instance type, OS, tenancy (host, dedicated, default)
  - Spot instances:
    - Short workloads, cheap, can lose instances.
    - Discount of up to 90% compared to On-demand.
    - Useful for workloads that are resilient to failure: batch jobs, data analysis, image processing, any distributed workloads, workloads with a flexible start and end time.
    - No suitable for critical jobs or databases.
    - How to use: create Spot instance request.

    ![](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/spot_lifecycle.png)

    - Spot instance request state:

    ![](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/spot_request_states.png)

    - Can only cancel Spot instance requests that are open, active or disabled. Canceling a Spot request does not terminate instances (Still have to terminate the assoicated Spot instances then).
    - Spot Fleets = set of Spot instances + (optional) On-demand instances.
    - Spot Fleets allow us to automatically request Spot instances with the lowest price.

  - Dedicated hosts:
    - Book an entire physical server, control instance placement.
    - Useful for software that have complicated licensing model (BYOL), or for companies that have strong regulatory or compliance needs.
  - Dedicated instances:
    - No other customers will share your hardware, but may share hardware with other instances in the same account.
    - No control over instance placement.
  - Capacity reservations:
    - Reserve On-demand instances capacity in a specific AZ for any duration.
    - No time commitment (create/cancel anytime), no billing discounts.
    - Suitable for short-term, uninterrupted workloads that needs to be in specfic AZ.
- *Note for instance purchasing options, create a decision tree.*
- Private vs Public IP (IPv4 is still the most common format used online, only be using IPv4).
  - Private IP:
    - Machine can only be identified on a private network only.
    - The IP must be unique across the private network (but 2 different private networks can have the same IPs).
    - Machines connect to internet using a NAT + internet gateway (proxy).
    - Only a specificed range of IPs can be used as private IP.
  - Public IP:
    - Machine can be identified on the internet.
    - Must be unique across the whole web.
    - Can be geo-located easily.
- Elastic IPs:
  - Start/stop EC2 -> public IP is changed.
  - Fixed public IP -> Elastic IP.
  - Can attach to one instance at a time.
  - **Try to avoid using Elastic IP**:
    - Often reelfect poor architectural decisions.
    - Instead, use a random public IP and register a DNS name to it.
    - Or, use a Load balancer and don't use a public IP.
- Placement Groups:
  - To control over the EC2 Instance placement strategies:
    - Cluster - clusters instances into a low-latency group in a single AZ.
      - Pros: Great network
      - Cons: If the rack fails, all instances fails at the same time
      - Use case:
        - Big Data job that needs to complete fast.
        - Application that needs extermely low latency and high network throughput.
    - Spread - spreads instances (<= 7 instances/group/AZ) across underlying hardware.
      - Pros: Can span across AZ -> reduced risk. EC2 instances are on different physical hardware.
      - Cons: Limited to 7 instances per AZ per placement group.
      - Use case:
        - Application that needs to maximize high availability.
        - Critical applications where each instance must be isolated from failure from each other.
    - Partition - spreads instances across many different partitions (which rely on different sets of racks) within an AZ.
      - Cluster + Spread.
      - Use case: HDFS, HBase, Cassandra, Kafka.

![](https://user-images.githubusercontent.com/29729545/162229203-a79a5752-25cf-41d8-a72d-abfa92d74e02.png)

- Elastic Network Interfaces (ENI):
  - Logical component in a VPC that represents a virtual network card.
  - Independent, can attach on the fly EC2 instances.
  - Bound to a specific AZ.
- EC2 hibernate:
  - Stop/Terminate
  - Start: OS boots -> EC2 User data script is run -> OS boots up -> application starts, cached get warmed up -> Take time! -> Solution?
  - Hibernate: in-memory (RAM) state is preserved (is written to a file in the root EBS volume) -> boot faster (OS is not stopped/started).
  - Use case: long-running processing, saving the RAM state, services that take time to initialize.
  - Instance RAM size <= 150BG/Root volume must be EBS, encrypted/On-Demand, Reserved, Spot.
  - Can not hibernated >  60 days.

![](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/hibernation-flow.png)

## 4. EC2 Instance storage

- EBS:
  - Network drive you can attach to your instance while they run.
  - Only be mounted to 1 instance at a time.
  - Bound to a specific AZ.
  - Have a provisioned capacity (size in GBs, and IOPS)
  - Controls the EBS behaviour when an EC2 instance terminates.
    - By default, root EBS volume is deleted.
    - By default, any other attached EBS volume is not deleted.
- EBS Snapshot:
  - Make a incremental backup (snapshot) at a point of time.
  - Not necessary to detach volume to do snapshot, but recommended.
  - Can copy snapshots across AZ or Region.
  - Features:
    - Snapshot archive: 75% cheaper, takes 24-72 hours for restoring.
    - Recycle Bin for EBS snapshots: automatically protect deleted snapshots.
    - Fast snapshot restore (FSR):

    ![](https://a.b.cdn.console.awsstatic.com/6a98289778c38e57ce43d43ab74b677f9e026ce9a3881582df5a1f56de4a81fd/f8eae9c8d72566f61cb3e7d325627d7f.png)

  - Snapshot pricing: charges for snapshots are based on the amount of data stored. Because snapshots are incremental, deleting a snapshot mnight not reduce your storage costs.
  - How the incremental snapshots work?

  ![](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/snapshot_1a.png)

  - Relations among incremental snapshots of different volumes.

  ![](https://docs.aws.amazon.com/images/AWSEC2/latest/UserGuide/images/snapshot_1c.png)

  - Check out [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html).
- AMI (Amazon Machine Image):
  - AMI are customization of an EC2 instance.
  - Built for a specific region.
  - Public AMI/Private AMI/AWS Marketplace AMI.
  - AMI Process : AMI Image -> Instance -> AMI Image -> Instance.

  ![](https://a.b.cdn.console.awsstatic.com/311e85f9ee2b8f5015e6953f1d9bc4d717e331cc94b3c6d9691e98516f58dd0b/assets/img/How-it-works.png)

- EC2 Instance store:
  - EBS volumes are network driver -> limited performance -> use EC2 Instance store for better performance:
    - Better I/O Volume
    - EC2 Instance store lose storage if they're stopped.
    - Good for buffer/cache/scratch data/temporary content.
    - Risk of data loss if hardware fails.
    - Backups and Replications are your responsibility.
- EBS Volume types:
  - 6 types:
    - gp2/gp3 (SSD): general purpose SSD volume -> wide variety for workloads.
    - io1/iop2 (SSD): highest-performance SSD volume -> mission-critical low-latency or high-throughput workloads.
    - st 1 (HDD): low cost HDD volume -> frequently accessewd, throughtput-intenstive workloads.
    - sc 1 (HDD): lowest cost HDD volume -> less frequently accessed workloads.
  - gp2/gp3 + io1/io2 -> boot volumes.
  - Check more [here](https://jayendrapatil.com/aws-ebs-volume-types/) and [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html).

  ![](https://www.testpreptraining.com/tutorial/wp-content/uploads/2019/08/image015.png)

  ![](https://sf.ezoiccdn.com/ezoimgfmt/jayendrapatil.com/wp-content/uploads/2016/03/EBS_Volume_Types.png?ezimgfmt=ng:webp/ngcb1)

- EBS Multi-attach - io1/io2 family:
  - Attach the same EBS volume to multiple EC2 instances (<= 16 instances) in the same AZ.
  - Each instance has full read-write permissions to the high-performance volume.
  - Use cases:
    - Archive higher application availabiliuty.
    - Application must manage concurrent write operations.
  - Must use a file system that's cluster-aware.
- EBS Encryption:
  - Create an encrypted EBS volume:
    - Data at rest is encrypted inside the volume.
    - All the data in flight moving between the instance and the volume is encrypted.
    - All snapshots are encrypted.
    - All volumes created from the snapshot are encrypted.
  - Minimal impact on latency.
  - KMS (AES-256).
- EFS - Elastic File System:
  - Manage NFS that can be mounted on many EC2
  - EFS works with EC2 instances in multi-AZ
  - High available, scale, expensive (3x gp2), pay per use
  - Use cases: content management, web serving, data sharing,...
  - Use NFSv4.1 protocol
  - Use security group to control access
  - Compatible with Linux based AMI
  - KMS
  - File system scales automatically, pay-per-use, no capacity planning
  - EFS scale: 1000s of concurrent NFS clients, 10GB+/s throughput.
    - Performance mode: General purpose (default - web server, CMS,...), Max I/O (big data, media processing)
    - Throughput mode: Bursting (1 TB = 50MiB/s + burst of up to 100MiB/s)
  - Storage classes:
    - Storage tiers (life cycle management):
      - Standard + Infrequent access (EFS -IA)
    - Availability and durability:
      - Standard: Mutli AZ
      - One zone: One AZ

    ![](https://docs.aws.amazon.com/images/efs/latest/ug/images/efs-standard.png)

    ![](https://docs.aws.amazon.com/images/efs/latest/ug/images/efs-one-zone.png)

- EFS vs EBS:
  - EBS volumes:
    - can be attached to only 1 instance at a time.
    - locked at the AZ level.
    - gp2: IO increases if the disk size increases.
    - io1: can increase IO independently.
    - Take migrate across AZ: volume -> take snapshot -> restore to another AZ
  - EFS:
    - Mount 100s of instances across AZ.
    - EFS share websites files.
    - Only for Linux instances (POSIX).
    - EFS has higher price point than EBS.
    - Can leverage EFS-IA for cost savings.

## 5. High availability and Scalability: ELB & AS

- High availability and Scalability:
  - Vertical vs Horizontal Scaling:
    - Vertical scaling: increase instance size.
    - Horizontal scaling: increase number of instances (auto scaling group & load balancer)

  ![](https://www.cloudzero.com/hubfs/blog/horizontal-vs-vertical-scaling.webp)

  - HA:
    - Usually + horizontal scaling.
    - Run application/system in at least 2 data centers (== AZ)
    - Passive (for example: RDS multi az) / Active (for example: horizontal scaling)
- ELB - ELastic Load Balancing:
  - A managed load balancer.
    - AWS guarantees that it will be working.
    - AWS takes care of upgrades, maintenance, high availability.
    - AWS provides only a few configuration knobs.
  - It is intergrated with many AWS offerings/services.
  - Healthcheck:
    - Enable the load balancer to know if instances it forwards traffic are available.
    - Port + route.
  - 4 kinds:
    - Classic Load Balancer (v1 - legacy).
    - Application Load Balancer (v2):
      - HTTP (v1.1, v2), HTTPS, WebSocket (layer 7) + Redirect
      - Multiple HTTP applications across machine (target groups)
        - EC2 target groups
        - ECS tasks
        - Lambda functions - HTTP request is translated into a JSON event
        - IP addresses - must be private
      - Multiple applications on the same machine (ex: containers)
      - Routing tables to different target groups.
      - Fit for microservices & container-based application.
      - Port mapping feature to redirect to a dynamic port in ECS.
      - Latency ~ 400ms
    - Network Load Balancer (v2):
      - TCP, TLS, UDP (layer 4)
      - Handle million of request per seconds.
      - Latency ~ 100ms
      - Has 1 static IP per AZ, and supports assigning Elastic IP.
      - Target groups:
        - EC2 instances.
        - IP addresses - must be private.
        - Application Load Balancer.
      - Healthcheck: TCP HTTP HTTPS protocols.
    - Gateway Load Balancer
      - IP Protocol (layer 3)
      - Deploy, scale, and manage a fleet f 3rd party network virtual appliances in AWS.
      - Functions:
        - Transparent Network Gateway.
        - Load Balancer.
      - GENEVE protocol port 6081.
      - Target groups:
        - EC2 instances.
        - IP addresses - must be private
  - Security groups:
  - Fixed hostname `XXX.region.elb.amazonaws.com`
  - Applications servers don't see the IP of client directly.
    - The true IP of the client is inserted in the header `X-Forwarded-For`.
    - Proxy protocol.
  - Sticky sessions (session affinity): the same client is always redirected to the same instance behind a load balancer. The "cookie" used for stickiness has an expiration date you control.
    - Application-based cookie.
      - Custom cookie.
      - Application cookie: generated by the load balancer (AWSALBAPP).
    - Duration-based cookie: Generated by the load balancer (AWSALB).
  - Cross zone load balancing:
    - Each load balancer instance distributes evenly across all registered instances all AZ.
    - ALB: enabled by default, no charges for inter AZ data.
    - NLB & GWLB: disabled by default, charges for inter AZ data.

  ![](https://cloudacademy.com/wp-content/uploads/2019/08/Screen-Shot-2019-08-02-at-9.46.42-AM.png)

  - SSL/TLS certificates:
    - Allows traffic between your clients and load balancer to be encrypted in transit.
    - X.509 certificate
    - Managed by AWS Certificate Manager (ACM)
  - Connection draining/Deregistration Delay:
    - Time to complete "in-flight requests" while the instance is de-registering or unhealthy.
    - Stops sending new requests to the EC2 instance which is de-registering.
    - Default: 300s.
- Auto Scaling Group:
  - Automatically register new instances to a load balancer.
  - Re-create an EC2 instance in case a previous one is terminated.
  - Free.
  - Attributes:
    - Launch template: AMI + Instance type, EC2 User Data, EBS Volume, Security Groups,...
    - Min/Max size/Initial Capacity.
    - Scaling policies.
  - Scale an ASG based on CloudWatch alarms.
  - Scaling policies:
    - Dynamic scaling policies:
      - Target tracking scaling:
        - Most simple and easy to setup.
        - Example: average ASG CPU to stay at around 40%.
      - Simple/Step scaling:
        - Alarm is triggerd -> do scale.
      - Scheduled actions:
        - Anticipate a scaling based on known usage patterns.
        - Example: increase the min capacity to 10 at 5pm on Fridays.
    - Predictive scaling: continuously forecast load and schedule scaling ahead.
    - Metrics:
      - CPU Utilization: average CPU utilization across instances.
      - Request count/target.
      - Average Network In/Out.
      - Any custom metric (on CloudWatch)
    - Cooldowns:
      - During the cooldown period, ASG will not launch or terminate additional instances (to allow for metrics to stabilize).
