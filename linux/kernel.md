# Kernel

Source: <https://serversfor.dev/linux-inside-out/the-linux-kernel-is-just-a-program/>

## 1. What is a kernel?

Computers are built from CPUs, memory, and other devices, like video cards, network cards, keyboards, displays, and a lot of other stuff.

These devices can be manufactured by different companies, have different capabilities, and can be programmed differently.

An operating system kernel provides an abstraction to use these devices and resources conveniently and securely. Without one, writing programs would be much more difficult. We would need to write the low-level code to use every device that our program needs, and it’s likely that it wouldn’t work on other computers.

A kernel

- gives us APIs to interact with the hardware over a unified interface
- manages how programs can use the computer’s CPU, memory and other resources
- provides access control over what resources can a program access
  provides additional features like firewalls, file systems, mechanisms for programs to communicate, etc.

## 2. Where is the kernel?

```shell
ls -l /boot

System.map-6.12.43+deb13-amd64
System.map-6.12.48+deb13-amd64
config-6.12.43+deb13-amd64
config-6.12.48+deb13-amd64
efi
grub
initrd.img-6.12.43+deb13-amd64
initrd.img-6.12.48+deb13-amd64
vmlinuz-6.12.43+deb13-amd64
vmlinuz-6.12.48+deb13-amd64
```

This single file `vmlinuz-6.12.48+deb13-amd64` is the kernel:

- `vmlinuz`: vm for virtual memory, linux, and z indicating compression.
- `6.12.48+deb13`: this is the kernel version, and the distribution (Debian 13)
- `amd64`: this is the architecture of our system

## 3. How system calls actually work?

Modern CPUs have different execution modes:

- **User mode (restricted)**: Where your programs run. They have limited access to memory and some CPU instructions. It is a sandboxed mode.
- **Kernel mode (privileged)**: Where the kernel runs. It has total access to all memory and all hardware instructions.

When a program wants to perform an operation that needs elevated privileges, it puts the system call number and arguments into the CPU registers (these are small memory banks built into the processor) and executes a built-in CPU instruction (on x86_64 architecture this is `SYSCALL`).

This instruction causes the CPU to instantly switch from user mode to kernel mode. The program stops here and control is handed over to the kernel.

The kernel looks at the registers, sees what the program wants to perform, checks if it is allowed to, and then performs the action.

The kernel puts the result back into a register and switches the CPU back to user mode. The program resumes its normal operation.
