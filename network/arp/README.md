# ARP

## Introduction

- Address Resolution Protocol (ARP) is used to translate an IPv4 address into a MAC address, allowing Layer 2 communications to occur.
- When a source host has to send an IPv4 packet to a destination host on the same subnet, it executes an ARP request to get the MAC address of the destination host.
- The source host will send an ARP request to the Ethernet broadcast address ff:ff:ff:ff:ff:ff. All of the host on the subnet will receive the ARP request that was broadcasted, but, only the destination host will answer to the ARP request with the MAC address associated with its IPv4 address.

![](https://netbeez.net/wp-content/uploads/2018/01/84-How-ARP-works-in-Linux-systems-Images.002.jpeg)

- Once the source has obtained the destination MAC address from the destination host, it encapsulates the IPv4 packet into a Layer 2 frame, and sends it to the destination host.

![](https://netbeez.net/wp-content/uploads/2018/01/84-How-ARP-works-in-Linux-systems-Images.001-2.jpeg)
