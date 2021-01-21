# Jsonnet

- [Jsonnet](#jsonnet)
  - [1. What is Jsonnet?](#1-what-is-jsonnet)
  - [2. Features (note)](#2-features-note)
    - [2.1. Simplified for humans](#21-simplified-for-humans)
    - [2.2. Data operations](#22-data-operations)
    - [2.3. Local variable](#23-local-variable)
    - [2.4. Modularity](#24-modularity)
    - [2.5. Object-orientation](#25-object-orientation)
  - [3. Jsonnet Cli](#3-jsonnet-cli)
    - [3.1. Installation](#31-installation)
    - [3.2. Examples](#32-examples)
  - [4. Jsonnet style guide](#4-jsonnet-style-guide)

## 1. What is Jsonnet?

- Jsonnet is a data templating language. These data templates are transfomered into JSON object using Jsonnet library or commandline tool.
- As a language, Jsonnet is _extension of JSON_ - a valid JSON object is always valid Jsonnet template.

## 2. Features (note)

Check out the [full version](https://jsonnet.org/learning/tutorial.html).

### 2.1. Simplified for humans

```json
{
    // Jsonnet example
    person1: {
        name: "Alice",
        welcome: "Hello " + self.name + "!",
    },
    person2: self.person1 { name: "Bob" },
}
```

- Commenting (C-style and Python-style comment).
- Object fields (the strings to the left of the color) don't have quotes.
- Referencing - one part of the structure can refer to another part using `self` and `super` keywords.

### 2.2. Data operations

```json
{
    foo: [1, 2, 3], # arithmetic
    bar: [x * x for x in self.foo if x >= 2], # conditionals
    baz: { ["field" + x]: x for x in self.foo }, # array comprehension, quite similar to Python
    obj: { ["foo" + "bar"]: 3 },
}
```

### 2.3. Local variable

- Define a local variable using `local` keyword.
- Local variables won't shown up in JSON output but fields they are assigned to will.

```json
// outside the object, ends with ";"
local utils = import "myimport.jsonnet";
{
   // inside the object, ends with ","
   local my_var = "This variable is private",
   my_use: my_var

}
```

### 2.4. Modularity

- It's possible to import both code and raw data from other files.
- The `import` construct is like copy/pasting Jsonnet code (end with `.libsonnet`). Raw JSON can be imported this way too.
- The `importstr` construct is for verbatim UTF-8 text.

```json
// martinis.jsonnet
{
    "Vodka Martini": {
        ingredients: [
            { kind: "Vodka", qty: 2 },
            { kind: "Dry White Vermouth", qty: 1 },
        ],
        garnish: "Olive",
        served: "Straight Up",
    },
    Cosmopolitan: {
        ingredients: [
            { kind: "Vodka", qty: 2 },
            { kind: "Triple Sec", qty: 0.5 },
            { kind: "Cranberry Juice", qty: 0.75 },
            { kind: "Lime Juice", qty: 0.5 },
        ],
        garnish: "Orange Peel",
        served: "Straight Up",
    },
}

// bar_menu.jsonnet
{
    cocktails: import "martinis.jsonnet" + {
        Manhattan: {
            ingredients: [
                { kind: "Rye", qty: 2.5 },
                { kind: "Sweet Red Vermouth", qty: 1 },
                { kind: "Angostura", qty: "dash" },
            ],
            garnish: "Maraschino Cherry",
            served: "Straight Up",
        },
        Cosmopolitan: {
            ingredients: [
                { kind: "Vodka", qty: 1.5 },
                { kind: "Cointreau", qty: 1 },
                { kind: "Cranberry Juice", qty: 2 },
                { kind: "Lime Juice", qty: 1 },
            ],
            garnish: "Lime Wheel",
            served: "Straight Up",
        },
    }
}
```

- Like Python, functions have positional keywords, named parameters and default arguments.

```json
// This function returns an object. Although
// the braces look like Java or C++ they do
// not mean a statement block, they are instead
// the value being returned.
local Sour(spirit, garnish='Lemon twist') = {
  ingredients: [
    { kind: spirit, qty: 2 },
    { kind: 'Egg white', qty: 1 },
    { kind: 'Lemon Juice', qty: 1 },
    { kind: 'Simple Syrup', qty: 1 },
  ],
  garnish: garnish,
  served: 'Straight Up',
};

{
  'Whiskey Sour': Sour('Bulleit Bourbon',
                       'Orange bitters'),
  'Pisco Sour': Sour('Machu Pisco',
                     'Angostura bitters'),
}
```

### 2.5. Object-orientation

- Objects extend other object.
- The _object composition operator_ +, which merges two objects, choosing the right hand side when fields collide.
- The `self` keyword, a reference to the current object.

```json
local Base = {
  f: 2,
  g: self.f + 100,
};

local WrapperBase = {
  Base: Base,
};

{
  Derived: Base + {
    f: 5,
    old_f: super.f,
    old_g: super.g,
  },
  WrapperDerived: WrapperBase + {
    Base+: { f: 5 },
  },
}
```

## 3. Jsonnet Cli

### 3.1. Installation

- [C++](https://github.com/google/jsonnet#building-jsonnet)
- [Go](https://github.com/google/go-jsonnet#installation-instructions):

```bash
go get github.com/google/go-jsonnet/cmd/jsonnet
```

### 3.2. Examples

- Evaluate a file:

```json
# landingpage.jsonnet
{
  person1: {
    name: 'Alice',
    welcome: 'Hello ' + self.name + '!',
  },
  person2: self.person1 { name: 'Bob' },
}
```

```bash
$ jsonnet landingpage.jsonnet

{
   "person1": {
      "name": "Alice",
      "welcome": "Hello Alice!"
   },
   "person2": {
      "name": "Bob",
      "welcome": "Hello Bob!"
   }
}
```

- Evaluate a snippet:

```bash
$ jsonnet -e '{ x: 1 , y: self.x + 1 } { x: 10 }'

{
   "x": 10,
   "y": 11
}
```

- Multiple file output: generate multiple JSON files from a single Jsonnet file.

```json
// multiple_output.jsonnet
{
  "a.json": {
    "x": 1,
    "y": $["b.json"].y
  },
  "b.json": {
    "x": $["a.json"].x,
    "y": 2
  }
}
```

```bash
$ jsonnet -m . multiple_output.jsonnet
a.json
b.json
$ cat a.json
{
   "x": 1,
   "y": 2
}
$ cat b.json
{
   "x": 1,
   "y": 2
}
```

- YAML Stream output:

```json
// yaml_stream.jsonnet
local
  a = {
    x: 1,
    y: b.y,
  },
  b = {
    x: a.x,
    y: 2,
  };

[a, b]
```

```bash
 jsonnet -y . yaml_stream.jsonnet
---
{
   "x": 1,
   "y": 2
}
---
{
   "x": 1,
   "y": 2
}
```

## 4. Jsonnet style guide

Check out [Databrick's repostiory](https://github.com/databricks/jsonnet-style-guide).
