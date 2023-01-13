# Asyncio

Source:

- <https://superfastpython.com/python-asyncio/>
- <http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/>
- <https://cheat.readthedocs.io/en/latest/python/asyncio.html>

Table of content:

- [Asyncio](#asyncio)
  - [1. Asynchronous Programming](#1-asynchronous-programming)
  - [2. What is asyncio?](#2-what-is-asyncio)
    - [2.1. Coroutine](#21-coroutine)
    - [2.2. Event loop](#22-event-loop)

## 1. Asynchronous Programming

- Alright, before we dive into asyncio library, let's talk about Asynchronous Programming? What is this? Generaly, **Asynchronous programming** is a programming paradigm that does not block.

![](http://blogs.quovantis.com/wp-content/uploads/2015/08/Synchronous-vs.-asynchronous.jpg)

- There are some terms you have to understand:

  - [**Asynchronous function call**](https://en.wikipedia.org/wiki/Asynchronous_procedure_call): request that a function is called at some time and in some manner, allowing the caller to resume and perform other activities.
  - **Future**: a handle on asynchronous function call allowing the status of the call to be checked and results to be retrieved.
  - **Asynchronous task**: used to refer to the aggregate of an asynchronous function call and resulting future.
  - **Non-blocking I/O**: performing I/O operations via asynchronous requests and responses, rather than waiting for operations to complete.
  - [**Asynchronous I/O**](https://en.wikipedia.org/wiki/Asynchronous_I/O): a shorthand that refers to combining asynchronous programming with non-blocking I/O.
  - [**Coroutine**](https://en.wikipedia.org/wiki/Coroutine):

    - Computer program component that generalizes subroutines for non-preemptive multitasking, by allowing execution to be suspended and resumed.
    - Or, this is _A function that can be suspended and resumed_.

    ![](https://www.modernescpp.com/images/blog/Cpp20/co_return/FunctionsVersusCoroutines.png)

- **Asynchronous programming** is the use of asynchronous techniques, such as issuing asynchronous tasks or function calls.
- Next, let's consider asynchronous programming support in Python: [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), [threading](https://docs.python.org/3/library/threading.html), and [asyncio](https://docs.python.org/3/library/asyncio.html).

![](https://uploads-ssl.webflow.com/5d2dd7e1b4a76d8b803ac1aa/5fc4d4d7136c7e1ffefdeb9c_3Yj-uX_DZuoCF4QKp_ONfdS_YEbxxc56Ee1sk_XZtreYRBrShwBlTL7LJko0Mm1MB-LiHuTT-ED6P0jx3ku0ZBx8KfeUB3BhWNaDfxDy0CdUA-pmYGlhFoAgQwSm1VHBNp_-8rLK.jpeg)

- When should choose which one? It really depends on the use cases. [Masnun's post](http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/) provides us a nice pseudo code:

  ```python
  if io_bound:
      if io_very_slow:
        print("Use Asyncio")
      else:
        print("Use Threads")
  else:
      print("Multi Processing")

  ```

- But this article is about asyncio, right? Let's take a closer look at asyncio.

## 2. What is asyncio?

- Python 3.4 introduced the asyncio library, and Python 3.5 produced the `async/await` expressions to use it palatably.
- asyncio takes a very, very explicit approach to asynchronous programming: only code written in methods flagged as `async` can call any code in an asynchronous way.
- The module provides both a high-level and low-level API.
  - The high-level API is for Python application developers.
  - The low-level API is for library and framework developers.

### 2.1. Coroutine

- A _coroutine_ is a method that can be paused when we have a potentially long-running task and then resumed when that task is finished. In Python, the language implemented first-class support for coroutines and asynchronous programming when the keywords `async` and `await` were explicitly added to the language.
- Coroutine vs Task:
  - A Future-like object that runs a Python coroutine. [...] Tasks are used to run coroutines in event loop. ([Python 3 docs](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task))
  - A coroutine can be wrapped in an `asyncio.Task` object and executed independently, as opposed to being executed directly within a coroutine. We will learn more about Task later.
- Coroutine vs Thread:
  - A coroutine is defined as a function.
  - A thread is an object created and managed by the underlying operating system and represented in Python as a `threading.Thread` object.
  - This means that coroutines are typically faster than thread.
  - Coroutine executes within one thread, therefore a single thread may execute many coroutines.
- Coroutine vs Process:
  - Processes, like threads, are created and managed by the underlying operating system and are represented by a `multiprocessing.Process` object.
- Enough talking, show me code:

```python ./custom_coro.py
```

### 2.2. Event loop

- Async code can only run inside an _event loop_. The event loop is the driver code that manages the [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking).
