# Scale Cube - three dimension scalability model

Source: <http://theartofscalability.com/>

![](https://microservices.io/i/DecomposingApplications.021.jpg)

- `X-axis scaling`:
  - Consist of running multiple copies of an application behind of load balancer.
  - Drawback:
    - Each copy potentially accesses all of the data, caches require more memory to be effective.
    - It does not tackle the problems of increasing development and application complexity.
- `Y-axis scaling`:
  - Splits application into multiple, different services. Each service is responsible for one or more closely related functions.
  - Decomposition: verb-based and noun-based.
- `Z-axis scaling`:
  - Each server runs an identical copy of the code. Each server is responsible for only a subset of the data.
  - Some component of the system is responsible for routing each request to the appropriate server.
  - Commoly used to scale database (sharding)
  - Benefits:
    - Each server only deals with a subset of the data.
    - Improve cache utilization and reduce memory usage and I/O traffic.
    - Improve transaction scalability since requests are typically distributed acrosss multiple servers.
    - Improve fault isolation since a failure only makes part of the data in accessible.
  - Drawbacks:
    - Increase application complexity.
    - Need to implement a partitioning scheme.
    - It does not tackle the problems of increasing development and application complexity.
