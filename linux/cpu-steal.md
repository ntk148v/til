# CPU Steal Time

```
Steal time is the percentage of time a virtual CPU waits for a real CPU while the hypervisor is servicing another virtual processor.
```

- Use `top` command, if your VM displays a high %st in top (steal time), this means CPU cycles are being taken away from your VM to serve other purposes.

```bash
top
```

- Rule of thumb: **if steal time is greater than 10% for 20 minutes, the VM is likely in a state that it is running slower than it should**. When this happens:
  - Shut down the instance and move it to another physical server.
  - If steal time remains high, increase the CPU resources.
