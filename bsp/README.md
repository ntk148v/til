# Build Server Protocol (BSP)

Source: <https://build-server-protocol.github.io/>

- Protocol for IDEs and build tools to communicate about compile, run, test, debug and more.
- Problem that BSP solves: The BSP defines common functionality that both build tools (servers) and IDEs (client) understand, to reduce the effort required by tooling developers to integrate between available IDEs and build tools.
- It takes inspiration from the LSP, and can be used together with LSP in the same architecture.

![](https://i.imgur.com/q4KEas9.png)

- BSP can also be used without LSP. In the example above, IntelliJ acts as a BSP client even if IntelliJ does not use LSP.
- BSP is not an approved standard. The creation of BSP clients and servers is under active development.
