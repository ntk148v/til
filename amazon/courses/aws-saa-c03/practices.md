# Practice Tests Note

## Practice Test 1

1. S3

- Minimum days for transition from Tier X -> Tier Y: 30 days.
- S3 One-Zone IA: lower-cost option, infrequently accessed and re-creatable data, don't require the availability and resilience.

![](https://docs.aws.amazon.com/AmazonS3/latest/dev/images/lifecycle-transitions-v2.png)

2. IAM

- Create a new IAM role with the required permissions to access the resources in the production environment. The users can then assume this IAM role while accessing the resources from the production environment.

3. Block access from countries -> WAF

- Use AWS WAF to block or allow requests based on conditions that you specify, such as the IP addresses.

4. AutoScaling

- ALB is best suited for load balancing HTTP and HTTPS traffic and provides advanced request routing targeted at the delivery of modern application architectures, including microservices and containers.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q2-i1.jpg)

5. Route53

- Use Route53 based geolocation routing policy to restrict distribution of content to only the locations in which you have distribution rights.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q38-i1.jpg)

- Use georestriction to prevent users in specific geographic locations from accessing content that you're distributing through a CloudFront web distribution

6. S3

- You can place a retention period on an object version either explicity or through a bucket default setting -> apply -> specify a `Retain Until Date` for object version.

7. SQS

- SQS is a fully managed message queuing service -> decouple and scale microservices, distributed systems, and serverless applications.
- FIFO queues support up to 300 messages/second -> Batch 10 messages per operation (maximum), FIFO queues can support up to 3000 messages/second.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q34-i1.jpg)

8. EBS, EFS, S3

- Cost of test file storage on S3 Standard < Cost of test file storage on EFS < Cost of test file storage on EBS.

9. AWS FSx for Lustre

- FSx for Lustre: high-performance file system - machine learning, high-performance computing (HPC), video processing, and finacial modeling. FSx for Lustre integrates with S3, making it easy to process data sets with the Lustre file system.
- FSx for Windows File Server: Service Message Block (SMB) protocol, built on Windows Server, and Microsoft AD integration. Not integrate with S3.
- EMR: big data platform for processing vast amount of data using open source tools such as Apache Spark, Hive, HBase, Flink, ... Uses Hadoop -> distribute data and processing across a resizable cluster of Amazon EC2 instances. Doesn't offer the same storage and processing speeds as FSx for Lustre.
- Glue: fully managed ETL service to prepare and load data for anaytics (batch ETL processing).

10. KMS

- Delete a customer master key (CMK) in KMS -> KMS enforces a waiting period (7-30 days) -> Pending deletion.

11. DAX and ElastiCache

![](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/images/dax_high_level.png)

12. Autoscaling group

- Target tracking policy: you select a scaling metric and set a target value. Amazon EC2 Auto Scaling creates and manages the CloudWatch alarms that trigger the scaling policy and calculates the scaling adjustment based on the metric and the target value. The scaling policy adds or removes capacity as required to keep the metric at, or close to, the specified target value.
  - For example: Configure a target tracking scaling policy to keep the average aggregate CPU utilization of your Auto Scaling group at 50 percent.

!![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q30-i1.jpg)

13. AWS API Gateway

- API Gateway creates RESTful APIs that enable stateless client-server communication and API Gateway also creates WebSocket APIs that adhere to the WebSocket protocol, which enables stateful, full-duplex communication between client and server.

![](https://d1.awsstatic.com/serverless/New-API-GW-Diagram.c9fc9835d2a9aa00ef90d0ddc4c6402a2536de0d.png)

14. S3

- Features can only be suspended once they have been enabled: Versioning.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q39-i1.jpg)

15. Account

- Create a strong password for the AWS account root user
- Enable MFA for the AWS account root user account.

16. RDS

- Multi-AZ synchronous replication. Read replicas asynchronous replication (within an AZ, Cross-AZ, Cross Region)

17. ECS

- ECS with EC2 launch type is charged based on EC2 instances and EBS volumes used. ECS with Fargate launch type is charged based on vCPU and memory resources that the containerized application requests.

18. Global Accelerator

- Global Accelerator: Utilizes the Amazon global network -> improve the performance of your applications by lowering first-byte latency and jiter. Non-HTTP use cases -> gaming, IoT, VoIP. ELB is an ideal target for AWS Global Accelerator.
- CloudFront: CDN.

19. S3

- S3 Standard-IA storage class is for data that is accessed less frequently but requires rapid access when needed.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q15-i1.jpg)

- For a small monthly object monitoring and automation charge, S3 Intelligent-Tiering monitors access patterns and automatically moves objects that have not been accessed to lower-cost access tiers -> optimize costs by automatically moving data to the most cost-effective access tier, without performance impact or operational overhead.

20. CloudFront

- Distribute content with low latency and high data transfer speeds.

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q62-i2.jpg)

21. Kinesis Data Streams

- Amazon Kinesis Data Streams enables real-time processing of streaming big data. It provides ordering of records, as well as the ability to read and/or replay records in the same order to multiple Amazon Kinesis Applications.
  - Routing related records to the same record processor (as in streaming MapReduce).
  - Ordering of recods.
  - Ability for multiple applicatitons to consume the same stream concurrency.
  - Ability to consume records in the same order a few hours later.
- SNS: fully managed pub/sub messaging service, not real-time processing of data.
- SQS: high scalable hosted queue for storing message as they travel between computers.

22. Kinesis Data Streams + Lambda + DynamoDB

- KDS can continously capture gigabytes of data per second from hundred of thousands of sources.
- Lambda integrates natively with Kinesis Data Streams. The polling, checkpointing, and error handling complexities are abstracted when you use this native integration. The processed data can then be configured to be saved in DynamoDB.

23. EC2

- Reserved EC2 instances for 24/7, on-demand for dev

![](https://assets-pt.media.datacumulus.com/aws-saa-pt/assets/pt1-q47-i2.jpg)

24. S3

- Achieve thousands of transactions per second.
- No limits to the number of prefixes in a bucke -> increase read/write performance by parallelize reads. For example, if you create 10 prefixes in an Amazon S3 bucket to parallelize reads -> scale read performance to 55000 read requests/second.

25. API Gateway, SQS, Kinesis

- Throttling is the process of limiting the number of requests an authorized program can submit to a given operation in a given amount of time.

26. CloudFront

- Skip the regional edge cache:
  - Proxy methods PUT/POST/PATCH/OPTIONS/DELETE go directly to the origin
  - Dynamic content, as determined at request time.

27. EFS

- Can connect to EFS file systems from EC2 instances in the other AWS regions using an inter-region VPC peering connection, and from on-premises servers using an AWS VPN connection.
