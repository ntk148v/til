# Questions

## Does Redis lock during write?

Redis is single-threaded. All commands are atomic. While command is running, no other command can be executed. But since everything is in memory, commands are (normally) pretty fast.
So no, redis does not allow reading during writing, but that's not a problem.
