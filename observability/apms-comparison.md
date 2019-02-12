# APM Comparison

## Criterias

* Basic features - Have or not? Not details how it works, performance.
    * Graphing - Monitor status & Alert.
    * Logging
    * Alerting
    * Tracing
    * Metrics - Monitoring
    * Name mapping
* Real-time health-check (Near real-time)
* Compliance check
* Auto-discovery (Relationship)
* Root Cause Analysis
* Agent-based
* Scalability
* Customizable integrations
* What can it monitor? (Container, cloud, service, tradition servers, database)

## Features

* Basic features - Have or not? Not details how it works, performance.
    * Graphing - Monitor status & Alert.
    * Logging
    * Alerting
    * Tracing
    * Metrics - Monitoring
    * Name mapping
* Real-time health-check (Near real-time)
* Compliance check
* Auto-discovery (Relationship): manageiq
* Root Cause Analysis
* Agent-based
* Scalability
* Customizable integrations
* What can it monitor? (Container, cloud, service, tradition servers, database)
* Alert push (group - deduced) - Metric, Log, Trace pull.
* Load - lazy load - http2 + streaming /grpc
* Caching mechanism
* Etcd mapping
* Kubernetes tech stack

## TODO

* Kubernetes
* Etcd
* manageiq
* Elasalert
* Caching

## Datadog

https://blog.underdog.io/inside-datadogs-tech-stack/

* Use agent, collects events and metrics from hosts and sents them to Datadog. The Datadog agent is open-source.
* More than 200 built-in integrations. Allow to write a custom integrations.
* [Service Map](https://www.datadoghq.com/blog/service-map/)
* Auto-discovery: Docker labels & Kubernetes only.

## Dynatrace

* OneAgent: essentially a set of specialized processes that run on each monitored host. OneAgent collects metrics from the operating system it runs on compares the metrics to baseline performance metrics. **Install just one agent, one time forever - zero manual configuration**. -> pros + cons?
* Dynatrace [auto-discovers](https://www.dynatrace.com/platform/application-topology-discovery/) all the components and dependencies of your entire technology stack end-to-end.
    * Dynatrace detects billions of causal dependencies between websites, applications, services, processes, hosts, networks, and cloud infrastructure with minutes.
* Dynatrace AI engine can identify anomalies and performance issues the cause of the problem. This is all done automatically and you don't need to configure anything.
* Extend Dynatrace: Dynatrace offers a number approaches that you can use to extend Dynatrace out-of-the-box monitoring to address your environment's specific monitoring needs.
    * OneAgent Plugins: [How do I create a Python custom plugin](https://www.dynatrace.com/support/help/extend-dynatrace/oneagent-plugins/how-do-i-create-a-python-custom-plugin/)
    * Dynatrace API
    * OneAgent SDK
    * ActiveGate Plugins
    * JMX plugins

## AppDynamics

* AppDynamics still Flash in parts of the UI, it sucks

https://www.comparitech.com/net-admin/appdynamics-vs-dynatrace/

* [135 Extensions](https://www.appdynamics.com/community/exchange/)

## NewRelic

https://blog.overops.com/appdynamics-vs-new-relic-which-tool-is-right-for-you-the-complete-guide/

https://www.dynatrace.com/platform/comparison/apm-dynatrace-vs-appdynamics-vs-newrelic/

## Hawkular

* Hawkular is a set of Open Source projects designed to be a generic solution for common monitoring problems. Hawkular projects provide REST services that can be used for all kinds of monitoring needs.
* The monitoring services provided by Hawkular have been adopted by different projects and are central to the Middleware management solution in ManageIQ project.
