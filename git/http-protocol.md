# Git HTTP protocol

Source: <https://git-scm.com/docs/protocol-v2>

- Packet-line framing.
- Init client request
  - Client sends request to get the list of refs that server has for that repository.

  ```shell
  C: GET /<user>/<repo>/info/refs?service=git-upload-pack HTTP/1.1

  C: Header: Git-Protocol: version=2
  ```

  - Server returns the capability advertisement.

  ```shell
  S: 200 OK
  S: <Some headers>
  S: ...
  S:
  S: 000eversion 2\n
  S: <capability-advertisement>
  ```

- Capability advertisement:
  - A server which decides to communicate (based on a request from a client) using protocol version 2, notifies the client by sending a version string followed by an advertisement of its capabilities.
  - Each capability is a key with an optional value. Some capabilities will describe commands which can be requested to be executed by the client.

  ```shell
  capability-advertisement = protocol-version
        capability-list
        flush-pkt
  ```

- Command request:
  - A client can then issue a request to select the command it wants with any particular capabilities or argument.
  - Only a single command can be request at a time.

  ```shell
  request = empty-request | command-request
  empty-request = flush-pkt
  command-request = command
      capability-list
      delim-pkt
      command-args
      flush-pkt
  command = PKT-LINE("command=" key LF)
  command-args = *command-specific-arg
  ```

  - The server will then check to ensure the client's request is comprised of a valid command as well as capabilities which were advertised -> execute command.
  - The client has received the entire response from the server -> execute another command or terminate the connection.

- Capabilities: Two different types of capabilities:
  - Normal capabilities: can be used to convey information, or alter the behavior of a request.
  - Commands: the core action that a client wants to perform.
  - List of capabilities: check [git's doc](https://git-scm.com/docs/protocol-v2).

## Git clone

- Client sends a POST message with the list of object that it has, and the list of object that it wants.

```rest
POST /<user>/<repo>/git-upload-pack

Header: Git-Protocol: version=2
Header: Content-Type: application/x-git-upload-request
Header: Accept: application/x-git-upload-request
```

- Client sends a POST message with the list of object that it has, and the list of object that it wants.

```rest
POST /<user>/<repo>/git-upload-pack

Header: Git-Protocol: version=2
Header: Content-Type: application/x-git-upload-request
Header: Accept: application/x-git-upload-request
```
