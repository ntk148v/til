# Conventional Commits

Source: <https://www.conventionalcommits.org/en/v1.0.0/>

The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of.

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The commit contains the following structural elements, to communicate intent to the consumers of your library:

1. **fix**: a commit of the type `fix` patches a bug in codebase -> `PATCH` in SemVer.
2. **feat**: a commit of the type `feat` introduces a new feature to the codebase -> `MINOR` in SemVer.
3. **BREAKING CHANGE**: a commit that has a footer `BREAKING CHANGE:`, or appends a `!` after the type/scope, introduces a breaking API change -> `MAJOR` in SemVer.
4. _types_ other than `fix:` and `feat:` are allowed, for example: `build:`, `ci:`, `docs:`,...
5. _footers_ other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to [git trailer format](https://git-scm.com/docs/git-interpret-trailers).

Some examples:

- Commit message with description and breaking change footer.

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

- Commit message with `!` to draw attention to breaking change.

```
feat!: send an email to the customer when a product is shipped
```

- Commit message with multi-paragraph body and multiple footers.

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```
