# Jujutsu - a version control system

Source:

- <https://martinvonz.github.io/jj/latest/>
- <https://steveklabnik.github.io/jujutsu-tutorial/introduction/introduction.html>
- <https://ahal.ca/blog/2024/jujutsu-mercurial-haven/>
- <https://v5.chriskrycho.com/essays/jj-init/>

## 1. Overview

- `jujutsu - jj` is a new(ish) version control system originally developed by Martin Von Zweigbergk of Google.
- jujutsu is two things:
  - **It is a new front-end to Git**
  - **It is a new design for distributed version control**. In particular, Jujutsu brings to the table a few key concepts - none of which are themselves novel, but the combination of which is _really_ nice to use in practice:
    - _Changes_ are distinct from _revisions_: an idea borrowed from Mercurial, but quite different from Git's model.
    - Conflicts are first-class item: an idea borrowed from [Pijul](https://pijul.org/) and [Darcs](https://darcs.net/).
    - The user interface is not only reasonable but actually really good: an idea borrowed from … literally every VCS other than Git.

> WIP
