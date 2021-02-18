# Docker entrypoint scripts

Many docker entrypoint scripts for docker do something like this:

```bash
#!/bin/bash
set -e

... code ...

exec "$@"
```

So what are `set -e` and the `exec "$@"` for?

- According to [BashFAQ#105](http://mywiki.wooledge.org/BashFAQ/105), `set -e` (`set -o errexit` or `trap ERR`) was an attempt to add "automatic error detection" to the shell. Its goal was to cause the shell to abort any time an error occurred, so you don't have to put `|| exit 1` after each important command.
- `exec "@"`: `"$@"` bit will expand to the list of positional parameters (usually the command line arguments), individually quoted to avoid word splitting and filename generation ("globbing"). `exec` will replace the current process with the process resulting from executing its argument. `exec "$@"` will run the command given by the command line parameters in such a way that the current process is replaced by.
    - **without exec**: parent shell starts -> parent shell forks child -> child runs -> child exits -> parent shell exits.
    - **with exec**: parent shell starts -> parent shell forks child, replaces itself with child -> child runs -> child exits.
- This is important in Docker for signals to be proxied correctly. For example, if a container was started without `exec`, it will not receive a `SIGTERM` upon `docker stop` and will not get a chance to shutdown cleanly. In some cases, it can lead to data loss or zombie processes.
