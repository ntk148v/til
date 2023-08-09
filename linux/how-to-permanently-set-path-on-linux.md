# How to permanently set $PATH on Linux/Unix

Source: <https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix>

There are multiple ways to do it. The actual solution depends on the purpose.

The variable values are usually stored in either a list of assignments or a shell script that is run at the start of the system or user session. In case of the shell script you must use a specific shell syntax and `export` or `set` commands.

## System wide

1. `/etc/environment` List of unique assignments. Allows references. Perfect for adding system-wide directories like `/usr/local/something/bin` to PA`TH variable or defining `JAVA_HOME`. Used by PAM and systemd.

2. `/etc/environment.d/*.conf` List of unique assignments. Allows references. Perfect for adding system-wide directories like `/usr/local/something/bin` to PATH variable or defining `JAVA_HOME`. The configuration can be split into multiple files, usually one per each tool (Java, Go, and Node.js). Used by systemd that by design do not pass those values to user login shells.

3. `/etc/xprofile` Shell script executed while starting X Window System session. This is run for every user that logs into X Window System. It is a good choice for PATH entries that are valid for every user like `/usr/local/something/bin`. The file is included by other script so use POSIX shell syntax not the syntax of your user shell.

4. `/etc/profile` and `/etc/profile.d/*` Shell script. This is a good choice for shell-only systems. Those files are read only by shells in login mode.

5. `/etc/<shell>.<shell>rc`. Shell script. This is a poor choice because it is single shell specific. Used in non-login mode.

## User session

1. `~/.pam_environment`. List of unique assignments, no references allowed. Loaded by PAM at the start of every user session irrelevant if it is an X Window System session or shell. You cannot reference other variables including HOME or PATH so it has limited use. Used by PAM.

2. `~/.xprofile` Shell script. This is executed when the user logs into X Window System system. The variables defined here are visible to every X application. Perfect choice for extending PATH with values such as ~/bin or ~/go/bin or defining user specific GOPATH or NPM_HOME. The file is included by other script so use POSIX shell syntax not the syntax of your user shell. Your graphical text editor or IDE started by shortcut will see those values.

3. `~/.profile`, ~`/.<shell>_profile`, `~/.<shell>_login` Shell script. It will be visible only for programs started from terminal or terminal emulator. It is a good choice for shell-only systems. Used by shells in login mode.

4. `~/.<shell>rc`. Shell script. This is a poor choice because it is single shell specific. Used by shells in non-login mode.

## Notes

GNOME on Wayland starts a user login shell to get the environment. It effectively uses the login shell configurations `~/.profile`, `~/.<shell>_profile`, `~/.<shell>_login` files.

## Man pages

- [environment](https://linux.die.net/man/1/environment)
- [environment.d](https://linux.die.net/man/1/environment.d)
- [bash](https://linux.die.net/man/1/bash)
- [dash](https://linux.die.net/man/1/dash)

## Distribution-specific documentation

- [Ubuntu](https://help.ubuntu.com/community/EnvironmentVariables#Persistent_environment_variables)
- [Arch Linux](https://wiki.archlinux.org/index.php/Environment_variables)

## Related

[Difference between Login Shell and Non-Login Shell?](https://unix.stackexchange.com/a/46856/39410)
