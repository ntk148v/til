# WebSocket

Source: <https://ably.com/topic/websockets-vs-http>

![](https://images.ctfassets.net/ee3ypdtck0rk/0mExYcxsnzccWxnktAKjc/e26578a6c46c48a02308a222440c6d69/websockets.png?w=891&h=866&q=50&fm=webp)

- WebSockets allow both the server and client to push messages at any time without any relation to a previous request.
  - Bi-directional protocol: either client/server can send a message to the other party.
  - Full-duplex communication: client and server can talk to each other independently at the same time.
  - Single TCP connection: client and server communicate over that same TCp connection (persistent connection) throughout the lifecycle of WebSocket connection.
- Pros:
  - An event-driven protocol -> truly realtime communication.
  - Keep a single, persistent connection open while eliminating latency problems that arise with HTTP request/response-based methods.
  - Generally do not use XMLHttpRequest, and as such, headers are not sent everytime we need to get more information from the server.
- Cons:
  - Don't automatically recover when connections are terminated.
- When can a web socket be used:
  - Real-time web application
  - Gaming application
  - Chat application
