# AWS SAA-C03

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

## 6. RDS+Aurora+ElastiCache

- RDS - Relational Database Service:
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

- Policy Simulator: https://policysim.aws.amazon.com/
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

  - Data migration: Snowcone, Snowball Edge, Snowmobile.
  - Edge computing: Snowcone, Snowball Edge.
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

  - Data migration workflow:

  ![](https://d2908q01vomqb2.cloudfront.net/e1822db470e60d090affd0956d743cb0e7cdf113/2020/12/08/AWS-Snow-Family-data-migration-workflow.png)
