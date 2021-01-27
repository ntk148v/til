# Buffers vs Tab Pages

Source: https://joshldavis.com/2014/04/05/vim-tab-madness-buffers-vs-tabs/

## 1. Buffers

- Buffers in vim are **the in-memory text of files**. For example, when you open a file, the content of the files is laoded into a buffer.

```bash
# Open 2 buffers
# use :bnext to move to .zshrc
$ vim .vimrc .zshrc
```

- Use buffers to open up all required files to get current task done.

## 2. Windows

- A window in Vim is just **a viewport on a buffer**.
- A window can view any buffer.
- Use window when you need to view multiple buffers.

## 3. Tab pages

- The naming is quite confusing, it would be `layout` or `viewport`. Check out [stackoverflow question](https://stackoverflow.com/questions/102384/using-vims-tabs-like-buffers/103590#103590).
- A tab page is **a collection of windows**.
- Tabs were only designed to let us have different layouts of windows (horizontal/vertical, etc.). They aren't intended to be where an open file lives; an open file is instead loaded into a buffer.
- *If you are using a single tab for each file, that isn't how tabs in Vim were designed to be used**.
- Use tabs when working on different projects.
