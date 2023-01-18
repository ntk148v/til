# Border Gateway Protocol (BGP)

Source:

- <https://tools.ietf.org/html/rfc4271>
- <https://en.wikipedia.org/wiki/Border_Gateway_Protocol>
- <https://www.cloudflare.com/learning/security/glossary/what-is-bgp/>

- **BGP** is a standardized exterior gateway protocol designed to exchange routing and reachability information among autonomous systems (AS) on the Internet. BGP is classified as a path-vector routing protocol, and it makes routing decisions based on paths, network policies, or rule-sets configured by a network administrator.
  - Postal service of the Internet.
  - When someone submits data via the internet, BGP is responsible for looking at all of the available paths that data could travel and picking the best route, which usually means hopping between autonomous systems.
- **Autonomous system** (Post office branch).

![](https://www.cloudflare.com/img/learning/security/glossary/what-is-bgp/network-of-networks.svg)

- Use BGP routing to get the transimissions to their desitinations.

![](https://www.cloudflare.com/img/learning/security/glossary/what-is-bgp/bgp-simplified.svg)

- The structure of the internet is constantly changing -> Every AS must be kept up to date with information regarding new routes as well as obsolete routes -> Peering sessions where each AS connects to neighboring ASes with a TCP/IP connection for the purpose of sharing routing information.
- Routes are exchanged and traffic is transmitted over the Internet using external BGP (eBGP). Autonomous systems can also use an internal version of BGP to route through their internal networks, which is known as internal BGP (iBGP).
- [Comparing Opensource BGP](https://elegantnetwork.github.io/posts/comparing-open-source-bgp-stacks/)
