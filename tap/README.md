# Test Anything Protocol (TAP)

Source: <https://testanything.org>

TAP, the Test Anything Protocol, is a simple text-based interface between testing modules in a test harness. It decouples the reporting of errors from the presentation of the reports.

One of its major uses is for noise reduction; when you have a suite of many tests, making them TAP producers and using a TAP consumer to view them helps ensures that you will see everything you need to notice and diagnose breakage without being distracted by a flood of irrelevant success messages. It can assist other forms of analysis and statistics-gathering as well.

Here’s what a TAP test stream looks like:

```text
1..4
ok 1 - Input file opened
not ok 2 - First line of the input valid
ok 3 - Read the rest of the file
not ok 4 - Summarized correctly # TODO Not written yet
```

- TAP producers can be many things, from unit and integration testing frameworks to visual testing software, lint tooling, build systems, etc. Support exists in many languages, but there are also language-agnostic.
- Tap consumers are programs that take the input and transform, process, or format it. This can range from adding color, full reformatting, transforming to different output formats such as JUnit or HTML, running analysis and statistics on it, integrating it into CI/CD like Jenkins, or even getting desktops notifications, if so desired.
