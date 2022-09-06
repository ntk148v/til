# Debugging in Nginx

## 1. Scenario

- A client got a http error 400 (bad request) when accessing certain pages of website.

## 2. Debugging in Nginx

- Firstly, check the backend log. If there is nothing wrong, move to the next step.
- Identify client's IP address.
- Nginx allows to set a certain IP address or range into debug mode by using the [debug_connection](http://nginx.org/en/docs/ngx_core_module.html#debug_connection) parameter in the events context.

```
events {
    # Debugging a certain IP
    debug_connection <client's IP address>; # client getting http 400 errors
}
```

- Note that, you have to enable debug mode in Nginx. If you're using Docker image to provision Nginx, you can use `nginx-debug` binary that produces verbose output when using higher log levels.

```bash
$ docker run --name my-nginx -v /host/path/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx nginx-debug -g 'daemon off;'
```

```yaml
web:
  image: nginx
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
  command: [nginx-debug, '-g', 'daemon off;']
```

- Restart Nginx and access website again to reproduce the http 400 error. This request will be logged in detail!
- Check the log and see if there is anything wrong.
