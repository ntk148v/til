# Profiling zsh startup time

- Measuring initial startup time.

```shell
$ time zsh -i -c exit
zsh -i -c exit  0,24s user 0,13s system 111% cpu 0,328 total
```

- Enable profiling:

  - Zsh has a builtin profiler to profile startup time usage. It is called `zprof`.
  - It can be enabled by adding to your `zshrc`:

  ```shell
  # Top of zshrc
  zmodload zsh/zprof

  # Your zshrc content

  # Bottom of zshrc
  zprof
  ```

- Start up zsh again, it will start profiling:

```shell
$ zsh
```

- Making changes and repeat the above steps.
