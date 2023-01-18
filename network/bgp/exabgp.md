# ExaBGP

Source:

- <https://github.com/Exa-Networks/exabgp>
- <https://www.trex.fi/2016/exabgp-trex.pdf>
- <https://thepacketgeek.com/exabgp/getting-started/>
- <https://hackmd.io/@dch/B1io2ldAX?type=view>
- <https://vincent.bernat.ch/en/blog/2013-exabgp-highavailability>

## Introduction

- A highly flexible BGP speaker that allows you to control BGP announcements programmtically.
- It can also receive BGP updates from peers and feed those to your application in parsed form.
- Takes care of all the details running BGP State Machine, keepalives and protocol encoding.
- Supports IPv4/IPv6, L2VPN, L3VPN,...
- ExaBGP should not be compared to Quagga or BIRD as ExaBGP does not interact with the operating system to apply any announcements to the routing table.
- Example:
  - Integration is done by configuring your application in ExaBGP's configuration file
  - ExaBGP starts your app as a subprocess
  - UnixPipes are used to do IO (The API works by reading `STDOUT` from your process and sending your process information through `STDIN`)
  - You can announce/withdraw routes, add/remove neighbors,...
