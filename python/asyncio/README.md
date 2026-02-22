# Asyncio

Source:

- <https://superfastpython.com/python-asyncio/>
- <http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/>
- <https://cheat.readthedocs.io/en/latest/python/asyncio.html>
- <https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-2.html>

Table of contents:

- [Asyncio](#asyncio)
  - [1. Asynchronous Programming](#1-asynchronous-programming)
  - [2. What is asyncio?](#2-what-is-asyncio)
    - [2.1. Coroutine](#21-coroutine)
    - [2.2. Event loop](#22-event-loop)
    - [2.3. Task](#23-task)
  - [3. Play with asyncio](#3-play-with-asyncio)
    - [3.1. asyncio.gather()](#31-asynciogather)
    - [3.2. asyncio.wait() and asyncio.wait_for()](#32-asynciowait-and-asynciowait_for)
    - [3.3. asyncio.shield()](#33-asyncioshield)
    - [3.4. Blocking task in asyncio](#34-blocking-task-in-asyncio)
    - [3.5. Handle exception](#35-handle-exception)
    - [3.5. Common errors](#35-common-errors)

> **NOTE**:
> Most of examples in this post are taken from **Source**.
> Always a WIP post

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
  - Calling a coroutine does not execute it, but rather returns a coroutine object.
  - How to run it? The answer is using event loop. _Coroutine objects can only run when event loop is running_. Let's move to the next section.

```python
async def custom_coro():
    return 2+2


async def main():
    # await for custom coroutine
    result = await custom_coro()
    print(result)


m = main()
# not executed yet; coro is a coroutine, not 4
print(type(m))

# <class 'coroutine'>
# sys:1: RuntimeWarning: coroutine 'main' was never awaited
```

### 2.2. Event loop

- Async code can only run inside an _event loop_. The event loop is the driver code that manages the [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking). This is a heart of asyncio, it does many things:
  - Execute coroutines
  - Execute callbacks
  - Preform network i/o
  - Run subprocesses
- Let's run the previous example:

```python
import asyncio


async def custom_coro():
    return 2+2


async def main():
    # await for custom coroutine
    result = await custom_coro()
    print(result)

m = main()

# start the coroutine program
asyncio.run(m)

# 4
```

- `asyncio` module provides functions for accessing and interacting with the event loop - low level.
  - Create/Get a loop:
    - [`asyncio.new_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.new_event_loop): create and return a new event loop object.

    ```python
    import asyncio

    # create and access a new asyncio event loop
    loop = asyncio.new_event_loop()
    # report defaults of the loop
    print(loop)

    # <_UnixSelectorEventLoop running=False closed=False debug=False>

    ```

    - [`asyncio.get_running_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop) (Python >= 3.7): returns the running event loop in the current OS thread. If there is no running event loop a RuntimeError is raised. This function can only be called from a coroutine or a callback.

  - Run a loop:
    - If you want to a long-running loop that keeps responding to events untils it's told to stop, use [`loop.run_forever()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_forever)
    - If you want to compute some finite work using coroutines and then stop, use [`loop.run_until_complete(<future or coroutine>)`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_until_complete).
  - Stop a loop: [`loop.stop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.stop).
  - Get a loop to call an awaitable: Use [`asyncio.ensure_future`](https://docs.python.org/3/library/asyncio-task.html#asyncio.ensure_future).
  - Run blocking code in another thread: If you need to call some blocking code from a coroutine, and don’t want to block the whole thread, you can make it run in another thread using coroutine [`loop.run_in_executor`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_in_executor)

  ```python
  fn = functools.partial(method, *args)
  result = await loop.run_in_executor(None, fn)
  ```

- For application developers, should typically use the high-levle asyncio functions `asyncio.run()`, and should rarely need to reference the loop object or call its method.
  - `asyncio.run()`: always creates a new event loop and closes it at the end. It should be used as a main entry point for asyncio programs, and should ideally only be called once. [Python 3 docs](https://docs.python.org/3/library/asyncio-task.html)

### 2.3. Task

- Tasks provide a handle on independently scheduled and running coroutines and allow the task to be queried, cancelled, and results and exceptions to be retrieved later.
  - The _asyncio event loop_ manages _tasks_. As such, all _coroutines_ become and are managed as _tasks_ within the event loop.
  - A Future is a special
- There are 2 main ways to create and schedule a task:
  - Create task with high-level API: [`asyncio.create_task`](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task).

  ```python
  # define a coroutine
  async def task_coroutine():
      # ...
  # create a task from a coroutine
  task = async.create_task(task_coroutine())
  ```

  - Create task with low-level API:
    - [`asyncio.ensure_future`](https://docs.python.org/3/library/asyncio-future.html#asyncio.ensure_future)

    ```python
    # create and schedule a task
    task = asyncio.ensure_future(task_coroutine())
    ```

    - [`loop.create_task`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_task):

    ```python
    # get the current event loop
    loop = asyncio.get_event_loop()
    # create and schedule the task
    task = loop.create_task(task_coroutine())
    ```

- Although we can schedule a coroutine to run independently as a task with the `create_task()` function, it may not run immediately. In fact, the task will not execute until the event loop has an opportunity to run.

```python
import asyncio


async def task_coroutine():
    print('execute the task')
    # wait for a bit
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    # wait for the task to complete
    await task
    print('main coroutine done')


# start the asyncio program
asyncio.run(main())

# main coroutine started
# execute the task
# main coroutine done
```

- This is good to know task's life cycle:
  - You can check whether task is done or is cancelled (`done()`, `cancelled()`).
  - To get its result, use `result()`.
  - To get its exception, use `exception()`.

  ![](https://superfastpython.com/wp-content/uploads/2022/09/Asyncio-Task-Life-Cycle.png)

- One more thing, we can add a done callback to a task via `add_done_callback()`. This method tasks the name of a function call when the task is done.

```python
import asyncio


def callback(task):
    print('this is a callback of', task)


async def task_coroutine():
    print('execute the task')
    # wait for a bit
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    task.add_done_callback(callback)
    # wait for the task to complete
    await task
    print('main coroutine done')


# start the asyncio program
asyncio.run(main())

# main coroutine started
# execute the task
# this is a callback of <Task finished name='Task-2' coro=<task_coroutine() done, defined at /.../run_task_callback.py:8> result=None>
# main coroutine done
```

- Create many tasks:

```python
import asyncio


async def task_coroutine(index):
    print(f'task {index} is running')
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # start many tasks
    started_tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    # allow some of the tasks time to start
    await asyncio.sleep(1)
    # get all tasks
    tasks = asyncio.all_tasks()

    for task in tasks:
        print(f'> {task.get_name()}, {task.get_coro()}')

    for task in started_tasks:
        await task

asyncio.run(main())

# main coroutine started
# task 0 is running
# task 1 is running
# task 2 is running
# task 3 is running
# task 4 is running
# task 5 is running
# task 6 is running
# task 7 is running
# task 8 is running
# task 9 is running
# > Task-3, <coroutine object task_coroutine at 0x7fbab1016e30>
# > Task-6, <coroutine object task_coroutine at 0x7fbab0ea4c10>
# > Task-11, <coroutine object task_coroutine at 0x7fbab0ea4e40>
# > Task-2, <coroutine object task_coroutine at 0x7fbab1016ce0>
# > Task-9, <coroutine object task_coroutine at 0x7fbab0ea4d60>
# > Task-4, <coroutine object task_coroutine at 0x7fbab10175a0>
# > Task-7, <coroutine object task_coroutine at 0x7fbab0ea4c80>
# > Task-5, <coroutine object task_coroutine at 0x7fbab0ea49e0>
# > Task-10, <coroutine object task_coroutine at 0x7fbab0ea4dd0>
# > Task-8, <coroutine object task_coroutine at 0x7fbab0ea4cf0>
# > Task-1, <coroutine object main at 0x7fbab1016650>
```

## 3. Play with asyncio

We will go through some common usage.

### 3.1. asyncio.gather()

- [`asyncio.gather()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather): allows the caller to group multiple awaitables together.
  - Call `gather()` with:
    - Multiple tasks
    - Multiple coroutines
    - Mixture of tasks and coroutines
  - It returns an `asyncio.Future` object that represents the group of awaitables.
- Run many coroutines:
  - Allow a program to prepare the tasks that are to be executed concurrently and then trigger their execution all at once and wait for them to complete.

  ```python
  import asyncio


  async def task_coroutine(index):
      print(f'> task {index} executing')
      await asyncio.sleep(2)


  async def main():
      print('main coroutine started')
      group_coros = [task_coroutine(i) for i in range(10)]
      await asyncio.gather(*group_coros)
      print('main done')

  asyncio.run(main())

  # main coroutine started
  # > task 0 executing
  # > task 1 executing
  # > task 2 executing
  # > task 3 executing
  # > task 4 executing
  # > task 5 executing
  # > task 6 executing
  # > task 7 executing
  # > task 8 executing
  # > task 9 executing
  # main done
  ```

### 3.2. asyncio.wait() and asyncio.wait_for()

- [`asyncio.wait()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait): wait for a collection of asyncio tasks to complete. The call to wait can be configured to wait for different conditions, such as all tasks being completed, the first task completed and the first task falling with an error.

```python
import asyncio
import random


async def task_coroutine(index):
    value = random.random()
    print(f'> task {index} executing')
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')


async def main():
    print('main coroutine started')
    tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    # wait for all tasks to complete
    done, pending = await asyncio.wait(tasks)
    # wait for the first tasks to complete
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # wait for the first tasks to failed
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    # you can play with done and pending
    print('main done')

asyncio.run(main())

# main coroutine started
# > task 0 executing
# > task 1 executing
# > task 2 executing
# > task 3 executing
# > task 4 executing
# > task 5 executing
# > task 6 executing
# > task 7 executing
# > task 8 executing
# > task 9 executing
# > task 4 done after sleep 0.02505134629289052 seconds
# > task 0 done after sleep 0.15302129609152493 seconds
# > task 8 done after sleep 0.1565534467066032 seconds
# > task 5 done after sleep 0.1676313361328544 seconds
# > task 1 done after sleep 0.3886707880704876 seconds
# > task 3 done after sleep 0.45932413337182765 seconds
# > task 6 done after sleep 0.5445482469243019 seconds
# > task 2 done after sleep 0.6234779487073143 seconds
# > task 9 done after sleep 0.7615839933532805 seconds
# > task 7 done after sleep 0.7726912337045355 seconds
# main done
```

- You can wait for an asyncio task or coroutine to complete _with a timeout_ using `asyncio.wait_for()` function.

```python
import asyncio


async def task_coroutine(index):
    print(f'> task {index} executing')
    value = 2
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')


async def main():
    print('main coroutine started')
    # create a task
    task = task_coroutine(1)

    try:
        # you can change timeout and sleep (in task_coroutine)
        # to play with it
        await asyncio.wait_for(task, timeout=3)
        print('main done')
    except asyncio.TimeoutError:
        print('main gave up waiting , task cancelled')

asyncio.run(main())

# main coroutine started
# > task 1 executing
# main gave up waiting , task cancelled
```

### 3.3. asyncio.shield()

- Asyncio task can be cancelled by calling `cancel()` method, but you can protect a task from being cancelled by wrapping it to `asyncio.shield()`.

```python
import asyncio


async def task_coroutine(index):
    print(f'> task {index} executing')
    value = 2
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')

# cancel the given task after a moment


async def cancel_task(task):
    # block for a moment
    await asyncio.sleep(1)
    # cancel the task
    cancelled = task.cancel()
    print(f'cancelled: {cancelled}')


async def main():
    print('main coroutine started')
    # create a task
    coro = task_coroutine(1)
    task = asyncio.create_task(coro)
    shielded = asyncio.shield(task)
    #  create a task to cancel the first task
    asyncio.create_task(cancel_task(shielded))

    try:
        result = await shielded
        print(f'> got: {result}')
    except asyncio.cancelledError:
        print('shield was cancelled')

    await asyncio.sleep(0.5)
    print(f'shielded: {shielded}')
    print(f'task: {task}')
    print('main done')

asyncio.run(main())

# main coroutine started
# > task 1 executing
# cancelled: True
# shield was cancelled
# shielded: <Future cancelled>
# task: <Task pending name='Task-2' coro=<task_coroutine() running at .../shield.py:7> wait_for=<Future pending cb=[Task.task_wakeup()]>>
# main done
```

### 3.4. Blocking task in asyncio

- The focus of asyncio is asynchronous programming and non-blocking IO. Nevertheless, we often need to execute a blocking function call within an asyncio program -> it will cause the event loop to stop, preventing any other coroutines from progressing.
- asyncio provides 2 ways to solve this.
  - [`asyncio.to_thread()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread) (high level API):
    - I/O Bound Task.

  ```python
  import asyncio
  import time


  def blocking_task():
      print('> task starting')
      time.sleep(2)
      print('> task done')


  async def main():
      print('main running the blocking task')
      # to_thread creates a ThreadPoolExecutor behind the scenes
      # to execute blocking calls
      coro = asyncio.to_thread(blocking_task)
      task = asyncio.create_task(coro)
      print('main doing other things')
      await asyncio.sleep(1)
      await task

  # run the asyncio
  asyncio.run(main())

  # main running the blocking task
  # main doing other things
  # > task starting
  # > task done
  ```

  - [`loop.run_in_executor`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor) (low level API): tasks an executor and a function to execute.

  ```python
  import asyncio
  import time


  def blocking_task():
      print('> task starting')
      time.sleep(2)
      print('> task done')


  async def main():
      print('main running the blocking task')
      loop = asyncio.get_running_loop()
      # execute a function in a separate thread
      # If None -> ThreadPoolExecutor
      # Can pass ProcessPoolExecutor
      await loop.run_in_executor(None, blocking_task)
      print('main doing other things')
      await asyncio.sleep(10)

  # run the asyncio
  asyncio.run(main())

  # main running the blocking task
  # > task starting
  # > task done
  # main doing other things
  ```

### 3.5. Handle exception

- A coroutine wrapped by a task may raise an exception that is not handled. You can retrieve this kind of exception via `exception() method`.

```python
import asyncio


async def task_coroutine():
    print('> executing the task')
    await asyncio.sleep(1)
    raise Exception('Something went wrong')


async def main():
    print('main coroutine started')
    task = asyncio.create_task(task_coroutine())
    await asyncio.sleep(2)
    ex = task.exception()
    print(f'got exception: {ex}')
    print('main coroutine done')

asyncio.run(main())


# main coroutine started
# > executing the task
# got exception: Something went wrong
# main coroutine done

# # Without exception() call
# main coroutine started
# > executing the task
# main coroutine done
# Task exception was never retrieved
# future: <Task finished name='Task-2' coro=<task_coroutine() done, defined at ...exception.py:4> exception=Exception('Something went wrong')>
# Traceback (most recent call last):
#   File "...exception.py", line 7, in task_coroutine
#     raise Exception('Something went wrong')
# Exception: Something went wrong
```

- You can't retrieve an exception from a cancelled task. Instead, `CancelledError` exception is raised when calling the `exception()` method.
- Awaiting a task that fails with an exception will cause the exception to be propagated to the caller. You have to handle with the try/except.

```python
import asyncio


async def task_coroutine():
    print('> executing the task')
    await asyncio.sleep(1)
    raise Exception('Something went wrong')


async def main():
    print('main coroutine started')
    task = asyncio.create_task(task_coroutine())
    try:
        await task
    except Exception as ex:
        print(f'got exception: {ex}')
    print('main coroutine done')

asyncio.run(main())

# main coroutine started
# > executing the task
# got exception: Something went wrong
# main coroutine done
```

### 3.5. Common errors

- Trying to run coroutines by calling them

```python
async def coro():
    print('shit')

# error attempt at calling  a coroutine like a function
coro()

# right thing to do
# run a coroutine
asyncio.run(coro())

# suspend the current coroutine and schedule the other coroutine using await
await coro()
```

- Not letting coroutines run in the event loop

```python
# create a coroutine object
coro = coro()
# got RuntimeError if you don't run it

# right thing to do
asyncio.run(coro)

# schedule coroutine to run independently as a task
task = asyncio.create_task(coro)
```

- Using the asyncio low-level API
- Exiting the main coroutine too early: the main coroutine has nothing else to do, it should wait on the remaining tasks.

```python
all_tasks = asyncio.all_tasks()
# get the current task
current_task = asyncio.current_task()
# remove the current task from the list of all tasks
all_tasks.remove(current_task)
# suspend until all tasks are completed
await asyncio.wait(all_tasks)
```

- Assuming race conditions and deadlocks are not possible:
  - A _race condition_ involves two or more units of concurrency executing the same ciritcal section at the same time and leaving a resource or data in an inconsitent or unexpected state. That can lead to data conrruption and data loss.
  - A _deadlock_ is when a unit of concurrency waits for a condition that can never occur, such as for a resource to become available.
