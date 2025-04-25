# Nginx mirror

Source:

- <http://nginx.org/en/docs/http/ngx_http_mirror_module.html>
- <https://alex.dzyoba.com/blog/nginx-mirror/>
- <https://blog.liorp.dev/blog/devops/mirroring-htp-requests-with-nginx/>

The `ngx_http_mirror_module` module (1.13.4) implements mirroring of an original request by creating background mirror subrequests. Responses to mirror subrequests are ignored.
