# AWX

## 1. Install in Docker

- AWX already has the guide for it, but I want to do my version: <https://github.com/ansible/awx/blob/devel/tools/docker-compose/README.md>
- Clone repo:

```shell
git clone -b x.y.z https://github.com/ansible/awx.git
```

- Start the container.

```shell
$ # install requirements
$ PYTHON=python3.10 make docker-compose
```

- Access <https://localhost:8043>.
- If you face `process.env.` page, may be your UI installation is failed.

```shell
$ docker exec -it awx-container bash
# inside container
$ make clean-ui
$ make ui-devel
# If your environment requires proxy
$ npm config set https-proxy http://proxy
$ npm config set proxy http://proxy
```
