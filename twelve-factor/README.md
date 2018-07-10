# The Twelve-factor app

https://12factor.net/

## Codebase

> One codebase tracked in revision control, many deploys.

* Tracked in a VCS - Git, Mercurial, Subversion.
* A *codebase* is any single repo (in centralized revision control system like Subversion), or any set of repos who share a root commit (in a decentralized revision control system like Git).
* 1 codebase/app, n deploys of the app. A *deploy* is a running instance of the app.

![codebase-deploys](https://12factor.net/images/codebase-deploys.png)

## Dependencies

> Explicitly declare and isolate dependencies

* A twelve-factor app never relies on implicit existence of system-wide packages.

## Config

> Store config in environment

* App's config varies across deploys:
	* Resource handles to the database, Memcached and other backing services.
	* Credentials to external services such as Amazon S3 or Twitter.
	* Per-deploy values such as the canonical hostname for the deploy.
* Stores config in environment variables.

## Backing services

> Treat backing services as attached resources

![attached-resources](https://12factor.net/images/attached-resources.png)

* A *backing service* is any service the app consumes over the network as part of its normal operation.
* Each distinct backing service is a *resource*.
* Resources can be attached to and detached from deploys at will.

## Build, relase, run

> Strictly separate build and run stages

* A codebase is transformed into deploy through 3 stages:
	* The *build stage* converts a code repo into an executable bundle known as a *build*.
	* The *release stage* takes the build produced by the build stage and combines it with the deploy's current config.
	* The *run stage* runs the app in the execution environment.
* The twelve-factor app uses strict separation between the build, release and run stages.

![release](https://12factor.net/images/release.png)

## Processes

> Execute the apps as one or more stateless processes

* Twelve-factor processes are stateless and share-nothing. Any data that needs to persist must be stored in a stateful backing service (typically a db).
* ~~sticky sessions~~ (cache user session data in memory of the app's process and expecting future requests from the same visitor to be routed to the same process) -> violate -> Session state data is a good candidate for a datastore that offers time-expiration (Memcached, Redis).

## Port binding

> Export services via port binding

* The twelve-factor app is completely self-contained.
* Export services via port binding.
* One app can become the backing service for another app.

## Concurrency

> Scale out via the process model

![process-types](https://12factor.net/images/process-types.png)

* Diverse workloads -> assign each type of work to a process type.
* The array of process types and number of processes of each type is known as the *process formation*.
* Twelve-factor app processes should never daemonize or write PID files.

## Disposability

> Maximize robustness with fast startup and graceful shutdown

* Twelve-factor app processes are disposable (start and stop at a moment's notice).

## Dev/prod parity

## Logs

## Admin processes
