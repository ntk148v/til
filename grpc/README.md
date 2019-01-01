# GRPC

## The escalation of data transfer

* Develope APIs -> REST + HTTP + JSON as transportation protocol & data schema, respectively.
* Problems beign when we get a API has a big continous volume of requests -> Amount of memory used on tasks like data transportation -> A burden on the API.
* gRPC (server-client model & a serialization technique) -> shrink the amount of resources used on remote calls -> scale more capacity per API instance.
* gRPC draws: operations like debugging get more difficult than REST/JSON (gRPC encapsulates the trasportation logic that utilizes binary serialization to do the transportation).

## RPC

* Remote Procedure Call - A client-server solution is developed, where the details of transport are abstracted from the developer, been responsible only for impleting the server & client inner logic.
* gRPC only has the concept of a client-server application.

## gRPC

* gRPC = a client-server application (principles from the original RPC) + HTTP2 + streams.
* Multi-language, multi-platform framework.
    * Native implementation in C, Java   and   Go.
    * C stack wrapped by C++, C#, Node, ObjC, Python, Ruby, PHP.
    * Platforms supported: Linux, Android, iOS, MacOS, Windows.
* Transport over HTTP/2+ TLS.
    * Leverage existing network protocols   and   infrastructure.
    * Efficient use of TCP - 1 connection shared across concurrent framed streams.
    * Native support for secure bidirectional streaming.
* C/C++ implementation goals.
    * High throughput   and   scalability, low latency.
    * Minimal external dependencies.
* Proto file -> gRPC generates for us a server   and   a stub where we develop our server & client logic.

![grpc-architecture](https://alexandreesl.files.wordpress.com/2017/05/grpc-1.png?w=720)

## Protocol Buffers

* gRPC's serialization mechanism.
* Binary data representation.
* Structures can be extended   and   maintain backward compatibility.
* Code generators for many languages.
* Strongly typed.
* Not required for gRPC, but very handy.

## HTTP/2

### Using an HTTP/1.1 transport   and   its limitations

* Request-Response protocol
    * Each connection supports pipelining but not parallelism (in-order only).
    * Need multiple connections per client-server pair to avoid in-order stalls across multiple requests -> multiple CPU-intense TLS handshakes, higher memory footprint.
* Content may be compressed but headers are text format
* Natually supports single-direction streaming but not bidirectional

### HTTP/2 in a Nutshell

* One TCP connection for each client-server pair
* Request -> Stream
    * Streams are multiplexed using framing
* Compact binary framing layer
* Header compression
* Directly supports bidirectional streaming

## Types of gRPC applications

gRPC applications can be written using 3 types of processing:
* **Unary RPCs**: The simplest type   and   more close to classical RPC consists of a client sending one message to a server, that makes somoe processing   and   returns one message as response.
* **Server streams**: On this type, the client sends one message for the server, but receives a stream of messages from the server. The client keeps reading the messages from the server until there is no more mesages to read.
* **Client streams**: This type is the opposite of the server streams one, where on this case is the client who sends a stream of messages to make a request for the server   and   them waits for the server to produce a single response for the series of request messages provided.
* **Bidirecional stream RPC**: This is the more complex but also more dynamic of all the types. On this model, we have both client & server reading & writing on streams, which are stablished between the server & client. This streams are independent from each other, which means that could be possible for a client to send a message to a server by one stream   and   vice-versa at the same time. This allows us to make multiple processing scenarios, such as clients sending all the messages before the responses, clients & servers "ping-poinginig" messages between each other & so on.

## Sync vs Async

* Synchronous processing occurs when we have a communication where the client thread is blocked when a message is sent & is been processed.
* Asynchronous processing occurs when we have this communication with the processing been done by other threads, making the whole process been non-blocking.

## Deadlines & timeouts

* Deadline: how much time a gRPC client will wait on a RPC call to return before assuming a problem has happened. On the server's side, the gRPC services can query this time, verifying how much time it has left.
* Timeout -> DEADLINE\_EXCEEDED error + RPC call is terminated.

## RPC termination

* On gRPC, both clients & servers decide if a RPC call is finished or not locally independently. This means that a server can decide to end a call before a client has transmitted all their messages & a client can decide to end a call before a server has transmitted one or all of their responses.

## Channels

* Channels are the way a client stub can connect with gRPC services on a given host & port.
* Channels can be configured specific by client.

## Refs

* [GRPC: TRANSPORTING MASSIVE DATA WITH GOOGLE’S SERIALIZATION](https://alexandreesl.com/tag/grpc/)
* [gRPC Motivation and Design Principles.](https://grpc.io/blog/principles)
* [Building High Performance APIs In Go Using gRPC And Protocol Buffers](https://medium.com/@shijuvar/building-high-performance-apis-in-go-using-grpc-and-protocol-buffers-2eda5b80771b)
