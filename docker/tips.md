# Tips & Tricks

## 1. Retrieve file that was deleted during the image build

Use [docker image save](https://docs.docker.com/engine/reference/commandline/image_save) to export a tarball that contains a tarball per layer.

```shell
docker image save alpine -o alpine.tar
# Extract thing
```

<https://docs.docker.com/engine/reference/commandline/image_save/>

## 2. Analyze Docker disk usage

Use [docker system df](https://docs.docker.com/engine/reference/commandline/system_df/) to show Docker disk usage.

```shell
docker system df -v
Images space usage:

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE      SHARED SIZE   UNIQUE SIZE   CONTAINERS
alpine       latest    b2aa39c304c2   10 days ago   7.05MB    0B            7.05MB        0

Containers space usage:

CONTAINER ID   IMAGE     COMMAND   LOCAL VOLUMES   SIZE      CREATED   STATUS    NAMES

Local Volumes space usage:

VOLUME NAME                                                        LINKS     SIZE

Build cache usage: 0B

CACHE ID   CACHE TYPE   SIZE      CREATED   LAST USED   USAGE     SHARED
```

## 3. Build image behind proxy with cert (workaround)

- Download your certificate file in the same directoryy as Dockerfile, named it as `your_cert.crt`.
- Create the Dockerfile:

```Dockerfile
FROM alpine
COPY your_cert.crt /usr/local/share/ca-certificates/your_cert.crt
RUN cat /usr/local/share/ca-certificates/your_cert.crt > /etc/ssl/certs/ca-certificates.crt
RUN apk add --no-cache curl
# ...
```

- Build it:

```shell
docker build --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$http_proxy --build-arg NO_PROXY="$no_proxy" --build-arg http_proxy=$http_proxy --build-arg https_proxy=$http_proxy --build-arg no_proxy="$no_proxy" -t your-image .
```
