# Disaster Recovery

Source:

- <https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/introduction.html>
- <https://www.vmware.com/topics/glossary/content/disaster-recovery.html>

- Disaster recovery (DR) is the process of preparing for and recovering from a disaster. An event that prevents a workload or system from fulfilling its business objectives in its primary deployed location is considered a disaster.
- DR is an important part of resiliency strategy and concerns how workload responds when a disaster strikes. This response must be based on organization's business objectives which specify workload's strategy for avoiding loss of data, known as the [Recovery Point Objective](./rto-rpo.md), and reducing downtime where workload is not available for use, known as the [Recovery Time Objective](./rto-rpo.md).
- Compare to availability:

  - Disaster recovery measures objectives for one-time event.
  - Availability objectives measure mean values over a period of time.

    ![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/resiliency-objectives.png)

  - DR focuses on disaster events, whereas availability focuses on more common disruptions of smaller scale such as component failures, network issues, software bugs, and load spikes.

- How does disaster recovery work?
  - Disaster recovery relies upon the replication of data and computer processing in an off-premises location not affected by the disaster.
  - When servers go down because of a natural disaster, equipment failure or cyber attack, a business needs to recover lost data from a second location where the data is backed up. Ideally, an organization can transter its computer processing to that remote location as well in order to continue operations.
- 5 Top elements of an effective disaster recovery plan:
  - Disaster recovery team: a group of specialists will be responsible for creating, implementing, and managing the disaster recovery plan. This plan should define each team member's role and responsibilities. In the event of disaster, the recovery team should know how to communicate with each other, employees, vendors, and customers.
  - Risk evaluation: Assess potential hazards that put your organization at risk. Depending on the type of event, strategize what measures and resources will be needed to resume business. For example, in the event of a cyber attack, what data protection measures will the recovery team have in place to respond?
  - Business-critical asset identification: A good disaster recovery plan includes documentation of which systems, applications, data, and other resources are most critical for business continuity, as well as the necessary steps to recover data.
  - Backups: Determine that needs backup (or to be relocated), who should perform backups, and how backups will be implemented. Include a [RPO](./rto-rpo.md) that states the frequency of backups and a [RTO](./rto-rpo.md) that defines the maximum amount of downtime allowable after a disaster. These metrics create limits to guide the choice of IT strategy, processes and procedures that make up an organization's disaster recovery plan. The amount of downtime an organization can handle and how frequently the organization backs up its data will inform the disaster recovery strategy.
  - Testing and optimization: The recovery team should continually test and update its strategy to address ever-evolving threats and business needs. By contunually ensuring that a company is ready to face the worst-case scenarios in disaster situations, it can successfully navigate such challenges.
- What are the types of disaster recovery?
  - Back-up: This is simplest type of disaster reocvery and entails storing data off site or on a removable driver.
  - Cold site: An organization sets up a basic infrastructure in a second, rarely used facility that provides a place for employees to work after a natural disaster or fire. It can help with business continuity because business operations can continue, but it does not provide a way to protect or recover important data, so a cold site must be combined with other methods of disaster recovery.
  - Hot site: A hot site maintains up-to-date copies of data at all times. Hot sites are time-consuming to set up and more expensive than cold sites, but they dramatically reduce down time.
  - Disaster Recovery as a Service (DRaaS):
  - Back Up as a Service:
  - Datacenter disaster recovery:
  - Virtualization:
  - Point-in-time copies: Point-in-time snapshot, make a copy of the entire database at a given time. Data can be restored from this backup, but only if the copy is stored of site or on a virtual machine that is unaffected by the disaster.
  - Instant recovery: Instant recovery is similar to point-in-time copies, except that instead of copying a database, instant recovery takes a snapshot of an entire virtual machine.
