# Linux Enforcement & Auditing tools

With Golang demonstration

## Introduction

**Enforcement tools** use the policy to change behavior of a process by preventing system calls from succeeding, or in the some cases, killing the process. Seccomp, seccomp-bpf, SELinux, and AppArmor are examples of enforcement tools.

**Auditing tools** use the policy to monitor the behavior of a process and notify when its behavior steps outside the policy. Auditd and Falco are examples of auditing tools.

## seccomp

### Overview

The goal of sandboxing is to reduce the potential attack surface by reducing the actions that a process can perform.

[Seccomp](https://en.wikipedia.org/wiki/Seccomp) is a mechanism in the Linux kernel that allows a process to make a one-way transition to a restricted state where it can only perform a limited set of system calls. If a process attempts any other system calls, it is killed via a `SIGKILL` signal.

### Demonstration

```go
// Example in https://sysdig.com/blog/selinux-seccomp-falco-technical-discussion/
// Convert from C to Golang
package main

import (
 "fmt"
 "os"

 "golang.org/x/sys/unix"
)

func main() {
 f, err := os.OpenFile("output.txt", os.O_WRONLY, 0644)
 if err != nil {
  fmt.Println(err)
  return
 }
 defer f.Close()

 fmt.Println("Calling prctl() to send seccomp strict mode...")
 if err = unix.Prctl(unix.PR_SET_SECCOMP, unix.SECCOMP_MODE_STRICT, 0, 0, 0); err != nil {
  fmt.Println(err)
  return
 }

 fmt.Println("Writing to an already open file...")
 if _, err = f.WriteString("test"); err != nil {
  fmt.Println(err)
  return
 }

 fmt.Println("Trying to open file for reading...")
 f, err = os.OpenFile("output.txt", os.O_RDONLY, 0644)
 if err != nil {
  fmt.Println(err)
  return
 }
 fmt.Println("You will not see this message. The process will be killed first")
}
```

## seccomp-bpf

### Overview

Although restrictive and undoubtedly very secure, seccomp’s strict mode is…strict. You can’t do much other than read/write to already open files. What if you want to combine application with flexible policies or per-application profiles to allow for a limited richer set of actions?

[seccomp-bpf](https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt) is an extension to seccomp that allows specifying a filter that is applied to every system call. The filter is written using [BPF](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter). The BPF program loaded into the kernel starts with a system call + arguments and results in a filtering decision. Based on the results of the filter, the system call can be allowed, blocked, or the process can be killed.

### Demonstration

A Go program to create a folder named `moo` in `/tmp`.

1. First check if the local system supports seccomp and has the required dependencies for `libseccomp-golang`. You should get the following returned:

```bash
~ grep CONFIG_SECCOMP /boot/config-$(uname -r)
CONFIG_SECCOMP=y
CONFIG_SECCOMP_FILTER=y
```

2. Ensure that `libseccomp-dev` installed on local system

```bash
~ sudo apt install libseccomp-dev
```

3. The basic program:

```go
package main

import (
 "fmt"
 "syscall"
)

func main() {
 err := syscall.Mkdir("/tmp/moo", 0755)
 if err != nil {
  panic(err)
 } else {
  fmt.Println("I just created a folder")
 }
}
```

```bash
github.com/ntk148v/testing/golang/seccomp-bpf  master ⇡$? via 🐹 v1.12.7 took 43s go build -o basic-make-a-folder
```

```bash
github.com/ntk148v/testing/golang/seccomp-bpf  master ⇡$? via 🐹 v1.12.7 strace -c ./basic-make-a-folder
I just created a folder
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
  0.00    0.000000           0         1           write
  0.00    0.000000           0         8           mmap
  0.00    0.000000           0       114           rt_sigaction
  0.00    0.000000           0         8           rt_sigprocmask
  0.00    0.000000           0         3           clone
  0.00    0.000000           0         1           execve
  0.00    0.000000           0         3           fcntl
  0.00    0.000000           0         2           sigaltstack
  0.00    0.000000           0         1           arch_prctl
  0.00    0.000000           0         1           gettid
  0.00    0.000000           0         3           futex
  0.00    0.000000           0         1           sched_getaffinity
  0.00    0.000000           0         1           mkdirat
  0.00    0.000000           0         1           readlinkat
------ ----------- ----------- --------- --------- ----------------
100.00    0.000000                   148           total
```

3. Achieve the goal of limiting the syscalls available.

```go
// Implements seccomp filters using a whitelist approach.
package main

import (
 "fmt"
 "syscall"

 libseccomp "github.com/seccomp/libseccomp-golang"
)

// whitelist - syscalls contains the names of the syscalls
// that we want to our process to have access to.
func whiteList(syscalls []string) {
 // Apply a "deny all" filter
 filter, err := libseccomp.NewFilter(libseccomp.ActErrno.SetReturnCode(int16(syscall.EPERM)))
 if err != nil {
  fmt.Printf("Error creating filter: %s\n", err)
 }
 // Add elements to whitelist
 for _, element := range syscalls {
  fmt.Printf("[+] Whitelisting: %s\n", element)
  syscallID, err := libseccomp.GetSyscallFromName(element)
  if err != nil {
   panic(err)
  }
  filter.AddRule(syscallID, libseccomp.ActAllow)
 }
 // Load the filter which applies the filter we just created
 filter.Load()
}

func main() {
 // A string array contains the names of syscalls extracted
 // from `strace` output.
 var syscalls = []string{
  "write", "mmap", "rt_sigaction", "rt_sigprocmask",
  "clone", "execve", "fcntl", "sigaltstack", "arch_prctl",
  "gettid", "gettid", "futex", "sched_getaffinity",
  "mkdirat", "readlinkat", "exit_group",
 }

 whiteList(syscalls)

 err := syscall.Mkdir("/tmp/moo", 0755)
 if err != nil {
  panic(err)
 } else {
  fmt.Println("I just created a folder")
 }
}
```

```bash
github.com/ntk148v/testing/golang/seccomp-bpf  master ⇡$? via 🐹 v1.12.7 go run main.go
[+] Whitelisting: write
[+] Whitelisting: mmap
[+] Whitelisting: rt_sigaction
[+] Whitelisting: rt_sigprocmask
[+] Whitelisting: clone
[+] Whitelisting: execve
[+] Whitelisting: fcntl
[+] Whitelisting: sigaltstack
[+] Whitelisting: arch_prctl
[+] Whitelisting: gettid
[+] Whitelisting: gettid
[+] Whitelisting: futex
[+] Whitelisting: sched_getaffinity
[+] Whitelisting: mkdirat
[+] Whitelisting: readlinkat
[+] Whitelisting: exit_group
I just created a folder
```

3. Syscall blocking action: Try to remove the created folder in the end.

```go
    ...
    // Create folder source
    ....
    // Attempt to execute a shell command
 // Force remove the /tmp/moo first
 err = syscall.Rmdir("/tmp/moo")
 if err != nil {
  panic(err)
 } else {
  fmt.Println("I just removed a folder")
 }
```

```bash
github.com/ntk148v/testing/golang/seccomp-bpf  master ⇡$? via 🐹 v1.12.7 go run main.go
[+] Whitelisting: write
[+] Whitelisting: mmap
[+] Whitelisting: rt_sigaction
[+] Whitelisting: rt_sigprocmask
[+] Whitelisting: clone
[+] Whitelisting: execve
[+] Whitelisting: fcntl
[+] Whitelisting: sigaltstack
[+] Whitelisting: arch_prctl
[+] Whitelisting: gettid
[+] Whitelisting: gettid
[+] Whitelisting: futex
[+] Whitelisting: sched_getaffinity
[+] Whitelisting: mkdirat
[+] Whitelisting: readlinkat
[+] Whitelisting: exit_group
I just created a folder
panic: operation not permitted

goroutine 1 [running]:
main.main()
 /home/kiennt/Workspace/github.com/ntk148v/testing/golang/seccomp-bpf/main.go:53 +0x172
exit status 2
```

## Resources

1. Sysdig: <https://sysdig.com/blog/selinux-seccomp-falco-technical-discussion/>
2. Heroku: <https://blog.heroku.com/applying-seccomp-filters-on-go-binaries>
