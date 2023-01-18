# Building Resilient Infrastructure with Nomad

## 1. Restarting tasks

Source: <https://www.hashicorp.com/blog/resilient-infrastructure-with-nomad-restarting-tasks>

- Nomad Job workflow (simplified)

![](https://www.datocms-assets.com/2885/1534979559-nomad-resiliency-part01-job-workflow.png?fit=max&q=80&w=2000)

- Nomad makes task workloads resilient by allowing job authors to specify strategies for _automatically_ restarting failed and unresponsive tasks as well as automatically rescheduling repeatedly failing tasks to other nodes.

![](https://www.datocms-assets.com/2885/1534979778-nomad-resiliency-part01-restarts.png?fit=max&q=80&w=2000)

- Nomad _restarts failed tasks_ on the same node according to the directives in the [restart](https://www.nomadproject.io/docs/job-specification/restart.html) stanza of the job file.

```hcl
group "cache" {
  ...
  restart {
    attempts = 2
    interval = "30m"
    delay = "15s"
    mode = "fail"
  }
  task "redis" {
    ...
  }
}
```

- Nomad _restarts unresponsive tasks_ according to the directives in the [check_restart](https://www.nomadproject.io/docs/job-specification/check_restart.html) stanza.

```hcl
task "redis" {
  ...
  service {
    check_restart {
      limit = 3
      grace = "90s"
      ignore_warnings = false
    }
  }
}
```

- Tasks that are not running successfully after the specificed number of restarts may be failing due to an issue with the node they are running on such as failed hardware, kernel deadlock or other unrecoverable errors. Using the [reschedule](https://www.nomadproject.io/docs/job-specification/reschedule.html) stanza, operators tell Nomad under what circumstances to reschedule failing jobs to another node (not previously used for the task). The reschedule stanza does not apply to system jobs because they run on every node.

```hcl
group "cache" {
  ...
  reschedule {
    delay          = "30s"
    delay_function = "exponential"
    max_delay      = "1hr"
    unlimited      = true
  }
}
```

## 2. Scheduling and self-healing

Source: <https://www.hashicorp.com/blog/resilient-infrastructure-with-nomad-scheduling>

- Nomad client agent

![](https://www.datocms-assets.com/2885/1535497620-nomad-resiliency-part02-architecture.png?fit=max&q=80&w=2000)

- Scheduling is the process of determining the appropriate allocations and is done as part of an _evaluation_.

![](https://www.datocms-assets.com/2885/1535497633-nomad-resiliency-part02-scheduling.png?fit=max&q=80&w=2000)
