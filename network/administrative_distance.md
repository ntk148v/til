# Administrative distance

## Introduction

Administrative distance (AD) or route preference is a number of arbitrary unit assigned to dynamic routes, static routes, and directly connected routes. The value is used in routers to rank routes from most preferred (low AD value) to least preferred (high AD value). When multiple paths to the same destination are available in its routing table, the router uses the route with the lowest administrative distance.

## Default administrative distances

### Cisco

| Routing protocol                                   | Administrative distance |
| -------------------------------------------------- | ----------------------- |
| Directly connected interface                       | 0                       |
| Static route                                       | 1                       |
| Dynamic Mobile Network Routing (DMNR)              | 3                       |
| EIGRP summary route                                | 5                       |
| External BGP                                       | 20                      |
| EIGRP internal route                               | 90                      |
| IGRP                                               | 100                     |
| Open Shortest Path First (OSPF)                    | 110                     |
| Intermediate System to Intermediate System (IS-IS) | 115                     |
| Routing Information Protocol (RIP)                 | 120                     |
| Exterior Gateway Protocol (EGP)                    | 140                     |
| ODR                                                | 160                     |
| EIGRP external route                               | 170                     |
| Internal BGP                                       | 200                     |
| Next Hop Resolution Protocol (NHRP)                | 250                     |
| Default static route learned via DHCP              | 254                     |
| Unknown and unused                                 | 255                     |

## Junipter

| Routing protocol             | Administrative distance |
| ---------------------------- | ----------------------- |
| Directly connected interface | 0                       |
| Static routes                | 5                       |
| OSPF internal routes         | 10                      |
| IS-IS Level 1 Internal       | 15                      |
| IS-IS Level 2 Internal       | 18                      |
| RIP                          | 100                     |
| Aggregate (route summary)    | 130                     |
| OSPF external routes         | 150                     |
| IS-IS Level 1 External       | 160                     |
| IS-IS Level 2 External       | 165                     |
| BGP                          | 170                     |
