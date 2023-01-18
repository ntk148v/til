# Software Defined Perimeter (SDP) protocol

Source:

- [SDP Specification 1.0 (Cloud Security Alliance)](https://downloads.cloudsecurityalliance.org/initiatives/sdp/Software_Defined_Perimeter.pdf)
- <https://www.cloudflare.com/learning/access-management/software-defined-perimeter/>

- [Software Defined Perimeter (SDP) protocol](#software-defined-perimeter-sdp-protocol)
  - [1. Introduction](#1-introduction)
  - [2. System Overview](#2-system-overview)
  - [3. SDP vs. VPN](#3-sdp-vs-vpn)

## 1. Introduction

- SDP is a way to hide Internet-connected infrastructure so that external parties and attackers cannot see it, whether it is hosted on-premise or in the cloud.
- The goal: to base the network perimeter on software instead of hardware.
- A software-defined perimeter forms a virtual boundary around company assets at the network layer, not the application layer.
- The protocol is divied into 2 sections:
  - The control plane describes how Initiating Hosts (IH) and Accepting Hosts (AH) communicate with the Controller.
  - The data plane describes how IHs communicate with AHs.
- Design objective: provide an interoperable security control for IPv4 and IPv6.

## 2. System Overview

- Concept: SDP aims to give application owners the ability to deploy perimeter functionality where needed in order to isolate services from unsecured networks.
- Architecture: SDP consists of 2 components:
  - SDP Hosts: initiate connections or accept connections -> interact with SDP Controllers via a secure control channel
    - Initiating SDP Hosts (IH): request a list of Accepting Hosts (AH) to which they can connect.
    - Accepting SDP Hosts (AH): rejects all communication from all hosts other than the SDP Controller. The AH accepts connections from an IH only after instructed to do so by the Controller.
  - SDP Controller: determines which SDP hosts can communicate with each other.

![](https://upload.wikimedia.org/wikipedia/commons/d/d3/Software_Defined_Perimeter_Architecture.png)

- With an SDP, it should not be technologically possible to connect with a server unless authorized to do so. SDPs allow access to users only after 1) verifying user identity, and 2) assessing the state of the device.
- Workflow:
  - SDP Controllers are brought online and connected to the appropriate optional authentication and authorization services.
  - SDP Hosts are brought online. These hosts connect to and authenticate to the Controllers. However, they do not acknowledge communication from any other Host and will not respond to any non-provisioned request.
  - Each Initiating Host that is brought online connects with, and authenticates to, the SDP Controllers.
  - After authenticating the Initiating SDP Host, the SDP Controllers determine a list of Accepting Hosts to which the Initiating Hosts is authorized to communicate.
  - The SDP Controller instructs the Accepting SDP Hosts to accept communication from the Initiating Hosts as well as any optional policies required for encrypted communications.
  - The Initiating SDP Host initiates a mutual VPN connection to all authorized Accepting Hosts.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Software_Defined_Perimeter_Workflow.png/310px-Software_Defined_Perimeter_Workflow.png)

- Implementations (Deployment Models):
  - Client-to-Gateway
  - Client-to-Server
  - Server-to-Server
  - Client-to-Server-to-Client
- Applications:
  - Enterprise application isolation
  - Private Cloud and Hybrid Cloud
  - Software as a Service
  - Infrastructure as a Service
  - Platform as a Service
  - Cloud-based VDI
  - Internet-of-things

## 3. SDP vs. VPN

- SDPs may incorporate VPNs into their architecture to create secure network connections between user devices and the servers they need to access.
- SDPs are very different from VPNs:
  - VPNs enable all connected users to access the entire network. SDPs don't share network connections.
  - SDPs may be asier to manage than VPNs, especially if internal users need multiple levels of access:
    - Managing several different levels of network access using VPNs involves deploying mutiple VPNs.
    - SDP: a separatet network connection is established for each user.
  - SDPs are location- and infrastructure-agnostic.
- An SDP is one way to implement Zero Trust security.
