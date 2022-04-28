# Analyzing Network Protocols with Wireshark

> Quick note to Pluralsight's course, not a complete guide.

## 1. Using Wireshark to analyze ARP

- IPv6 does not use ARP. It uses a function called neighbor discovery which essentially takes the place of the ARP function in its operation.
- Check ARP protocol if you see:
  - Problems connecting  to an application
  - Intermittent connectivity
  - Unicast flooding
- ARP requests are broadcasted while responses are unicasted.

## 2. Using Wireshark to analyze IPv4, IPv6, and ICMP

- IPv4 protocol:
- TTL: as that packet travels through a network, each router will  decrement this value by 1. If this value ever goes down to 0 or expires, the router will drop the packet and reply with an ICMP message indicating that the TTL was exceeded -> useful to determine how many router hops away a station is (255, 128, 64)
- ICMP protocol:
  - ICMP types: 0 = Echo reply, 3 = Destination unreachable, 5 = Redirect, 8 = Echo request, 11 = Time to live exceeded
  - ICMP codes: 0 = Network unreachable, 1 = Host unreachable, 3 = Port unreachable, 4 = Fragmentation needed
- IPv6 protocol:
  - 8 blocks: A unique network identifier, subnet ID, Host/Interface
  - Link local address range: `fe80::/64`
  - Global address range: `2000::/3`
  - Unique local address range: `fc00::/7`

## 3. Using Wireshark to analyze Core Services - UDP, DHCP, and DNS

- UDP:
  - No connection necessary
  - TIme sensitive applications
  - Simple - no options
- DHCP:
  - Discover (Broadcast) -> Offer (Broadcast) -> Request (Broadcast) -> Ack
- DNS:

## 4. Using Wireshark to analyze Core Applicataions - FTP, HTTPs, and SSL

- FTP:
  - Simple File Transfer
  - FTP Client or built-in browser
  - Not a secure protocol (clear text on wire)
  - sFTP: secure FTP -> add a layer of transport security - SSH
  - TFTP: trivial FTP - used within LAN over UDP -> configurations files to network devices
- HTTPs and TLS:
