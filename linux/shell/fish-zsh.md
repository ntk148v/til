# Fish vs ZSH

## 1. What is ZSH?

- Z shell (ZSH)
- Unix shell utility, command interpreter, and scripting language built on top of Bash.
- Extend Bash features.
- Customizable.

## 2. What is Fish?

- Linux and macOS shell, command interpreter, and shell scripting language.

## 3. Comparison

| ZSH                                                                                                                                     | Fish                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Follows and supports the Posix standard                                                                                                 | Doesn't follow the Posix standard                                                        |
| Supports both the use of aliases and functions                                                                                          | Doesn't allow the use of alilases but uses functions to manage the use of aliases        |
| Doesn't offer auto suggestions and syntax hightlighting out of the box (but it has plugins for these)                                   | Auto-suggestions and syntax-hightlighting are offered out of box                         |
| Scripting language is based on Bash, it may not very beginner-friendly. But if you are familiar with Bash, ZSH is easier to start with. | Has a sane scripting syntax (more clean and readable code).                              |
| Searching through command history is not as easy compared to Fish. But you can integrate with FZF, it's great                           | Automatically duplicate commands making it easy to search through the history of command |
