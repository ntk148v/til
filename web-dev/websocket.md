# WebSocket

Source:

- <https://ably.com/topic/websockets>
- <https://ably.com/topic/the-challenge-of-scaling-websockets>

Table of content:

- [WebSocket](#websocket)
  - [1. What is WebSocket?](#1-what-is-websocket)
  - [2. Pros and Cons](#2-pros-and-cons)
  - [3. Use case](#3-use-case)
  - [4. Scaling the WebSocket server layer](#4-scaling-the-websocket-server-layer)

## 1. What is WebSocket?

- WebSockets allow both the server and client to push messages at any time without any relation to a previous request.
  - Bi-directional protocol: either client/server can send a message to the other party.
  - Full-duplex communication: client and server can talk to each other independently at the same time.
  - Single TCP connection: client and server communicate over that same TCP connection (persistent connection) throughout the lifecycle of WebSocket connection.
- WebSocket technology consists of two core building blocks:
  - WebSocket protocol:
    - Enables ongoing, full-duplex, bidirectional communication between client and server over an underlying TCP connection.
    - Allow clients and servers to communicate in realtime, allowing for efficient and responsive data transfer in web applications.
  - WebSocket API:
    - A programming interface for creating WebSocket connectins and managing the data exchange between client and server.
    - Provides a simple and standardized way for developers to use the WebSocket protocol in their applications.
- [How do WebSockets work?](https://ably.com/topic/how-do-websockets-work)

  - Opening a WebSocket connection: opening handshake -> consists of an HTTP request/response exchange between client and server.
  - Data transmissions over WebSockets: Client and server can exchange messages (frame) over the WebSocket connection
  - Closing a WebSocket connection: closing handshake -> sending a close message.

## 2. Pros and Cons

- Pros:
  - Enable realtime communication between client and server -> reduce latency, and improve performance and responsiveness of web apps.
  - Persistent and bidirectional -> more flexible than HTTP, more efficient (allow data to be transmitted without the need for repetitive HTTP headers and handshake)
- Cons:
  - Not optimized for streaming audio and video data
  - Don't automatically recover when connections are terminated
  - Stateful -> hard to scale (need to share connection state across servers).

## 3. Use case

- WebSocket offers low-latency communication capabilities which are needed for use cases where it’s critical for data to be sent and consumed in realtime or near-realtime.
  - Live chat
  - Data broadcast
  - Data synchronization
  - Multiplayer collaboration
  - In-app alerts and notifications
  - Realtime location traclomg

## 4. Scaling the WebSocket server layer

- There are 2 main paths you can take to scale server layer:

![](https://images.ctfassets.net/ee3ypdtck0rk/1Eu1PnOyty4TJRJOwMp1Zp/9bfff65545d75a7f2717875e1b181e3f/horizontal-vs-vertical-scaling.png.png?w=1841&h=841&q=50&fm=webp)

- Vertical scaling (scale-up):
  - Add more power to an existing server.
  - There's a finite amount of resources you can add, which limits the number of connections your system can handle.
  - Need an additional mechanism, such as another intervening reverse proxy, to balance traffic between the server processes.
  - Single point of failure.
- Horizontal scaling (scale out): add more servers to share the workload.
  - Load balancer.
  - Aware of Sticky sessions.
  - WebSockets + Pub/sub.
- Manging WebSocket connections:
  - Load shedding WebSocket connections:
    - Test -> Discover the maximum load
    - Backoff retry mechanism
    - Drop existing (idle) connections to reduce the load on system
  - Restoring connections:
    - Reconnection strategies: Exponential backoff.
    - Reconnection with continuity:
      - Data integrity (guaranteed ordering and exactly-once delivery) is crucial for some use cases
      - Once WebSocket connection is re-established, data stream must be resumed precisely where it left off.
      - Consider how to cache messages and whether to transfer data to persistent storage.
      - Manage stream resumes when a WebSocket client reconnects and think about how to synchronize the connection state across your servers.
- Practice: [Slack scaling story](https://slack.engineering/migrating-millions-of-concurrent-websockets-to-envoy/).I
