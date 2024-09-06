# Sessions

Check out the [document](http://vimdoc.sourceforge.net/htmldoc/usr_21.html#21.4), here is the scenario to explain how it works and how its use case.

- You are editing a dozen of files, complex window layout,... but this is the end of the day, you need to quit work.
- You will have to open all these files again next day.
- Hah, don't worry, Vim already provides a very cool feature for you - `sessions`.
- Create one.

```vim
:mks ~/.vim/sessions/foo.vim
```

- Easily pick up where you left off, everything will be exactly as you left it: the working directory, your windows, splits and buffers...

```vim
:source ~/.vim/sessions/foo.vim
```

```bash
vim -S ~/.vim/sessions/foo.vim
```
