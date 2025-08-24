# React

Source: <https://www.geeksforgeeks.org/reactjs/react/>

## 1. What is React?

- A Javascript library
- Used to create single-page applications
- Allows for the creation of reusable UI components
- Core features:
  - Virtual DOM: React updates only the changed parts of the DOM, resulting in faster rendering.
  - One-way data binding: ensures predictable and easy to debug data flow.
  - Component-based architecture: break UI into reusable pieces, improving the code reusability and scalability.

```js
import React from 'react';

// Define a React functional component
function App() {
    // render HTML-like code JSX inside the component
    return (
        <div>
            <h1>Hello World</h1>
        </div>
    );
}

// export so it can be used in other files
export default App;
```

## 2. Basic

React operates by creating an in-memory _virtual DOM_ rather than directly manipulating the browser’s DOM. It performs necessary manipulations within this virtual representation before applying changes to the actual browser DOM.

![](https://media.geeksforgeeks.org/wp-content/uploads/20250128163105949839/Browser-DOM-Virtual-DOM.webp)

- Intially, there is an Actual DOM(Real DOM) containing a div with two child elements: h1 and h2.
  - Creates a lightweight copy of the DOM (Virtual DOM).
- React maintains a previous Virtual DOM to track the UI state before any updates.
- When a change occurs, React generates a New Virtual DOM
- React compares the previous Virtual DOM with the New Virtual DOM using a process called reconciliation.
  - Compares it with the previous version to detect changes (diffing).
  - Updates only the changed parts in the actual DOM (reconciliation), improving performance.
- React identifies the differences (in this case, the new h3 element).
- Instead of updating the entire DOM, React updates only the changed part in the New Actual DOM, making the update process more efficient.

### 2.1. Components

React follows a **component-based approach**, where the UI is broken down into reusable components. These components:
- Can be functional or class-based.
- It allows code reusability, maintainability, and scalability.

Functional component:
- Stateful or Stateless (manage using React Hooks)
- Simpler sytntax (small and reusable)
- Performance (faster since they don't require a 'this' keyword)

```js
import React from 'react';

// Creating a simple functional component
function Greeting() {
  return (
    <h1>Hello, welcome to React!</h1>
  );
}

export default Greeting;
```

Class component:
- ES class that extends React.Component.
- State management: State is managed using the this.state property.
- Lifecycle methods.

```js
class Greet extends React.Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
  }
}
```

Props are read-only inputs passed from a parent component to a child component (immutable).

```js
function Greet(props) {
    return <h2>Welcome, {props.username}!</h2>;
}

// Usage
<Greet username="Anil" />;
```

State is a Javascript object managed within a component, allowing it to maintain and update its own data overtime (mutable and controlled entirely by the component).
- State updates trigger re-renders.
- Functional components use the useState hook to manage state.

```js
function Counter() {
    const [count, setCount] = React.useState(0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() =>
                setCount(count + 1)}>Increment</button>
        </div>
    );
}
```

In React, you can nest components inside other components.

### 2.2. JSX

![](https://media.geeksforgeeks.org/wp-content/uploads/20250813142958772966/react_jsx-1.webp)

JSX stands for JavaScript XML, and it is a special syntax used in React to simplify building user interfaces. JSX allows you to write HTML-like code directly inside JavaScript, enabling you to create UI components more efficiently. Although JSX looks like regular HTML, it’s actually a syntax extension for JavaScript.

```js
const element = <h1>Hello, world!</h1>;
```

When React processes this JSX code, it converts it into Javascript using Babel. This Javascript code then creates real HTML elements in the browser's DOM.

![](https://media.geeksforgeeks.org/wp-content/uploads/20250813144401818841/how_jsx_works.webp)

### 2.3. Conditional rendering

Conditional rendering allows dynamic control over which UI elements or content are displayed based on specific conditions. It is commonly used in programming to show or hide elements depending on user input, data states, or system status. This technique improves user experience by ensuring that only relevant information is presented at a given time. It enables components to display different outputs depending on states or props. This ensures that the UI updates dynamically based on logic instead of manually manipulating the DOM.

> [!note]
> I don't know this section is basic programming (if/else). [Figure out yourself](https://www.geeksforgeeks.org/reactjs/reactjs-conditional-rendering/).

### 2.4. Prop drilling

Prop drilling refers to the practice of passing data through several layers of nested components in React, even though intermediate components don't directly utilize this data. This means that a middle component doesn't necessarily need the data, but it must still pass it down to the next component, creating an unnecessary and sometimes lengthy chain of props.

```js
import React from "react";

// Parent component that holds the message and passes it down
function Parent() {
    const message = "Hello from Parent";
    return (
        <div>
            <Child message={message} />
        </div>
    );
}

function Child({ message }) {
    return (
        <div>
            <Grandchild message={message} />
        </div>
    );
}

function Grandchild({ message }) {
    return (
        <div>
            <p>Message: {message}</p>
        </div>
    );
}

export default function App() {
    return (
        <div>
            <Parent />
        </div>
    );
}

// the message is passed from Parent to Grandchild through the Child, even though the Child does not use it. This can become unmanageable as the app scales.
```

**Prop drilling is problematic.** How to avoid it?

1. Using Context API

The React Context API provides a way to share values (like state, functions, or constants) between components without explicitly passing props.
- createContext() creates a context (UserContext) to share data across components.
- The App component uses UserContext.Provider to pass userName ('geeksforgeeks') as the context value.
- ParentComponent and its children (ChildComponent, GrandChildComponent) are wrapped by the provider.
- GrandChildComponent accesses the context value using useContext(UserContext).
- The value ('geeksforgeeks') is displayed in a <p> tag as “Hello, geeksforgeeks!”.

```js
import React, { createContext, useContext } from 'react';
const UserContext = createContext();
const App = () => {
    const userName = 'geeksforgeeks';
    return (
        <UserContext.Provider value={userName}>
            <Parent />
        </UserContext.Provider>
    );
};
const Parent = () => {
    return <Child />;
};
const Child = () => {
    return <GrandChild />;
};
const GrandChild = () => {
    const userName = useContext(UserContext); // Access context value
    return <p>Hello, {userName}!</p>;
};
export default App;
```

2. Using Custom hooks

Custom hooks are reusable functions in React that encapsulate stateful logic, starting with use (e.g., useFetch). They improve code reusability, keep components clean, and allow sharing logic across components.

```js
import React, { createContext, useContext } from "react";
const UserContext = createContext();
const useUser = () => { return useContext(UserContext); };
const App = () => {
    const userName = "GeeksforGeeks";

    return (
        <UserContext.Provider value={userName}>
            <Component />
        </UserContext.Provider>
    );
};
const Component = () => {
    return <Child />;
};
const Child = () => { return <Grand />; };
const Grand = () => {
    const userName = useUser();
    return <p>Hello, {userName}!</p>;
};
export default App;
```

3. Global state management (Redux, Zustasnd, MobX)

In this approach we use libraries such as Redux, Zustand, or MobX manage application state globally, eliminating the need for prop drilling entirely.

### 2.5. React Hooks

React offers various hooks to handle state, side effects, and other functionalities in functional components.

![](https://media.geeksforgeeks.org/wp-content/uploads/20250808130739313342/hooks_in_react.webp)

**1. State hooks**

State hooks allow functional components to manage state in a more efficient and modular way. They provide an easier and cleaner approach to managing component-level states in comparison to class components.
- useState: The useState hook is used to declare state variables in functional components. It allows us to read and update the state within the component.

```js
const [state, setState] = useState(initialState);
// state: The current value of the state.
// setState: A function used to update the state.
// initialState: The initial value of the state, which can be a primitive type or an object/array
```

- useReducer: The useReducer hook is a more advanced state management hook used for handling more complex state logic, often involving multiple sub-values or more intricate state transitions.

```js
const [state, dispatch] = useReducer(reducer, initialState);
// state: The current state value.
// dispatch: A function used to dispatch actions that will update the state.
// reducer: A function that defines how the state should change based on the dispatched action.
// initialState: The initial state value.
```

**2. Context hooks**

The useContext hook in React is a powerful and convenient way to consume values from the React Context API in functional components. It allows functional components to access context values directly, without the need to manually pass props down through the component tree.

```js
import React, { createContext, useContext, useState } from "react";

const ThemeContext = createContext();

function App() {
    const [theme, setTheme] = useState("light");

    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
    };

    return (
        <ThemeContext.Provider value={theme}>
            <div>
                <h1>Current Theme: {theme}</h1>
                <button onClick={toggleTheme}>Toggle Theme</button>
                <ThemeDisplay />
            </div>
        </ThemeContext.Provider>
        // The provider makes the context value accessible to all components below it in the component tree
    );
}

function ThemeDisplay() {
    const theme = useContext(ThemeContext);
    // useContext allows you to consume context values, making it easier to share data across components without prop drilling.

    return <h2>Theme from Context: {theme}</h2>;
}

export default App;
```

**3. Effect hooks**

Effect hooks, specifically useEffect,useLayoutEffect, and useInsertionEffect, enable functional components to handle side effects in a more efficient and modular way.

- useEffect: used to handle side effects in functional components. It allows you to perform actions such as data fetching, DOM manipulation, and setting up subscriptions, which are typically handled in lifecycle methods like componentDidMount or componentDidUpdate in class components.

```js
useEffect(() => {
    // Side effect logic here
}, [dependencies]);
// useEffect(() => { ... }, [dependencies]); runs side effects after rendering.
// The effect runs based on changes in the specified dependencies.
```

- useLayoutEffect: The useLayoutEffect is used when we need to measure or manipulate the lawet before the browser paints, ensuring smooth transitions and no flickering.

```js
useLayoutEffect(() => {
  // Logic to manipulate layout or measure DOM elements
}, [dependencies]);
```

- useInsertionEffect: The useInsertionEffect is designed for injecting styles early, especially useful for server-side rendering (SSR) or styling libraries, ensuring styles are in place before the component is rendered visually.

```js
useInsertionEffect(() => {
    // Logic to inject styles or manipulate stylesheets
}, [dependencies]);
```

**4. Performance hooks**

Performance Hooks in React, like useMemo and useCallback, are used to optimize performance by avoiding unnecessary re-renders or recalculations.

- useMemo: React hook that memoizes the result of an expensive calculation, preventing it from being recalculated on every render unless its dependencies change. This is particularly useful when we have a computation that is expensive in terms of performance, and we want to avoid recalculating it on every render cycle.

```js
import React, { useState, useMemo } from "react";

function App() {
    const [count, setCount] = useState(0);
    const [text, setText] = useState("");

    // use memoizes the result of expensiveCalculation, and only recomputes when count changes.
    const expensiveCalculation = useMemo(() => {
        console.log("Expensive calculation...");
        return count * 2;
    }, [count]);

    return (
        <div>
            <h1>Count: {count}</h1>
            <h2>Expensive Calculation: {expensiveCalculation}</h2>
            <button onClick={() => setCount(count + 1)}>Increment Count</button>

            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type something"
            />
        </div>
    );
}

export default App;
```

- useCallback: React hook that helps to memoize functions, ensuring that a function is not redefined on every render unless its dependencies change. This is particularly useful when passing functions as props to child components, as it prevents unnecessary re-renders of those child components.

```js
const memoizedCallback = useCallback(() => { doSomething(a, b); }, [a, b]);
```

## 2.6. React Router

React Router is a JavaScript library designed specifically for React to handle client-side routing. It maps specific URL paths to React components, allowing users to navigate between different pages or sections without refreshing the entire page.

There are three types of routers:
- BrowserRouter: The BrowserRouter is the most commonly used router for modern React applications. It uses the HTML5 History API to manage routing, which allows the URL to be dynamically updated while ensuring the browser's address bar and history are in sync.
- HashRouter: The HashRouter is useful when you want to use a URL hash (#) for routing, rather than the HTML5 history API. It doesn't require server configuration and works even if the server doesn't support URL rewriting.
- MemoryRouter: The MemoryRouter is used in non-browser environments, such as in React Native or when running tests.
