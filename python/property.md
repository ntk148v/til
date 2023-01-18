# Python @property

[Source](https://www.programiz.com/python-programming/property)

## A example

```python
class Celsius:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32
```

We could make objects out of this class and manipulate the attribute `temperature` as we wished.

```sh
>>> cel = Celsius()
>>> cel.temperature = 37
>>> cel.__dict__
{'temperature': 37}
```

Therefore, `cel.temperature` internally becomes `cel.__dict__['temperature']`. Some clients started using class in their program. They did all kinds of assignments to the object.

But something wents wrong here. The temperatures cannot go bellow [-273 degree celsius](https://en.wikipedia.org/wiki/Celsius). So upgrading class will be needed. One more version will be released afterwards.

## Using getters and setters

Another solution will be to hide the attribute `temperature` (make it private) and define new getter and setter interfaces to manipulate it.

```python
class Celsius:
    def __init__(self, temperature=0):
        self.set_temperature(temperature)

    def to_fahrenheit(self):
        return (self.get_temperature() * 1.8) + 32

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")>
        self._temperature = value
```

Please note that private variables don't exist in Python. The language itself don't apply any restrictions.

But the above update still has a big problem, all users who implemented class Celsius have to modify their code from `obj.temperature` to `obj.get_temperature()`... In other words, it means this refactoring was not backward compatible.

## The Power of @property

```python
class Celsius:
    def __init__(self, temperature = 0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        self._temperature = value

    temperature = property(get_temperature,set_temperature)
```

Any code that retrieves the value of `temperature` will automatically call `get_temperature()` instead of a dictionary lookup. Similarly, any code that assigns a valye to `temperature` will automatically call `set_temperature()`.

Note that, the actual temperature value is stored in the private variable `_temperature`. The attribute `temperature` is a property object which provides interface to this private variable.

## Diggin Deeper into Property

```python
property(fget=None, fset=None, fdel=None, doc=None)
```

A property object has 3 methods, `getter()`, `setter()` and `deleter()` to specify `fget`, `fset` and `fdel`.

```python
temperature = property(get_temperature,set_temperature)
# Break down!
# make empty property
temperature = property()
# assign fget
temperature = temperature.getter(get_temperature)
# assign fset
temperature = temperature.setter(set_temperature)
```

Enhancement with Python decorators

```python
class Celsius:
    def __init__(self, temperature = 0):
        self._temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        self._temperature = value
```
