# C4 Model

Software architecture diagrams are fantastic way to communicate how you're planning to build software system (up-front design), or how existing software system works. However, it's very likely that the majority of the software architecture diagrams you've seen are a confused mess of boxes and lines. An unfortunate and unintended side effect of the Agile Software Development is that many teams have stopped and scaled back their diagraming and documentation efforts, including the use of Unified Modeling Language (UML).

Teams are switching to a much simpler approach: "boxes and lines" diagrams. But as the result, teams've lost the ability to communicate software architecture. That's why **C4 model** was created, to help software development teams describe and communicate software architecture, both during up-front design sessions and when retrospectively documenting an existing codebase.

```
It's a way to create maps of your code, at various levels of detail, in the same way you would use something like Google Maps to zoom in and out of an area you're interested in
-- C4 model documentation --
```

![](https://c4model.com/img/c4-overview.png)

- C4 model is an "abstraction-first" approach to diagramming software architecture, based upon abstractions that reflect how software architects and developers think about and build software.
- C4 model considers the static structures of a **software system** in terms of **containers**, **component**, and **code**.
  - Software system: describes something that delivers value to its users, whether they are human of not (includes the software system you are modelling, and the other software systems upon which your software system depends).
  - Container (*Not Container in Docker!*): represents an application or a data store. A cotnainer is something that needs to be running order for the overall software system to work:
    - Server-side web application.
    - Client-side web application.
    - Mobile app.
    - File system.
    - Database.
    - ...
  - Component: a grouping of related functionality encapsulated behind a well-defined interface. All components inside a container typically execute in the same process space.
  - Code: Classes, interfaces, objects, functions,...

![](https://c4model.com/img/abstractions.png)

- Visualising this hierarchy of abstraction is then done by creating a collection of **Context**, **Container**, **Component** and **Code** (UML class) diagrams.

| Level                     | Scope                    | Primary elements                                                                                            | Supporting elements                                                                                                 | Intended audience                                                                                                                             | Recommended for most teams                                                                                                         | Note                              |
| ------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1. System context diagram | A single software system | The software system in scope                                                                                | People and software systems (external dependencies) that are directly connected to the software system in scope.    | Everybody                                                                                                                                     | Yes                                                                                                                                |                                   |
| 2. Container diagram      | A single software system | Containers within the software system in scope                                                              | People and software systems directly connected to the containers                                                    | Technical people inside and outside of the software development team; including software architects, developers, and operations/support staff | Yes                                                                                                                                | Say nothing about deployments,... |
| 3. Component diagram      | A single container       | Components within the container in scope                                                                    | Containers (within the software system in scope) + people and software systems directly connected to the components | Software architects and developers                                                                                                            | No, only create component diagrams if you feel they add value, and consider automating their creation for long-lived documentation |                                   |
| 4. Code                   | A single component       | Code elements (classes, interfaces, objects, functions, database tables, etc) within the component in scope | Software architects and developers                                                                                  | No, for long-lived documentation, most IDEs can generate this level of detail on demand                                                       |                                                                                                                                    |

- Supplementary diagrams:

| Level                       | Scope                                       | Primary elements                                                       | Supporting elements                                              | Intended audience                                                    | Recommended for most teams | Note |
| --------------------------- | ------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------- | ---- |
| 5. System landscape diagram | An enterprise                               | People and software systems related to the enterprise in scope         |                                                                  | Intended audience                                                    |                            |      |
| 6. Dynamic diagram          | An enterprise, software system or container | Depends on the diagram scope; enterprise, software system, container   |                                                                  | People, inside and outside of the software development team          |                            |      |
| 7. Deployment diagram       | One or more software systems                | Deployment nodes, software system instances, and containers instances. | Infrastructure nodes used on the deployment of the software team | Technical people inside and outside of the software development team |                            |

- C4 and UML: although the example diagrams above are created using a "boxes and lines" notation, the core diagrams can be illustrated using UML within the appropriate use of packages, components, and stereotypes.
