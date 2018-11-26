## OpenStack Mistral

> Just a clone of OpenStack Mistral official documentation.

## What is Mitral?

Mistral is OpenStack workflow service. The main aim of the project is to provide capability to define, execute and manage tasks and workflows without writing code.

## Use cases

* Cloud Cron: a system administrator can scheduler cloud tasks for periodical execution.
* Cloud Environment Deployment: tools like Heat can represent deployment steps as a workflow and use Mistral to run it.
* Live Migration: on CPU close to 100% run specific migration workflow.
* Long-Running Business Process.
* Big Data Analysis & Reporting.

## Basic concepts

* Workflow: consists of tasks (at least one) describing what exact.
* Task: an activity executed within the workflow definition.
* Action: work done when an exact task is triggered.

## Mistral components

![mistral-architecture](https://docs.openstack.org/mistral/latest/_images/mistral_architecture.png)

* API server: Exposes REST API to operate and monitor the workflow executions.
* Engine: Pick ups the workflows from the workflow queue. It handles the control and dataflow of workflow of workflow exectuions. It also computes which tasks are ready and places them in a task queue. It passes the data from task to task, deals with condition transitions...
* Task executors: Executes task actions. It picks up the tasks from the queue, run actions, and sends results back to the engine.
* Scheduler: Stores and executes delayed calls, triggers workflows on events.
* Notifier: On workflow and task execution, events are emitted at certain checkpoints such as when a workflow execution is launched or when it is completed. The notifier routes the events to configured publishers. The notifier can either be configured to execute locally on the workflow engine or can be run as a server much like the remote executor server and listens for events. Running the notifier as a remote server ensures the workflow engine quickly unblocks and resumes work.
* Persistence: Stores workflow definitions, current execution states and past execution results.

## Terminology

### Workbooks

* Combine multiple entities of any type (workflows and actions) into one document.
* Upload to Mistral service.
* Mistral will parse it and saves its workflows and actions as independent objects which will be accessible via their own API endpoints.
* Namespacing: Mistral uses workbook name as a prefix for generating final names of workflows and actions included into the workflow.

![mistral-workbook-namespacing](https://docs.openstack.org/mistral/latest/_images/Mistral_workbook_namespacing.png)

* YAML template:

```yaml
---
version: '2.0'

name: # Workbook name. Required
description: # Workbook description. Optional
tags: # String with arbitraty comma-separated. Optional
workflows: # Dictionary containing workflow definitions. Optional
actions: # Dictionary containting ad-hoc action definitions. Optional
```

### Workflows

* Workflow represents a process that can be described in a various number of ways and that can do some jobs. Each workflows consists of tasks (at least one) describing what exact steps should be made during workflow execution.
* **Direct workflow**: consists of tasks combined in a graph where every next task after another one depending on produced result. Direct workflow is considered to be completed if there aren't any transitions left that could be used to jump to next tasks.

![direct-workflow](https://docs.openstack.org/mistral/latest/_images/Mistral_direct_workflow.png)

```yaml
---
version: '2.0'
create_vm_and_send_email:
  type: direct
  input:
    - vm_name
    - image_id
    - flavor_id
  output:
    result: <% $.vm_id %>
  tasks:
    create_vm:
      action: nova.servers_create name=<% $.vm_name %> image=<% $.image_id %> flavor=<% $.flavor_id %>
      publish:
        vm_id: <% $.id %>
      on-error:
        - send_error_email
      on-success:
        - send_success_email
    send_error_email:
      action: send_email to='admin@mysite.org' body='Failed to create a VM'
      on-complete:
        - fail
    send_success_email:
      action: send_email to='admin@mysite.org' body='Vm is successfully created and its id is <% $.vm_id %>'
```

* **Reverse workflow**: all relationships in workflow task graph are dependencies. In order to run this type of workflow we need to specify a task that needs to be completed - `target task`.
    * Task T1 is chosen a target task. So when the workflow starts Mistral will run only tasks T7, T8, T5, T6, T2 and T1 in the specified order (starting from the tasks that have no dependencies).

![reverse-workflow](https://docs.openstack.org/mistral/latest/_images/Mistral_reverse_workflow.png)

```yaml
---
version: '2.0'
create_vm_and_send_email:
  type: reverse
  input:
    - vm_name
    - image_id
    - flavor_id
  output:
    result: <% $.vm_id %>
  tasks:
    create_vm:
      action: nova.servers_create name=<% $.vm_name %> image=<% $.image_id %> flavor=<% $.flavor_id %>
      publish:
        vm_id: <% $.id %>
    search_for_ip:
      action: nova.floating_ips_findall instance_id=null
      publish:
        vm_ip: <% $[0].ip %>
    associate_ip:
      action: nova.servers_add_floating_ip server=<% $.vm_id %> address=<% $.vm_ip %>
      requires: [search_for_ip]
    send_email:
      action: send_email to='admin@mysite.org' body='Vm is created and id <% $.vm_id %> and ip address <% $.vm_ip %>'
      requires: [create_vm, associate_ip]
```

### Actions

* Actions are a particular instruction associated with a task that will be performed when the task runs (running a shell script, making an HTTP request, or sending a signal to an external system)
* Actions can be synchronous or asynchronous:
    * Synchronous action:

    ![sync-action](https://docs.openstack.org/mistral/latest/_images/Mistral_actions.png)

    * Asynchronous action:

    ![async-action](https://docs.openstack.org/mistral/latest/_images/Mistral_actions.png)

* Action defines what exactly needs to be done when task starts. Action is similar to a regular function in general purpose programming language like Python.
    * System actions
    * Ad-hoc actions

* System actions
    * [std actions](https://docs.openstack.org/mistral/latest/user/wf_lang_v2.html#system-actions)
    * [openstack actions](./mapping.json)

### Execution

* Executions are runtime objects and they reflect the information about the progress and state of concrete execution type.
* **Workflow execution**
    * A particular execution of specific workflow.
    * User submits a workflow to run -> An object is created in db for execution of this workflow.
    * It containts all information about workflow itself, about execution progress, state, input and output data.
    * `Workflow execution = (task execution)+`.

* **Task execution**
    * Defines a workflow execution steps.
    * It has a state and result.
    * All the actual task states belonging to current execution are persisted in DB.
    * Task result is an aggregation of all *action executions* belonging to current *task execution*.
    * `Task execution = (action execution)+`.

* **Action execution**
    * Execution of specific action.
    * Action execution has a state, input and output data.

### Cron-triggers

* An object allowing to run workflow on a schedule.

## Main Features

### Task result / Data flow

* Mistral supports transferring data from 1 task to another.
* [YAQL](https://github.com/openstack/yaql)

### Task affinity

* A feature which could be useful for executing particular tasks on specific Mistral executors:
    * You need to execute the task on a single executor.
    * You need to execute the task on any executor within a named group.

* Similar to Nova Host aggregates.

### Task policies

* Any Mistral task regardless of its workflow type can optionally have configured policies.
* Policies control the flow of the task - for example, a policy can delay task execution before the task starts of after the task completes.
* Different types of policies:
    * pause-before
    * wait-before
    * wait-after
    * timeout
    * retry

### Join

* Join flow control allows to synchronize multiple parellel workflow branches and aggregate their data.
* **Full join (join: all)** When a task has property "join" assigned with value "all" the task will run only if all upstream tasks (ones that lead to this task - Task A has B mentioned in any of its "on-success", "on-error" & "on-complete" clauses) are completed and corresponding conditions have triggered.
* **Partial join (join: X)** When a task has a numeric value assigned to the property "join", then the task will run once at least this number of upstream tasks are completed and the correspoinding conditions have triggered.
* **Discriminator (join: one)** Discriminator is the special case of Partial Join where the "join" property has the value 1.

### Processing collections (with-items)

* Use the *with-items* keyword that associates an action or a workflow with a task run multiple times.
* The values of the *with-items* task property contains an expression in the form: **<variable\__name> in <% YAQL\__expression %>**.

### Execution expiration policy

* By default Mistral will store all exections indefinitely and over time the number stored will accumulate.
* By default this feature is disabled.

```ini
# Enable this feature
[execution_expiration_policy]
evaluation_interval = 120  # 2 hours
older_than = 10080  # 1 week
max_finished_executions = 500
```

* This policy defines:
    * The maximum age of an execution since the last updated (in minutes).
    * The maximum number of finished executions.
