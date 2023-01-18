# HTTP/2.0

Source: <https://developers.google.com/web/fundamentals/performance/http2>

- [HTTP/2.0](#http20)
  - [1. Introduction](#1-introduction)
  - [2. Design](#2-design)
    - [2.1. Binary framing layer](#21-binary-framing-layer)
    - [2.2. Streams, messages, and frames](#22-streams-messages-and-frames)
    - [2.3. Request and response multiplexing](#23-request-and-response-multiplexing)
    - [2.4. Stream prioritization](#24-stream-prioritization)
    - [2.5. One connection per origin](#25-one-connection-per-origin)
    - [2.6. Flow control](#26-flow-control)
    - [2.7. Server push](#27-server-push)
    - [2.8. Header compression](#28-header-compression)

## 1. Introduction

- Major revision of the HTTP network protocol.
- It was derived from the earlier experimental [SPDY](https://en.wikipedia.org/wiki/SPDY) protocol.
- Goals:
  - Reduce latency by enabling full request and response multiplexing.
  - Minimize protocol overhead via efficient compression of HTTP header fields.
  - Add supprt for request prioritization and server push.
- HTTP/2 does not modify the application semantics of HTTP in any way. All the core concepts, such as HTTP methods, status codes, URIs, and header fields, remain in place.

## 2. Design

- HTTP/1.x drawbacks:
  - Clients need to use multiple connections to achieve concurrency and reduce latency.
  - Does not compress request and response headers ->  unncessary network traffic.
  - Does not allow effective resource prioritization, resulting in poor use of the underlying TCP connection.
- HTTP/2.0:
  - Introduce header field compression.
  - Allow multiple concurrent exchanges on the same connection.
  - Allow interleaving of request and response messages on the same connection and use an effective coding for HTTP header fields.
  - Allow prioritization of requests, letting more important requests complete more quicky.
- All the core of all performance enhancements of HTTP/2 is the new **binary framing layer**.

### 2.1. Binary framing layer

- How the HTTP messages are encapsulated and transferred between the client and server.

![](https://developers.google.com/web/fundamentals/performance/http2/images/binary_framing_layer01.svg)

- New optimized encoding mechanism between the socket interface and the higher HTTP API exposed to our applications: HTTP sematics are unaffected but the way they are encoded while in transit is different.
- All HTTP/2 communication is split into smaller messages and frames, each of which is encoded in binary format.

### 2.2. Streams, messages, and frames

- HTTP/2 terminology:
  - *Stream*: A bidirectional flow of bytes within an established connection, which may carry one or more messages.
  - *Message*: A complet sequence of frames that map to a logical request or response message.
  - *Frame*: The smallest unit of communication in HTTP/2, each containing a frame header, which at a minimum identitifes the stream to which the frame belongs.

![](https://developers.google.com/web/fundamentals/performance/http2/images/streams_messages_frames01.svg)

- All communication is perfomed over a sinle TCP connection that can carry any number of bidirectional *streams*.
- Each *stream* has a unique identifier and optional priority information that is used to carry bidirectional *messages*.
- Each *message* is a logical HTTP message, such as a request/response, which consists of one or more *frames*.
- The *frame* is the smallest unit of communication that carries a specific type of data—e.g., HTTP headers, message payload, and so on. Frames from different streams may be interleaved and then reassembled via the embedded stream identifier in the header of each frame.

### 2.3. Request and response multiplexing

- New binary framing layer -> allow the client and server to break down an HTTP message into independent frames, interleave them, and then reassemble them on the other end -> enable full request and response multiplexing.

![](https://developers.google.com/web/fundamentals/performance/http2/images/multiplexing01.svg)

### 2.4. Stream prioritization

- The HTTP/2 standard allows each stream to have an associated weight and dependency:
  - Each stream may be assigned an interger weight (>=1 and <= 256>).
  - Each stream may be given an explicit dependency on another stream.

- The combination of stream dependencies and weights allows the client to construct and communicate a "prioritization tree".

![](https://developers.google.com/web/fundamentals/performance/http2/images/stream_prioritization01.svg)

- *The parent stream should be allocated resources ahead of its dependencies*.
- *Streams that share the same parent (in other words, sibling streams) should be allocated resources in proportion to their weight*.

### 2.5. One connection per origin

- All HTTP/2 connections are persistent, and only one connection per origin is required, which offers numerous performance benefits.

### 2.6. Flow control

- A mechanism to prevent the sender from overwhelming the receiver with data it may not want or be able to process
- HTTP/2 provides a set of simple building blocks that allow the client and server to implement their own stream- and connection-level flow control:
  - Flow control is directional. Each receiver may choose to set any window size that it desires for each stream and the entire connection.
  - Flow control is credit-based. Each receiver advertises its initial connection and stream flow control window (in bytes), which is reduced whenever the sender emits a `DATA` frame and incremented via a `WINDOW_UPDATE` frame sent by the receiver.
  - Flow control cannot be disabled.
  - Flow control is hop-by-hop, not end-to-end.

### 2.7. Server push

- The server is able to send multiple responses for a single client request.

![](https://developers.google.com/web/fundamentals/performance/http2/images/push01.svg)

- Push resources can be:
  - Cached by the client
  - Reused across different pages
  - Multiplexed alongside other resources
  - Prioritized by the server
  - Declined by the client
- The client needs to know which resources the server intends to push to avoid creating duplicate requests for these resources -> send all `PUSH_PROMISE` frames, which contain just the HTTP headers of the promised resource, ahead of the parent’s response.

### 2.8. Header compression

- HTTP/2 compresses request and response header metadata using the HPACK compression format that uses two simple but powerful techniques:
  - It allows the transmitted header fields to be encoded via a static Huffman code, which reduces their individual transfer size.
  - It requires that both the client and server maintain and update an indexed list of previously seen header fields (in other words, it establishes a shared compression context), which is then used as a reference to efficiently encode previously transmitted values.

![](https://developers.google.com/web/fundamentals/performance/http2/images/header_compression01.svg)
