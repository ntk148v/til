# Latency, Bandwidth, Throughput and Response Time

Source: <https://www.perfmatrix.com/latency-bandwidth-throughput-and-response-time/>

Latency, Bandwidth, Throughput and Response Time; somehow these terms are very confusing.

We have a water tank (orange), water pipe (green), and water (blue). The water tank represents a server, the pipe represents a communication channel with a certain width and the water represents data.

![](https://www.perfmatrix.com/wp-content/uploads/2019/09/Latency-Bandwidth-and-Throughput-Illustration.png)

- Latency:
  - The time taken by water to travel from one end to another end.
  - Unit: milliseconds, seconds, minutes or hours.
  - In performance testing, the term latency of a request is the travel time from client to server and server to client.

  ```unknown
  - A request starts at t=0
  - Reaches a server in 1 second (at t=1)
  - The server takes 2 seconds to process (at t=3)
  - Reaches to the client end in 1.2 seconds (at t=4)
  -> latency = 2.2 seconds
  ```

- Bandwidth:
  - The capacity of the pipe (communication channel). It indicates the maximum water that passes through the pipe.
  - In performance testing, bandwidth is the maximum amount of data that can be transferred per unit of time through a communication channel is called the channel's bandwidth.

- Throughput:
  - The water flowing from the pipe can be represented as 'throughput'.
  - In performance testing terms ‘The amount of data moved successfully from one place to another in a given time period is called Data Throughput.
  - Units: bits per second (bps), megabits per second (Mbps) or gigabits per second (Gbps)
  - Throughput can never be more than Bandwidth.

- Response time:
  - The amount of time from the moment that a user sends a request until the time that the application indicates that the request has been completed and reached back to the user.

  ```unknown
  - A request starts at t=0
  - Reaches a server in 1 second (at t=1)
  - The server takes 2 seconds to process (at t=3)
  - Reaches to the client end in 1.2 seconds (at t=4)
  -> latency = 2.2 seconds
  -> Response time = 4.2 seconds
  ```

- Some important points:
  - Solving bandwidth is easier than solving latency.
  - If throughput is nearly equal to bandwidth, it means the full capacity of the network is being utilized which may lead to network bandwidth issues
  - An increase in response time with a flat throughput graph shows a network bandwidth issue.
  - Ideally, consistent throughput indicates an expected capacity of network bandwidth.
  - Ideally, response time and throughput should be constant during a steady state.
  - Latency is affected by connection type, distance and network congestion.
