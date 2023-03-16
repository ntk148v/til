# Disaster Recovery

Source: <https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/introduction.html>

- Disaster recovery (DR) is the process of preparing for and recovering from a disaster. An event that prevents a workload or system from fulfilling its business objectives in its primary deployed location is considered a disaster.
- DR is an important part of resiliency strategy and concerns how workload responds when a disaster strikes. This response must be based on organization's business objectives which specify workload's strategy for avoiding loss of data, known as the [Recovery Point Objective](./rto-rpo.md), and reducing downtime where workload is not available for use, known as the [Recovery Time Objective](./rto-rpo.md).
- Compare to availability:

  - Disaster recovery measures objectives for one-time event.
  - Availability objectives measure mean values over a period of time.

    ![](https://docs.aws.amazon.com/images/whitepapers/latest/disaster-recovery-workloads-on-aws/images/resiliency-objectives.png)

  - DR focuses on disaster events, whereas availability focuses on more common disruptions of smaller scale such as component failures, network issues, software bugs, and load spikes.
