# Disaster Recovery and High Availability 101

Source:

- <https://blog.rabbitmq.com/posts/2020/07/disaster-recovery-and-high-availability-101/>
- <https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/introduction.html>
- <https://www.vmware.com/topics/glossary/content/disaster-recovery.html>
- <https://blog.invgate.com/high-availability-vs-disaster-recovery>

Table of content:

- [Disaster Recovery and High Availability 101](#disaster-recovery-and-high-availability-101)
  - [1. Business Continuity, High Availability, and Disaster Recovery](#1-business-continuity-high-availability-and-disaster-recovery)
  - [2. Keywords](#2-keywords)
    - [2.1. Loss of Data and Availability Objectives](#21-loss-of-data-and-availability-objectives)
    - [2.2. Types of Data and Business Impact](#22-types-of-data-and-business-impact)
    - [2.3. Data Redundancy Tools - Backups and Replication](#23-data-redundancy-tools---backups-and-replication)
    - [2.4. Fundamental Limits](#24-fundamental-limits)
    - [2.5. Rack Awareness](#25-rack-awareness)
  - [3. Top elements of an effective Disaster Recovery Plan](#3-top-elements-of-an-effective-disaster-recovery-plan)
  - [4. Types of Disaster Recovery](#4-types-of-disaster-recovery)

## 1. Business Continuity, High Availability, and Disaster Recovery

- High availability is not disaster recovery:
  - _High Availability_ typically refers to some kind of automated fail-over from one instance of deployed software to another in the event of a localised failure, such as a server or disk failing, or a limited network outage. The impact of failure on availability should either not be seen or be extremely low.
  - _Disaster Recovery_ typically refers to a response to a more major incident (a disaster) such as the loss of an entire data center, massive data corruption or any other kind of failure that could cause a total loss of service and/or data. Disaster Recovery attempts to avoid permanent partial or total failure or loss of a system and usually involves building a redundant system that is geographically separated from the main site.
  - Disaster Recovery compare to High Availability:
    - Disaster recovery measures objectives for one-time event.
    - Availability objectives measure mean values over a period of time.
    - DR focuses on disaster events, whereas availability focuses on more common disruptions of smaller scale such as component failures, network issues, software bugs, and load spikes.
- Both fall within the realm of _Business Continuity_.
  - Business Continuity (BC) is defined by ISO, the International Organization for Standardization, as “the capability of the organization to continue delivery of products or services at acceptable predefined levels following a disruptive incident”.
- Business Continuity Plan and Disaster Recovery Plan:
  - Business Continuity Plan focuses on keeping business operational during a disaster, while Disaster Recovery Plannin focuses on restoring data access and IT infrastructure after a disaster.
  - Disaster Recovery Plan is a subset of Business Continuity Plan, it should not be a standalone document.

![](https://www.boxuk.com/wp-content/uploads/2016/05/DR-BC-body-1.png)

## 2. Keywords

- Ultimately, we want to be able to recover fast from major incidents (disaster recovery) and deliver continued availability during more minor incidents (high availability). A major incident may involve losing a whole data center, due to fire, a power outage or extreme weather. A more minor incident might involve the partial loss of a data center, or simply the loss of a disk drive or server.
- Implementing a system that can recover from failure and disaster can be expensive both monetarily and also with regard to performance. Ultimately the implementation will be a balance of cost of implementation vs the cost of data loss and service interruption.
- In order to make that balance, we need to take into consideration:
  - The available tools for redundancy/availability and their limitations
  - The types of data and the associated costs to th business if lost

### 2.1. Loss of Data and Availability Objectives

- As part of Disaster Recovery Plan, an enterprise must decide on two key objectives with regard to disaster recovery.
- The _Recovery Point Objective (RPO)_ determines the maximum time period of data loss a business can accept as the result of a major incident.
  - Of course, the best is 0 seconds, meaning no data loss -> hard to achieve/serious downsides (cost, performance).
  - The higher values typically being easier to achieve a lower implementation cost.

![](https://blog.rabbitmq.com/assets/images/2020/07/rpo.png)

- The _Recovery Time Objective (RTO)_ determines the maximum time period of unavailability, aka the time it takes to recover and be operational again.
  - Again, we want 0 seconds, meaning a seamless failover with continued availability.
  - Consider the cost to implement it.

![](https://blog.rabbitmq.com/assets/images/2020/07/rto.png)

- These windows of availability and data loss may or may not overlap.

![](https://blog.rabbitmq.com/assets/images/2020/07/rpo-rto.png)

### 2.2. Types of Data and Business Impact

![](https://blog.rabbitmq.com/assets/images/2020/07/data-loss-impact.png)

- _Persistent data_: sticks around week after week and even year after year. If an enterprise loses its most valuable persistent data it can kill the company.
- _Transient data_: a short life, it may be data in-flight between two systems or data that can be evicted at any time. While losing transient data can be impactful, it is unlikely to cause a company to go out of business.
- _Source-of-truth data_: either master data and/or data that does't exist anywhere else.
- _Secondary data_: a copy (possibly filtered and transformed) of the source-of-truth that can be recovered from the source persistent store.
  - Example:
    - A cache stores secondary data that can be re-hydrated from a persistent store.
    - A microservice stores some small amount of data in a database that belongs to another service.
    - A distributed log streams database data modifications to other systems.
  - The loss of secondary data can cause:
    - Loss of availability while it is recovered from the source-of-truth.
    - Loss of performance capacity due losing “hot” data.
- The most damaging data loss would be loss of _source-of-truth persistent data_ and the least would be _transient secondary data_.

![](https://blog.rabbitmq.com/assets/images/2020/07/data-types.png)

### 2.3. Data Redundancy Tools - Backups and Replication

- Data systems usually offer one or two ways of safeguarding data in the event of failure.
- _Back-up_:
  - Full backups and incremental backups.
  - The recovering from backups involves potential data loss as there was potentially new data that entered the system since the last backup was made.
  - Take time: move backup files -> recovery from those files.
- _Replication_:
  - Data modifications are streamed from one node to another, meaning that data now resides in at least two locations.
  - Replication comes in two flavours:
    - _Synchronous replication_:
      - The client only gets the confirmation that operation has succeeded once it has been replicated to other nodes.
      - Advantages: no data loss
      - Disadvantages:
        - Waiting for an operation to be replicated adds latency
        - If the network is down between the nodes when availability may be lost
        - If the secondary node(s) is down then availability may be lost
    - _Asynchronous replication_:
      - The client gets the confirmation that the operation has succeeded when it has been committed locally. The replication is done in the background.
      - Advantages:
        - The operation is replicated in the background meaning that there is no additional latency for the client and no loss of availability if the network between the primary and secondary is down
      - Disadvantages:
        - There will a lag betwene the primary and secondary node, maening that data loss can occur in the event that the primary is lost.

### 2.4. Fundamental Limits

- The speed of light and the CAP theorem. These limits affect the costs and feasibility of the RPO and RTO values.
- The CAP theorem: The original statement of the theorem by Eric Brewer (also known as Brewer’s theorem) states that a computer system can at best provide two of the three properties from the following list:
  - _Consistency_: the view of the data is up-to-date on all members of a distributed computing system.
  - _Availability_: the data is always accessible for reading and updating
  - _Partition tolerance_: the distributed system continues to operate in the presence of a failure of the network where not all members can reach other members.

![](https://hazelcast.com/wp-content/uploads/2021/12/cap-theorem-diagram-800x753-1.png)

- In practical terms, a distributed system cannot be made immune to network failures -> have to choose to P, but we only get A or C.
- CAP classifies systems as either:
  - AP - Availability in a partitioned network.
    - AP systems continue to be available despite not reaching th desired redundancy level.
    - AP systems asynchronously replicate operations but this can cause data loss if a node is lost, this loss being due to replication lag.
    - The upside is lower latency as operations can be immediately confirmed to clients.
    - Choose an _AP system_ when _availability and/or latency is the most important consideration_.
  - CP - Consistency in a partitioned network.
    - CP systems lose availability if they cannot satisfy the necessary level of redundancy due to lack of connectivity to peer nodes.
    - CP systems synchronously replicate operations and only confirm to clients when those operations are safely committed to multiple nodes. This avoids data loss at the cost of higher latency.
    - Choose a _CP system_ when _consistency is the most important consideration_.
- Single vs. Multiple Data Center(s):
  - Within a single data center, you can choose either an AP or a CP system and many data systems are configurable allowing you to tune them towards availability or consistency.
  - Building a CP system across Multiple Data Centers is at best challenging and most likely infeasible.
  - AP systems can be built across multiple data centers but they increase the likelihood of data loss and also the size of the data loss window.

### 2.5. Rack Awareness

- Extra feature: data is replicated across racks or availability zones or data centers, basically any type of failure domain in your infrastructure.
- If data is replicated but still only exists on a single rack, then losing the entire rack means we lose the data.

![](https://blog.rabbitmq.com/assets/images/2020/07/rack-awareness-1.png)

- When spread out across AZs, the loss of one AZ cannot cause data loss or loss of availability.

![](https://blog.rabbitmq.com/assets/images/2020/07/rack-awareness-2-2.png)

## 3. Top elements of an effective Disaster Recovery Plan

- Disaster recovery team: a group of specialists will be responsible for creating, implementing, and managing the disaster recovery plan. This plan should define each team member's role and responsibilities. In the event of disaster, the recovery team should know how to communicate with each other, employees, vendors, and customers.
- Risk evaluation: Assess potential hazards that put your organization at risk. Depending on the type of event, strategize what measures and resources will be needed to resume business. For example, in the event of a cyber attack, what data protection measures will the recovery team have in place to respond?
- Business-critical asset identification: A good disaster recovery plan includes documentation of which systems, applications, data, and other resources are most critical for business continuity, as well as the necessary steps to recover data.
- Backups: Determine that needs backup (or to be relocated), who should perform backups, and how backups will be implemented. Include a [RPO](./rto-rpo.md) that states the frequency of backups and a [RTO](./rto-rpo.md) that defines the maximum amount of downtime allowable after a disaster. These metrics create limits to guide the choice of IT strategy, processes and procedures that make up an organization's disaster recovery plan. The amount of downtime an organization can handle and how frequently the organization backs up its data will inform the disaster recovery strategy.
- Testing and optimization: The recovery team should continually test and update its strategy to address ever-evolving threats and business needs. By contunually ensuring that a company is ready to face the worst-case scenarios in disaster situations, it can successfully navigate such challenges.

## 4. Types of Disaster Recovery

- Back-up: This is simplest type of disaster reocvery and entails storing data off site or on a removable driver.
- Cold site: An organization sets up a basic infrastructure in a second, rarely used facility that provides a place for employees to work after a natural disaster or fire. It can help with business continuity because business operations can continue, but it does not provide a way to protect or recover important data, so a cold site must be combined with other methods of disaster recovery.
- Hot site: A hot site maintains up-to-date copies of data at all times. Hot sites are time-consuming to set up and more expensive than cold sites, but they dramatically reduce down time.
- Disaster Recovery as a Service (DRaaS):
- Back Up as a Service:
- Datacenter disaster recovery:
- Virtualization:
- Point-in-time copies: Point-in-time snapshot, make a copy of the entire database at a given time. Data can be restored from this backup, but only if the copy is stored of site or on a virtual machine that is unaffected by the disaster.
- Instant recovery: Instant recovery is similar to point-in-time copies, except that instead of copying a database, instant recovery takes a snapshot of an entire virtual machine.
