# Iroh

Source:

- <https://www.iroh.computer/docs/>

## 1. Overview

Iroh is a Rust-based library designed to simplify peer-to-peer (P2P) networking by enabling direct connections between devices. It leverages public key-based addressing, bypassing traditional IP-based systems.
This approach ensures globally unique identifiers and seamless network traversal, even through NATs.
Built on the [QUIC](https://en.wikipedia.org/wiki/QUIC) protocol, Iroh provides features such as encryption, authentication, stream multiplexing, and low-latency connections.

**Iroh is "dial by public key"**

- You dial another node by its `NodeId`, a 32-byte ed25519 public key, allowing devices to connect directly without static IPs or domain names.
- It also doesn't change when you change networks.
- Basing connections on asymmetric public keys is what allows iroh to always end-to-end encrypt and authenticate connections.

**peer-to-peer**

- Iroh is built on peer-to-peer QUIC using both relays and holepunching.
- Peer to peer connectivity is established with the help of a relay server.
  - On startup peers register their NodeId with a home relay server.
  - The relay server provides assistance to traverse firewalls, NATs or others alike.
  - If no direct connection can be established, the connection is relayed via the server.
- Peers can also connect directly without using a relay server. For this, however, the listening peer must be directly reachable by the connecting peer via one of it's addresses.

**Iroh is built on QUIC**

QUIC gives iroh super-powers:

- encryption & authentication
- stream multiplexing
  - no head-of-line blocking issues
  - stream priorities
  - one shared congestion controller
- an encrypted, unreliable datagram transport
- zero round trip time connection establishment if you've connected to another node before

## 2. Concepts

### 2.1. Endpoints

- An _endpoint_ is the main API interface to create connections to (`connect`), and accept connections (`accept`) from other iroh nodes.
- Endpoints have a `NodeID` (the public half of an Ed25519 keypair) and the private key used to sign and decrypt messages.
- Connections are full-fledged QUIC connections, giving you access to most features of QUIC / HTTP3, including bidirectional and unidirectional streams.
- Endpoints are a low-level primitive that iroh exposes on purpose.

### 2.2. Relay

Relays are servers that help establish connections between devices.

- Relays temporarily route encrypted traffic until a direct, P2P connection is feasible. Once this direct path is set up, the relay server steps back, and the data flows directly between devices. This approach allows Iroh to maintain a secure, low-latency connection, even in challenging network situations.
- During the lifespan of a connection, networking conditions can change, for example when a user switched from 5G to WiFi, plugs in an ethernet cable, or a sysadmin modifies router configurations. The connection may change from direct to relayed, or even a mixed combination of the two. Iroh will automatically switch between direct and relayed connections as needed, without any action required from the application.
- number 0 provides a set of public relays that are free to use, and are configured by default. You're more than welcome to run production systems using the public relays if you find performance acceptable.
- Relays aren't the only way to find other iroh nodes. Iroh also supports local discovery, where nodes on the same local network can find each other & exchange dialing information without a relay using mDNS.

### 2.3. Discovery

Discovery is the glue that connects a Node Identifier to something we can dial. Discovery services resolve NodeIds to either a home Relay URL or direct-dialing information.

- Node discovery is an automated system for an Endpoint to retrieve addressing information. Each iroh node will automatically publish their own addressing information with configured discovery services.
- Discovery services:

| Discovery Implementation | Description                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------- |
| DNS (default)            | uses a custom Domain Name System server                                             |
| Local                    | uses an mDNS-like system to find nodes on the local network (Local Swarm Discovery) |
| Pkarr                    | use Pkarr servers over HTTP                                                         |
| DHT                      | uses the BitTorrent Mainline DHT                                                    |

### 2.4. Protocol

Iroh is organized into protocols: Composable networking software built on iroh connections.

- Iroh builds on QUIC connections, and uses application level protocol negotiation (ALPN, a widely used and well specified TLS extension) to run multiple protocols on the same QUIC endpoint
  - An ALPN identifier is the string that identifies the protocol and is used for protocol negotiation between endpoints.
  - For example, the iroh-blobs protocol ALPN is [`/iroh-bytes/4`](https://github.com/n0-computer/iroh-blobs/blob/124820698cd85691e0d72aeed6e1ac028886b34a/src/protocol.rs#L353).
- The accept loop is the main loop of an iroh server. It listens for incoming connections, and then processes them.
  - The accept loop is the entry point for all iroh protocols, and is where you can add your own protocol to the iroh stack.
  - It can run multiple protocols on the same endpoint.

### 2.5. Router

To make composing protocols easier, iroh includes a router for composing together multiple protocols.

The router implements the accept loop on your behalf, and routes incoming connections to the correct protocol based on the ALPN. We recommend using the router to compose protocols, as it makes it easier to add new protocols to your application.

### 2.6. Tickets

Tickets are a way to share dialing information between iroh nodes. They're a single token that contains everything needed to connect to another node, or to fetch a blob or document.

- Tickets are a single serialized token containing everything needed to kick off an interaction with another node running iroh. Here's an example of one:

```text
// Try pasting it into the iroh ticket explorer https://ticket.iroh.computer/ to break it down
docaaacarwhmusoqf362j3jpzrehzkw3bqamcp2mmbhn3fmag3mzzfjp4beahj2v7aezhojvfqi5wltr4vxymgzqnctryyup327ct7iy4s5noxy6aaa
```

- Tickets combine a piece of info with _dialing information for the node to fetch from_.
- Kinds of Tickets:

| Type       | Description                                                  | Contents                                           |
| ---------- | ------------------------------------------------------------ | -------------------------------------------------- |
| `node`     | A token for connecting to an iroh node                       | `Node Address`                                     |
| `blob`     | A token for fetching a blob or collection                    | `Hash`, `HashOrCollection`, `Node Address`         |
| `document` | A read/write access token to a document, plus a node address | `DocID`, `Read/Write Capability`, `[Node Address]` |

- Tickets are sensitive: if you share a ticket with someone, they can use it to connect to your machine.
- Document tickets are secrets: When you create a document ticket, you're creating a secret that allows someone to read or write to a document. This means that you should be careful about sharing document tickets with people you don't trust.

### 2.7. NodeAddr

Node Addresses or `NodeAddrs` are a common struct you'll interact when working with iroh to tell iroh what & where to dial.

```rust
pub struct NodeAddr {
    pub node_id: PublicKey,
    pub relay_url: Option<RelayUrl>,
    pub direct_addresses: BTreeSet<SocketAddr>,
}
```

- You'll interact with `NodeAddrs` a fair amount when working with iroh.
- When we call connect on an Endpoint, we need to pass either a `NodeAddr`, or something that can turn into a `NodeAddr`.
