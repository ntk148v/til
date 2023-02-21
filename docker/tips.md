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
