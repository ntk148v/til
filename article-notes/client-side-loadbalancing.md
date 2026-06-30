# Client side load balancing

Source: <https://engineering.zalando.com/posts/2026/06/client-side-load-balancing.html>

The Zalando article describes how they replaced a **shared infrastructure load balancer (Skipper)** with an **in-process client-side load balancer (CSLB)** for one of their highest-throughput services—handling **over one million requests per second**. The result was lower latency, better observability, higher resilience, and significant infrastructure cost savings. ([Zalando Engineering][1])

Let's walk through the architecture and the engineering decisions.

---

# The Problem

The architecture initially looked like this:

```text
                 Batch Request
                       │
                 Product Sets Service
                       │
        ┌──────────────┴──────────────┐
        │                             │
        │ fan-out (up to 50 requests) │
        ▼                             ▼
                  Skipper LB
        ┌───────┬─────────┬─────────┐
        ▼       ▼         ▼         ▼
      Pod A   Pod B     Pod C    Pod D
```

A single user request might require fetching 50 products.

Instead of contacting pods directly, every request went through **Skipper**, Zalando's Kubernetes ingress/load balancer.

Although each Skipper hop only added **hundreds of microseconds**, the batch request had to wait for **the slowest of 50 parallel requests**.

This is the classic "tail latency" problem.

If

```
each request = 300 µs LB overhead
50 requests in parallel
```

the latency becomes

```
max(request1...request50)

rather than

average(request1...request50)
```

Even tiny delays become amplified.

---

# Why Client-side Load Balancing?

Instead of

```text
Caller
   │
Load Balancer
   │
Server
```

they changed to

```text
Caller
   │
  chooses server itself
   │
Server
```

The client now knows all backend pods.

```text
Product Sets

Endpoint list

Pod A
Pod B
Pod C
Pod D

↓

hash(productID)

↓

choose Pod C

↓

HTTP directly to Pod C
```

No shared router in the middle.

---

# How does the client know backend pods?

The obvious solution would be polling Kubernetes.

```
Every 5 seconds

GET EndpointSlice
```

But imagine

```
500 application pods

×

poll every few seconds
```

This can overload the Kubernetes API server.

Instead they use a Kubernetes **Informer**.

An Informer works like

```
LIST once

↓

WATCH forever
```

```text
Kubernetes API
       │
 LIST EndpointSlices
       │
       ▼
 local cache

then

 WATCH

Pod Added
Pod Removed
Pod Updated

↓

update local routing table
```

Much cheaper than polling. ([Zalando Engineering][1])

---

# Why consistent hashing?

Suppose product 123 is requested constantly.

Without consistent hashing:

```
123

↓

Pod A

next request

↓

Pod D

next request

↓

Pod B
```

Every pod has to fetch the product into cache.

Bad cache locality.

Instead

```
hash(productID)

↓

Ring

↓

Always Pod C
```

Now Pod C already has product 123 cached.

This dramatically improves cache hit rate.

---

# But what happens when pods scale?

Suppose

```
A B C D
```

becomes

```
A B C D E
```

Naively rebuilding the hash ring immediately causes many keys to move.

```
123

before → Pod C

after → Pod E
```

Pod E's cache is empty.

Thousands of products suddenly miss cache.

Latency spikes.

---

# Their solution: N-Ring Fade-in

Instead of switching immediately

```
Old Ring

↓

New Ring
```

they run multiple routing rings simultaneously.

Example

```
90%

Old Ring

10%

New Ring
```

then

```
70%

Old

30%

New
```

then

```
50%

50%
```

until

```
100%

New
```

This gradually warms caches.

A brilliant detail is that **pods occupy identical positions in every ring**, so the new pod warms with exactly the traffic it will eventually own. ([Zalando Engineering][1])

---

# Their first mistake: throughput is not load

Initially they measured

```
Requests/sec
```

Suppose

```
1000 requests/sec

each = 1 ms
```

Looks busy.

Reality:

```
1000 × 1 ms

=

1 request in flight on average
```

The server is barely working.

Throughput isn't actual load.

---

# Occupancy (Little's Law)

Instead they estimate

```
Occupancy

=

total busy time

/

window length
```

Imagine

```
150 ms window

during that window

pod spent 75 ms processing
```

Occupancy

```
75 / 150

=

0.5
```

Meaning

```
roughly 50% utilized
```

This is much closer to real server pressure.

They combine

```
max(
    inflight_requests,
    occupancy
)
```

because occupancy misses requests that haven't completed yet, while instantaneous in-flight counts can miss bursty traffic between samples. ([Zalando Engineering][1])

---

# Bounded Load

Consistent hashing can overload a hot key.

Suppose

```
Celebrity product

↓

same pod forever
```

Eventually

```
Pod C

2000 req/sec

Pod D

100 req/sec
```

To avoid overload they use **bounded load**.

Algorithm:

```
Primary hash

↓

Is Pod overloaded?

↓

No

→ use it

↓

Yes

Walk clockwise

↓

Find next acceptable pod
```

Most requests still use their cache-optimal destination.

Only overloaded requests move elsewhere.

---

# Retry logic

Previously Skipper handled retries.

Now the application owns them.

Rules:

- one retry only
- retry only on transport errors or 5xx
- never retry 404 or other 4xx
- retry must choose a **different pod**

```text
Pod A failed

↓

Retry

↓

Pod C
```

Never retry to the same instance.

---

# Availability Zone awareness

They also experimented with

```
AZ1

↓

only AZ1 pods

AZ2

↓

only AZ2 pods
```

Benefits:

- lower latency
- less inter-AZ traffic
- lower cloud networking cost

However, this created an unexpected cache problem because each zone initially saw only a subset of the traffic and had to warm a much larger working set, increasing database reads. They paused this optimization until they could correctly account for load across both global and zone-local routing rings. ([Zalando Engineering][1])

---

# Operational advantages

The article highlights several benefits beyond raw latency:

- **Observability:** the application now knows exactly which backend was chosen and why, making it easier to distinguish application issues from load-balancer issues.
- **Resilience:** if the Kubernetes API is temporarily unavailable, the client continues using the last known endpoint list rather than failing immediately.
- **Fallback:** a configuration switch can instantly route all traffic back through Skipper if needed.
- **Cost savings:** removing roughly one million internal requests per second from Skipper reduced the Skipper fleet dramatically, and improved load distribution allowed the application to run with about **25% fewer pods**, saving over **$1,000 per day**. ([Zalando Engineering][1])

---

# Comparison: Server-side vs Client-side Load Balancing

| Server-side LB                                | Client-side LB                                       |
| --------------------------------------------- | ---------------------------------------------------- |
| Client sends every request to a load balancer | Client chooses backend directly                      |
| Infrastructure owns routing logic             | Application owns routing logic                       |
| Extra network hop                             | No intermediary hop                                  |
| Centralized observability                     | Per-client routing decisions and metrics             |
| Simple clients                                | More complex client implementation                   |
| Easier operationally                          | Better latency and cache locality at very high scale |

For most systems, a server-side load balancer (or Kubernetes `Service`) is the right choice because it's simpler and operationally mature. Client-side load balancing becomes attractive when the routing overhead itself is measurable—as in Zalando's case, where each incoming request fans out into dozens of internal calls and the service processes traffic at the scale of **millions of requests per second**. At that scale, eliminating even a few hundred microseconds per hop and optimizing cache locality translates into meaningful gains in latency, resilience, and infrastructure cost.

[1]: https://engineering.zalando.com/posts/2026/06/client-side-load-balancing.html?utm_source=chatgpt.com 'Client-Side Load Balancing at a Million Requests Per Second'
