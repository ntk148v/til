# AWS Solutions Architect (SAA-C03) Cheat Sheet

Source:

- <https://www.stellexgroup.com/blog/aws-solutions-architect-associate-saa-c03-cheat-sheet>
- <https://digitalcloud.training/category/aws-cheat-sheets/aws-solutions-architect-associate/>

## 1. EC2 instances

### 1.1. 300 Instance Types across 5 Instance Families

- AWS offers over 300 EC2 Instance Types across 5 Instance Families (General Purpose, Memory-optimized, Storage-optimized, and Accelerated computing).

### 1.2. Instance Purchasing Options

- On-demand instances: default option, for short term ad-hoc requirements where the job can't be interrupted.
- On-demand Capacity Reservations: The only way to reserve capacity for blocks of time such as 9am-5pm daily.
- Spot instance: highest discount potential (50-90%) but no commitment from AWS, could be terminated with 2 min notice. Could use for grid and high-performance computing.
- Reserved instance: for long-term workloads, _1 or 3 years commitment_ in exchange for 40-60% discount.
- Dedicated instance: run on hardware dedicated to 1 customer.
- Dedicated host: fully dedicated and _physically isolated_ server. Allows you to use your server-bound software licenses and addresses compliance and regulatory requirements and potentially reduce cost (billing per-hour not per-instance).
- Bare metal EC2 instance: for when the workload needs access to the hardware feature set (e.g. Intel hardware)

### 1.3. Launching instances

- Launch Configuration/Launch Template: used to create new EC2 instances using stored parameters such as instance family, instance type, AMI, key pair and security groups. Auto-scaling groups can launch instances using config templates.
- User data: Run on first boot - root user.
- Instance metadata can be accessed via a direct URI or by using `Instance Metadata Query Tool`.
- When you launch an Ec2 instance into a default VPC, it has a public and private DNS hostname and IP address. When you launch in a non-default VPC, it may not have a public hostname depending on the DNS and VPC configs.

// ** WIP **
