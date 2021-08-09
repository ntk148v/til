# HAProxy Rate Limiting

Source: https://www.haproxy.com/blog/four-examples-of-haproxy-rate-limiting/

## Intro

- Use rate limiting in HAProxy to stop clients from making too many requests and promote fair usage of your services during a window of time.

## Setting the Maximum connections

- Enable **queuing**: store excess connections in HAProxy until your servers are freed up to handle them.

```
# Send up to 30 connections/server at a time.
# After all servers reach their maximum -> the connections queue up in HAProxy
backend servers
    timeout queue 10s # receive 503 Service Unavailble error
    server s1 192.168.30.10:80 check  maxconn 30
    server s2 192.168.31.10:80 check  maxconn 30
    server s3 192.168.31.10:80 check  maxconn 30
```

## Sliding Window Rate Limiting

- Limit number of requests that a user can make within a certain period of a time (**a sliding window**).

```
frontend website
    bind :80
    # Allow <= 20 requests/client during the last 10 seconds
    stick-table  type ipv6  size 100k  expire 30s  store http_req_rate(10s)
    http-request track-sc0 src
    # Set the rate limit threshold and the action to take when someone exceeds it.
    # 429 Too many requests
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend servers
```

- `stick-table`: adds client as a record, the counters begin to be recorded as soon as the IP is added.

| key                 | value                          |
| ------------------- | ------------------------------ |
| client's IP address | counters (HTTP request/client) |


## Rate Limit by Fixed Time Window

- Rate Limit by fixed time window -> reset.

```
frontend website
    bind :80
    # http_req_cnt increments forever until reset (use Runtime API) or until the expiration is hit
    stick-table  type ipv6  size 100k  expire 24h  store http_req_cnt
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_cnt(0) gt 1000 }
    default_backend servers
```

- Enable Runtime API:

```
global
    stats socket /run/haproxy.sock mode 660 level admin u
```

- Install the `socat` utility and use it to invoke to the `clear table` Runtime API command to clear all records from the stick table.

```
# Use cron job to do this automatically each day
$ echo "clear table website" | sudo socat stdio /run/haproxy.sock
```

## Rate Limit by URL

- Some pages require more processing time than others -> stricter rate limit.
- Create a map file `/etc/haproxy/rates.map`:

```
/urla  10
/urlb  20
/urlc  30
```

```

frontend website
    bind :80
    stick-table  type binary  len 20  size 100k  expire 10s  store http_req_rate(10s)

    # Track client by base32+src (Host header + URL path + src IP)
    # use as stick-table key
    http-request track-sc0 base32+src

    # Check map file to get rate limit for path
    http-request set-var(req.rate_limit)  path,map_beg(/etc/haproxy/rates.map,20)

    # Client's request rate is tracked
    http-request set-var(req.request_rate)  base32+src,table_http_req_rate()

    # Subtract the current request rate from the limit
    # If less than zero, set rate_abuse to true
    acl rate_abuse var(req.rate_limit),sub(req.request_rate) lt 0

    # Deny if rate abuse
    http-request deny deny_status 429 if rate_abuse
    default_backend servers
```

## Rate Limit by URL Parameter

```
frontend website
    bind :80
    stick-table type string size 100k expire 24h store http_req_rate(24h)

    # check for token parameter
    acl has_token url_param(token) -m found

    # check if exceeds limit
    acl exceeds_limit url_param(token),table_http_req_rate() gt 1000

    # start tracking based on token parameter
    # store token as the key in stick-table
    http-request track-sc0 url_param(token) unless exceeds_limit

    # Deny if missing token or exceeds limit
    http-request deny deny_status 429 if !has_token or exceeds_limit
    default_backend servers
```

## More

https://gist.github.com/procrastinatio/6b6579230d99be5bfa26d04acd788e7a
