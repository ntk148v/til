# Extending with Shared Libraries

Source: <https://www.jenkins.io/doc/book/pipeline/shared-libraries/>

Shared libraries are Groovy code stored in external SCM, loaded into Pipelines to avoid repeating logic. Defined with a **name**, an **SCM source**, and an optional default **version**.

## Directory structure

```text
(root)
+- src                      # Java-style package dir, added to classpath
|   +- org/foo/Bar.groovy   # class org.foo.Bar
+- vars
|   +- foo.groovy           # global variable 'foo'
|   +- foo.txt              # help for 'foo'
+- resources                # adjunct files (external libs only)
|   +- org/foo/bar.json
```

- `src` — standard Java source layout; compiled into the classpath when running.
- `vars` — each file becomes a global variable in the Pipeline (e.g. `vars/log.groovy` → `log.info "hello"`). Multiple functions per file OK.
- `resources` — non-Groovy files loaded via the `libraryResource` step (not supported for internal libraries).

## Using a library

```groovy
@Library('utils') _        // load in any Pipeline
```

- `@Library('utils@version')` pins a version; `@Library('utils@pull/123/head')` tests a GitHub PR.
- Declarative Pipelines must call these variables inside a `script { }` block.

## Accessing steps from `src` classes

`src` classes can't call steps (`sh`, `git`) directly. Pass `this` (the script) in:

```groovy
// src/org/foo/Utilities.groovy
package org.foo
class Utilities implements Serializable {   // must be Serializable to suspend/resume
  def steps
  Utilities(steps) { this.steps = steps }
  def mvn(args) { steps.sh "${steps.tool 'Maven'}/bin/mvn -o ${args}" }
}
```

```groovy
@Library('utils') import org.foo.Utilities
def utils = new Utilities(this)
node { utils.mvn 'clean package' }
```

## Defining global variables (vars)

```groovy
// vars/sayHello.groovy
def call(String name = 'human') { echo "Hello, ${name}." }  // call() = reusable like a step
```

Used as `sayHello 'Joe'`. With a `Closure` argument it acts like a block step (`windows { bat 'cmd /?' }`). Global variables keep no state across builds — store state in a class, not a `vars` variable.

## Defining Declarative Pipelines

You can define `pipeline { ... }` blocks in shared libraries — only inside a `vars/*.groovy` `call` method, and only one per build.

## Loading resources

```groovy
def request = libraryResource 'com/mycorp/somelib/request.json'   // returns a String
```

## Third-party libraries & testing

- Prefer installing CLI tools on agents over `@Grab`; `@Grab` only works from **trusted** library code.
- Use **Replay** on a build to test untrusted-library changes in place.
