# Linux SO_REUSEPORT

Source: <https://www.muppetwhore.net/ljarchive/LJ/298/12538.html>

![](https://www.muppetwhore.net/ljarchive/LJ/298/12538c.jpg)

> Improve your server performance using a relatively new feature of the Linux networking stasck the `SO_REUSEPORT` socket option.

## 1. TCP connection and socket basics

- A TCP connection is defined by a unique 5-tuple:

```
[Protocol, Source IP Address, Source Port, Destination IP Address, Destination Port]
```

- TCP state:

![](https://upload.wikimedia.org/wikipedia/en/5/57/Tcp_state_diagram.png?20080306050740)

- Client application:
  - Protocol: created based on parameters provided by the application. The protocol is always TCP in this article.
  - Source IP Address and Port: usually set by the kernel when the applications call `connect()` without a prior invocation to `bind()`. The kernel picks a suitable IP address for communicating with the destination server and a source port from the ephemeral port range (`net.ipv4.ip_local_port_range`).
  - Destination IP Address and Port: set by the application by invoking `connect()`.
- Server application:
  - Protocol: TCP
  - Source IP Address and Port: set by the application when invokes `bind()`.
  - Destination IP Address and Port: a client connects to a server by completing the TCP 3-way handshake. The server's TCP/IP stack creates a new socket to track the client connection and sets its SourceIP:Port and DestinationIP:Port from the incoming client connection parameters. The new socket is transitioned to the `ESTABLISHED` state, while the server's `LISTEN` socket is left unmodifed returns with a reference to the newly `ESTABLISHED` socket.
- `TIME_WAIT` sockets: is created when an application closes its end of a TCP connection first. The socket state changes `ESTABLISHED -> FIN_WAIT -> FIN_WAIT2 -> TIME_WAIT`, before the socket is closed.
- The different states of a server socket. A server typically executes the following system calls at start up:

```shell
# Create a socket
server_fd = socket(...);
# Bind to a well known IP address and port number
ret = bind(server_fd, ...);
# Mark the socket as passive by changing its state to LISTEN
ret = listen(server_fd, ...);
# Wait for a client to connect and get a reference file descriptor
# After the client completes the TCP 3-way handshake, the kernel creates
# a second socket and returns a reference to server socket.
client_fd = accept(server_fd, ...);
```

## 2. The SO_REUSEADDR socket option

- When the server is restarted and invokes `bind()` on a socket with `SO_REUSEADDR` set, the kernel ignores all non-`LISTEN` sockets bound to the same IP:port combination.

## 3. The SO_REUSEPORT socket option

- While `SO_REUSEADDR` allows sockets to `bind()` to the same IP:port combination when existing `ESTABLISHED` or `TIME_WAIT` sockets may be present, `SO_REUSEPORT` allows binding to the same IP:port combination when existing `LISTEN` sockets also may be present -> permits a server process to be invokes multiple times, allowing many processes to listen for connections.
- When multiple sockets are in the `LISTEN` state, how does the kernel decide which socket, and thus, which application process - receives an incoming connection?
  - Look up a hash table by hashing the client IP:port and server IP:port values. This method provides a good distribution of connections among different `LISTEN` socketst .
