---
title: Saving and exiting files
path: vim/saving-and-exiting-files.md
---

Source: <https://docstore.mik.ua/orelly/unix3/vi/ch05_03.htm>

- `:w` Writes (saves) the buffer to the file but does not exit. You can (and should) use `:w` throughout your editing session to protect your edits against system failure or a major editing error.
- `:q` Quits the editor (and returns to the UNIX prompt).
- `:wq` Both writes the file and quits the editor. The write happens unconditionally, even if the file was not changed.
- `:x` Both writes the file and quits (exits) the editor. The file is written only if it has been modified.

- What's the difference between `:wq` and `:x`? Modification time. If you `:x` a buffer that hasn’t changed, the modification time will be untouched because the file isn’t re-saved. The `:wq` command will alter the modification time no matter what.
