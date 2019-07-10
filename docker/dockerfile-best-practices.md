# Dockerfile Best Practices

[Source](https://blog.docker.com/2019/07/intro-guide-to-dockerfile-best-practices/)

## Incremental build time

**Leverage caching**

### Tip 1. Order matters for caching

![](https://i0.wp.com/blog.docker.com/wp-content/uploads/2019/07/ef41db8f-fe5e-4a78-940a-6a929db7929d-1.jpg?ssl=1)

Order your steps from least to most frequently changing steps to optimize caching.

### Tip 2. More specific COPY to limit cache busts

![](https://i1.wp.com/blog.docker.com/wp-content/uploads/2019/07/0c1d0c4e-406c-468c-b6ba-b71ac68b9c84.jpg?ssl=1)

Only copy what's needed. If possible, avoid "COPY".

### Tip 3. Identity cacheable units such as apt-get update & install

![](https://i0.wp.com/blog.docker.com/wp-content/uploads/2019/07/2322a39e-bd7e-4a2b-9a8f-548a97dbacb4.jpg?ssl=1)

Each RUN instruction can be seen a cacheable unit of execution. Tomany of them can be unnecessary, while chaining all commands into one RUN instruction can bust the cache easily.

## Reduce Image Size

### Tip 4. Remove unnecessary dependencies

![](https://i1.wp.com/blog.docker.com/wp-content/uploads/2019/07/a1b36f64-1a30-45bf-8fcd-4f88437c189e.jpg?ssl=1)

Remove unnecessary dependencies and do not install debugging tools.

### Tip 5: Remove package manager cache

![](https://i1.wp.com/blog.docker.com/wp-content/uploads/2019/07/363961a4-005e-46fc-963b-f7b690be12ef.jpg?ssl=1)

Package managers maintain their own cache which may end up in the image. One way to deal with it is to remove the cache in the same RUN instruction that installed packages.

There are further ways to reduce image size such as multi-stage builds.

## Maintainability

### Tip 6: Use official images when possible

![](https://i0.wp.com/blog.docker.com/wp-content/uploads/2019/07/f336014d-d2aa-4c1b-a2bd-e1d5d6ed0d93.jpg?ssl=1)

Official images can save a lot of time spent on maintenance because all the installation steps are done and best practices are applied.

### Tip 7: Use more specific tags

![](https://i0.wp.com/blog.docker.com/wp-content/uploads/2019/07/9d991da9-bdb9-4108-8b36-296a5a3772aa.jpg?ssl=1)

Do not use the lastest tag. Instead, use more specific tags for your base images.

### Tip 8: Look for minimal favors

Some of those tags have minimal flavors which means they are even smaller images.

## Reproducibility

### Tip 9: Build from source in a consistent environment

The source code is the source of truth from which you want to build a Docker image.

![](https://i2.wp.com/blog.docker.com/wp-content/uploads/2019/07/f393ad07-c25d-4241-a40f-c6168e0ba4dd.jpg?ssl=1)

You should start by identifying all that's needed to build your application.

### Tip 10: Fetch dependencies in a separate step

![](https://i0.wp.com/blog.docker.com/wp-content/uploads/2019/07/41ea71ce-11c3-42a3-8d2b-05fe20901745.jpg?ssl=1)

By again thinking in terms of cacheable units of execution, we can decide that fetching dependencies is a separate cacheable unit that only needs to depend on changes to pom.xml and not the source code.

### Tip 11: Use multi-stage builds to remove build dependencies (recommended Dockerfile)

![](https://i1.wp.com/blog.docker.com/wp-content/uploads/2019/07/97ec1992-f0df-4c8f-82a0-e177c230e5c5.jpg?ssl=1)

Multi-stage builds is the go-to solution to remove build-time dependencies.
