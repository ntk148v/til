# Exit codes in Container and Kubernetes

Source: <https://komodor.com/learn/exit-codes-in-containers-and-kubernetes-the-complete-guide/>

## 1. What are Container Exit Codes?

- Exit codes are used by container engines, when a container terminates, to report why it was terminated.
- The most common exit codes used by containers are:

| Code | Name                            | What is means                                                                                                      |
| ---- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 0    | Purposely stopped               | Used by developers to indicate that the container was automatically stopped                                        |
| 1    | Application error               | Container was stopped due to application error orincorrect reference in the image specification                    |
| 125  | Container failed to run error   | The docker run command did not execute successfully                                                                |
| 126  | Command invoke error            | A command specified in the image specification could not be invoked                                                |
| 127  | File or directory not found     | File or directory specified in the image specification was not found                                               |
| 128  | Invalid argument used on exit   | Exit was triggered with an invalid exit code (not in range 0-255)                                                  |
| 134  | Abnormal termination (SIGABRT)  | The container aborted itself using the abort() function                                                            |
| 137  | Immediate termination (SIGKILL) | Container was immediately terminated by the operating system via SIGKILL signal                                    |
| 139  | Segmentation fault (SIGSEGV)    | Container attempted to access memory that was not assigned to it and was terminated                                |
| 143  | Graceful termination (SIGTERM)  | Container received warning that it was about to be terminated, then terminated                                     |
| 255  | Exit status out of range        | Container exited, returning an exit code outside the acceptable range, meaning the cause of the error is not known |

## 2. Understand and know what to do

1. Identify the Exit Code and understand.
2. Check the container logs (mostly) for new information.
3. Further checking

### 2.1. Exit Code 0

- Exit Code 0 means that the foreground process is not attached to a specific container.
- What to do?
  - Check the container logs to identify which library caused the container to exit
  - Review the code of the existing library and identify why it triggered Exit Code 0, and whether it is functioning correctly

### 2.2. Exit Code 1

- Exit Code 1 indicates that the container was stopped due to one of the following:
  - An application error: could be a simple programming error in code run by the container, such as "divide error",...
  - An invalid reference: this means the image specification refers to a file that does not exist in the container image.
- What to do?
  - Check the container logs to see if one of the files listed in the image specification could not be found.
  - If you can't find an incorrect file reference, check the container logs for an application error, and debug the library that caused the error.

### 2.3. Exit Code 125

- Common reasons:
  - An undefined flag was used in the command.
  - The user-defined in the image specification does not have sufficient permissions on the machine.
  - Incompatibility between the container engine and the host operating systems or hardware.
- What to do?
  - Check if the command used to run the container uses the proper syntax.
  - Check if the user running the container, or the context in which the command is executed in the image specification, has sufficient permissions to create containers on the host
  - If your container engine provides other options for running a container, try them. For example, in Docker, try docker start instead of docker run
  - Test if you are able to run other containers on the host using the same username or context. If not, reinstall the container engine, or resolve the underlying compatibility issue between the container engine and the host setup

### 2.4. Exit Code 126

- Common reasons: a missing dependency or an error in a continuous integration script used to run in the container.
- What to do?
  - Check the container logs to see which command could not be invoked
  - Try running the container specification without the command to ensure you isolate the problem
  - Troubleshoot the command to ensure you are using the correct syntax and all dependencies are available
  - Correct the container specification and retry running the container

### 2.5. Exit Code 127

- What to do? Same as Exit Code 126, identify the failing command and make sure you reference a valid filename and file path available within the container image.

### 2.6. Exit Code 128

- It means that code within the container triggered an exit command, but didn't provide a valid exit code. The Linux exit command only allows integers between 0-255, so if the process was exited with, for example, exit code 3.5, the logs will report Exit Code 128.
- What to do?
  - Check the container logs.
  - Identify where the offending library uses the `exit` command, and correct it to provide a valid exit code.

### 2.7. Exit Code 134 (SIGABRT)

- It means that the container abnormally terminated itself, closed the process and flushed open streams.
- What to do?
  - Check container logs.
  - Check if process abortion was planned, and if not, troubleshoot the library and modify it to avoid aborting the container.

### 2.8. Exit Code 137 (SIGKILL)

- It means the container has received a SIGKILL signal from the host OS.
- Common reasons:
  - Triggered when a container is killed via the container engine, for example `docker kill`.
  - Triggered by a Linux user sending a `kill -9` command to the process.
  - Triggered by Kubernetes after attempting to terminate a container and waiting for a grace period of 30 seconds.
  - Triggered automatically by the host, usually due to running OOM -> `docker inspect` - `OOMKilled`.
- What to do?
  - Check logs on the host to see what happened prior to the container terminating, and whether it previously received a SIGTERM signal (graceful termination) before receiving SIGKILL
  - If there was a prior SIGTERM signal, check if your container process handles SIGTERM and is able to gracefully terminate
  - If there was no SIGTERM and the container reported an OOMKilled error, troubleshoot memory issues on the host

### 2.9. Exit Code 139 (SIGSEGV)

- It means that the container received a SIGSEGV signal from the OS, Segmentation Error - a memory violation, caused by a container trying to access a memory location.
  - Code error.
  - Incompatibility between binaries and libraries.
  - Hardware incompatibility or misconfiguration.
- What to do?
  - Check if the container process handles SIGSEGV -> collect and report a stack trace.
  - If you need to further troubleshoot SIGSEGV, you may need to be set the OS to allow programs to run even after a segmentation fault occurs, to allow for investigation and debugging.
  - Check memory subsystems on the host and troubleshoot memory configuration.

### 2.10. Exit Code 143 (SIGTERM)

- It means that the container received a SIGTERM signal from the operating system, which asks the container to gracefully terminate, and the container succeeded in gracefully terminating (otherwise you will see Exit Code 137).
- What to do?
  - Check host logs to see the context in which the OS sent the SIGTERM signal (`kubelet logs`).
  - In general, Exit Code 143 doesn't require troubleshooting.

### 2.11. Exit Code 255

- It implies the main entrypoint of a container stopped with that status. It means that the container stopped, but it isn't known for what reason.
- What to do?
  - If the container is running in a VM, first try removing overlay networks configured on the VM and recreating them.
  - Try deleting and recreating the VM, then rerunning the container on it.
  - Failing the above, bash into the container and examine logs or other clues about the entrypoint process and why it is failing.

## 3. Which Kubernetes Errors are related to Container Exit Codes?

- Use `kubectl describe pod <name>`.
- Use the Exit Code provide by `kubectl` to troubleshoot the issue:
  - If the Exit Code is 0 – the container exited normally, no troubleshooting is required
  - If the Exit Code is between1-128 – the container terminated due to an internal error, such as a missing or invalid command in the image specification
  - If the Exit Code is between 129-255 – the container was stopped as the result of an operating signal, such as SIGKILL or SIGINT
  - If the Exit Code was exit(-1) or another value outside the 0-255 range, kubectl translates it to a value within the 0-255 range.
