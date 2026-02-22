# Load balancing strategies for Consul

- [Load balancing strategies for Consul](#load-balancing-strategies-for-consul)
  - [1. Consul directly](#1-consul-directly)
  - [2. Fabio](#2-fabio)
  - [3. Nginx/HAProxy with Consul template](#3-nginxhaproxy-with-consul-template)
  - [4. Nginx with Custom module](#4-nginx-with-custom-module)
  - [5. HAProxy 1.8](#5-haproxy-18)
  - [6. Traefik](#6-traefik)

Source:

- <https://www.hashicorp.com/blog/load-balancing-strategies-for-consul>
- <https://learn.hashicorp.com/collections/nomad/load-balancing>

## 1. Consul directly

- One approach to load balancing with Consul is to use Consul's built-in load balancing functionality. Consul integrates health checks with service discovery. This means that unhealthy hosts are never returned from queries to the service discovery layer. In this mode, applications and services talk directly to Consul each time they want to find other services in the datacenter.

```hcl
services:
  backend: backend.service.consul
```

- Pros
  - No reliance on external tools or processes
  - No other services to monitor or maintain
  - Highly available by default
  - As close to real time as possible
  - DNS is easy to use, minimal effort
  - Health check is distributed, minimal cluster load
- Cons
  - Single point of failure - even though Consul is highly available by - default, this mode provides no fail-over if Consul is unavailable or - inaccessible
  - Requires using the HTTP API directly in the application OR making DNS - queries and assuming port OR making two DNS queries to find the address - and port
  - Tight coupling between the application and Consul

## 2. Fabio

- Users register a service with a tag beginning with urlprefix-, like:

```
urlprefix-/my-service
```

- In this example, when a request is made to fabio at /my-service, fabio will automatically route traffic to a healthy service in the cluster.
- Pros
  - Rich integrations with Consul
  - More control over load balancing than the DNS approach
  - Strong community backing and adoption with over 4,000 GitHub stars
  - Support for TCP proxying
  - Accessing logging and a slew of other awesome features
  - HashiCorp Vault integration
  - Optional Web UI for routing visualization
  - Very detailed, open source documentation
- Cons
  - Requires an additional service to run and monitor
  - Tight coupling with Consul and Consul tags

## 3. Nginx/HAProxy with Consul template

- Use 3rd-party tool such as Nginx/HAProxy to balance traffic and an open source tool like Consul template to manage the configuration.

```
nginx.conf.tpl --> Consul template --> nginx.conf
```

```hcl
upstream myapp {
{{ range service "myapp" }}
  server {{ .Address }}:{{ .Port }}
{{ end }}
}
```

```
upstream myapp {
  server 10.2.5.60:13845
  server 10.6.96.234:45033
  server 10.10.20.123:18677
}
```

- Neither HAProxy nor Nginx are aware of Consul's existence.
- Pros
  - Handles applications running on non-default ports without additional API- requests
  - Nginx and HAProxy are both battle-tested tools
  - Organizations may already have expertise or existing infrastructure with- these tools
  - If Consul were to go offline, there is still a record of the last-known- good state of services
  - Consul Template also integrates with Vault, which makes this an ideal- solution if the configuration file has secret data like TLS private keys- or shared passwords
- Cons
  - Requires two additional services to manage and monitor - Nginx/HAProxy and Consul Template
  - Inefficient templates can place significant pressure on the Consul cluster due to blocking queries
  - Challenging to practice the "one service per container" paradigm
  - A "flappy" cluster (a cluster where services are flipping between healthy and unhealthy or a cluster with a lot of continuous rapid churn) can cause instability in the Nginx/HAproxy configuration

## 4. Nginx with Custom module

- Use [ngx_http_consul_backend_module](https://github.com/hashicorp/ngx_http_consul_backend_module).

```
http {
  server {
    listen       80;
    server_name  example.com;

    location /my-service {
      consul $backend service-name;
      proxy_pass http://$backend;
    }
  }
}
```

- Pros
  - Handles applications running on non-default ports without additional API requests
  - No external tools - just run Nginx and point directly to Consul
  - Using the official Consul SDK client library gives HTTP/2, stale queries, and more out of the box
- Cons
  - Requires compiling Nginx from source to install the custom module
  - Calls out to Consul on each request to the backend (each request eats the RTT of the request and the RTT of the Consul resolution)
  - Requires knowledge of Nginx custom modules to contribute
  - Does not integrate with Vault for TLS private keys or shared passwords
  - Module is not battle-tested (yet)

## 5. HAProxy 1.8

- Pros
  - No external tools - just run HAProxy and point directly to Consul
  - Handles graceful reloads, TTLs, etc
  - Supports Kubernetes and Docker Swarm service discovery too

- Cons
  - Requires HAProxy
  - Less flexibility over failure scenarios than Consul Template

## 6. Traefik
