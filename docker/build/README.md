# Build tricks

## 1. Build secrets

Source: <https://docs.docker.com/build/building/secrets/>

A build secret is any piece of sensitive information, such as password or API token, consumed as part of your applications build process.

## 1.1. The wrong way to copy secret

Do you ever try to `COPY` a file with credentials from your Dockerfile and then remove it with `rm` when you don't need it anymore?

```Dockerfile
FROM busybox
COPY .secrets /tmp
RUN rm /tmp/.secrets
```

Well, **this is so wrong** because you are just deleting the file from that layer but the credentials are still in the layer above.

```shell
$ docker build -t unsafe . -f Dockerfile.unsafe
 => [internal] load build definition from Dockerfile.unsafe                                                                                                                                                                      0.1s
 => => transferring dockerfile: 97B                                                                                                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/busybox:latest                                                                                                                                                                2.7s
 => [auth] library/busybox:pull token for registry-1.docker.io                                                                                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                0.0s
 => => transferring context: 2B                                                                                                                                                                                                  0.0s
 => [internal] load build context                                                                                                                                                                                                0.0s
 => => transferring context: 58B                                                                                                                                                                                                 0.0s
 => [1/3] FROM docker.io/library/busybox:latest@sha256:db142d433cdde11f10ae479dbf92f3b13d693fd1c91053da9979728cceb1dc68                                                                                                          0.6s
 => => resolve docker.io/library/busybox:latest@sha256:db142d433cdde11f10ae479dbf92f3b13d693fd1c91053da9979728cceb1dc68                                                                                                          0.0s
 => => sha256:db142d433cdde11f10ae479dbf92f3b13d693fd1c91053da9979728cceb1dc68 10.20kB / 10.20kB                                                                                                                                 0.0s
 => => sha256:a3e1b257b47c09c9997212e53a0b570c1666501ad26e5bf33461304babab47c7 610B / 610B                                                                                                                                       0.0s
 => => sha256:517b897a6a8312ce202a85c8a517d820b0fc5b6f5d14ec2a3267906f75680403 372B / 372B                                                                                                                                       0.0s
 => => sha256:430378704d12f9a980f41ae1a29c587974e1f0234d5dab0765fa95a4d764622e 2.16MB / 2.16MB                                                                                                                                   0.4s
 => => extracting sha256:430378704d12f9a980f41ae1a29c587974e1f0234d5dab0765fa95a4d764622e                                                                                                                                        0.1s
 => [2/3] COPY .secrets /tmp                                                                                                                                                                                                     0.1s
 => [3/3] RUN rm /tmp/.secrets                                                                                                                                                                                                   0.5s
 => exporting to image                                                                                                                                                                                                           0.1s
 => => exporting layers                                                                                                                                                                                                          0.0s
 => => writing image sha256:c5ca80eed7e66549a42da612b81a0e914223e3eef40360f87f0dd84d0090e333                                                                                                                                     0.0s
 => => naming to docker.io/library/unsafe                                                                                                                                                                                        0.0s

$ docker history unsafe

$ docker run -it --rm
```
