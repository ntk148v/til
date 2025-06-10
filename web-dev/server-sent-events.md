# Server-sent events (SSE)

While you are developing real-time projects, there is always a one-question mark on "how to send messages/updates from server to client". We can talk about three different ways to perform server-to-client updates: Client polling, Web Socket, Server-Sent Events (SSE).

## 1. Client polling

- The client sends requests to the server at regular intervals for new updates.
- It can be preferred for small-medium size projects.
- Easy to implement.
- Doesn't provide a fully-real time system that depends on the request intervals.

## 2. Web socket

- Provides bi-directional data transfer for client and server communication on real-time applications.

## 3. Server-sent events (SSE)

> (**Wikipedia**): A server push technology enabling a client to receive automatic updates from a server via an HTTP connection, and describes how servers can initiate data transmission towards clients once an initial client connection has been established.

- Almost every browser is supporting the SSE.
- SSE enables servers to send messages from the server to the client without any polling or long-polling.

![](https://miro.medium.com/v2/resize:fit:700/1*ZOvd7h41rtYPVvxUcyP5Kw.png)

- SSE streaming can be started by the client's GET request to server.

```http
GET /api/v1/live-scores
Accept: text/event-stream --> indicates the client waiting for event stream from the server
Cache-Control: no-cache
Connection: keep-alive
```

- List of pre-defined SSE field names include:
  - **event**: the event type defined by application
  - **data**: the data field for the event or message.
  - **retry**: the browser attempts to reconnect to the resource after a defined time when the connection is lost or closed.
  - **id**: id for each event/message
- **Disadvantages**:
  - The limitation in data format (UTF-8 messages, binary data is not supported).
  - When not used over HTTP/2, SSE suffers from a limitation to the maximum number of open connections, which can be especially painful when opening multiple tabs, as the limit is per browser and is set to a very low number (6) [mozilla](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events).
