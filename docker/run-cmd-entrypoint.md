# Docker best practices: Choosing between RUN, CMD, and ENTRYPOINT

Source: <https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/>

## RUN

- The `RUN` instruction is used in Dockerfile to execute commands that build and configure the Docker image.
- Each `RUN` instruction creates a new layer in the Docker image.

## CMD

- The `CMD` instruction specifies the default command to run when a container is started from the Docker image.
- `CMD` is useful for setting default commands and easily overridden parameters.

## ENTRYPOINT

- The `ENTRYPOINT` instruction sets the default executable for the container. It is similar to CMD but is overridden by the command-line arguments passed to docker run. Instead, any command-line arguments are appended to the ENTRYPOINT command.
- Note: Use `ENTRYPOINT` when you need your container to always run the same base command, and you want to allow users to append additional commands at the end.

## Combining CMD and ENTRYPOINT

The `CMD` instruction can be used to provide default arguments to an `ENTRYPOINT` if it is specified in the exec form. This setup allows the entry point to be the main executable and CMD to specify additional arguments that can be overridden by the user.

```Dockerfile
ENTRYPOINT ["python", "/app/my_script.py"]
CMD ["--default-arg"]
```

```shell
docker run myimage --user-arg -> python /app/my_script.py --user-arg
```

| Command    | Description                                                                                                                                                                                  | Use Case |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| CMD        | Defines the default executable of a Docker image. It can be overridden by docker run arguments. Utility images allow users to pass different executables and arguments on the command line.  |
| ENTRYPOINT | Defines the default executable. It can be overridden by the “--entrypoint” docker run arguments. Images built for a specific purpose where overriding the default executable is not desired. |
| RUN        | Executes commands to build layers. Building an image                                                                                                                                         |

## What is PID 1 and why does it matter?

In Docker containers, the process that runs as PID 1 is crucial, because it is responsible for managing all other processes inside the container. Additionally, PID 1 is the process that reviews and handles signals from the Docker host.

When commands are executed in Docker using the **shell form**, a shell process (`/bin/sh -c`) typically becomes PID 1. Still, it does not properly handle these signals, potentially leading to unclean shutdowns of the container. In contrast, when using the **exec form**, the command runs directly as PID 1 without involving a shell, which allows it to receive and handle signals directly.

## Shell and exec form

In the previous examples, we used two ways to pass arguments to the RUN, CMD, and ENTRYPOINT instructions. These are referred to as shell form and exec form. **Note**: The key visual difference is that the exec form is passed as a comma-delimited array of commands and arguments with one argument/command per element. Conversely, shell form is expressed as a string combining commands and arguments.

| Form       | Description                                                  | Example                                             |
| ---------- | ------------------------------------------------------------ | --------------------------------------------------- |
| Shell Form | Takes the form of <INSTRUCTION> <COMMAND>.                   | `CMD echo TESTorENTRYPOINT echo TEST`               |
| Exec Form  | Takes the form of <INSTRUCTION> ["EXECUTABLE", "PARAMETER"]. | `CMD ["echo", "TEST"]orENTRYPOINT ["echo", "TEST"]` |

```Dockerfile
# Shell form, useful for complex scripting
RUN apt-get update && apt-get install -y nginx

# Exec form, for direct command execution
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "nginx"]
```

```Dockerfile
# ENTRYPOINT with exec form for direct process control
ENTRYPOINT ["httpd"]

# CMD provides default parameters, can be overridden at runtime
CMD ["-D", "FOREGROUND"]
```

## Key differences between shell and exec

<figure class="wp-block-table"><table><tbody><tr><td></td><td><strong>Shell Form</strong></td><td><strong>Exec Form</strong></td></tr><tr><td><strong>Form</strong></td><td>Commands without <code>[]</code> brackets. Run by the container’s shell, e.g., <code>/bin/sh -c</code>.</td><td>Commands with <code>[]</code> brackets. Run directly, not through a shell.</td></tr><tr><td><strong>Variable Substitution</strong></td><td>Inherits environment variables from the shell, such as <code>$HOME</code> and <code>$PATH</code>.</td><td>Does not inherit shell environment variables but behaves the same for <code>ENV</code> instruction variables.</td></tr><tr><td><strong>Shell Features</strong></td><td>Supports sub-commands, piping output, chaining commands, I/O redirection, etc.</td><td>Does not support shell features.</td></tr><tr><td><strong>Signal Trapping &amp; Forwarding</strong></td><td>Most shells do not forward process signals to child processes.</td><td>Directly traps and forwards signals like <code>SIGINT</code>.</td></tr><tr><td><strong>Usage with ENTRYPOINT</strong></td><td>Can cause issues with signal forwarding.</td><td>Recommended due to better signal handling.</td></tr><tr><td><strong>CMD as ENTRYPOINT Parameters</strong></td><td>Not possible with the shell form.</td><td>If the first item in the array is not a command, all items are used as parameters for the <code>ENTRYPOINT</code>.</td></tr></tbody></table></figure>

## Decision Tree

- A decision tree for using RUN, CMD, and ENTRYPOINT in building a Dockerfile.

![](https://www.docker.com/wp-content/uploads/2024/07/2400x1260_run-cmd-entrypoint-980x515.png)

- A decision tree to help determine when to use exec form or shell form.

![](https://www.docker.com/wp-content/uploads/2024/07/2400x1260_decision-tree-exec-vs-shell-980x515.png)
