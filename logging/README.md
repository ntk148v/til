# Logging Best Practices

Source: <https://www.dataset.com/blog/the-10-commandments-of-logging/>

## 1. Don't write logs by yourself (AKA Don't reinvent the Wheel)

Never, ever use `printf` or write your log entries to files by yourself, or handle log rotation by yourself. Please do your ops guys a favor and use a standard library or system API call for this.

## 2. Log at the proper level

|        |                                                                                                                                        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| TRACE  | This is a code smell if used in production. This should be used during development to track bugs, but never committed to your VCS      |
| DEBUG  | Log at this level about anything that happens in the program.                                                                          |
| INFO   | Log at this level all actions are user-driven, or system specific                                                                      |
| NOTICE | This will certainly be the level at which the program will run in production (all the notable events that are not considered an error) |
| WARN   | Log at this level all events that could potenially become an error                                                                     |
| ERROR  | Log every error condition at this level.                                                                                               |
| FATAL  | This shouldn't happen a lot in a real program. Usually logging at this level signifies the end of the program.                         |

## 3. Employ the proper log category

The logging category allows us to classify the log message, and will ultimately, based on the logging framework configuration, be logged in a distinct way or not logged at all.

## 4. Write meaningful log messages

This might probably be the most important best practice.

- Add remediation information to the log message.
- Don't add a log message that depends on a previous message's content.

## 5. Write log message in English

## 6. Add context to your log messages

- Bad message:

```log
Transaction failed

User operation succeeds

java.lang.IndexOutOfBoundsException
```

- Without proper context, those messages are only noise, they don't add value and consume space that could have been useful during troubleshooting.
- Good message:

```log
Transaction 2346432 failed: cc number checksum incorrect

User 54543 successfully registered e-mail user@domain.com

IndexOutOfBoundsException: index 12 is greater than collection size 10
```

## 7. Log in machine parseable format

- Log entries are really good for humans but very poor for machines.
- Let's add the context in a machine parseable format in your log entry -> JSON.

## 8. But make the logs human readable as well

- Use a standard date and time format (ISO8601)
- Add timestamps either in UTC or local time plus offset
- Employ log levels correctly
- Split logs of different levels to different targets to control their granularity
- Include the stack trace when logging exceptions
- Include the thread’s name when logging from a multi-threaded application

## 9. Don't log too much or too little

## 10. Think of your audience

## 11. Don't log for troubleshooting purpose only

Just as log messages can be written for different audiences, log messages can be used for different reasons

- Auditing
- Profiling
- Statistics

## 12. Avoid vendor lock-in

## 13. Don't log sensitive information

Finally, a logging security tip: don’t log sensitive information. First, the obvious bits. Make sure you never log:

    Passwords
    Credit card numbers
    Social security numbers

Now, the not so obvious things you shouldn’t log.

    Session identifiers Information the user has opted out of
    Authorization tokens
    PII (Personal Identifiable Information, such as personal names)
