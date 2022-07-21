# OpenStack Zaqar

## What is Zaqar?

* Zaqar is a multi-tenant cloud messaging and notification service for web and mobile developer.
* The service features a REST API, which developer can use to send messages between various components of their SaaS and mobile applications, by using a variety of communication patterns.

## Key features

* Choice between 2 communication transports. Both with Keystone support:
    * Firewall-friendly, **HTTP-based RESTful API**.
    * **Websocket-based API**.

* Multi-tenants queues based on Keystone project IDs.
* Support for several common patterns including event broadcasting, task distribution, and point-to-point messaging.
* Component-based architecture with support for custom backends and message filters.
* Efficient reference implementation with an eye toward low latency and high throughput.
* High-available and horizontally scalable.
* Support for subscriptions to queues. Several notification types are available:
    * Email notifications
    * Webhook notifications
    * Websocket notification*s

