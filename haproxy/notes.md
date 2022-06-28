# Tips and notes

> Something cool when using HAProxy

## 1. Configuration allows two frontends to bind to the same IP and port

- Give a configuration where two `frontend` sections bind to the same IP and port. This configuration is still valid.

```
frontend fe1
  bind :80
  default_backend servers1

frontend fe2
  bind :80
  default_backend servers2

backend servers1
  server server1 127.0.0.1:8080

backend servers2
  server server1 127.0.0.1:8081
```

- You think it won't work? Nah, it works. HAProxy uses [SO_REUSEPORT](https://lwn.net/Articles/542629/).
  - The basic concept of SO_REUSEPORT is simple enough. Multiple servers (processes or threads) can bind to the same port.
  - To prevent unwanted processes from hijacking a port that has already been bound by a server using SO_REUSEPORT, all of the servers that later bind to that port must have an effective user ID that matches the effective user ID used to perform the first bind on the socket.
  - Therefore, HAProxy is still able to bind same ports. _It's a feature not bug!_.
- Although it's feature, it can lead to unwanted behavior. But don't worry, HAProxy has [noreuseport](https://cbonte.github.io/haproxy-dconv/2.0/configuration.html#3.2-noreuseport) directive to disable.
