# Python has too many package managers

Source: <https://dublog.net/blog/so-many-python-package-managers/>

[A new python dependency manager is like stumbling across a new Javascript](https://news.ycombinator.com/item?id=40911994)

There is one aspect of Python that has been an inexcusable pain-in-the ass over many years. That would be the fragmented Python package and environment management ecosystem, succinctly represented by the following XKCD comic:

![](https://dublog.net/images/python_environment_xkcd.png)

You see, a lot of other programming languages developed standardized ways to setup versioning, dependency resolution, and dev environment setup. C# has NuGet, Javascript has npm, Dart has pub, and most notably Rust has Cargo – quite possibly the most widely loved package manager tool in existence.

## 1. The sane way to do things

Package management would work like it does with Cargo - the rust package manager.
- A single master configuration TOML file where you simply list your dependencies and config settings.
- For extra reproducibility, whenever you build your environment and resolve all your package dependencies, a `\*.lock` file records all the packages you used along with their versions and hashes.
- Because dependency resolution is a directed acylic graph (DAG) resolution problem, the dependency retrieval and resolution should both be engineered to be relatively fast.

> WIP
