# What's the difference between code linters and formatters?

Source: <https://nono.ma/linter-vs-formatter>

TL;DR

    Linters flag bugs and bad practices
    Formatters fix your code to match style guides

## Linters

Code linters analyze code statically to flag programming errors, catch bugs, stylistic errors, and suspicious constructs,[^1] using the abstract syntax tree or AST. Code linting promotes and enforces best practices by ensuring your code matches your style guide.[^2]

You can expect a linter to warn you of functions whose complexity needs to be reduced, syntax improvements, code practices that go against configured or standard conventions, etc.

For instance, [eslint](https://github.com/eslint/eslint) is a widely-used JavaScript linter and [SonarLint](https://www.sonarqube.org/sonarlint/) is an IDE extension that you can use for linting code in VSCode.

For illustration purposes, here's a sample code cognitive complexity warning from SonarLint for a Python function.

```text
Refactor this function to reduce its Cognitive Complexity
from 37 to the 15 allowed. sonarlint(python:S3776)
```

## Formatters

Code formatters fix style—spacing, line jumps, comments—which helps enforce programming and formatting rules that can be easily automated, which helps reduce future code diffs by delegating formatting concerns to an automatic tool rather than individual developers.

For instance, [autopep8](https://github.com/peter-evans/autopep8) automatically formats Python code to conform to the [PEP 8 style guide](https://peps.python.org/pep-0008/).

As an example, take a look at the contents of this JSON file.

```json
// names.json
{ "names": ["James", "Claire", "Peter", "Lily"] }
```

By right-clicking on a JSON file with these contents on Visual Studio Code, you can select Format Document or press ⌥ + ⇧ + F (on macOS) to obtain the following results.

```json
// names.json
{
  "names": ["James", "Claire", "Peter", "Lily"]
}
```

[^1]: [Lint](<https://en.wikipedia.org/wiki/Lint_(software)>). Wikipedia.
[^2]: [Clean code linters](https://github.com/collections/clean-code-linters). GitHub.
