# Everyone run as root

Every proces in Kubernetes runs with a specific User ID. UID 0 is special, and dangerous

Linux assigns numeric IDs to processes:

- UID 0 = root (unrestricted access)
- UIDs 1-999 = system services
- UIDs 1000+ = regular users

Containers default to root. This isn't a bug - it's inherited from Docker's design choices. Convenient for development unnecessary risk in production.

User namespaces provide isolation, allow UID mapping:

- Process runs as UID 0 inside container.
- Maps to UID 100000 on host.

But most runtimes don't enable mapping. Root inside container = root on host for any resources the container can access.

On Kubernetes, security context fixes this. Kubernetes Security Context provides the controls:

- runAsUser: set specific UID.
- runAsNonRoot: enforce non-root execution.
