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
* Minize startup time.
* Shutdown gracefully.

## Dev/prod parity

> Keep development, staging, and production as similar as possible

* Gaps between development and production:
    * The time gap: A developer may work on code that takes days, weeks or even months to ggo into production. -> a developer may write code and have it deployed.
    * The personnel gap: Developers write code, ops engineers deploy it. -> developers who wrote code are closely involved in deploying it and watching its behavior in production.
    * The tools gap: Developers may be using a stack like Nginx, SQLite... while the production deploy use Apache, MySQL, Linux. -> Keep development and production as similar as possible.
* Design for continuous deployment by keeping the gap between development and production small.
* Tools: Chef, Docker, Vagrant...

## Logs

> Treat logs as event streams

* Never concerns itself with routing or storage of its output stream.
* ~~logfile~~, each running process writes its event stream, unbuffered to `stdout`.
    * Local development: developer will view stream in the foreground.
    * Staging or production deploys: each process's stream will be captured by the execution environment, collated together with all other streams from the app, and routed to one or more final destinations for viewing and long-term archival -> Fluentd, Logstash...
* The stream can be sent to a log indexing and analysis system -> ELK for e.x

## Admin processes

> Run admin/management tasks as one-off processes

* One-off administrative or maintenance tasks: db migrations, console, one-time scripts commited into the app's repo.
* Run in an identical environment as the regular long-running processes of the app - run against a release, using the same codebase and config.
