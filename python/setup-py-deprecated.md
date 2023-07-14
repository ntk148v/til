# Why you shouldn't invoke setup.py directly?

Source: <https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html>

**TL;DR**: The `setuptools` team no longer wants to be in the business of providing a command line interface and is actively working to become just a library for building packages. What you should do instead depends on your use case, but if you want some basic rules of thumb, there is a table in the [summary section](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html#summary).

This does not mean that `setuptools` itself is deprecated, or that using setup.py to configure your package builds is going to be removed. The only thing you must stop doing is directly executing the setup.py file — instead delegate that to purpose-built or standards-based tools, preferably those that work with any build backend.
