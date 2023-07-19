# Exit Codes

Source: <https://tldp.org/LDP/abs/html/exitcodes.html>

| Exit Code Number | Meaning                                                    |
| ---------------- | ---------------------------------------------------------- |
| 1                | Catchall for general errors                                |
| 2                | Misuse of shell builtins (according to Bash documentation) |
| 126              | Command invoked cannot execute                             |
| 127              | "command not found"                                        |
| 128              | Invalid argument to exit                                   |
| 128+n            | Fatal error signal "n"                                     |
| 130              | Script terminated by Control-C                             |
| 255\*            | Exit status out of range                                   |

According to the above table, exit codes 1 - 2, 126 - 165, and 255 [^1] have special meanings, and should therefore be avoided for user-specified exit parameters. Ending a script with exit 127 would certainly cause confusion when troubleshooting (is the error code a "command not found" or a user-defined one?). However, many scripts use an exit 1 as a general bailout-upon-error. Since exit code 1 signifies so many possible errors, it is not particularly useful in debugging.

[^1] Out of range exit values can result in unexpected exit codes. An exit value greater than 255 returns an exit code modulo 256. For example, exit 3809 gives an exit code of 225 (3809 % 256 = 225).
