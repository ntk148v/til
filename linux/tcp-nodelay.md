# TCP_NODELAY

Source:

- <https://brooker.co.za/blog/2024/05/09/nagle.html>
- <https://www.extrahop.com/blog/tcp-nodelay-nagle-quickack-best-practices>
- <https://datatracker.ietf.org/doc/html/rfc89>
- <https://linux.die.net/man/7/tcp>

The first thing to check when debugging latency issues in distributed systems is whether `TCP_NODELAY` is enabled.

```text
TCP_NODELAY
    If set, disable the Nagle algorithm. This means that segments are always sent as soon as possible, even if there is only a small amount of data. When not set, data is buffered until there is a sufficient amount to send out, thereby avoiding the frequent sending of small packets, which results in poor utilization of the network. This option is overridden by TCP_CORK; however, setting this option forces an explicit flush of pending output, even if TCP_CORK is currently set.
```

It is very important to understand the interactions between Nagle's algorithm and Delayed ACKs. The `TCP_NODELAY` socket option allows your network to bypass Nagle Delays by disabling Nagle's algorithm, and sending the data as soon as it's available. Enabling `TCP_NODELAY` forces a socket to send the data in its buffer, whatever the packet size. To disable Nagle's buffering algorithm, use the `TCP_NODELAY` socket option. To disable Delayed ACKs, use the `TCP_QUICKACK` socket option.

Enabling the `TCP_NODELAY` option turns Nagle's algorithm off. In the case of interactive applications or chatty protocols with a lot of handshakes such as SSL, Citrix and Telnet, Nagle's algorithm can cause a drop in performance, whereas enabling `TCP_NODELAY` can improve the performance.

## Should I enable `TCP_NODELAY`?

It really depends on what is your specific workload and dominant traffic patterns on a service. If you are dealing with non-interactive type traffic or bulk transfers such as SOAP, XMLRPC, HTTP/web traffic then enabling `TCP_NODELAY` to disable Nagle's algorithm is unnecessary.

Some contexts where Nagle's algorithm won't help and `TCP_NODELAY` should be enabled are:

- Highly interactive applications that communicate with a central server (Citrix, networked video games, etc)
- Telnet-connected devices Applications using chatty protocols (Telnet, SSL)

## How do I figure out if I should enable `TCP_NODELAY`?

Are you seeing a high number of "tinygrams" (packets that contain a relatively small payload compared to the overhead associated with the headers required to transfer the data.)

If you see lots of tinygrams or a high number of Nagle Delays as a percentage of overall traffic, then disable `TCP_NODELAY` that will allow Nagle's algorithm to reduce the tinygrams. Again leave the EDA running for some time and then look at the tinygram number, if this number is still very high then enable `TCP_NODELAY`, indicating Nagle's algorithm is not reducing the tinygrams.

Tuning tends to be an iterative process. It takes a some experimentation to know if you should or should not enable `TCP_NODELAY`, and your needs will change over time as your networking stack and applications grow and change.

## How do I know if `TCP_NODELAY` is helping?

After enabling `TCP_NODELAY` to disable Nagle's algorithm and going through the process of tuning, if you see a very low number of Nagle Delays as a percentage of overall traffic and a very low number of tinygrams then you know enabling `TCP_NODELAY` is helping.

Conversely if you see a high number of Nagle Delays as a percentage of overall traffic and a very high number of tinygrams then enabling `TCP_NODELAY` probably is not the best fit for your use case.
