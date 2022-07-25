# Perfect Core

Source: <https://docs.prefect.io/core>

- Perfect Core is workflow engine that makes it easy to take your data pipelines and add sematics like retries, logging, dynamic mapping, caching, failure notifications, and more.

## 1. Concepts

- Perfect is a tool for building data workflows. A workflow is a series of steps that are performed in a certain order.
- Check [Perfect's documentation](https://docs.prefect.io/core/concepts/tasks.html#overview) for more details.
- `Task`: represents a discrete action in a Perfect workflow. A task is like a function.
  - Tasks may be run individually
  - Each task should represent a single logical step of your workflows.
  - Retries don't create new task run.

```python
# Simple
from prefect import task

@task
def plus_one(x):
    return x + 1
# Subclass the Task class directly
from prefect import Task

class HTTPGetTask(Task):

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password
        super().__init__(**kwargs)

    def run(self, url):
        return requests.get(url, auth=(self.username, self.password))
# Retries
# this task will retry up to 3 times, waiting 10 minutes between each retry
Task(max_retries=3, retry_delay=datetime.timedelta(minutes=10))
```

- `Flows`: a container for `Tasks`. It represents an entire workflow or application by describing the dependencies between tasks. Flows are **DAGs** (Direct acyclic graphs).
  - Build flow with **functional API**.

```python
from prefect import task, Task, Flow
import random

@task
def random_number():
    return random.randint(0, 100)

class PlusOneTask(Task):
    def run(self, x):
        return x + 1

# Build up a computational graph in the background
with Flow('My Functional Flow') as flow:
    r = random_number()
    task = PlusOneTask() # First create the Task instance
    result = task(r) # then call it with arguments

# Run a flow
state = flow.run()
state.result[result]
```

  - Build flow with **imperative API**.

```python
flow = Flow("My imperative flow!")

# define some new tasks
name = Parameter("name")
second_add = add.copy()

# add our tasks to the flow
flow.add_task(add)
flow.add_task(second_add)
flow.add_task(say_hello)

# create non-data dependencies so that `say_hello` waits for `second_add` to finish.
say_hello.set_upstream(second_add, flow=flow)

# create data bindings
add.bind(x=1, y=2, flow=flow)
second_add.bind(x=add, y=100, flow=flow)
say_hello.bind(person=name, flow=flow)
```

  - Can leverage a ready-to-use state database and UI backend that already works perfectly to orchestrate any of flows and make monitoring and orchestration easy.

```python
# Before registering, call `perfect backend server` to configure Perfect for local orchestration
flow.register()
```

- `Parameters`: special tasks that can receive user inputs whenever a flow is run.

```python
from prefect import task, Flow, Parameter

@task
def print_plus_one(x):
    print(x + 1)

with Flow('Parameterized Flow') as flow:
    x = Parameter('x', default = 2)
    print_plus_one(x=x)

flow.run(parameters=dict(x=1)) # prints 2
flow.run(parameters=dict(x=100)) # prints 101
flow.run() # prints 3
```

- `States`: all information about tasks and flows is transmitted with rich `State` objects.
  - All `State` objects have 3 important characteristics: a `type`, `message`, and `result`.
  - Flow state transitions: `Scheduled -> Running -> Success / Failed`.
  - Task state transitions: `Pending -> Running -> Finished (Success/Failed)`
- `Engine`: Perfect's execution model is built around 2 classes: `FlowRunner` and `TaskRunner`.
  - Executors: The executor classes are responsible for actually running tasks - `LocalExecutor`, `LocalDaskExecutor`, and `DaskExecutor`.
