# Think about Performance before building a Web application

Source: <https://www.techempower.com/blog/2016/02/10/think-about-performance-before-building-a-web-application/>

## 1. What do we mean by performance?

High performance encompasses the following attributes:

- **Low latency**: A high-performance application will minimize latency and provide responses to user actions very quickly. Generally speaking, the quicker is better: ~0ms is superb; 100ms is good; 500ms is okay; a few seconds is bad; and several seconds may be approaching awful.
- **High throughput**: A high-performance application will be able to service a large number of requests simultaneously, staying ahead of the incoming demand so that any short-term queuing of requests remains short-term. Commonly, high-throughput and low-latency go hand-in-hand.
- **Performing well across a spectrum of use-cases**:  A high-performance application functions well with a wide variety of request types (some cheap, some expensive). A well-performing application will not slow, block, or otherwise frustrate the fulfillment of requests based on other users’ concurrent activities. Conversely, a low-performance application might have an architectural bottleneck through which many request types flow (e.g., a single-threaded search engine).
- **Generally respecting the value of user's time**: Overall, performance is in service of user expectations. A user knowns low performance when they see it, and unfortunately, they won't usually tell you if the performance doesn't meet their expectations; they'll just leave.
- **Scales with concurrency**: A high-performance application provides sufficient capacity to handle a reasonable amount of concurrent usage. Handling a user is nothing; 5 concurrently is easy; 500 is good; 50,000 is hard.
- **Scales with data size**: In many applications, network effects mean that as usage grows, so does the amount of "hot" data in play. A high-performance application is designed to perform well with a reasonable amount of hot data. A match-making system with 200 entities is trivial; 20,000 entities is good; 2,000,000 entities is hard.
- **Performs modestly complex calculations without requiring complex architecture**: A high-performance application (notably, one based on a high-performance platform) will be capable of performing modestly complex algorithmic work on behalf of users without necessary requiring the construction of a complex system architecture.

## 2. What are your application's performance needs?

It helps to start by determining whether your application needs, or will ever need to consider performance more than superficially.

We routinely see three situations with respect to application performance needs:

- Applications with known **high-performance needs**. These are applications that, for example, expect to see large data or complex algorithmic work from day one. Examples would be applications that match users based on non-trivial math, or make recommendations based on some amount of analysis of past and present behavior, or process large documents on the users’ behalf. You should go through each of the aspects in the previous section to consider what the performance characteristics are of your application.
- Applications with known **low-performance needs**. Some applications are built for the exclusive use of a small number of users with a known volume of data. In these scenarios, the needed capacity can be calculated fairly simply and isn’t expected to change during the application’s usable lifetime. Examples would be intranet or special-purpose B2B applications.
- Applications with as-yet **unknown performance needs**. We find a lot of people don’t know really how their application will be used or how many people will be using it. Either they haven’t put a lot of thought into performance matters, the complexity of key algorithms isn’t yet known, or the business hasn’t yet explored user interest levels.
