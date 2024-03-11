# Controlling Nginx

Source: <http://nginx.org/en/docs/control.html>

## How nginx reload work ? why it is zero-downtime?

nginx can be controlled with signals. The process ID of the master process is written to the file `/usr/local/nginx/logs/nginx.pid` by default. This name may be changed at configuration time, or in `nginx.conf` using the pid directive. The master process supports the following signals:

```text
TERM, INT	fast shutdown
QUIT	    graceful shutdown
HUP	        changing configuration, keeping up with a changed time zone (only for FreeBSD and Linux), starting new worker processes with a new configuration, graceful shutdown of old worker processes
USR1	    re-opening log files
USR2	    upgrading an executable file
WINCH	    graceful shutdown of worker processes
```

Individual worker processes can be controlled with signals as well, though it is not required. The supported signals are:

```text
TERM, INT	fast shutdown
QUIT	    graceful shutdown
USR1	    re-opening log files
WINCH	    abnormal termination for debugging (requires debug_points to be enabled)
```

In order for nginx to re-read the configuration file, a HUP signal should be sent to the master process. The master process first checks the syntax validity, then tries to apply new configuration, that is, to open log files and new listen sockets. If this fails, it rolls back changes and continues to work with old configuration. If this succeeds, it starts new worker processes, and sends messages to old worker processes requesting them to shut down gracefully. Old worker processes close listen sockets and continue to service old clients. After all clients are serviced, old worker processes are shut down.
