# Pipes

Source:

- <https://www.baeldung.com/linux/anonymous-named-pipes>

## 1. Overview

- A pipe is an important mechanism in Unix-based systems that allows us to communicate data from one process to another without storing anything on the disk
- Two types of pipes:
  - pipes (anonymous or unnamed pipes)
  - FIFO (named pipes)

## 2. Anonymous pipes

- Often referred to as a pipeline.
- The shell executes each command in a separate process running in the background, starting with the far left command. Then, the standard output of the command in the left side is connected to be the command's standard input on the right side.
- This mechanism lasts unitl all of the processes in the pipeline have been completed.
- Example:

```bash
$ netstat -tlpn | grep 127.0.0.1
(Not all processes could be identified, non-owned process info
will not be shown, you would have to be root to see it all.)
tcp 0 0 127.0.0.1:3306 0.0.0.0:* LISTEN -
# \& to refer to a pipeline, connecting both the standard output and the standard error of
# the command on the left side with the standard input of the command on the right side
# Supresses it the warning message
$ netstat -tlpn |& grep 127.0.0.1
tcp 0 0 127.0.0.1:3306 0.0.0.0:* LISTEN -
```

- Pipelines in Bash.

  - Bash has a variable called `PIPESTATUS`, which contains a list of exit staus from the processes in the most recently executed pipeline

    ```bash
    $ exit 1 | exit 2 | exit 3 | exit 4 | exit 5
    $ echo ${PIPESTATUS[@]}
    1 2 3 4 5
    ```

  - The return status of the execution of the whole pipeline will depend on the `pipefail` variable's status. If this variable is set, the return status of the pipeline will be the exit status of the rightmost command with a non-zero status or will be zero if all commands exit successfully. With the `pipefail` disabled, the return status of the pipe will be the exit status of the last command

    ```bash
    $ set -o pipefail
    $ exit 1 | exit 2 | exit 3| exit 4 | exit 0
    $ echo $?
    4
    $ set +o pipefail
    $ exit 1 | exit 2 | exit 3| exit 4 | exit 0
    $ echo $?
    0
    ```

- Pipeline in Zsh: similar but with a few differences. For example, Zsh has the `pipestatus` command. Zsh executes the commands in each pipeline in separate processes, except for the last command which is executed in the current shell environment.
- Using an anonymous pipe depends on the characteristics we've looking for. Some of them can be persistence, two-way communication, having a filename, creating a fileter, and restricting access permissions among others.

## 3. Named pipes

- FIFO - named pipes, is a special file similar to a pipe but with a name on the filesystem. Multiple processes can access this special file for reading and writing like any ordinary file.
- The name works only as a reference point for processes that need to use a name in the filesystem.
- Provides bidirectional communication.
- In Linux, create FIFO with `mknod` and `mkfifo`:

```bash
$ mkfifo pipe1
# Type 'p' - create a FIFO
$ mknod pipe2 p
$ ls -l
prw-r--r-- 1 kiennt kiennt 0 Feb 10 14:45 pipe1
prw-r--r-- 1 kiennt kiennt 0 Feb 10 14:45 pipe2
```

```bash
# 1st terminal
$ ls > pipe1
# 2nd terminal
$ cat < pipe1
# Set custom access permissions
$ mkfifo pipe3 -m 700
$ ls -l
pr-x------ 1 kiennt kiennt 0 Feb 10 14:45 pipe3
```

- Advanced example:

```bash
# From: https://en.wikipedia.org/wiki/Netcat
# Starts a nc server on port 12345 and all the connections get redirected to google.com:80
# Request -> nc -> google. But no response will not be sent back.
$ nc -l 12345 | nc www.google.com 80
# Bidirectional
$ mkfifo backpipe
$ nc -l 12345  0<backpipe | nc www.google.com 80 1>backpipe
```

- If we need a filename and we don't want to store data on the disk, what we're looking for is a FIFO. If we only need a name as a reference, with content that comes directly from another process.
