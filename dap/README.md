# Debug Adapter Protocol (DAP)

## 1. What is DAP?

- It takes a significant effort to implement the UI for a new debugger for features. Typically this work must be repeated for each development tool, as each tool uses different APIs for implementing its user interface.

![](https://microsoft.github.io/debug-adapter-protocol/img/without-DAP.png)

- Standardize an abstract protocol for how a development tool communicates with concrete debuggers.
  - An intermediary component takes over the role of adapting an existing debugger or runtime API to the DAP.

![](https://microsoft.github.io/debug-adapter-protocol/img/with-DAP.png)

- Since DAP was designed for supporting the debugging UI in a language agnostic way, it is fairly high-level and does not have to surface all the fine details of the underlying language and low-level debugger API.

## 2. How it works?

- Please check [How it works section](https://microsoft.github.io/debug-adapter-protocol/overview).
