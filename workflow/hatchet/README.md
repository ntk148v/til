# Hatchet

## 1. Introduction

- Run background tasks at scale.
- Instead of managing your own task queue or pub/sub system, you can use Hatchet to distribute your functions between a set of workers with minimal configuration or infrastructure.
- Concepts:
  - **Background tasks**:
    - Functions which are executed outside of the main req/resp cycle..
    - Useful for offloading work from your application, and for running complex, long-running or resource-intensive tasks.
  - **Workers**:
    - Hatchet is responsible for invoking tasks which run on workers.
    - Workers are long-running processes which are connected to Hatchet, and execute the functions defined in your tasks.
    - Slots are the number of concurrent task runs that a worker can execute, are configured using the `slots` option on the worker.
  - **Task**:
    - A unit of work that can be executed by Hatchet.
    - Tasks can be spawned from within another task or can be built into a DAG based workflow.
  - **Durable queue**:
    - Handle real-time interactions and business-critical task.

## 2. Ways of Running tasks

Once you have a running worker, you’ll want to run your tasks. Hatchet provides a number of ways of triggering task runs, from which you should select the one(s) that best suit(s) your use case.

1. Tasks can be run, and have their results waited on.
2. Tasks can be enqueued without waiting for their results ("fire and forget")
3. Tasks can be run on cron schedules.
4. Tasks can be triggered by events.
5. Tasks can be scheduled for a later time.

## 3. Flow control

- Worker slots: which is a way to control the number of tasks that can be executed concurrently on a given compute process.
- Concurrency:
  - Hatchet provides powerful concurrency control features to help you manage the execution of your tasks. This is particularly useful when you have tasks that may be triggered frequently or have long-running steps, and you want to limit the number of concurrent executions to prevent overloading your system, ensure fairness, or avoid race conditions.
  - Available strategies:
    - `GROUP_ROUND_ROBIN`: distribute task instances across available slots in a round-robin fashion based on the `key` function.
    - `CANCEL_IN_PROGRESS`: cancel the currently running task instances for the same concurrency key to free up slots for the new instance.
    - `CANCEL_NEWEST`: cancel the newest task instance for the same concurrency key to free up slots for the new instance.
- Rate limits:
  - Hatchet allows you to enforce rate limits on task runs, enabling you to control the rate at which your service runs consume resources, such as external API calls, database queries, or other service. By defining rate limits, you can prevent task runs from exceeding a certain number of requests per time window (e.g., per second, minute, or hour), ensuring efficient resource utilization and avoiding overloading external services.
  - Hatchet offers two patterns for Rate limiting task runs:
    - Dynamic rate limits: allows for complex rate limiting secnarios, such as per-user limits, by using `input` or `additional_metadata` keys to upsert a limit at runtime.
    - Static rate limits: allows for simple rate limiting for resources known prior to runtime (e.g., external APIs).
