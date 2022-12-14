# AWS SAA-C03

Sources & Refer:

- <https://www.awsgeek.com/>

Table of contents:

- [AWS SAA-C03](#aws-saa-c03)
  - [1. Getting started with AWS](#1-getting-started-with-aws)
  - [2. IAM](#2-iam)
  - [3. EC2](#3-ec2)
  - [4. EC2 Instance storage](#4-ec2-instance-storage)
  - [5. High availability and Scalability: ELB \& AS](#5-high-availability-and-scalability-elb--as)
  - [6. RDS+Aurora+ElastiCache](#6-rdsauroraelasticache)
  - [7. Route 53](#7-route-53)
  - [8. AWS Well-Architected Framework](#8-aws-well-architected-framework)
  - [9. S3](#9-s3)
  - [10. Amazon SDK, IAM Roles \& Policies](#10-amazon-sdk-iam-roles--policies)
  - [11. CloudFront, AWS Global Accelerator](#11-cloudfront-aws-global-accelerator)
  - [12. AWS Storage Extras](#12-aws-storage-extras)
  - [13. Amazon Messaging - Decoupling applications](#13-amazon-messaging---decoupling-applications)
  - [14. Containers on AWS](#14-containers-on-aws)
  - [15. serverless](#15-serverless)
  - [16. Databases](#16-databases)
  - [17. Data \& Analytics](#17-data--analytics)

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
  - AWS CLI (access keys): <https://github.com/aws/aws-cli>
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

## 6. RDS+Aurora+ElastiCache

- RDS - Relational Database Service:

  ![](https://www.awsgeek.com/Amazon-RDS/Amazon-RDS.jpg)

  - Managed DB service for DB use SQL as a query language.
    - Automated provisioning, OS patching.
    - Continous backups and restore to specific timestamp (Point in Time Restore)
    - Monitoring dashboards
    - Read replicas for improved read performance
    - Multi AZ setup for DR
    - Maintenance windows for upgrades
    - Scaling capacity:
      - Storage autoscaling:
        - Scale automatically if:
          - Free storage  < 10% of allocated storage.
          - Low-storage lasts at least 5 minutes.
          - 6 hours have passed since last modification.
        - Set Maximum storage threshold
        - Use cases: unpredictable workloads.
    - Storaged backed by EBS (gp2 or io1)
  - Databases: PostGres, MySQL, MariaDB, Oracle, SQL Server, Aurora.
  - Can't SSH into instances.
  - Read replicas for read scalability:
    - Up to 5 read replicas.
    - Replication is ASYNC -> read - eventually consistent.
    - For analytic use cases.
    - Network cost: data goes from AZ to others -> read replicas within same region -> no charges
  - Multi AZ:
    - SYNC replication
    - Free
    - Not used for scaling
    - Read replicas
  - Zero downtime switch from one AZ to multi AZ:
    - A snapshot is taken.
    - A new DB is restored from a snapshot in a new AZ
    - Synchronization is established between 2 databases
  - Custom: access to the underlying database and OS (by de-activate Automation Mode)
  - RDS Backups:
    - Automated backups:
      - Daily full backup.
      - Transaction logs: back up/5 minutes.
      - 1-35 days of retention -> 0 = disable automated backup.
    - Manual DB snapshots.
    - Trick: Stopped database, still pay for storage -> snapshot & restore.
- Amazon Aurora:
  - A proprietary technology from AWS.
  - Postgres and MySQL are both supported as Aurora DB.
  - AWS cloud optimized.
  - Costs more than RDS (20% more)
  - High availability and Read scaling:
    - 6 copies of data across 3 AZ:
      - 4/6: writes.
      - 3/6: reads.
      - Self healing with peer-to-peer replication.
      - Storage is stripped across 100s of volumes.
    - Cross Region replication.

    ![](https://docs.aws.amazon.com/images/AmazonRDS/latest/AuroraUserGuide/images/AuroraArch001.png)

  - Custom endpoints:
    - Define a subset of Aurora instances as a Custom Endpoint.
    - Example: Run analytics queries on specific replicas.
  - Serverless:
    - Automated database instantiation and auto-scaling based on actual usage.
    - Good for infrequent, intermittent or unpredictable workloads.
    - No capacity planning needed.
    - Pay per second, can be more cost-effective.
  - Multi-master:
    - Every node does R/W - vs promoting a RR as the new master.
  - Global Aurora:
    - Aurora Cross Region Read Replicas.
    - Aurora Global Database (recommended):
      - Cross regions.
      - Promote another region has an RTO of < 1 minute.
      - Cross region replication takes less than 1 second.
  - Machine learning:
    - Supported services: SageMaker, Comprehend.
    - Use caes: fraud detection, ads targeting, sentiment analysis, product recommendations.
  - Aurora Backups:
    - Automated Backups:
      - 1-35 days (can't be disabled)
      - point-in-time recovery.
    - Manual DB snapshots.
  - Database Cloning:
    - Create a new DB Cluster from an existing one.
    - Faster than snapshot & restore.
    - Very fast & cost-effective.
    - Useful to create a "staging" database from a "production" database without impacting the production database.
- RDB & Aurora Restore options:
  - Restoring a RDS/Aurora backup or a snapshot creates a new database.
  - Restoring database from S3.
    - Create a backup of db.
    - Store it on S3.
    - Restore the backup file onto a new RDS instance running MySQL.
- RDS & Aurora Security:
  - At-rest encryption.
  - In-flight encryption.
  - IAM authentication.
  - Security groups.
  - No SSH available.
  - Audit logs can be enabled -> CloudWatch.
- RDS Proxy:
  - Allow apps to pool and share DB connections established with the database.
  - Improving database effeciency by reducing the stress on database resources and minimize open connections.
  - Reduced RDS & Aurora failover time by up 66%.
  - Enforce IAM authentication.
  - Never publicity accesible (must be accessed from VPC).
- ElastiCache:

  ![](https://www.awsgeek.com/Amazon-ElastiCache/Amazon-ElastiCache.jpg)

  - Manage Redis or Memcached.
  - Caches: help reduce load off of databases for read intensive workloads, make application stateless.
  - AWS takes care of OS maintenance/patching, optimizations, setup, configuration, monitoring, failure recovery and backups.
  - Using involves heavy application code changes.
  - [DB cache](https://aws.amazon.com/getting-started/hands-on/boosting-mysql-database-performance-with-amazon-elasticache-for-redis/):
    - Applications queries ElastiCache, if not available, get from RDS and store in ElastiCache.
    - Help relieve load from RDS.
    - Cache must have an invalidation strategy to make sure only the most current data is used in there.
  - [User session store](https://aws.amazon.com/getting-started/hands-on/building-fast-session-caching-with-amazon-elasticache-for-redis/):
    - User logs into any of the application
    - The application writes the session data into ElastiCache.
    - The user hits another instance of our application.
    - The instance retrieves the data (from ElastiCache) and the user is already logged in.
  - [Redis vs Memcached](https://aws.amazon.com/elasticache/redis-vs-memcached/).
  - Cache security.
    - All caches:
      - Do not support IAM authentication.
    - Redis AUTH: password/token.
    - Memcached: SASL-based authentication.
  - [Patterns/Strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/Strategies.html):
    - Lazy loading: loads data into the cache only when necessary. All read data is cached, data can become stale in cache.
    - Write through: adds data or updates data in the cache whenever data is written to the database (no stale data).
    - Adding TTL: store temporary session data in a cache (using TTL features)

## 7. Route 53

- DNS - Domain Name System.
  - Domain registrar: Route 53, GoDaddy,...
  - DNS Records: A,AAAA,CNAME,NS,....
  - Zone File: contain DNS records
  - Nameserver: resolves DNS queries
- Route 53:
  - A highly available, scalable, fully managed and Authoritative (The customer can update the DNS records) DNS
  - Ability to check the health of your resources.
  - 100% availability SLA.
  - Records:
    - How you want to route traffic for a domain
    - Contain: Domain/Subdomain name + record type + value + routing policy + TTL
    - Supported DNS record types:
      - A/AAAA/CNAME/NS:
        - A: maps a hostname to IPv4
        - AAAA: maps a hostname to IPv6
        - CNAME: maps a hostname to another hostname
        - NS: Name servers for the hosted zone
      - CAA/DS/MX/NAPTR/PTR/SOA/TXT/SPF/SRV
  - Hosted zones:
    - A container for records that define how to route traffic to a domain and its subdomains
    - Public/Private Hosted zones.
    - 0.5$/month/hosted zone.
  - Records TTL: Except for Alias records, TTL is mandatory for each DNS record.
  - CNAME vs Alias:
    - CNAME: points a hostname to any other hostname. Only for Non Root domain (aka something.mydomain.com)
    - Alias:
      - Points a hostname to an AWS resource (app.mydomain.com => blahblah.amazonaws.com). Works for Root/Non Root Domain (aka mydomain.com)
      - An extension to DNS functionality.
      - Automatically recognizes changes in the resource's IP address.
      - Always of type A/AAAA
      - Can't set the TTL
      - Targets: Elastic Load Balancers, CloudFront Distributions, API Gateway, Elastic Beanstalk environments, S3 websites, VPC Interface endpoints, Global Accelerator accelerator, Route 53 record in the same hosted zone.
    - Routing policies:
      - Define how Route 53 responds to DNS queries.
      - Supported Routing policies:
        - Simple:
          - Typically, single resource (can specify multiple values -> random one is chosen by the client)
          - Alias enabled -> 1 AWS resource
          - No healthcheck
        - Weighted:
          - Control the % of the request that go to each specific resource

          ```
          traffic (%) = <weight for a specific record>/<sum of all the weights for all records>
          ```

        - DNS records must have the same name and type
        - Health checks.
        - Use cases: load balancing between regions, testing new application versions,...
        - Assign a weight of 0 to a record -> stop sending traffic
        - All records's weight = 0 -> all records will be returned equally

        - Failover: Active/Passive
        - Latency based:
          - Redirect to the resource that has the least latency (between users and AWS regions) close to use.
          - Health checks.
        - Geolocation:
          - Routing is based on user location.
          - Should create a "Default" record.
          - Use cases: web localization, restrict content distribution, load balancing,...
          - Health Checks
        - Multi-value answer:
          - Use when routing traffic to multiple resources
          - Health Checks
          - Up to 8 healthy records
          - Not substitute for having an ELB
        - Geoproximity (using Route 53 Traffic Flow feature):
          - Route traffic to resources based on the geographic location of users and resources.
          - Ability to shift more traffic to resources based on the defined bias.
          - Resources can be: AWS resources - Non-AWS resources.
          - Must use Route 53 Traffic Flow.
    - Health Checks:
      - HTTP Health Checks: public resources.
      - Automated DNS Failover.
      - Intergrated with CloudWatch metrics.
      - About 15 Global health checkers will check the endpoint health
      - Pass only: 2xx and 3xx status codes. Or based on the text in the first 5120 bytes of the response.
      - Configure you router/firewall to allow incoming requests from Health Checks.
      - Combined the result of multiple Health Checks into a single Health Check (using OR, AND, or NOT) -> perform maintenance to website without causing all health checks to fail.
      - Can't access Private endpoints -> Workaround: CloudWatch Metric + Alarm -> Health Check checks that alarm.
- Domain Registar vs DNS Service:
  - Buy/Register your domain name with a Domain Registar
  - Domain Registar provides you with a DNS Service to manage DNS records, but you can use another DNS Service.
  - DNS Service != Domain Registar

## 8. AWS Well-Architected Framework

- It's deserverd [its own article](../../well-architected-framework/README.md).

## 9. S3

![](https://www.awsgeek.com/Amazon-S3/Amazon-S3.jpg)

- Simple Storage Service
- Use cases:
  - Backup and storage
  - Disaster recovery
  - Archive
  - Hybrid Cloud storage
  - Application hosting
  - Media hosting
  - Data lakes and big data analytics
  - Software delivery
  - Static website
- Buckets:
  - Store objects ("files") in "buckets" (directories)
  - Globally unique name
  - Defined at region level (S3 looks like a global service but buckets are created in region)
  - Naming convetion
    - No uppercase, no underscore
    - 3-63 characters long
    - Not an IP
    - Must start with lowercase letter or number
    - Must NOT start with the prefix xn--
    - Must NOT end with the suffix -s3alias
- Objects:
  - Objects have a Key
  - Key is the FULL path: `s3://my-bucket/my_file.txt`
  - Key = prefix + object name
  - Values are the content of the body:
    - Max size: 5TB
    - Upload more than 5GB, must use "multi-part upload"
  - Metadata (list of key/value pairs)
  - Tags (Unicode key/value pair) - security/lifecycle
  - Version ID (if versioning is enabled).
- Security:
  - User-based: IAM policies

  ![](https://docs.aws.amazon.com/images/AmazonS3/latest/userguide/images/user-policy.png)

  - Resource-based:

    ![](https://docs.aws.amazon.com/images/AmazonS3/latest/userguide/images/resource-based-policy.png)

    - Bucket policies: bucket wide rules - allow cross account
      - JSON based policies.
      - Use cases:
        - Grant public access to the bucket
        - Force objects to be encrypted at upload
        - Grant access to another account (Cross account)
    - Object Access Control List (ACL)
    - Bucket Access Control List (ACL)
  - Encryption: encrypt objects using keys.
- Versioning:
  - Enabled at bucket level
  - Best practices to version your buckets:
    - Protect against unintended deletes -> restore a version
    - Easy roll back to previous version
  - All file is not versioned -> enable version -> version "null"
  - Suspend versioning -> not delete the previous versions
- [Replication](https://aws.amazon.com/s3/features/replication/) (Cross-region replication & Same-region replication):
  - Must enable Versioning in source and destination buckets
  - Buckets can be in different AWS accounts
  - Copying is asynchronous
  - IAM permissions
  - Use cases:
    - CRR: compliance, lower latency access, replication across accounts
    - SRR: log aggregation, live replication between production and test accounts

  ![](https://d1.awsstatic.com/Products/product-name/s3/S3-blast-HIW.fec9a333a2c7492f18fe92cd8952a0d7f6a141d5.png)

- [Replication](https://aws.amazon.com/s3/features/replication/) (Batch Replication):
  - CRR and SRR: only new objects are replicated.
  - Replicate existing objects/retry objects were unable to replicate using Batch replication
  - Use cases: backfill newly created buckets, retry replication, migration
- Replication Time Control:
  - Replication Time Control replicates most objects "that you upload" to S3 in seconds, and 99.99% of those objects within 15 minutes.

  ![](https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/replication-time-control-updated.7e4011429383a586f314f6ece8e582b7be91ee4b.png)
- Storage classes:

| Name                              | Overview                                                                                                              | Availability | Use cases                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------- |
| Standard - General Purpose        | Used for frequently accessed data, low latency, high throughput                                                       | 99.99%       | Big data analytics, mobile & gaming applications, content distribution,...  |
| Standard - Infrequent Access (IA) | Lower cost than S3 standard                                                                                           | 99.9%        | Disater recovery, backups                                                   |
| One Zone - IA                     |                                                                                                                       | 99.5%        | Storing secondary backup copies of on-premises data, or data you can create |
| Glacier Instant Retrieval         | Millisecond retrieval, great for data accessed a quarter. (store >= 90 days)                                          |              | Archive/Backup                                                              |
| Glacier Flexible Retrieval        | Expedited (1-5 minutes),  Standard (3-5 hours), Bulk (5-12 hours) - free (store >= 90days)                            |              | Archive/Backup                                                              |
| Glacier Deep Archive              | Standard (12 hours), Bulk (48 hours) (store >= 180 days)                                                              |              | Archive/Backup, long term storage                                           |
| Intelligent Tiering               | Small monthly monitoring and auto-tiering free, move objects automatically between Access Tiers, no retrieval charges |              |                                                                             |

  ![](https://static.us-east-1.prod.workshops.aws/public/a965bfb5-cf47-4f7c-aae6-82cceb3572f3/static/images/002_services/002_storage/003_s3/s3_storage_classes.png?classes=shadow&width=1024px)

  ![](https://res.cloudinary.com/practicaldev/image/fetch/s--v3YS5Oxn--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/htu5kvq6u5qffovohc20.png)

- Moving between Storage Classes:
  - Can transition objects between Storage Classes.
  - Moving objects can be automated using a **Lifecycle Rules**.
    - Transition actions: configure objects to transition to annother storage class (ex: move to Standard IA class 60 days after creation)
    - Expiration actions: configure to expire (delete) objects after some time (ex: can be used to delete old versions of files)
    - Rules can be created for a certain prefix (ex: `s3://mybucket/mp3/*`) or certain object tags (ex: `Department: Finance`)
    - Example:
      - Application on EC2 creates thumbnails (from source images). These thumbnails can be recreated easily, and only need to be kept for 60 days. The source images should be able to be immediately retrieved for these 60 days, and afterwards, the user can wait up to 6 hours.
        - S3 source images: Standard -> Glacier after 60 days (Lifecycle configuration)
        - S3 thumbnails: One-Zone IA -> expired after 60 days (Lifecycle configuration)
      - Should be able to recover your deleted S3 objects immediately for 30 days (rarely). After this time, and for up to 1 year, recover time should be within 48 hours.
        - Enable S3 Versioning: "deleted objects" are in fact hidden by a "delete marker" and can be recovered.
        - "Noncurrent versions" of the object -> Standard IA -> Glacier Deep Archive (afterwards).

  ![](https://docs.aws.amazon.com/images/AmazonS3/latest/userguide/images/lifecycle-transitions-v3.png)

- Storage Class Analysis:
  - Help to decide when to transition the right data to the right storage class -> you can create Lifecycle rules then.
  - Only provide recommendations for Standard or Standard IA.
  - Daily update.
- Requester Pays:
  - In general, bucket owners pay for all S3 storage and data transfer costs.
  - With Requester Pays buckets, the requester instead of the bucket owner pays the cost of the request and the data download from the bucket.
  - The requester must be authenticated.

  ![](https://user-images.githubusercontent.com/29729545/151326716-7681bab7-d7c2-4c5e-afdf-aeb5d66abd01.png)

- Event Notifications:
  - Example: `S3:ObjectCreated,S3:ObjectRemoved,S3:ObjectRestore,...`
  - To enable, add a notification configuration that identifies the events.

  ![](https://media.amazonwebservices.com/blog/2014/s3_notification_flow_2.png)

  - Can send events to Amazon EventBridge. Unlike other destinations, you don't need to select which event types you want to deliver (all of them are sent!).
    - Advanced filtering
    - Multiple destinations
    - EventBridge Capabilities: Archive, Replay Events, Repliable Delivery
- Baseline Performance:
  - Automatically scales to high request rates, latency.
  - Baseline performance: 3500 PUT/COPY/POST/DELETE 5500 GET/HEAD per second per prefix in a bucket (no limit number of prefixes in a bucket).
- Performance guidelines:
  - Measure performance.
  - Scale Storage connections horizontally: Spread requests across many connections.
  - Use byte-range fetches:
    - Parallelize Gets by requesting specific byte ranges.
    - `Range` HTTP header.
    - Better resilience in case of failures.
  - Retry requests for latency-sensitive applications.
  - Combine S3 and EC2 in the same AWS region.
  - Use Amazon S3 Transfer Acceleration to minimize latency caused by distance.
    - Increase transfer speed by transferring file to an AWS edge location which will forward the data to the S3 bucket in the target region.
    - Compatible with the multi-part upload.

  ![](https://static1.tothenew.com/blog/wp-content/uploads/2016/04/Selection_136.png)

  - Use Latest version of the AWS SDKs.
  - Multi-part upload: recommended for files > 100MB, must use for files > 5GB -> parallelize uploads
  - Use Caching for Frequently Accessed Content (CloudFront, ElasticCache, Elemental MediaStore)
- Select & Glacier Select:
  - Retrieve less data using SQL by performing server-side filtering.
  - Can filter by rows & columnes.
  - Less entwork transfer, less CPU cost client-side.
  - Glacier is priced in 3 dimensions:
    - GB of Data Scanned
    - GB of Data Returned
    - Select requests

  ![](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2017/11/28/s3_select.png)

- Batch Operations:
  - Perform bulk operations on existing S3 objects with a single request:
    - Modify object metadata & properties
    - Encrypt un-encrypted objects
    - Modify ACLs, tags
    - Restore objects from S3 Glacier
    - ...
  - A job consist of a list of objects, the action to perform, and optional parameters.
  - Use S3 inventory to list objects and use S3 Select to filter objects.

  ![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2021/11/11/Fig1.png)

- Security:
  - Object encryption: You can encrypt objects in S3 buckets using 1/4 methods:
    - Server-Side encryption (SSE):
      - SSE with S3-managed keys (SSE-S3):
        - Encryption keys handled, managed, and owned by AWS.
        - AES-256
        - Must set header `"x-amz-server-side-cryption":"AES256"`

        ![](https://user-images.githubusercontent.com/29729545/147951666-48c6c7af-c3b0-42fd-b434-ed21edcb1f9e.png)

      - SSE with KMS keys stored in AWS KMS (SSE-KMS):
        - Leverage AWS KMS to manage keys.
        - Must set header `"x-amz-server-side-cryption":"aws:kms"`
        - KMS limits: upload - call GenerateDataKey KMS API, download - call Decrypt KMS API -> Count towards the KMS quota/s.
      - SSE with Customer-provided keys (SSE-C):
        - You manage your own keys.
        - HTTPS must be used, encryption keys must provided in HTTP headers, for every HTTP request made.

        ![](https://user-images.githubusercontent.com/29729545/147952597-e8809e11-cf3a-4dab-af64-8a15b80a4849.png)

    - Client-side encryption:
      - Use library - AmazonS3 Client-side encryption library
      - Client: encrypt/decrypt data when send/retrieve.
      - Fully manages the keys and encryption cycle.

    ![](https://user-images.githubusercontent.com/29729545/147953387-1df6f1ad-3e43-4590-9bc1-2555815e23ab.png)

  - Encryption in transit (SSL/TLS).
  - Default encryption vs Bucket policies:
    - Force encryption:
      - Use a bucket policy and refuse any API call to PUT an S3 object without headers.

      ```JSON
      {
        "Version": "2012-10-17",
        "Id": "PutObjPolicy",
        "Statement": [
            {
                    "Sid": "DenyIncorrectEncryptionHeader",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::<bucket_name>/*",
                    "Condition": {
                            "StringNotEquals": {
                                "s3:x-amz-server-side-encryption": "AES256"
                            }
                    }
            },
            {
                    "Sid": "DenyUnEncryptedObjectUploads",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::<bucket_name>/*",
                    "Condition": {
                            "Null": {
                                "s3:x-amz-server-side-encryption": true
                            }
                }
            }
        ]
      }
      ```

      ```JSON
      {
        "Version": "2012-10-17",
        "Id": "PutObjPolicy",
        "Statement": [
            {
                    "Sid": "DenyIncorrectEncryptionHeader",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::<bucket_name>/*",
                    "Condition": {
                        "StringNotEquals": {
                            "s3:x-amz-server-side-encryption": "aws:kms"
                                }
                    }
            },
            {
                    "Sid": "DenyUnEncryptedObjectUploads",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::<bucket_name>/*",
                    "Condition": {
                        "Null": {
                            "s3:x-amz-server-side-encryption": true
                                }
                        }
            }
        ]
      }
      ```

      - Default encryption option.
    - Bucket policies are evaluated before "default encryption".
    - Cross-Origin Resource Sharing (CORS):
      - Origin = scheme (protocol) + host (domain) + port
      - Web browser based mechanism to allow request to other origins while visiting the main origin.
      - The requests won't be fulfilled unless the other origin allows for the requests, using CORS Headers (ex: Access-Control-Allow-Origin).
      - If a client makes a cross-origin request on S3 bucket, we need to enable the correct CORS headers (*popular example question*).
      - Can allow for a specific origin or for `*` (all).
    - Multi-Factor Authentication:
      - Force users to generate a code on a device (usually a mobile phone or hardware) before doing important operations on S3.
        - Permanently delete an object version.
        - Suspend Versioning on the bucket.
      - Versioning must be enabled.
      - Only the bucket owner (root account) can enable/disable MFA delete.
    - Access logs:
      - Access logs will be logged into Logging Bucket (in the same AWS region).
      - That data can be analyzed using data analysis tools.
      - Do not set your logging bucket to be the monitored bucket.
    - Pre-signed URLs:
      - Generate pre-signed URLs using the S3 Console, CLI or SDK.
      - URL expiration.
      - Users given a pre-signed URL inherit the permissions of the user that generated the URL for GET/PUT.
      - Use cases:
        - Allow only logged-in users to download data from S3 bucket.
        - Allow an ever-changing list of users to download files by generating URLs dynamically.
        - Allow temporarily a user to upload a file to a precise location in S3 bucket.
    - Glacier Vault Lock:
      - Adopt Write Once Read Many (WORM) model: prevent further edits after uploading.
      - Create a Vault Lock Policy.
      - Lock the policy for future edits.
      - Helpful for compliance and data retention.
    - Object Lock:
      - Adopt a WORM model.
      - Block an object version deletion for a specified amount of time.
      - Versioning must be enabled.
    - Access Points:
      - Each Access point gets its own DNS and policy to limit who can access it.
        - A specific IAm user/group.
        - One policy/Access point -> easier to manage than complex bucket policies.
      - When to use:
        - Large shared data sets.
        - Copy data securely.
        - Restrict access to VPC.
        - Test new access policies.
        - Limit acess to specific account IDs.
        - Provide a unique name.

      ![](https://d1.awsstatic.com/re19/Westeros/Diagram_S3_Access_Points.fa88c474dc1073aede962aaf3a6af2d6b02be933.png)

    - Object Lambda:
      - Use AWS Lambda Functions to change the object before it is retrieved by the caller application.
      - Only 1 S3 Bucket is needed, on top of which we create S3 Access Point and S3 Object Lambda Access Point.
      - Use cases:
        - Redacting personally identifiable information for analytics or non-production environments.
        - Converting across data formats.
        - Compressing or decompressing.
        - Resizing and watermarking images.

      ![](https://d2908q01vomqb2.cloudfront.net/da4b9237bacccdf19c0760cab7aec4a8359010b0/2021/03/16/s3-object-lambda-architecture-1-1024x520.png)

## 10. Amazon SDK, IAM Roles & Policies

- Policy Simulator: <https://policysim.aws.amazon.com/>
- EC2 instance metadata
- AWS SDK - Software Development Kit:
  - If you don’t specify or configure a default region, then us-east-1 will be chosen by default

## 11. CloudFront, AWS Global Accelerator

- CloudFront:
  - Content Delivery Network (CDN)
  - Improves read performance, content is caced at the edge.
  - DDoS protection (+ Shield - AWS WAF)
  - Origins:
    - S3 Bucket:
      - Enhanced security with CloudFront Origin Access Control (OAC)
      - CloudFront can be used as an ingress (to upload files to S3)
    - Custom origin (HTTP):
      - Application Load Balancer
      - EC2 instance
      - S3 website (must first enable the bucket as a static S3 website)
      - Any HTTP backend
  - CloudFront vs S3 Cross Region Replication
    - CloudFront:
      - Global Edge network
      - Files are cached for a TTL
      - Great for static content that must be available everywhere
    - S3 Cross Region Replication:
      - Setup for each region you want to replication to happen
      - Files are updated in near real-time
      - Read only
      - Great for dynamic content that needs to available at low-latency in few regions+
    - ALB or EC2 as an origin:
      - EC2: public + security allow Public IP of edge locations.
      - ALB: public + security allow Public IP of edge locations. EC2 instances: allow ALB IP.
    - Geo Restriction:
      - Can restrict who can access your distribution:
        - Alowlist.
        - Blocklist.
      - "country": determined using 3rd party Geo-IP database.
      - Use case: Copyright Laws to control access to content.
    - Pricing:
      - The cost of data out per edge location varies.

      ![](https://www.logicata.com/wp-content/uploads/2022/02/cloudfront-pricing-1-1024x373.jpg.webp)

      - Price classes:
        - Reduce the number of edge locations for cost reduction.
        - 3 price classes:
          - All: all regions.
          - 200: most regions, but excludes the most expensive regions.
          - 100: only the least expensive regions.
      - Cache invalidations:
        - CloudFront only refresh content after the TTL has expired.
        - Force cache refresh by performing a CloudFront Invalidation.
        - Can validate all files/special path.
- Global Accelerator:
  - Leverage the AWS internal network to route to your application.
  - 2 Anycast IP are created for your application.
    - Anycast IP: all serves hold the same IP address and the client is routed to the nearest one.
  - The Anycast IP send traffic directly to Edge Locations.
  - The Edge locations send the traffic to your application.
  - Works with Elastic IP, EC2 instance, ALB, NLB, public or private.
  - Consistent performance:
    - Intelligent routing to lowest latency and fast regional failover.
    - Internal AWS network.
  - Health checks:
    - Helps make your application global (<= 1 minute for unhealthy)
    - Great for disaster recovery.
  - Security:
    - only 2 external IP need to be whitelisted.
    - DDoS protection.
  - How it works:
    - When a request to made to an accelerator static IP address, the request is first routed to a nearby Global Accelerator edge location over the public internet via the Anycast BGP protocol.
    - The accelerator accepts the request if there is a listener configured that matches the protocol and port, then determines the most optimal endpoint group based on:
      - Geographic proximity to the edge location.
      - Traffic dial settings.
      - Health of the endpoints in the endpoint group.
    - If the endpoint group closest to the edge location has the traffic dial configured to 100 percent and the endpoints in the region are passing health checks, the request is forwarded over the AWS global network.
    - If the endpoint group closest to the edge location has the traffic dial configured to less than 100 percent, the configured percentage of requests received by the edge location is sent tothe closest endpoint group, and the remaining requests are distributed to other endpoint groups weighted by geographic proximity and the traffic dials settings.
    - For endpoint groups with multiple endpoints, Global Accelerator spreads the traffic across the endpoints using a 5 tuple hash based on protocol, src IP, dst IP, src port, dst port. If endpoint weights are configured, Global Accelerator sends traffic to an endpoint based on weight that you assign to it as a proportion of the total weight for all endpoints in the group.

    ![](https://d2908q01vomqb2.cloudfront.net/5b384ce32d8cdef02bc3a139d4cac0a22bb029e8/2019/03/29/image-1-1024x576.png)

- Global Accelerator vs CloudFront:
  - CloudFront:
    - Improves performance for both cacheable content and dynamic content (api acceleration and dynamic site delivery).
    - Content is served at the edge.
  - Global Accelerator:
    - Improves performance for a widge range of applications over TCP or UDP by proxying packets at the edge to applications running in one or more AWS regions.
    - Good fit for non-HTTP use cases: gaming (UDP), IoT (MQTT), or Voice over IP.
    - Good for HTTP use cases:
      - that require static IP addresses.
      - that require deterministic, fast regional failover.

## 12. AWS Storage Extras

- AWS Snow Family:
  - High-secure, portable **offline devices** to collect and process data at the edge, and migrate data into and out of AWS.
    - If it takes more than a week to transfer over the network, use Snowball devices

  ![](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2020/12/08/You-need-the-right-tool-to-move-data-so-you-can-innovate-anywhere-options-for-data-transfer.png)

  - Data migration:
    - Snowball Edge:
      - Physical data transport solution.
      - Alternative to moving data over the network (and paying network fees).
      - Pay per data transfer job.
      - Provide block storage and Amazon S3-compatible object storage.
      - Storage Optimized vs Compute Optimized.
      - Use cases: large data cloud migrations, DC decommission, disaster recovery.
    - Snowcone:
      - Small, portable computing, anywhere, rugged & secure, withstands harsh environments.
      - Device used for edge computing, storage, and data transfer.
      - 8 TBs of usable storage.
      - Must provide your own battery/cables.
      - Can be sent back to AWS offline/connect it to internet and use AWS DataSync to send data.
    - Snowmobile:
      - Transfer exabytes (1 EB = 1,000,000 TBs) of data.
      - Capacity: 100PB
      - High security: temperature controllerd, GPS, 24/7 video surveillance.
      - Bettern than Snowball if you transfer more than 10PB.

  ![](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2020/12/08/Summary-comparison-of-the-AWS-Snow-Family.png)

  ![](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2020/12/08/AWS-Snow-Family-data-migration-workflow.png)

  - Edge computing:
    - Process data while it's being created on an edge location (limited/no internet access, limited/no easy access to computing power).
    - Uses cases: preprocess data, machine learning at the edge, transcoding media streams.
    - Snowcone:
      - 2 CPUs, 4 GB memory
      - Use-C power
    - Snowball Edge (Compute optimized):
      - 52 vCPUs, 208 GB memory
      - Optional GPU
    - Snowball Edge (Storage optimized):
      - Up to 40 vCPUs, 80 GB memory
      - Object storage clustering available
  - AWS OpsHub to manage Snow Family Device.
- Snowball into Glacier:
  - Snowball can't import to Glacier directly.
  - Must use Amazon S3 first, in combination with an S3 lifecycle policy.
- Amazon FSx:
  - Launch 3rd party high-performance file system on AWS.
  - Fully managed service.
  - FSx for Windows (File Server):
    - FSx for Windows is a fully managed Windows file system share drive
    - Can be mounted on Linux EC2 instance.
    - Scale up to 10s of GB/s, millions of IOPS, 100s PB of data
    - SDD/HDD.
    - Data is backed-up daily to S3.

    ![](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2020/02/26/Figure-1-reference-architecture-connecting-a-Windows-client-to-an-Amazon-FSx-file-system-over-AWS-Direct-Connect.png)

  - FSx for Lustre:
    - Lustre is a type of parallel distributed file system, for large-scale computing.
    - Machine Learning, High Performance Computing, Video Processing, Financial Modeling,...
    - Scale up to 100s GB/s, millions of IOPs, sub-ms latencies.
    - SSD/HDD
    - Seamless integration with S3.
    - Deployment Options:
      - Scratch File System:
        - Temporary storage.
        - Data is not replicated.
        - High burst (faster!)
        - Usage: short-term processing, optimize costs.

      ![](https://docs.aws.amazon.com/images/fsx/latest/LustreGuide/images/fsx-lustre-scratch-architecture.png)

      - Persistent File System:
        - Long-term storage.
        - Data is replicated
        - Usage: long-term processing, sensitive data.

      ![](https://docs.aws.amazon.com/images/fsx/latest/LustreGuide/images/fsx-lustre-persistent-architecture.png)

  - FSx for NetApp ONTAP:
    - Managed NetApp ONTAP
    - Storage shrinks or grows automatically.
    - Snapshots, replication, low-cost, compression and data-deduplication.
    - Point-in-time instantaneous cloning (helpful for testing new workloads)
  - FSx for OpenZFS:
    - Managed OpenZFS file system.
    - Up to 1,000,000 IOPS with < 0.5ms latency.
    - Snapshots, compression and low-cost.
    - Point-in-time instantaneous cloning (helpful for testing new workloads)
- Hybrid Cloud for Storage:
  - Cloud + On-premises
  - S3 is a proprietary storage technology -> expose S3 data on-premises -> AWS Storage Gateway.
- AWS Storage Gateway:
  - Bridge between on-premises data and cloud data
  - Use cases: disaster recovery, backup & restore, tiered storage, on-premises cache & low-latency files access
  - Require hardware.
  - Types:
    - S3 File Gateway:
      - Configured S3 buckets are accessible using the NFS and SMB protocol.
      - Most recently used data is cached in the file gateway.
      - Transition to S3 Glacier using a Lifecycle Policy.
    - FSx File Gateway:
      - Native access t Amazon FSx for Windows File Server.
      - Local cache for frequently accessed data.
      - Windows native compatiblity.
      - Useful for group file shares and home directories.
    - Volume Gateway:
      - Block storage using iSCSI protocol backed by S3 (S3 -> EBS).
      - Cached volumes: low latency access to most recent data.
      - Stored volumes: entire dataset is on premise, scheduled backups to S3.
    - Tape Gateway:
      - Virtual Tape Library (VTL) backed by S3 and archived by Glacier.
      - Back up data using existing tape-based processes (iSCSI interface).
- AWS Transfer Faimly:
  - A fully-managed service for file transfers into and out of S3 or EFS using FTP protocol (FTPS, SFTP).
  - Managved infrastructure, scalable, reliable, HA.
  - Pay per provisionewd endpoint per hour + data transfers in GB.
  - Usage: sharing files, public datasets, CRM, ERP,...
- AWS Data Sync:
  - Move large amount of data to and from:
    - On-premises/other cloud -> AWS (needs agent)
    - AWS -> AWS (different storage services) (no agent)
  - Replication tasks can be scheduled hourly, daily, weekly
  - File permissions and metadata are preserved.
- **AWS Storage Comparison**:
  - S3: Object Storage
  - S3 Glacier: Object Archival
  - EBS volumes: Network storage for one EC2 instance at a time
  - Instance Storage: Physical storage for your EC2 instance (high IOPS)
  - EFS: Network File System for Linux instances, POSIX filesystem
  - FSx for Windows: Network File System for Windows servers
  - FSx for Lustre: High Performance Computing Linux file system
  - FSx for NetApp ONTAP: High OS Compatibility
  - FSx for OpenZFS: Managed ZFS file system
  - Storage Gateway: S3 & FSx File Gateway, Volume Gateway (cache & stored), Tape Gateway
  - Transfer Family: FTP, FTPS, SFTP interface on top of Amazon S3 or Amazon EFS
  - DataSync: Schedule data sync from on-premises to AWS, or AWS to AWS
  - Snowcone / Snowball / Snowmobile: to move large amount of data to the cloud, physically
  - Database: for specific workloads, usually with indexing and querying

## 13. Amazon Messaging - Decoupling applications

- Amazon SQS:

  ![](https://www.awsgeek.com/Amazon-SQS/Amazon-SQS.jpg)

  - Standard Queue Service
  - Fully managed service.
  - Standard Queue:
    - Attributes:
      - Unlimited throughput, unlimited number of messages in queue.
      - Default retention of messages: 4 days, maximum of 14 days.
      - Low latency (<10ms)
      - Limitation of 256KB per message sent.
    - At least once delivery, occsionally -> can have duplicate messages.
    - Best effort ordering -> can have out of order messages.
    - Produce: SDK (SendMessage API)
    - Consumer:
      - Consumers (running on EC2 instance, servers, or AWS Lambda)
      - Poll SQS for messages (<= 10 messages)
      - Delete using SDK (DeleteMessage API)
  - Security:
    - Encryption: in-flight using HTTPS API, at-rest encryption using KMS keys, client-side encryption.
    - Access controls: IAM policies to regulate access to the SQS API.
    - SQS Access Policies (~ S3 bucket policies): cross-account access to SQS/allow other services to write to SQS.
  - Message visibility timeout:
    - After a message is polled by a consumer, it becomes invisible to other consumers.
    - Default: timeout 30s (min 0s - max 12h).
    - Message has 30s to be processed.
    - Afterwards, the message is "visible" in SQS.
    - A consumer could call the ChangeMessageVisibility API to get more time.
    - Timeout: high -> consumers crashes, long recover.
    - Timeout: low -> may get duplicates.

    ![](https://docs.aws.amazon.com/images/AWSSimpleQueueService/latest/SQSDeveloperGuide/images/sqs-visibility-timeout-diagram.png)

  - Long polling:
    - Long Polling: When a consumer requests messages from the queue, it can optionally "wait" for messages to arrive if there are none in the queue.
    - The wait time: 1-20s.
    - Decreases the number of API calls made to SQS while increasing efficiency and reducing latency of your application.
    - Can be enabled at queue level/API level.
  - First In First Out (FIFO) Queue.
    - Limited throughput: 300 msg/s without batching, 3000 msg/s with.
    - Exactly-once send capability (by removing  duplicates)
    - Messages are processed in order by the consumer.
  - Usages:
    - SQS + AutoscalingGroup + CloudWatch.
    - Decouple between applications.
    - Buffer to database writes.
- Amazon SNS:

  ![](https://www.awsgeek.com/Amazon-SNS/Amazon-SNS.jpg)

  - Simple Notification Service.
  - The "event producer"  only sends message to one SNS topic.
  - Many "event receivers" (subscriptions).
  - 100,000 topics limit.
  - <=12,500,000 subscriptions/topic.
  - SNS can integrate with a lot of AWS services.
  - Publish:
    - Topic publish (using the SDK):
      - Create a topic
      - Create a subscription (or many)
      - Publish to the topic
    - Direct publish (for mobile apps SDK):
      - Create a platform application
      - Create a platform endpoint
      - Publish to the platform endpoint
      - Works with Google GCM, Apple APNS, Amazon ADM...
  - Security:
    - Encryption: in-flight, at-rest, client-side.
    - Access controls: IAM policies to regulate access to the SNS API.
    - SNS Access Policies (~ S3 bucket policies).
  - SNS + SQS:
    - Fan out - push once in SNS, receive in the all SQS queues that are subscribers.
    - Make sure SQS queue access policy allows for SNS to write.
  - Applicatiopn:
    - S3 events to multiple queues.
    - SNS to Amazon S3 through Kinesis Data Firehoe.
  - FIFO topic:
    - Similar features as SQS FIFO: Ordering by Message Group ID, deduplication using Deduplication ID or Content Based deduplication.
    - Can only have SQS FIFO queues as subscribers.
    - Fanout + ordering + deduplication: SNS FIFO + SQS FIFO.
  - Messages filtering:
    - JSON Policy used to filter messages sentg to SNS topic's subscriptions.
    - If a subscription doesn't have a filter policy, it receives every message.

    ![](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2022/11/22/Payload-filtering-example3.png)

- Amazon Kinesis:
  - Makes it easy to collect, process, and analyze streaming data in real-time.
  - Ingest real-time such as: application logs, metrics, website clickstreams, IoT telemetry data...
  - Types:
    - Data Streams:
      - Capture, process, and store data streams.

      ![](https://d1.awsstatic.com/Digital%20Marketing/House/1up/products/kinesis/Product-Page-Diagram_Amazon-Kinesis-Data-Streams.e04132af59c6aa1e9372cabf44a17749f4a81b16.png)

      - Retention: 1-365 days.
      - Once data is inserted, can't be deleted (immutability)
      - Data that shares the same partition goes to the sane shard (ordering)
      - Capacity modes:
        - Provisioned Mode:
          - Choose the number of shards provisioned, scale manually or using API.
          - Pay per shard provisioned per hour.
        - On-demand Mode:
          - No need to provision or manage the capacity.
          - Scale automatically.
          - Pay per stream per hour & data in/out per GB.
      - Security:
        - Control access/authorization using IAM policies.
        - Encryption: in-flight, at-rest, clien side.
        - VPC Endpoints available for Kinesis to access within VPC.
        - Monitor API calls using CloudTrail.
      - The capacity limits are defined by the number of shards within the data stream. The limits can be exceeded by either data throughput or the number of reading data calls. Each shard allows for 1 MB/s incoming data and 2 MB/s outgoing data.
    - Data Firehose:
      - Load data streams into AWS data stores.
      - Fully managed service, no administrator, autoscaling, serverless.
      - Pay for datga going through Firehose.
      - Near Real time: 60s latency.
      - Support custom data transformation using AWS Lambda.

      ![](https://d1.awsstatic.com/pdp-how-it-works-assets/product-page-diagram_Amazon-KDF_HIW-V2-Updated-Diagram@2x.6e531854393eabf782f5a6d6d3b63f2e74de0db4.png)

      - Data Firehose vs Data Stream.

      | Data Streams                                | Data Firehose                                                 |
      | ------------------------------------------- | ------------------------------------------------------------- |
      | Streaming service for ingest at scale       | Load streaming data into S3/Redshift/ES/3rd party/custom HTTP |
      | Write custom code (producer/consumer)       | Fully managed                                                 |
      | Real-time (20)ms)                           | Near real-time (60s)                                          |
      | Manage scaling (sharings splitting/merging) | Auto scaling                                                  |
      | Data storage for 1-365 days                 | No data storage                                               |
      | Support replay capability                   | Doesn't support replay capability                             |

    - Data Analytics:
      - Analyze data streams with SQL or Apache Flink.

      ![](https://d1.awsstatic.com/architecture-diagrams/Product-Page-Diagram_Amazon-Kinesis-Data-Analytics_HIW.82e3aa53a5c87db03c766218b3d51f1a110c60eb.png)

      - Use cases: deliver streaming data in seconds, create real-time analytics, perform stateful processing.
    - Video Streams:
      - Capture, process, and store video streams.

      ![](https://d1.awsstatic.com/re19/KVS_WebRTC/product-page-diagram_Kinesis-video-streams_how-it-works_01.cb5682fffec40aed239111f7454a586b31d6e680.png)

- Kinesis vs SQS FIFO ordering:
  - Ordering data into Kinesis: using partition key.
  - Ordering data into SQS FIFO:
    - If you don't use a Group ID, messages are consumed in the order they are sent, with only one consumer.
    - To scale the number of consumers -> Group -> Group ID (similar to partition key in Kinesis/consumer group id in Kafka).
  - Kinesis Data Streams:
    - The maximum amount of consumers in parallel = number of shards.
    - Can receive up to 5 MB/s of data.
    - **Send a lot of data, data orderd per shard**
  - SQS FIFO:
    - The number of consumers = number of groups -> *dynamic number of consumers*
    - Up to 300 messages per second (3000 using batching)
- SQS vs SNS vs Kinesis:
  - SQS:
    - Consumer "pull data"
    - Data is deleted after being consumed
    - Can have as many workers (consumers) as we want
    - No need to provision throughput
    - Ordering - FIFO queues
    - Individual message delay capability
  - SNS:
    - Push data io many subscribers
    - Up to 12,500,000 subscribers
    - Data is not persisted.
    - Pub/Sub
    - Up to 100,000 topics
    - No need to provision throughput
    - Integrates with SQS for fan-out
    - FIFO capability
  - Kinesis:
    - Standard: pull data, Enhanced-fan out: push data
    - Possibility to replay data
    - Meant for real-time big data, analytics and ETL
    - Ordering at shard level
    - Data expires after X days
    - Provisioned  mode or on-demand capacity mode
- Amazon MQ:
  - SQS, SNS are "cloud-native" services: proprietary protocols from AWS.
  - Traditional applications may use open protocols (MQTT, AMQP, STOMP,...)
  - Migrate: two options
    - Re-engineering the application to use SQS and SNS.
    - Use Amazon MQ!
  - Amazon MQ: maanged message broker service for: RabbitMQ and ActiveMQ
    - Doesn't scale as much as SQS, SNS
    - Run on servers, can run in Multi-AZ with failover (active - passive), integrate with Amazon EFS for storage
    - Both queue features (SQS) and topic features (SNS)

## 14. Containers on AWS

- Amazon ECS - Elastic Container Service:

  ![](https://d1.awsstatic.com/product-page-diagram_Amazon-ECS%402x.0d872eb6fb782ddc733a27d2bb9db795fed71185.png)

  - EC2 Launch type:
    - Launch Docker containers on AWS = Launch ECS Tasks on ECS Clusters.
    - EC2 Launch type: you must provision & maintain the infrastructure (EC2 instances)
    - Each EC2 instance must run the ECS agent to register in the ECS Cluster.
    - AWS takes care of staring/stopping containers.
  - Fargate Launch type:
    - Launch Docker containers on AWS.
    - You do not provision the infrastructure (no EC2 instance to manage)
    - Serverless
    - Create task definitions
  - IAM Roles for ECS:
    - EC2 Instance Profile (EC2 Launch type only)
      - Used by the ECS agent
      - Make API calls to ECS service
      - Send container logs to CloudWatch logs
      - Pull Docker image from ECR
      - Reference sensitive data in Secrets Manager or SSM Parameter Store
  - ECS Task Role:
    - Allow each task to have a specific role
    - Use different rioles for the different ECS services you run
    - Task Role is defined in the task definition
  - Load Balancer integrations:
    - ALB suppported and works for most use cases
    - NLB recommended only for high throughput/high performance use cases, or to pair it with AWS Private Link
    - Elastic Load Balancer supported but not recommended (no advanced features - no Fargate)
  - Data Volumes (EFS):
    - Mount EFS file sytems onto ECS tasks
    - Works for both EC2 and Fargate launch types
    - Tasks running in any AZ will share the same data in the EFS file system
    - Fargate + EFS = serverless
    - Use cases: persistent multi-AZ shared storage for your containers.
  - Tasks - Auto scaling:
    - Automatically increase/decrease the desired number of ECS tasks
    - AWS Application Autoscaling:
      - CPU utilization
      - Memory Utilization
      - ALB request count per target
    - Target tracking - scale based on target value for a specific CloudWatch metric.
    - Step scaling - scaled on a specified CloudWatch alarm.
    - Scheduled scaling - scale based on a specified date/time.
    - EC2 Service Auto scaling (task level) != EC2 Auto scaling (EC2 instance level)
  - EC2 Launch type - Auto scaling EC2 instances:
    - Auto Scaling Group Scaling
      - Scale your ASG based on CPU utilization
      - Add EC2 instances over time
    - ECS Cluster Capacity Provider
      - Used to automatically provision and scale the infrastructure for your ECS tasks
      - Capacity Provider paired with an Auto Scaling Group
- Amazon ECR - Elastic Container Registry:
  - Store and manage Docker images on AWS
  - Fully integrated with ECS, backed by S3
  - Access is controlled through IAm
  - Support image vulnerability scanning, versioning, image tags,...
- Amazon EKS - Elastic Kubernetes Service
  - Launch managed Kubernetes clusters on AWS
  - An alternative to ECS.
  - EKS supports EC2 mode and Fargate.
  - Use case: if your company is already running Kubernetes on-premises or in another cloud, and want to migrate to AWS using Kubernetes.

  ![](https://d1.awsstatic.com/product-page-diagram_Amazon-EKS%402x.ddc48a43756bff3baead68406d3cac88b4151a7e.ddc48a43756bff3baead68406d3cac88b4151a7e.png)

  ![](https://d1.awsstatic.com/partner-network/QuickStart/datasheets/amazon-eks-on-aws-architecture-diagram.64cf0e40c45ade8107daf6a3ef5e2e05134d9a4b.png)

  - Node Types:
    - Managed Node Groups:
      - Create and manage Nodes (EC2 instances) for you
      - Nodes are aprt of an ASG managed by EKS
      - Support On-demand or Spot instances
    - Self-managed nodes:
      - Nodes created by you and registered to the EKS cluster and managed by an ASG
      - You can use prebuilt AMI
    - Fargate: Serverless
  - Data volumes:
    - Need to specify StorageClass manifest on your EKS cluster
    - Leverages a Container Storage Interface (CSI) compliant driver
    - Support for:
      - Amazon EBS
      - Amazon EFS
      - Amazon FSx for Lustre
      - Amazon FSx for NetApp ONTAP
- AWS App Runner:
  - Fully managed service that makes it easy to deploy web applications and APIs at scale
  - No infrastructure experience required
  - Start with your source code or container image
  - Automatically builds and deploy the web app
  - APC access support
  - Connect to database, cache, and message queue services
  - Use cases: web apps, APis, microservices, rapid production deployments

## 15. serverless

- AWS Lambda:
  - Virtual functions - no servers to manage (ofc this's serverless, right)
  - Limited by time - short executions
  - Run on-demand
  - Benefits:
    - Easy pricing: pay per request and compute time
    - Integrated with the whole AWS suite of services
    - Integrated with many programming language
    - Easy monitoring through CloudWatch
    - Easy to get more resources per functions
  - AWS Lambda container image:
    - Must implement the Lambda Runtime API
    - ECS/Fargate is preferred for running arbitrary Docker images
  - [AWS Lambda integrations](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html):
    - API Gateway
    - Kinesis
    - DynamoDB
    - S3
    - CloudFront
    - CloudWatch Events EventBridge & Logs
    - SNS
    - SQS
    - Cognito

    ![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2019/06/27/Screen-Shot-2019-06-27-at-2.23.51-PM-1024x510.png)

  - Limits:
    - Per Region:
      - Execution:
        - Memory allocation 128 MB - 10GB
        - Maximum execution tim: 900s (15 minutes)
        - Environment variables (4KB)
        - Disk capacity: 512 MB to 10GB
        - Concurrency executions: 1000 (can be increased)
      - Deployment:
        - Lambda function deployment size: 50MB
        - Size of uncompressed deployment (code + dependencies): 250MB
        - Can use the /tmp directory to load other files at startup
        - Size of environment variables: 4KB
  - Customization at the Edge:
    - Execute some form of the logic at the edge - Edge Function:
      - A code that you write and attach to CloudFront distributions
      - Run close to users to minimize latency
    - CloudFront has two kinds of functions:
      - CloudFront Functions:
        - Lightweight functions written in JS
        - Used to change Viewer requests and response
        - Native feature of CloudFront
        - Use cases:
          - Cache key normalization
          - Header manipulation
          - URL rewrites or redirects
          - Request authen and author
      - Lambda@Edge:
        - Lambda functions written in NodeJS or Python
        - Used to change CloudFront requests and responses (Viewer request response, Origin request response)
        - Use cases:
          - Longer execution time
          - Adjustable CPU or memory
          - Your code depends on a 3rd libraries
          - Network access to use external service for processing
          - File system access or access to the body of the HTTP requests
    - Use case: customize the CDN content, web security and privacy, dynamic web application at the edge,...
    - Pay for use
  - Lambda in VPC:
    - Default, Lambda fuction is launched outside your own VPC (in an AWS-owned VPC)
    - Can't access resources in your VPC
    - Lambda in VPC: define the VPC ID, the Subnet, and the Security Groups. Lambda will create an ENI in your subnets.

    ![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2019/07/02/lambda-develope-mao-1024x484.jpg)

    - Lambda functions are deployed in your VPC -> to access RDS -> use RDS proxy.
- Amazon DynamoDB:
  - Overview:
    - Fully managed, highly available with replication across multiple AZs.
    - NoSQL database.
    - Scale to massive workloads, distrbuted database
    - Millions of requests per seconds, trillions of row, 100s of TB of storage.
    - Fast and consistent in performance.
    - Integrated with IAM for security, authorization and administration.
    - Low cost and auto scaling.
    - No maintenance or patching, always available.
  - Standard or IA.
  - Basic:
    - Made of Tables.
    - Each table has a Primary Key. DynamoDB supports 2 types of Primary Key:
      - Partition Key: simple primary key, composed of 1 attribute knowns as the partition key.
      - Partition Key and Sort Key (composite primary key): All data under a partition key is sorted by the sort key value.
    - Each table can have an infinite number of items (rows). Size of item <= 400KB
    - Each item has attributes.

    ![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2018/09/10/dynamodb-partition-key-1.gif)

  - Read/Write Capacity Modes:
    - Provisioned Mode (default):
      - Number of reads/writes per second.
      - Plan capacity beforehand.
      - Pay for provisioned Read Capacity Units (RCU) and Write Capacity Unit (WCU)
      - Possibility to add auto-scaling mode for RCU and WCU
    - On-demand Mode:
      - Automatically scale
      - No capacity planning needed
      - Pay for what you use, more expensive
      - Great for unpredictable workloads, steep sudden spikes
  - DynamoDB Accelerator (DAX):
    - Memory cache for DynamoDB
    - Help solve read congestion by caching
    - Microseconds latency for cached data
    - Doesn't require application logic modification (compatible with existing DynamoDB APIs)
    - 5 minutes TTL (default)
    - vs ElasticCache: store Aggregation result. DAX stores individual objects cache, quey & scan cache.
  - Stream Processing:
    - Ordered stream of item-level modifications (create/update/delete) in a table
    - Use cases:
      - React to changes in real-time
      - Real-time usage analytics
      - Insert into dervative tables
      - Implement cross-region replication
      - Invoke AWS Lambda on changes to your DynamoDB table
    - vs Kinesis Data Streams: Kinesis Data Streams offers 1 year retention, high # of consumers, process using AWS Lambda, Kinesis Data Analytics,... Stream Processing: limited # of consumers.
  - Global Tables:
    - Make a DynamoDB table accessible with low latency in multiple-regions
    - Active-Active replication
    - Application can READ and WRITE to the table in any region.
    - Must enable DynamoDB Streams as a pre-requisite: to get a changelog and use that changelog to replicate data across replica tables in other AWS Regions.
  - Time to live (TTL):
    - Automatically delete items after an expiry timestamp.
    - Use cases: reduce stored data by keeping only current items, adhere to regulatory obligations, web session handling...
    - You identify a specific attribute name for it.
  - Backups for disaster recovery:
    - Continuous backups using point-in-time recovery (PITR).
    - On-demands backups.
  - Integration with S3:
    - Export to S3 (must enable PITR)
    - Import to S3
- API Gateway:
  - Overview:
    - AWS Lambda + API Gateway: no infrastructure to manage
    - Support for the WebSocket protocol
    - Handle API versioning
    - Handle differnt environments
    - Handle security
    - Create API keys, handle request throttling
    - Swagger/OpenAPI
    - Transform and validate requests and responses
    - Generate SDK and API specifications
    - Cache API responses
  - Integrations high level:
    - Lambda function: invoke Lambda function.
    - HTTP: expose HTTP endpoints in the backend.
    - AWS Service: expose any AWS API through the API Gateway.
  - Endpoint types:
    - Edge-optimized (default): for global clients
      - Geographically distributed clients.
      - API requests are routed to the nearest CloudFront Edge Location which improves latency.
      - API Gateway still lives in 1 AWS Region
    - Regional: for clients within the same region
    - Private: only be accessed from your VPC using ENI
  - Security:
    - User authentication through:
      - IAM roles (internal applications)
      - Cognito (external users)
      - Custom autorizer (own logic)
    - Custom Domain name HTTPS security
- Amazon Step functions:
  - Build serverless visual workflow to orchestrate your Lambda functions.
  - Workflow as a Service
  - Integrate with other AWS services
  - Use cases: order fulfillment, data processing, web applications,...
- Amazon Cognito:
  - A developer-centric and cost-effictive customer identify and access management (CIAM) service that scales to millions of users.
  - Main components:
    - User pool: User directory that provides sign-up and sign-in options for app user.
    - Identity pool: Enable you to grant your users access to other AWS services.

  ![](https://docs.aws.amazon.com/cognito/latest/developerguide/images/scenario-cup-cib.png)

  - [Authentication flow](https://docs.aws.amazon.com/cognito/latest/developerguide/authentication-flow.html):
    - For example, basic auth: *store token in AWS Security Token Service* (STS)

    ![](https://docs.aws.amazon.com/images/cognito/latest/developerguide/images/amazon-cognito-ext-auth-basic-flow.png)

## 16. Databases

- [How to choose a database](https://aws.amazon.com/startups/start-building/how-to-choose-a-database/)
- Questions to choose the right datbase based on architecture:
  - Read-heavy, write-heavy, or balanced workload? Throughput needs? Will it change, does it need to scale or fluctuate during the day?
  - How much data to store and for how long? Will it grow? Average object size?
  - How are they accessed?
  - Data durability? Source of truth for the data?
  - Latency requirements? Concurrent users?
  - Data model? How will you query the data? Joins? Structured? Semi-structured?
  - Strong schema? More flexibility? Reporting? Search? RDBMS? NoSQL?
  - License costs? Switch to Cloud Native DB such as Aurora?
- Database Types:
  - RDBMS (=SQL/OLTP): RDS, Aurora - great for joins
  - NoSQL database - no joins, no SQL: DynamoDB (~JSON), ElasticCache (key-value pairs), Neptune (Graphs), DocumentDB (for MongoDB), Keyspaces (for Apache Cassandra)
  - Object store: S3 (for big objects) / Glacier (for backups/archives)
  - Data warehouse (=SQL Analytics/BI): Redshift (OLAP), Athena, EMR
  - Search: OpenSearch (JSON) - free text, unstructured searches
  - Graphs: Amazon Neptune - displays relationships between data
  - Ledger: Amazon Quantum Ledger Database
  - Time series: Amazon Timestream
- Amazon RDS:
  - Managed PostgreSQL/MySQL/Oracle/SQL Server/MariaDB/Custom
  - Provisioned RDS Instance Size and EBS Volume Type & Size
  - Auto-scaling capability for Storage
  - Support for Read Replicas and Multi AZ
  - Security through IAM, Security Groups, KMS, SSL in transit
  - Automated Backup with Point-in-time restore feature (35 days)
  - Manual DB snapshot for longer-term recovery
  - Managed and scheduled maintenance (with downtime)
  - Support for IAM authentication, integration with Secrets Manager
  - RDS custom for access to and customize the underlying instance (Oracle & SQL Server)
  - Use case: Store relational datasets (RDBMS/OLTP), perform SQL queries, transactions
- Amazon Aurora:
  - Compatible API for PostgreSQL/MySQL, separation of storage and compute.
  - Storage: data is stored in 6 replicas, across 3 AZs.
  - Compute: Cluster of DB instance across multiple AZ, autoscaling of Read Replicas
  - Same security/monitoring/maintenance features as RDS
  - Know the backup & restore options for Aurora
  - Serverless
  - Multi-master - continuous writes failover
  - Global: up to 16 DB Read instances in each region
  - Machine Learning: perform ML using SageMaker & Comprehend
  - Database cloning: new cluster from existing one, faster than restoring a snapshot
  - Use case: same as RDS, but with less maintenance / more flexibility, performance & features.
- ElastiCache:
  - Redis/Memcached
  - In-memory data store, sub-ms latency
  - Must provision an EC2 instance type
  - Support for clustering (Redis) and Multi AZ, Read replicas (sharding)
  - Security through IAM, Security Groups, KMS, Redis Auth
  - Backup/Snapshot/Point in time maintenance
  - Requires some application code changes to be leveraged
  - Use case: Key-value store, Frequent reads, less writes, cache results for DB queries, store session data for website, cannot use SQL.
- DynamoDB:
  - AWS proprietary technology, managed serverless NoSQL database, millisecond latency
  - Capacity modes: provisioned capacity with optional auto scaling or on-demand capacity
  - Can replace ElastiCache as key/value store (storing session data for example, using TTL feature)
  - High available, Multi AZ by default, Read and Write are decoupled, transaction capability
  - DAX cluster for read cache, microsecond read latency
  - Security, authen and author - IAM
  - Event processing: DynamoDB Streams -> Lambdad, Kinesis Data Streams
  - Global Table feature: active-active setup
  - Automated backup (35 days) with PITR, or on-demand backups
  - Export/import to/from S3
  - Great  to rapidly evolve schemas
  - Use case: serverless applications development (small documents 100s KB), distributed serverless cache, doesn't have SQL query language available
- S3:
  - Key/value store for objects
  - Great for bigger objects, not so great for many small objects
  - Serverles, scales infinitely, max object size is 5 TB, versioning capability
  - Tiers: Standar, Infrequent Access, Intelligent, Glacier + lifecycle policy
  - Features: Versioning, Encryption, Replication, MFA-Delete, Access logs,...
  - Security: IAM, Bucket Policies, ACL, Access Points, Object lambda, CORS, Objects/Vault Lock
  - Encryption: SSE-S3, SSE-KMS, SSE-C, client-side, TLS in transit, default encryption
  - Batch operations
  - Performance: multi-part upload, S3 transfer acceleration, S3 Select
  - Automation: S3 Event notifications (SNS, SQS, Lambda, EventBridge)
  - Use cases: static files, key value store for big files, website hosting
- DocumentDB:
  - An "AWS implementation" for MongoDB.
  - Full managed, high available with replication across 3 AZ
  - DocumentDB storage automatically grows in increments of 10GB, up to 64TB
  - Auto scaling
- Amazon Neptune:

  ![](https://www.awsgeek.com/Amazon-Neptune/Amazon-Neptune.jpg)

  - Fully managed graph database
  - High available across 3 AZ, with up to 15 read replicas
  - Build and run applications working with highly connected datasets - optimized for these complex and hard queries
  - Can store up to billions of relations and query the graph with milliseconds latency
  - Replication
  - Great for knowledge graphs (Wiki), fraud detection, recommendation engines, social netwokring
- Amazon Keyspaces (for Apache Cassandra):
  - A managed Apache Cassandra-compatible database service
  - Serverless, scalable, high available, fully managed by AWS
  - Auto scale tables up/down based on the application traffic
  - Tables are replicated 3 times across Multi AZ
  - Use Cassandra Query Language (CQL)
  - Single-digit millisecond latency at any scale, 1000s for requests per second
  - Capacity: On-demand mode or provisioned mode with autoscaling
  - Encryption, backup, PITR (35 days)
  - Use case: store IoT devices info, time-series data,...
- Amazon QLDB:
  - Quantum Ledger Database
  - A ledger is a book recording financial transactions
  - Fully managed, serverless, high available, replication across 3 AZ
  - Used to review history of all the changes made to your application data over time
  - Immutable system: no entry can be removed or modified, cryptographically verifiable
  - Difference with Amazon Managed Blockchain: no decentralization component, in accordancewith financial regulation rules
- Amazon Timestream:
  - Fully managed, fast, scalable, serverless time series database
  - Auto scaling
  - Store and analyze trillions of events per day
  - 1000s times faster & 1/10th the cost of relational databases
  - Scheduled queries, multi-measure  records, SQL compatibility
  - Data storage tiering: recent data, kept in memory and historical data kept in a cost-optimized storage
  - Built-in time series analytics functions
  - Encryption in transit and at rest
  - Use case: IoT apps, operational applications, real-time analytics,...

  ![](https://www.awsgeek.com/Amazon-Timestream/Amazon-Timestream.jpg)

## 17. Data & Analytics

- Athena:
  - Serverless query service to analyze data stored in Amazon S3
  - Use standard SQl languages to query the files
  - Support CSV, JSON, ORC, Avro, and Parquet
  - Commonly used with Amazon Quicksight for reporting/dashboards
  - Use case: Business intelligence/analytics/reporting, analyze & query VPC flow logs, ELB logs, CloudTrail trails,...
  - Analyze data in S3 using serverless? -> Athena

  ![](https://www.xenonstack.com/hubfs/amazon-athena-tools.png)

  - Use colummar data for cost-saving (less scan)
    - Apache Parquet or ORC is recommened
    - Hugo performance improvement
    - Use Glue to convert your data -> Parquet or ORC
  - Compress data for smaller retrievals
  - Partition datasets in S3 for easy query on virtual columns
  - Use larger files (128MB) to minimize overhead
  - Federated Query:
    - Allow you to run SQl queries across data stored in relational, non-relational, object, and custom data sources
    - Use Data Source Connectors that run on AWS Lambda to run Federated Queries
- Redshift:
  - Based on PostgreSQL, but it's not used for OLTP
  - It's OLAP - online analytical processing (analytics and data warhousing)
  - 10x better performance than other data warehouses, scale to PBs of data
  - Columnar storage of data (instead of row based) & parallel query engine
  - Pay as you go based on the instances provisioned
  - Has a SQL interface for performing the queries
  - Quicksight or Tableau
  - vs Athena: faster queries/joins/aggregations (thanks to indexes)
  - Cluster:

  ![](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2018/11/21/ScaleRedshift2.png)

  - Provision the node size in advance
  - Use Reserved Instances for cost savings
  - Has no "Multi AZ" mode
  - Snapshots are Point-in-time backups of a cluser, stored internally in S3
  - Snapshots are incremental
  - Restore a snapshot -> a new cluster
  - Automated: every 8 hours, ever 5 GB, or on a schedule. Set retention
  - You can configure Amazon Redshift to auto copy snapshots of cluster to another AWS Region
  - Load data into Redshift: Large inserts are much better!
    - Kinesis Data firehose
    - S3 using copy command
    - EC2 Instance with JDBC driver
  - Redshift Spectrum:
    - Query data that is already in S3 without loading it.
    - Require Redshift cluster

    ![](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2017/07/18/redshift_spectrum-1.gif)

- OpenSearch:
  - Elasticsearch!
  - DynamoDB, queries only exist by primary key or indexes - OpenSearch, search any field, even partially matches
  - Cluster of instances (not serverless)
  - Ingestion from Kinesis Data Firehose, AWS IoT, and CloudWatch Logs
  - Security through Cognito & IAM, KMS encryption, TLS
  - Dashboard
  - Patterns:
    - DynamoDB -> DynamoDB Stream -> Lambda Function -> Amazon OpenSearch
    - CloudWatch Logs -> Subscription Filter -> Lambda Function -> Amazon OpenSearch (Real time)
    - CloudWatch Logs -> Subscription Filter -> Kinesis Data Firehose -> Amazon OpenSearch (Near real time)
    - Kinesis Data Streams -> Kinesis Data Firehose (integrate with Lambda for data transformation) -> Amazon OpenSearch
    - Kinesis Data Streams -> Lambda Function -> Amazon OpenSearch
  - Amazon EMR:
    - Elastic MapReduce
    - Create Hadoop clusters (Big Data) to analyze and process vast amount of data
    - Apache Spark, HBase, Presto, Flink,...
    - Auto-scaling and integrated with Spot instances
    - Use case: data processing, machine learning, web indexing, big data...
    - Node types:
      - Master node: manage the cluster, coordinate, manage health - long running
      - Core node: Run tasks and store data - long running
      - Task node (optional): just to run tasks - usually Spot
    - Purchasing options:
      - On-demand
      - Reserved (min 1 year): cost savings
      - Spot instances: cheaper

    ![](https://docs.aws.amazon.com/images/emr/latest/ManagementGuide/images/cluster-node-types.png)

- Amazon QuickSight:
  - Serverless machine learning-powered business intelligence service to create interactive dashboards.
  - Use cases: business analytics, building visualizations, perform ad-hoc analysis, get business insights using data,..
  - Enterprise edition: Column-level security (CLS)
- Amazon Glue:
  - Managed extract, transform, and load (ETL) service
  - Useful to prepare and transform data for analytics
  - Serverless

  ![](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2020/02/05/ParquetWriterAWSGlue3.png)

  - Glue Job Bookmarks: prevent re-processing old data
  - Glue Elastic Views:
    - Combine and replicate data across multiple data stores using SQL
    - No custom code
    - Leverage a "virtual table" (materialized view)
  - Glue DataBrew: clean and normalize data using pre-built transformation
  - Glue Studio: new GUI
  - Glue Streaming ETL (built on Apache Spark Structured Streaming): compatible with Kinesis Data Streaming, MSK
- AWS Lake Formation:
  - Data lake = central place to have all your data for analytics purposes
  - Fully managed service that makes it easy to setup a data lake in days
  - Discover, cleanse, transform, and ingest data into Data Lake
  - It automates many complex manual steps (collecting, cleansing, moving, cataloging data,...) and de-duplicate (using ML Transforms)
  - Out-of-box source blueprints
  - Fing-grained access control
  - Built on top of AWS Glue

  ![](https://docs.aws.amazon.com/images/lake-formation/latest/dg/images/overview-diagram.png)

- Kinesis Data Analytics:
  - For SQL applications:
    - Real-time analytics using SQL
    - Add reference data from Amazon S3 to enrich streaming data
    - Fully managed, no servers to provision
    - Auto scaling
    - Pay for actual consumption rate

  ![](https://docs.aws.amazon.com/images/kinesisanalytics/latest/dev/images/kinesis-app.png)

  - For Apache Flink:
    - Use Flink to process and analyze streaming data
    - Run any Apache Flink application on a managed cluster on AWS
- Amazon Managed Streaming for Apache Kafka (MSK):
  - Alternative to Kinesis
  - Fully managed Kafka
  - MSK Serverless
  - vs Kinesis Data Streams:
    - Kinesis Data Streams:
      - 1 MB message size limit
      - Data Streams with Shards
      - Shard Splitting & Merging
      - TLS in-flight encryption
      - KMS at-rest encryption
    - MSK:
      - 1 MB default -> can configure
      - Kafka Topics for partitions
      - Can only add partitions to a topic
      - PLAINTEXT or TLS in-flight encryption
      - KMS at-rest encryption
  - Consumers: Kinesis Data Analytics for Flink, Glue, Lambda, Applications.
