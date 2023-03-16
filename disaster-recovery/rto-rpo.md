# RTO and RPO

Source:

- <https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/business-continuity-plan-bcp.html>
- <https://en.wikipedia.org/wiki/Disaster_recovery>

Table of content:

- [RTO and RPO](#rto-and-rpo)
  - [O. Overview](#o-overview)
  - [1. RTO](#1-rto)
  - [2. RPO](#2-rpo)
  - [3. Relationship](#3-relationship)

## O. Overview

RTO and RPO are two of the most important parameters of a disaster recovery or data protection plan. These are objectives that can guide enterprise to choose an optional cloud backup and disaster recovery plan.

At first glance, these two terms appear to be quite similar. The best way to understand the difference between them is to associate the “RP” in “RPO” by imagining that they stand for “Rewrite Parameters” and the “RT” in “RTO” as “Real-Time.”

![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/recovery-objectives.png)

## 1. RTO

- Recovery Time Objective (RTO) is the maximum acceptable delay between the interruption of service and restoration of service. This objective determines what is considered an acceptable time window when service is unavailable and is defined by the organization.
- "How much time did it take to recover after notification of business process disruption?"

## 2. RPO

- Recovery Point Objective (RPO) is the maximum acceptable amount of time since the last data recovery point. This objective determines what is considered an acceptable loss of data between the last recovery point and the interruption of service and is defined by the origanization.
- "Up to what point in time could the business process's recovery proceed tolerably given the volume of data lost during that interval?"
- This parameter is measured in time: from the moment a failure occurs to your last valid data backup. For example, if you experience a failure now and your last full data backup was 24 hours ago, the RPO is 24 hours.

## 3. Relationship

- RTO and the RPO must be balanced, taking business risk into account, along with other system design criteria.
- The more stringent the RTO and RPO, the more expensive achieving them can be. For example, if you run a full corporate data backup every day for lower RPO, you’ll consume more storage and network resources than you would if you ran them every week, inflating the expense. To get a handle on costs, identify your desired RTO/RPO values based on your criticality tiers, then research ways to achieve them as cost-effectively as possible as part of your disaster recovery strategy.
- RPO designates the variable amount of data that will be lost or will have to be re-entered during network downtime. RTO designates the amount of “real time” that can pass before the disruption begins to seriously and unacceptably impede the flow of normal business operations.
  - The recovery time objective (RTO) is the target period of time for downtime in the event of IT downtime while recovery point objective is the maximum length of time from the last data restoration point.
