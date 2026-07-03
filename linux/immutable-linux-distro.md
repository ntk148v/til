# The Immutable Linux Paradox

Source: <https://jnsgr.uk/2025/09/immutable-linux-paradox/>

[Ubuntu Core](https://ubuntu.com/core) has been at the forefront of this movement for IoT, appliances and edge deployments, with work ongoing to release a “Core Desktop” experience. Other projects such as [NixOS](https://nixos.org/), [Fedora Silverblue](https://fedoraproject.org/atomic-desktops/silverblue/) and [Red Hat image mode](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/introducing-image-mode-for-rhel_using-image-mode-for-rhel-to-build-deploy-and-manage-operating-systems) are gaining adoption, alongside more specialised immutable distributions such as SteamOS and Talos.

## 1. What is an immutable Linux distribution?

> [!IMPORTANT]
> The key principle of an immutable OS is that the core system is unchangeable at runtime.
> Every OS installation has at least one filesystem that stores system software, user software, and user data. Immutable OSes must cleanly separate “system” and “user” software and data, such that regular user interactions cannot compromise the integrity of the OS.

Immutable deployments are often separated into three layers:

- Base OS: immutable core, updated only through controllerd mechanisms.
- Applications: user applications, often delivered in containerised formats such as Snap, Flatpak, AppImageg, cpak.
- User data: writable
