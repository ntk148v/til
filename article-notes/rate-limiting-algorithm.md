# Rate Limiting

Source:

- https://konghq.com/blog/how-to-design-a-scalable-rate-limiting-algorithm
- https://hechao.li/2018/06/25/Rate-Limiter-Part1/

Rate limiting protectes APIs from overuse by limiting how often each user can call the API. This protects them from inadvertent or malicious overuse.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/01-rate-limit-kong.png)

## 1. Rate Limiting Algorithms

### 1.1. Leaky buckets

- [Leaky buckets](https://en.wikipedia.org/wiki/Leaky_bucket) - a queue which you can think of as a bucket holding the requests.

  - A request is registered --> the end of queue.
  - At a regular interval, queue --> the 1st item (FIFO queue).
  - Queue is full, additional requests are discarded.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/02-rate-limit-kong.png)

- Advantages:

  - Easy to implement.
  - It smooths out bursts of requests and processes them at an approximately average rate.

- Disadvantages:
  - A burst of traffic can fill up the queue with old requests and starve more recent requests from being processed.
  - It also provides no guarantee that requests get processed in a fixed amount of time.

### 1.2. Fixed window

- Fixed window:

  - A window size of n seconds is used to track the rate.
  - Each incoming request increments the counter for the window.
  - Counter > threshold, the request is discarded.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/03-rate-limit-kong.png)

- Advantages:
  - Ensure more recent requests gets processed without being starved by old requests.
- Disadavantages:
  - A single burst of traffic that occurs near the boundary of a window can result in twice the rate of requests being processed, because it will allow requests for both the current and next windows within a short time.

### 1.3. Sliding log

- Sliding log:

  - Involves tracking a timestamp log for each consumer's request.
  - These logs are usually stored in a hash set or table that is sorted by time.
  - Logs with timestamps beyond a threshold are discarded.
  - When a new request comes in, we calculate the sum of logs to determine the request rate. If the request would exceed the threshold rate, then it is held.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/04-rate-limit-kong.png)

- Advantages:

  - It doesn't suffer from the boundary conditions of fixed windows.

- Disadvantages:
  - It can be very expensive to store an unlimited number of logs for every request.
  - It's also expensive to compute.

### 1.4. Sliding window

- Sliding window:
  - Low processing cost of the fixed window + improved boundary conditions of the sliding log.
  - Track a counter for each fixed window.
  - Account for a weighted value of the previous window's request rate based on the current timestamp.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/05-rate-limit-kong.png)

- Advantages:
  - Avoid the starvation problem of leaky bucket and bursting problems of fixed window.

## 2. Rate Limiting in Distributed system

### 2.1. Synchronization policies

- Enforce **global rate limit** -> must set up a policy.
- If each node were to track its own rate limit, then a consumer could exceed a global rate limit when requests are sent to different nodes.
- Solution:
  - Setup sticky sessions in LB so that each consumer gets sent to exactly one node --> a lack of fault tolerance and scaling problems.
  - Use a centralized data store (Redis/cassandra) to store the counts for each window and consumer --> increase latency making requests to the data store, and race conditions.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/06-rate-limit-kong.png)

### 2.2. Race conditions

- [Race conditions](https://en.wikipedia.org/wiki/Race_condition):
  - **get-then-set** - get rate limit counter, counter++, put counter back to the data store.
  - Problem: Req 1 performs a full cycle of read-increment-store -> Req 2 is coming, gets the invalid (lower) counter value.

![](https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/06-2-rate-limit-kong.png)

- Use **lock** -> performance bottleneck.
- **set-and-get**!

### 2.3. Optimizing for performance

...
