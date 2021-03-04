# Linux network namespace

## 1. What is network namespace?

An installation of Linux shares a single set of network interfaces and routing table entries. With network namespaces, you can have different and separate instances of network interfaces and routing tables that operate independent of each other.

## 2. Play with network namespace

> Ubuntu 20.04

```bash
# Create network namespace
ip netns add blue
# List network namespaces
ip netns list
# Assign interfaces to network namespaces
# Create the veth pair
ip link add veth0 type veth peer name veth1
# Verify the veth pair was created
ip link list
# Move veth1 to the blue namespace
ip link set veth1 netns blue
# Run ip link list (global namespace), veth1 has disappeared
ip link list
# Run ip link list in the blue namespace
# ip netns exec <network namespace> <command to run against that namespace>
ip netns exec blue ip link list
# Configure interface in blue namespace
ip netns exec blue ip addr add 10.1.1.1/24 dev veth1
ip netns exec blue ip link set dev veth1 up
ip netns exec blue ip a
# Delete
ip netns delete blue
```
