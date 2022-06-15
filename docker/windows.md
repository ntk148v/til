# Container platform tools on Windows

## 1. Windows and Linux container platform

- In Linux, container management tools like Docker are built on a more granlar set of container tools: runc and containerd.

![](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/media/docker-on-linux.png)

- On Windows, Host Compute Service (HCS). Docker still calls directly into the GCS. Going forward, however, container management tools exapnding to include Windows containers and the Windows container host could call into containerd and runhcs the way they call on containerd and runc.

![](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/media/hcs.png)

## 2. Can Windows containers be hosted on Linux?

Source: <https://stackoverflow.com/questions/42158596/can-windows-containers-be-hosted-on-linux>

- You can run Linux containers on Windows host (WSL2, Hyper-V).
