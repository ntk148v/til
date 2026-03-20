# Postmodern Python (2026)

Source:

- <https://rdrn.me/postmodern-python/>

# 1. Setup

- Use [uv](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager, written in Rust.

> [!note]
> **But why?** Don't be lazy, do [research yourself](https://docs.astral.sh/uv/#highlights).

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- uv will:
  - install Python for you.
  - manage your `pyproject.toml` dependencies in a standard way.
  - create lock files.
  - ...
- Getting started:

```shell
# create a new project
$ uv init postmodern
$ cd postmodern
# create lockfiles, install Python deps
$ uv sync
Using CPython 3.12.9
Creating virtual environment at: .venv
Resolved 1 package in 34ms
Audited in 0.00ms
$ tree -a .
.
├── hello.py
├── pyproject.toml
├── .python-version
├── README.md
├── uv.lock
└── .venv
    ├── bin
    │   ├── activate
    │   ├── activate.bat
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── activate.nu
    │   ├── activate.ps1
    │   ├── activate_this.py
    │   ├── deactivate.bat
    │   ├── pydoc.bat
    │   ├── python -> /home/kiennt/.local/share/uv/python/cpython-3.12.9-linux-x86_64-gnu/bin/python3.12
    │   ├── python3 -> python
    │   └── python3.12 -> python
    ├── CACHEDIR.TAG
    ├── .gitignore
    ├── lib
    │   └── python3.12
    │       └── site-packages
    │           ├── _virtualenv.pth
    │           └── _virtualenv.py
    ├── lib64 -> lib
    └── pyvenv.cfg

7 directories, 22 files
```

- You might familiar with `setup.py`, Python used to use this file for installing libraries. There was a brief dalliance with `setup.cfg` but then [PEP-518/PEP-621/PEP-631](https://peps.python.org/pep-0518/) came along and saved the day by standardising around pyproject.toml

```toml
[project]
name = "postmodern"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

- Let's add `ruff`:

```shell
$ uv add --dev ruff
Resolved 2 packages in 647ms
Prepared 1 package in 722ms
Installed 1 package in 202ms
 + ruff==0.15.7

$ uv add pydantic
Resolved 7 packages in 576ms
Installed 5 packages in 45ms
 + annotated-types==0.7.0
 + pydantic==2.12.5
 + pydantic-core==2.41.5
 + typing-extensions==4.15.0
 + typing-inspection==0.4.2
```

```toml
[project]
name = "postmodern"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.12.5",
]

[dependency-groups]
dev = [
    "ruff>=0.15.7",
]
```

- Instead activate virtualenv, we can just use `uv run` (but you always be able to activate virtualenv).

## 2. Linting and formatting

- [ruff](https://docs.astral.sh/ruff/) now does everything they did.

```shell
# format (what black used to do)
$ uv run ruff format
# lint (what flake8 used to do)
$ uv run ruff check --fix
```

- Similar to `setup.cfg`, you can add the following:

```toml
[tool.ruff]
# if this is a library, enter the _minimum_ version you
# want to support, otherwise do py313
target-version = "py313"
line-length = 120  # use whatever number makes you happy

[tool.ruff.lint]
# you can see the looong list of rules here:
# https://docs.astral.sh/ruff/rules/
# here's a couple to start with
select = [
	"A",    # warn about shadowing built-ins
	"E",    # style stuff, whitespaces
	"F",    # important pyflakes lints
	"I",    # import sorting
	"N",    # naming
	"T100", # breakpoints (probably don't want these in prod!)
]
# if you're feeling confident you can do:
# select = ["ALL"]
# and then manually ignore annoying ones:
# ignore = [...]

[tool.ruff.lint.isort]
# so it knows to group first-party stuff last
known-first-party = ["postmodern"]
```

## 3. Typing

> Check out: <https://typing.python.org/en/latest/>

- We use [ty](https://docs.astral.sh/ty/), yes, Astral's products again, seems like they know exactly what they do.

```shell
$ uv add --dev ty
$ uv run ty check
```

- And, as with the formatters/linters, you should get it [integrated with your editor](https://docs.astral.sh/ty/editors/).

## 4. Testing

- We still use [pytest](https://docs.pytest.org/).

```shell
$ uv add --dev pytest
$ uv run pytest
```

## 5. Task runner

- [poethepoet](https://github.com/nat-n/poethepoet) works pretty well.

```shell
$ uv add --dev poethepoet
```

- Setup `pyproject.toml`

```toml
[tool.poe.tasks]
# run with eg `uv run poe fmt`
fmt = "ruff format"
lint = "ruff check --fix"
check = "ty check"
test = "pytest"
# run all the above
all = [ {ref="fmt"}, {ref="lint"}, {ref="check"}, {ref="test"} ]
```

- Then any time you've made some changes or are preparing to commit, you can run:

```shell
$ uv run poe test
$ uv run poe all
```

## 6. CI/CD

- Github sample action:

```yaml
# .github/workflows/pr.yml
name: pr
on:
  pull_request:
    types: [opened, reopened, synchronize]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: "0.5.14"
      - run: | # abort if the lockfile changes
          uv sync --all-extras --dev
          [[ -n $(git diff --stat requirements.lock) ]] && exit 1
      - run: uv run poe ci:fmt # check formatting is correct
      - run: uv run poe ci:lint # and linting
      - run: uv run poe check # typecheck too
      - run: uv run poe test # then run your tests!
```

- Dockerfile:

```Dockerfile
# Stage 1: Builder
# Use an official Python base image
FROM python:3.13-slim AS build

# Install uv by copying the binary from the official uv image, which is more efficient than pip install
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for optimized bytecode compilation and link mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files (e.g., pyproject.toml, requirements.txt, uv.lock) first for better Docker layer caching
COPY requirements.txt ./

# Install dependencies into a virtual environment in the build stage
# Use a cache mount for faster rebuilds of dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Stage 2: Runtime
# Use a minimal, production-ready base image (often the same slim image)
FROM python:3.13-slim

WORKDIR /app

# Copy the installed packages (virtual environment) from the build stage to the runtime stage
COPY --from=build /app/.venv /app/.venv

# Place the virtual environment's bin directory at the front of the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Command to run your application
CMD ["python", "your_app_script.py"]
```
