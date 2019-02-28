# StackStorm

## What is StackStorm?

StackStorm is a platform for integration and automation across services and tools.

StackStorm helps automate common operational patterns:
* Facilitataed Troubleshooting.
* Automated remediation.
* Continuos Deployment.

## How it works?

![stackstorm-architecture](https://docs.stackstorm.com/_images/architecture_diagram.jpg)

StackStorm plugs into the environment via the extensible set of adapters containing sensors and actions.
* Sensors: Python plugins for either inbound or outbound integration that receives or watches for events respectively.
* Triggers: StackStorm representations of external events.
* Actions: StackStorm outbound integrations.
* Rules: map triggers to actions (or to workflows), applying matching criteria and mapping trigger payload to action inputs.
* Workflows: stich actions together into "uber-actions", defining the order, transition conditions, and passing the data.
* Packs: the units of content deployment.
* Audit trail: of action executions, manual or automated, is recorded and stored with full detilas of triggering context and execution results.

## Automation basics

### Actions

* Perform arbitrary automation or remendiation tasks in your environment.

* Actions can be executed when a Rule with matching criteria is triggered. Multiple actions can be strung together into a Workflow.

* **An action runner** is the execution environment for user-implemented actions.

* An action is composed of two parts:
    * A YAML metadata file which describes the action, and its inputs.
    * A script file which implements the action logic.

* **Built-in Parameters**: args, cmd, cwd, env, dir.

* Parameters of runners can be overridden but not all attributes for runner parameters can be overridden.

* **Environment Variables Available to Actions:
    * ST2\_ACTION\_PACK\_NAME: name of the pack which the currently executed action belongs to.
    * ST2\_ACTION_\_EXECUTION\_ID: execution id of the action being currently executed.
    * ST2\_ACTION\_API\_URL: full url to the public API endpoint.
    * ST2\_ACTION\_AUTH\_TOKEN: auth token which is available to the action until it completes. When the action completes, the token gets revoked.

* Convert Existing scripts into Actions:
    * Make sure the script conforms to conventions.
    * Create a metadata file.
    * Update argument parsing in the script.
* Writing Custom Python Actions - Example.

```yaml
---
name: "echo_action"
runner_type: "python-script"
description: "Print message to standard output."
enabled: true
entry_point: "my_echo_action.py"
parameters:
    message:
        type: "string"
        description: "Message to print."
        required: true
        position: 0
```

```python
# my_echo_action.py
import sys

from st2common.runners.base_action import Action

class MyEchoAction(Action):
    def run(self, message):
        print(message)

        if message == 'working':
            return (True, message)
        return (False, message)
```

* Pre-defined actions: `core` pack (`core.local, core.remote, core.http`) 

### Sensors and Triggers

* Sensors are a way to integrate external systems and events with StackStorm (periodically poll some external system/passively wait for inbound events). Sensors are written in Python, and must follow the StackStorm-defined sensor interface requirements.

```yaml
# metadata file
---
  class_name: "SampleSensor"
  entry_point: "sample_sensor.py"
  description: "Sample sensor that emits triggers."
  trigger_types:
    -
      name: "event"
      description: "An example trigger."
      payload_schema:
        type: "object"
        properties:
          executed_at:
            type: "string"
            format: "date-time"
            default: "2014-07-30 05:04:24.578325"
```

```python
from st2reactor.sensor.base import PollingSensor
from st2reactor.sensor.base import Sensor


class SampleSensor(Sensor):
    # ....

class SamplePollingSensor(PollingSensor):
    # ....
```

* Triggers are StackStorm constructs that identify the incoming events to StackStorm. A trigger is a tuple of type (string) and optional parameters (object). Rules are written to work with triggers. Sensors typically register triggers thouygh this is not strictly required.

* Each sensor runs as a separate process.

* Sensor service provides different services to the sensor via public methods.

* Common operations:
    * `dispatch(trigger, payload, trace_tag)`: Allows the sensor to inject trigger into the system.
    * `get_logger(name)`: Allows the sensor instance to retrieve the logger instance which is specific to that sensor.

* Datastore management operations:
    * `list_values(local=True, prefix=None)`: Allows to list the values in the datastore.
    * `get_value(name, local=True, decrypt=False)`: Allows to retrive a single value from the datastore.
    * `set_value(name, value, ttl=None), local=True, encrypt=False)`: Allows to store (set_) a value in the datastore.
    * `delete_value(name, local=True)`: Allows to delete an existing value from the datastore.
