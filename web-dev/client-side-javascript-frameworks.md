# Client-side JavaScript frameworks

- [Client-side JavaScript frameworks](#client-side-javascript-frameworks)
  - [1. Introduction](#1-introduction)
  - [2. Framework main features](#2-framework-main-features)

Source: <https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks>

## 1. Introduction

- Developers who worked with JavaScript wrote tools to solve the problems they faced, and packaged them into reusable packages called **libraries** -> share with others.
- A **frameworks** is a library that offers opinions about how software gets built.
- Frameworks:
  - [Angular](https://angular.io/)
  - [Vue](https://vuejs.org/)
  - [React](https://reactjs.org/)
- Why do frameworks exist? Solve problem - every time we change our application's state, we need to update the UI to match.
- Every JavaScript frameworks offer a way to write user interfaces more *declaratively*, they allow you to write code that describes how your UI should  look, and the framework makes it happen in the DOM behind the scenes.

```js
// vue example
<ul>
  <li v-for="task in tasks" v-bind:key="task.id">
    <span>{{task.name}}</span>
    <button type="button">Delete</button>
  </li>
</ul>
```

- Other advantages:
  - *Tooling*: each framework's ecosystem provides tooling that improves the developer experience.
  - *Compartmentalization*:  Abstract the different parts of their user interfaces into *components* - maintainable, reusbale chunks of code that can communicate with one another.
  - *Routing*: Modern web applications typically do not fetch and render new HTML files - they load a single HTML shell, and continually update the DOM inside it (**single page apps - SPAs**). An SPA is complex -> + routing (**client-side routing**).

- Things to consider when using frameworks:
  - Familiarity with the tool.
  - Overengineering.
  - Larger code base and abstraction.
- Alternatives to client-side frameworks:
  - A content management system
  - Server-side rendering
  - A static site generator

## 2. Framework main features

- **Domain-specific languages (DSLs)**:
  - DSLs know how to read data variables, and this data can be used to streamline the process of writing your UI.
  - DSLs can't be read by the browser directly, they must be transformed into JavaScript or HTMl first. [Transformation is an extra step in the development process](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Overview#transformation), but framework tooling generarlly includes the required tools to handle this step, or can be adjusted to include this step.
  - [JSX](https://reactjs.org/docs/introducing-jsx.html), which stands for JavaScript and XML, is an extension of JavaScript that brings HTML-like syntax to a JavaScript environment.
  - [Handlebars](https://handlebarsjs.com/) templating language resembles HTML, but it has the option of pulling data in from elsewhere. This data can be used to influence the HTML that an application ultimately builds.
  - [TypeScript](https://www.typescriptlang.org/) is a *superset* of JavaScript, meaning it extends JavaScript - all JavaScript code is valid TypeScript, but not the other way around.

    ```js
    // javascript
    functionadd(a, b) {
      return a + b;
    }
    ```

    ```ts
    // typescript
    function add(a: number, b: number) {
      return a + b;
    }
    ```

- **Writing components**: Most frameworks have some kind of component model. React components can be written with JSX, Ember components with Handlebars, and Angular and Vue components with a templating syntax that lightly extends HTML.
  - *Properties* (props) is external data that a component needs in order to render.
  - *State* - a robust state-handling mechanism is key to an effective framework, and each component may have data that needs its state controlled. This state will persist in some way as long as the component is in use. Like props, state can be used to affect how a component is rendered.
  - *Events* - In order to be interactive, components need ways to respond to browser events, so our applications can respond to our users. Frameworks each provide their own syntax for listening to browser events, which reference the names of the equivalent native browser events.

- **Styling components**: Each framework offers a way to define styles for your components - or for the application as a whole.

- **Handling dependencies**: All major frameworks provide mechanism for handling dependencies - using components inside other components. sometimes with multiple hierachy levels.
  - Components in components.
  - Dependency injection.
  - Lifecyle: a collection of phases a component goes through from the time it is appended to the DOM and then rendered by the browser (often called mounting) to the time that it is removed from the DOM (often called unmounting).

- **Rendering elements**:
  - *Virtual DOM*: an approach whereby information about your browser's DOM is stored in JavaScript memory. Your application updates this copy of the DOM, then compares it to the "real" DOM -> builds a "diff" between the updated virtual DOM and currently rendered DOM -> apply diff to the real DOM.
  - *Incremental DOM*: simliar to the virtual DOM in that it builds a DOM diff to decide what to render, but different in that it doesn't create a complete copy of the DOM in JavaScript memory. It ignores the parts of the DOM that do not need to be changed.
  - *Glimmer VM*: a separate process through which Ember's templates are transpiled into a kind of "byte code" that is easier and faster to read than JavaScript.

- **Routing**: To avoid a broken experience in sufficiently complex apps with lots of views, each of the frameworks covered in this module provides a library (or more than one library) that helps developers implement client-side routing in their applications.
- **Testing**:
  - Each framework's ecosystem provides tooling that facilitates the writing of tests.
  - Testing tools are not built into the frameworks themselves, but the command-line interface tools used to generate framework apps give you access to the appropriate testing tools.
