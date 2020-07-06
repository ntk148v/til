# Creating and discovering plugins

Three major approaches to doing automatic plugin discovery

## 1. Using name convention

If all of the plugins for your application follow the same naming convention, you can use [pkgutil.iter_modules()](https://docs.python.org/3.6/library/pkgutil.html#pkgutil.iter_modules) to discover all of the top-level modules that match the naming convention.

```python
import importlib
import pkgutil

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('flask_')
}
```

## 2. Using namespace packages

[Namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/) can be used to provide a convetion for where to place plugins and also provides a way to perform discovery.

If you can make the sub-package `myapp.plugins` a namespace package then offer distributions can provide modules and packages to that namespace.

```python
import importlib
import pkgutil

import myapp.plugins

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(myapp.plugins)
}
```

## 3. Using package metadata

Setuptools provides special support for plugins. By providing the `entry_points` argument to setup() in `setup.py/setup.cfg` plugins can register themselves for discovery.

For example, you have a `setup.py`:

```python
setup(
    ...
    entry_points={'myapp.plugins': 'a = myapp_plugin_a'},
    ...
)
```

Then you can discover and load all of the registered entry points by using `pkg_resources.iter_entry_points()`:

```python
import pkg_resources

discovered_plugins = {
    entry_point.name: entry_point.load()
    for entry_point
    in pkg_resources.iter_entry_points('myapp.plugins')
}
```
