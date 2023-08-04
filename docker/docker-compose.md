# Docker Compose

> This is not a full documentation, just a note about some interesting things.

## 0. Why Docker Compose?

The `docker` command line supports many flags to fine-tune your container, and it's difficult to remember them all when replicating an environment. Doing so is even harder when your application is not a single container but a combination of many containers with various dependency relationships. Based on this, `docker-compose` quickly became a popular tool because it lets users declare all the infrastructure details for a container-based application into a single YAML file using a simple syntax directly inspired by the `docker run` command line.

## 1. Improve Docker Compose modularity with [`include`](https://docs.docker.com/compose/multiple-compose-files/include/)

Source: <https://www.docker.com/blog/improve-docker-compose-modularity-with-include/>

> Compose >= v2.20.0

- Still, an issue persists for large applications using dozens, maybe hundreds, of containers, with ownership distributed across multiple teams. When using a monorepo, teams often have their own “local” Docker Compose file to run a subset of the application, but then they need to rely on other teams to provide a reference Compose file that defines the expected way to run their own subset.
- Extend a compose file.
  - Refer to another Compose file and select a service you want to also use in your own application, with the ability to override attributes for your own needs.
  - It's not an acceptable solution when you want to reuse someone else’s configuration as a “black box” and don’t know about its own dependencies.

```yaml
services:
  database:
    extends:
      file: ../commons/compose.yaml
      service: db
```

- Merge compose files.

  - Define a Compose file for database service.

  ```yaml
  services:
    database:
      builld: .
      env-file:
        - ./db.env
  ```

  - Switch to another team and build a web application, which requires access to the database:

  ```yaml
  services:
    webapp:
      depends_on:
        - database
  ```

  - Merge these compose files:

  ```shell
  docker compose -f compose.yaml -f ../database/compose.yaml
  ```

  - In doing so, the relative paths set by the second Compose file won’t get resolved as designed by the authors but from the local working directory.

- Using `include` to reuse content from other teams.

  - Get a whole Compose file included in your own application model (copy/paste).
  - It will manage relative path references so that the included Compose file will be parsed the way the author expects, running from its original location.

  ```yaml
  include: ../database/compose.yaml

  services:
    webapp:
      depends_on:
        - database
  ```
