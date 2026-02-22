# Tuning Envoy for Performance

Well, when you try to find Nginx or HAproxy performance tuning, the results are detailed documentations: [this](https://www.nginx.com/blog/tuning-nginx/), [this](https://www.cloudbees.com/blog/performance-tuning-haproxy), [this](https://www.freecodecamp.org/news/how-we-fine-tuned-haproxy-to-achieve-2-000-000-concurrent-ssl-connections-d017e61a4d27/),...

Replace Nginx/HAproxy with Envoy, this is a different story. Therefore, I decide to write this guide.

- [Tuning Envoy for Performance](#tuning-envoy-for-performance)
  - [1. Getting started](#1-getting-started)
  - [2. First thing first, tuning your Linux OS](#2-first-thing-first-tuning-your-linux-os)
    - [2.1. The backlog queue](#21-the-backlog-queue)
    - [2.2. File descriptors](#22-file-descriptors)
    - [2.3. Ephemeral ports](#23-ephemeral-ports)
    - [2.4. TCP buffer](#24-tcp-buffer)
  - [3. Tuning Envoy](#3-tuning-envoy)
    - [3.1. Concurrency](#31-concurrency)
    - [3.2. SO_REUSEPORT](#32-so_reuseport)
    - [3.3. Listen connection balancing](#33-listen-connection-balancing)
    - [3.4. Limits tuning](#34-limits-tuning)

## 1. Getting started

- A basic understanding of the Envoy architecture and configuration concepts is assumed.
- Assume Envoy is deployed in Linux distro (kernel 2.6+).
- Change one settings at a time, and set it back to the default value if the change does not improve performance.
- Follow [How to benchmark Envoy guide](https://www.envoyproxy.io/docs/envoy/latest/faq/performance/how_to_benchmark_envoy).
- Every section is combined of 4 sections:
  - What: Quick intro about the change.
  - Why: Explain why you should make this change.
  - How: The ideal change.

## 2. First thing first, tuning your Linux OS

- Note that, you should check the kernel log for error messages indicating that a settings is too low, and adjust it as advised.

### 2.1. The backlog queue

- What:
  - The following settings relate to connections and how they are queued.
  - If you have a high rate of incoming connections, you may get uneven levels of performance (for example, some connections appear to be staling).
- Why: [The origin post](https://www.alibabacloud.com/blog/tcp-syn-queue-and-accept-queue-overflow-explained_599203)
  - SYN Queue and Accept Queue: During the TCP handshake process, the Linux kernel maintain these two queues. Both queues have length and size limits. If the limit is exceeded, the kernel discards the connection Drop or return the RST packet.

  ![](https://yqintl.alicdn.com/0f72fe628f4e77b59f92d149c8584476f8d6fc5d.png)
  - Check of relevant indicators

  ```shell
  # -n Does not resolve the service name
  # -t only show tcp sockets
  # -l Displays LISTEN-state sockets
  $ ss -int
  # Recv-Q: The size of the current accept queue, which means the 3 connections have been completed and are waiting for the application accept() TCP connections
  # Send-Q: The maximum length of the accept queue, which is the size of the accept queue.
  $ ss -nt
  # Recv-Q: The number of bytes received but not read by the application
  # Send-Q: The number of bytes sent but not ack.

  # Check the overflow status of TCP SYN queue and accept queue
  $ netstat -s | grep -i "listen"
  ```

  - The maximum length of TCP Accept queue is controlled by `min(somaxconn, backlog)` (Check [related kernel code, if you want](https://github.com/torvalds/linux/blob/master/net/socket.c)):
    - somaxconn (`/proc/sys/net/core/somaxconn`).
    - backlog is one of TCP protocol's listen function parameters, which is the size of the int listen(int sockfd, int backlog) function's backlog.
  - `tcp_max_syn_backlog` represents the maximal number of connections in SYN RECV queue (when your server received SYN, sent SYN-ACK and haven't received ACK yet).
  - Nginx blog has metioned `net.core.netdev_max_backlog`: The rate at which packets are buffered by the network card before being handed off to the CPU (per CPU core settings).

- How: Increase these values to improve performance on machines with a high amount of bandwidth. The exact numbers are depend on your system.
  - Increase `net.core.somaxconn`.

  ```shell
  # Increase value
  net.core.somaxconn=<value>
  # Restart service
  # Check the accept queue size
  $  ss -lnt
  ```

  - Increase `net.ipv4.tcp_max_syn_backlog`.

  ```shell
  # Increase value
  net.ipv4.tcp_max_syn_backlog=<value>
  ```

  - Increase `net.core.netdev_max_backlog`.

  ```shell
  # Increase value
  net.core.netdev_max_backlog=<value>
  ```

### 2.2. File descriptors

- What:
  - File descriptors are operating system resources used to represent connections and open files, among other things.
  - Proxy usually takes up to two file descriptors/connection:
    - 1 file descriptor for the client connection.
    - Another for the connection to the proxied server.
- Why:
  - Sockets are considered equilvalent to files from the system perspective!
  - `sys.fs.file-max`: The system-wide limit of file descriptors.
  - `nofile`: The user file descriptor limit, set in `/etc/security/limits.conf` file.
- How:
  - Increase the total file descriptors.

  ```shell
  # Update to 1 mil
  fs.file-max = 10000000
  # Update to 1 mil
  fs.nr_open = 10000000
  # Update /etc/security/limits.conf
  * soft nofile 10000000
  * hard nofile 10000000
  root soft nofile 10000000
  root hard nofile 10000000
  ```

### 2.3. Ephemeral ports

- What:
  - Each connection to an upstream server uses a temporary, or _ephemeral_ port.
- Why:
  - `net.ipv4.ip_local_port_range`: the start and end of the range of port values. If you see that you are running out of ports, increase the range.
- How:
  - Increase the range of ports.

  ```shell
  net.ipv4.ip_local_port_range=1024    65023
  ```

### 2.4. TCP buffer

- What:
  - If your host handles a huge number of connections, it costs a lot of memory.
- Why:
  - `net.ipv4.tcp_rmem`: Contains 3 values that represent the minimum, default and maximum size of the TCP socket receive buffer.
  - `net.ipv4.tcp_wmem`: Similar to the `net.ipv4.tcp_rmem` this parameter consists of 3 values, a minimum, default, and maximum.
  - `net.ipv4.tcp_mem`: The overall.
- How:
  - Reduce these values in order to reduce memory use.

  ```shell
  net.ipv4.tcp_mem = 786432 1697152 1945728
  net.ipv4.tcp_rmem = 4096 4096 16777216
  net.ipv4.tcp_wmem = 4096 4096 16777216
  ```

## 3. Tuning Envoy

### 3.1. Concurrency

- What:
  - Envoy uses a single process with multiple _threads_ architecture. A single primary thread controls various sporadic coordination tasks while some number of worker threads perform listening, filtering, and forwarding.
  - Once a connection is accepted by a listener, the connection spends the rest of its lifetime bound to a single worker thread.
  - Envoy does no have any blocking IO operations in the event loop, even logging is implemented in a non-blocking way.
- Why:
- How: Leave `--concurrency` be unset (providing one worker thread per logical core on your machine).

### 3.2. SO_REUSEPORT

- What:
  - By default, Envoy disable resuse port feature.
- Why:
  - Multiple server sockets listen on the sameport. Each server socket corresponds to a listening thread. When the kernel TCP stack receives a client connection request (SYN), according to the TCP 4-tuple (srcIP, srcPort, destIP, destPort) hash algorithm, select a listening thread, and wake it up. The new connection is bound to the thread that is woken up. So connections are more evenly distributed across threads than non-`SO_REUSEPORT` (in this case, all worker threads share on socket).

  ![](https://www.muppetwhore.net/ljarchive/LJ/298/12538c.jpg)

- How:
  - Config `enable_reuse_port` option (version >= 1.20). If you use the older version (1.18 for example), you can check `reuse_port`:
    - <https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto>
    - <https://www.envoyproxy.io/docs/envoy/v1.18.3/api-v3/config/listener/v3/listener.proto>

### 3.3. Listen connection balancing

- What:
  - By default, there is no coordination between worker threads. This means that all worker threads independently attempt to accept connections on each listener and rely on the kernel to perform adequate balancing between threads.
- Why:
  - For most workloads, the kernel does a very good job of balancing incoming connections (better if you enable SO_REUSEPORT).
  - For some workloads, particularly those that have a small number of very long lived connections, it may be desirable to have Envoy force balance connections between worker threads. Envoy allows for different types of [connection balancing](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-field-config-listener-v3-listener-connection-balance-config).
- How:
  - Config can be found [here](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-msg-config-listener-v3-listener-connectionbalanceconfig).

### 3.4. Limits tuning

- Envoy is a production-ready edge proxy, however, the default settings are tailored for the service mesh use case, and some values need to be adjusted when using Envoy as an edge proxy.
- Check [here](https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge).

```yaml
overload_manager:
  refresh_interval: 0.25s
  resource_monitors:
    - name: "envoy.resource_monitors.fixed_heap"
      typed_config:
        "@type": type.googleapis.com/envoy.extensions.resource_monitors.fixed_heap.v3.FixedHeapConfig
        # TODO: Tune for your system.
        max_heap_size_bytes: 2147483648 # 2 GiB
  actions:
    - name: "envoy.overload_actions.shrink_heap"
      triggers:
        - name: "envoy.resource_monitors.fixed_heap"
          threshold:
            value: 0.95
    - name: "envoy.overload_actions.stop_accepting_requests"
      triggers:
        - name: "envoy.resource_monitors.fixed_heap"
          threshold:
            value: 0.98

admin:
  address:
    socket_address:
      address: 127.0.0.1
      port_value: 9090

static_resources:
  listeners:
    - address:
        socket_address:
          address: 0.0.0.0
          port_value: 443
      listener_filters:
        # Uncomment if Envoy is behind a load balancer that exposes client IP address using the PROXY protocol.
        # - name: envoy.filters.listener.proxy_protocol
        #   typed_config:
        #     "@type": type.googleapis.com/envoy.extensions.filters.listener.proxy_protocol.v3.ProxyProtocol
        - name: "envoy.filters.listener.tls_inspector"
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.listener.tls_inspector.v3.TlsInspector
      per_connection_buffer_limit_bytes: 32768 # 32 KiB
      filter_chains:
        - filter_chain_match:
            server_names: ["example.com", "www.example.com"]
          transport_socket:
            name: envoy.transport_sockets.tls
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
              common_tls_context:
                tls_certificates:
                  - certificate_chain: { filename: "certs/servercert.pem" }
                    private_key: { filename: "certs/serverkey.pem" }
                alpn_protocols: ["h2,http/1.1"]
          filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                use_remote_address: true
                normalize_path: true
                merge_slashes: true
                path_with_escaped_slashes_action: UNESCAPE_AND_REDIRECT
                common_http_protocol_options:
                  idle_timeout: 3600s # 1 hour
                  headers_with_underscores_action: REJECT_REQUEST
                http2_protocol_options:
                  max_concurrent_streams: 100
                  initial_stream_window_size: 65536 # 64 KiB
                  initial_connection_window_size: 1048576 # 1 MiB
                stream_idle_timeout: 300s # 5 mins, must be disabled for long-lived and streaming requests
                request_timeout: 300s # 5 mins, must be disabled for long-lived and streaming requests
                http_filters:
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:
                  virtual_hosts:
                    - name: default
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/" }
                          route:
                            cluster: service_foo
                            idle_timeout: 15s # must be disabled for long-lived and streaming requests
  clusters:
    - name: service_foo
      per_connection_buffer_limit_bytes: 32768 # 32 KiB
      load_assignment:
        cluster_name: some_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: 127.0.0.1
                      port_value: 8080
      typed_extension_protocol_options:
        envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
          "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
          explicit_http_config:
            http2_protocol_options:
              initial_stream_window_size: 65536 # 64 KiB
              initial_connection_window_size: 1048576 # 1 MiB

layered_runtime:
  layers:
    - name: static_layer_0
      static_layer:
        envoy:
          resource_limits:
            listener:
              example_listener_name:
                connection_limit: 10000
        overload:
          global_downstream_max_connections: 50000
```
