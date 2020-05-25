# Cadvisor

Before do anything with cadvisor, double check your `max_user_watches`:

```bash
$ cat /proc/sys/fs/inotify/max_user_watches # default is 8192
$ sudo sysctl fs.inotify.max_user_watches=1048576 # increase to 1048576
```

There are [many issues](https://github.com/google/cadvisor/search?q=max_user_watches&type=Issues) related to it.
