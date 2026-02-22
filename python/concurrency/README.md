# Python Concurrency

Source: <https://realpython.com/python-concurrency/>

- [Python Concurrency](#python-concurrency)
  - [1. Overview](#1-overview)
  - [2. How to Speed up an I/O-bound program](#2-how-to-speed-up-an-io-bound-program)
  - [3. How to Speed up a CPU-bound program](#3-how-to-speed-up-a-cpu-bound-program)

> Note that: This is not a complete version, you may want to check the original source for detail explaination.

## 1. Overview

- Definitions:

```txt
Concurrency (n): the fact of two or more events or circumstances happening or existing at the same time.
Conccurency (n - computing): the ability to execute more than one program or task simultaneously.
```

- In Python, the things that are occurring simultaneously are called by differented names (thread, task, process).
- _Same same but different_: These things are only the same if you view from the a high level. Once you start digging into the details, they all represent sightly different thing:
  - `mutiprocessing` actually runs at literally the same time.
  - `threading` and `asyncio` both run on a single processor and therefore only run one at time. But these things are different:
    - `threading`: Threads follow the model of [preemptive multitasking](https://en.wikipedia.org/wiki/Preemption_%28computing%29#Preemptive_multitasking). Each thread executes one task. OS schedule a thread on a CPU, and after a fixed interval (or when the thread gets blocked typically due to an IO operation, whichever happens first), OS interrupts the thread and schedules another waiting thread on CPU.
    - `asyncio`: In [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking), there is a queue of tasks. When a task is scheduled for execution, it executes till a point of its choice (typically an IO wait) and yields control back to the event loop scheduler, which puts it the waiting queue, and schedules another tasks. At any time, only one task is executing, but it gives an appearance of concurrency.

    ![](https://uploads-ssl.webflow.com/5e712f74eaa45ee264cce4d5/5e8dd0e1c5c5940f7f80fbbe_1*r94wLYporfXxgaIakEfBIA.png)

- In summary:

![](https://files.realpython.com/media/Screen_Shot_2018-10-17_at_3.18.44_PM.c02792872031.jpg)

| Concurrency Type                     | Switching Decision                                                    | Number of Processors |
| ------------------------------------ | --------------------------------------------------------------------- | -------------------- |
| Pre-emptive multitasking (threading) | The operating system decides when to switch tasks external to Python. | 1                    |
| Cooperative multitasking (asyncio)   | The tasks decide when to give up control.                             | 1                    |
| Multiprocessing (multiprocessing)    | The processes all run at the same time on different processors.       | Many                 |

- When is Concurrency useful? Concurrency can make a big difference for two types of problems. These are generally called CPU-bound and I/O-bound.

| I/O-Bound Process                                                                                                     | CPU-Bound Process                                                                        |
| --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Your program spends most of its time talking to a slow device, like a network connection, a hard drive, or a printer. | You program spends most of its time doing CPU operations.                                |
| Speeding it up involves overlapping the times spent waiting for these devices.                                        | Speeding it up involves finding ways to do more computations in the same amount of time. |

- We will follow same examples that show you how concurrency resolves these two problems.

## 2. How to Speed up an I/O-bound program

- Example: Donwload content over the network, you will be downloading web pages from a few sites, but it really could be any network traffic.
- [Synchronous version](./io_bound_sync.py):

  ```python
  import requests
  import time


  def download_site(url, session):
      with session.get(url) as response:
          print(f"Read {len(response.content)} from {url}")


  # download_all_sites() walks through a list of sites,
  # downloading each one in turn
  def download_all_sites(sites):
      with requests.Session() as session:
          for url in sites:
              download_site(url, session)


  if __name__ == "__main__":
      sites = [
          "https://www.jython.org",
          "http://olympus.realpython.org/dice",
      ] * 80
      start_time = time.time()
      download_all_sites(sites)
      duration = time.time() - start_time
      print(f"Downloaded {len(sites)} in {duration} seconds")
  ```

  ```shell
  $ python io_bound_sync.py
  [...]
  # Note that, network traffic is dependent on many factors. Therefore, your results
  # may vary significantly.
  Downloaded 160 in 40.372735023498535 seconds
  ```

- [`threading` version](./io_bound_threading.py):

  ```python
  import concurrent.futures
  import requests
  import threading
  import time


  thread_local = threading.local()


  # Each thread needs to create its own requests.Session() object.
  # Because the OS is in control of when your tasks gets interrupted
  # and another task starts, any data that is shared between threads
  # needs to be protected, or thread-safe. Unfortunately, requests.Session()
  # is not thread-safe.
  # Solution
  # threading.local() creates an object that looks like a global
  # but is specific to each thread.
  def get_session():
      if not hasattr(thread_local, "session"):
          thread_local.session = requests.Session()
      return thread_local.session


  def download_site(url):
      session = get_session()
      with session.get(url) as response:
          print(f"Read {len(response.content)} from {url}")


  def download_all_sites(sites):
      # ThreadPoolExecutor = Thread + Pool + Executor
      # Thread
      # Pool: create a pool of threads, each of which can run concurrency.
      # Executor: the part that's going to control how and when each of the
      #           threads in the pool will run.
      # Use as context manager to mange creating and freeing the pool of Threads.
      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
          executor.map(download_site, sites)


  if __name__ == "__main__":
      sites = [
          "https://www.jython.org",
          "http://olympus.realpython.org/dice",
      ] * 80
      start_time = time.time()
      download_all_sites(sites)
      duration = time.time() - start_time
      print(f"Downloaded {len(sites)} in {duration} seconds")
  ```

  ```shell
  $ python io_bound_sync.py
  [...]
  # Note that, network traffic is dependent on many factors. Therefore, your results
  # may vary significantly.
  Downloaded 160 in 10.222740650177002 seconds
  ```

  - Execution diagram: It uses multiple threads to have multiple one requests out of websites at the same time.

  ![](https://files.realpython.com/media/Threading.3eef48da829e.png)
  - Problem: Threads can interact in ways that are subtle and hard to detect. These interactions can cause race conditions that frequently result in random, intermittent bugs that can be quite difficult to find.

- [`asyncio` version](./io_bound_asyncio.py).
  - A single Python object - event loop, controls how and when each task gets run. The event loop is aware of each task and knows what state it's in.
  - The tasks never give up control without intentionally doing so.
  - The main flow:

  ![](https://www.pythontutorial.net/wp-content/uploads/2022/07/python-event-loop.svg)
  - `async` and `await`: `await` allows the task to hand control back to the event loop. `async`: that function about to be defined uses `await`.

  ```python
  import asyncio
  import time

  import aiohttp


  async def download_site(session, url):
      async with session.get(url) as response:
          print("Read {0} from {1}".format(response.content_length, url))


  async def download_all_sites(sites):
      # Tasks can share a session because they are all running on the same thread
      async with aiohttp.ClientSession() as session:
          tasks = []
          for url in sites:
              task = asyncio.ensure_future(download_site(session, url))
              tasks.append(task)
          # Keep the session context alive until all of tasks have completed.
          await asyncio.gather(*tasks, return_exceptions=True)

  if __name__ == "__main__":
      sites = [
          "https://www.jython.org",
          "http://olympus.realpython.org/dice",
      ] * 80
      start_time = time.time()
      # Python >=3.7
      asyncio.run(download_all_sites(sites))
      # Legacy
      # asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
      duration = time.time() - start_time
      print(f"Downloaded {len(sites)} sites in {duration} seconds")
  ```

  - The execution diagram:

  ![](https://files.realpython.com/media/Asyncio.31182d3731cf.png)
  - Note that, there is no way for the eventloop to break in if a task does not hand control back to it -> run off and hold process for a long time.

- [`multiprocessing` version](./io_bound_multiprocessing.py).

  ```python
  import requests
  import multiprocessing
  import time

  session = None


  def set_global_session():
      global session
      if not session:
          session = requests.Session()


  def download_site(url):
      if session is None:
          return
      with session.get(url, verify=False) as response:
          name = multiprocessing.current_process().name
          print(f"{name}:Read {len(response.content)} from {url}")


  def download_all_sites(sites):
      # Pool creates a number of separate Python interpreter processes and
      # has each one run the specified function on some of the items
      # in the iterable - a list of sites.
      # initializer=set_global_session: Each process in Pool has its own memory
      # space, so we create one session for each process. Initialize a global
      # session variable to hold the single session for each process.
      with multiprocessing.Pool(initializer=set_global_session) as pool:
          pool.map(download_site, sites)


  if __name__ == "__main__":
      sites = [
          "https://www.jython.org",
          "http://olympus.realpython.org/dice",
      ] * 80
      start_time = time.time()
      download_all_sites(sites)
      duration = time.time() - start_time
      print(f"Downloaded {len(sites)} in {duration} seconds")
  ```

  ```shell
  $ python io_bound_multiprocessing.py
  [...]
  Downloaded 160 in 5.616464614868164 seconds
  ```

  - The execution diagram:

  ![](https://files.realpython.com/media/MProc.7cf3be371bbc.png)

## 3. How to Speed up a CPU-bound program

- An I/O-bound problem spends most of its time waiting for external operations, like a network call, to complete. A CPU-bound problem, on the other hand, does few I/O operations, and its overall execution time is a factor of how fast it can process the required data.
- [Sync version](./cpu_bound_sync.py)

  ```python
  import time


  def cpu_bound(number):
      return sum(i * i for i in range(number))


  def find_sums(numbers):
      for number in numbers:
          cpu_bound(number)


  if __name__ == "__main__":
      numbers = [5_000_000 + x for x in range(20)]

      start_time = time.time()
      find_sums(numbers)
      duration = time.time() - start_time
      print(f"Duration {duration} seconds")
  ```

  ```shell
  $ python cpu_bound_sync.py
  Duration 21.667335033416748 second
  ```

  - The execution diagram:

  ![](https://files.realpython.com/media/CPUBound.d2d32cb2626c.png)

- [`threading` version](./cpu_bound_threading.py)

  ```python
  import concurrent.futures
  import time


  def cpu_bound(number):
      return sum(i * i for i in range(number))


  def find_sums(numbers):
      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
          executor.map(cpu_bound, numbers)


  if __name__ == "__main__":
      numbers = [5_000_000 + x for x in range(20)]

      start_time = time.time()
      find_sums(numbers)
      duration = time.time() - start_time
    print(f"Duration {duration} seconds")
  ```

  ```shell
  $ python cpu_bound_threading.py
  Duration 22.9144287109375 seconds
  ```

  - Threading version shows a slower result. Because threads (and tasks) run on the same CPU in the same process. That means that the one CPU is doing all of the work of the non-concurrent code + the extra work of setting up threads or tasks.

- [`multiprocessing` version](./cpu_bound_multiprocessing.py)

  ```python
  import multiprocessing
  import time


  def cpu_bound(number):
      return sum(i * i for i in range(number))


  def find_sums(numbers):
      with multiprocessing.Pool() as pool:
          # map() method to send individual number
          # to worker-processes as they become free
          pool.map(cpu_bound, numbers)


  if __name__ == "__main__":
      numbers = [5_000_000 + x for x in range(20)]

      start_time = time.time()
      find_sums(numbers)
      duration = time.time() - start_time
      print(f"Duration {duration} seconds")
  ```

  ```shell
  $ python cpu_bound_multiprocessing.py
  Duration 5.507646322250366 seconds
  ```

  - The execution diagram:

  ![](https://files.realpython.com/media/CPUMP.69c1a7fad9c4.png)
  - Problem: sometimes it requires more communication between the process -> complex!
