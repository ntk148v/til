# How to capture terminal sessions and output with the Linux script command

- `script` command creates a typescript file from your terminal session.
- The purpose of script is that you can easily grab sample output from any command through an interactive session exactly as it's displayed in your terminal.

## Usage

```bash
~
➜ script -h

Usage:
 script [options] [file]

Make a typescript of a terminal session.

Options:
 -a, --append                  append the output
 -c, --command <command>       run command rather than interactive shell
 -e, --return                  return exit code of the child process
 -f, --flush                   run flush after each write
     --force                   use output file even when it is a link
 -q, --quiet                   be quiet
 -t[<file>], --timing[=<file>] output timing data to stderr or to FILE
 -h, --help                    display this help
 -V, --version                 display version

For more details see script(1).
```

```bash
~
➜ script --t=<logfile> -q -a <script file>
~
➜ cd /tmp
/tmp
➜ script --t=script_log -q scriptfile
/tmp
➜ mkdir testfolder
/tmp
➜ touch testfolder
/tmp
➜ ls testfolder
/tmp
➜ who
kiennt   tty7         2021-02-04 08:11 (:0)
/tmp
➜ exit # Ctrl-D, the script exits and display exit
/tmp took 40s
➜ cat scriptfile
Script started on 2021-02-04 08:57:11+0700
/tmp
➜ mkdir testfolder
/tmp
➜ touch testfolder
/tmp
➜ ls testfolder
/tmp
➜ who
kiennt   tty7         2021-02-04 08:11 (:0)
/tmp
➜ exit # Ctrl-D, the script exits and display exit

Script done on 2021-02-04 08:57:52+0700
```
