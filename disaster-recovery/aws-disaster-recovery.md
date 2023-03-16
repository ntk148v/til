# AWS Disaster recovery options

Source: <https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html>

Disaster recovery strategies available to you within AWS can be broadly categorized into four approaches, ranging from the low cost and low complexity of making backups to more complex strategies using multiple active Regions.

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/disaster-recovery-strategies.png)

DR strategies and RTO:

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/recovery-time-objective.png)

DR strategies and RPO:

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/recovery-point-objective.png)

## Backup and restore

- Suite for mitigating against data loss or corruption.

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/backup-restore-architecture.png)

## Pilot light

- Replicate data from one Region to another and provision a copy of core workload infrastructure.

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/pilot-light-architecture.png)

- Minimize the ongoing cost of disaster recovery by minizing the active resources, and simplifies recovery at the time of a disaster because the core infrastructure requirements are all in place.

## Warm standby

- Full system is up and running, but at minimum size
- Upon disaster, we can scale to production load

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/warm-standby-architecture.png)

## Multi-site active/active

- Very low RTO -> very expensive.
- Full production scale is running AWS and On premise.

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/multi-site-active-active-architecture.png)
