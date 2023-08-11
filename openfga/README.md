# OpenFGA

Source:

- <https://openfga.dev>
- <https://auth0.com/blog/auth0s-openfga-open-source-fine-grained-authorization-system/>
- <https://embesozzi.medium.com/keycloak-integration-with-openfga-based-on-zanzibar-for-fine-grained-authorization-at-scale-d3376de00f9a>

## 1. Introduction

- OpenFGA (Open Fine-Grained Authorization) is an open source solution to _Fine-Grained Authorization_ that applied the concept of _ReBAC_.
- _Fine-Grained Authorization_ is being able to grant individual users access to specific objects or resources in a system.
  - For instance: Google Drive, where access can be granted either to documents, or folders; it can be granted to users individually or as a group. Access regularly changes as new documents are created and shared with specific users, whether inside the same company or outside.
- _Relationship Based Access Control (ReBAC)_ allows expressing rules based on relations that users have with objects and that objects have with other objects. For example, a user can view a document if they can view its parent folder.

## 2. Concepts

> The OpenFGA service answers authorization checks by determining whether a _relationship_ exists between an _object_ and a _user_. Checks takes into consideration the _authorization model_ of the system and the _relationship tuples_ present in the system at that time in order to make a decision.

![](./openfga.png)

- **Type**: a string, it should define a class of objects with similar characteristics (`workspace`, `repository`, `organization`, ...).
- **Type definition**: a configuration that defines all possible relations a user or another object can have in relation to this type.
- **Authorization model**: a combination of one or more type definitions. This is used to define the permission model of a system.
  - Authorization model, together with **relationship tuples**, allow determination of whether a relationship exists between a **user** and an **object**.
- **Store**: a OpenFGA entity used for organizing data needed to answer authorization checks. Each store contains one or more versions of an **authorization model** and may contain various **relationship tuples**.
- **Object**: represents an entity in the system. We can define how various users have a relationship to it through relationship tuples and the authorization model.

  - An object is a combination of a type and an identifier.
  - For example:

  ```dsl
  workspace:fb83c013-3060-41f4-9590-d3233a67938f
  repository:auth0/express-jwt
  organization:org_ajUc9kJ
  document:new-roadmap
  ```

- **User**: an entity in the system that can be related to an object.

  - An user is a combination of a type, an identifier and an optional relation.
  - For example:

  ```dsl
  # any identifier
  user:anne
  user:4179af14-f0c0-4930-88fd-5570c7bf6f59
  # any object
  workspace:fb83c013-3060-41f4-9590-d3233a67938f
  repository:auth0/express-jwt
  # a group or a set of users
  organization:org_ajUc9kJ#members
  # everyone
  *
  ```

- **Relation**: a string defined in the type definition of authorization model that defines the possibility of a relationship between an object of the same type as the type definition and a user in the system.
- **Relation definition**: lists the conditions or requirements under which this relationship would be possible.
- **Directly related user type**: an array specified in the type definition to indicate what types of users can be directly related to that relation.
- **Relationship tuple**: a tuple consisting of a user, relation and object stored in OpenFGA.

  - For example:

  ```json
  [
    {
      "user": "user:anne",
      "relation": "editor",
      "object": "document:new-roadmap"
    }
  ]
  ```

- **Relationship**: the realization of a relation between a user and an object.
- **Direct and Implied relationship**:

  - A direct relationship R between user X and object Y means the relationship tuple (user=X, relation=R, object=Y) exists.

    - `user:anne` has a direct relationship with `document:new-roadmap` as `viewer` if the type definition allows it (allows direct relationship type restrictions), and one of the following relationship tuples exist.

    ```json
    [
      // Anne of type user is directly related to the document
      {
        "user": "user:anne",
        "relation": "viewer",
        "object": "document:new-roadmap"
      }
    ]
    ```

  - An implied (or computed) relationship R exists between user X and object Y if user X is related to an object Z that is in a direct or implied relationship with object Y.

    - `user:anne` has an implied relationship with `document:new-roadmap` as `viewer` if the type definition allows it, and the presence of relationship tuples satisfying the relationship exist.

    ```dsl
    type document
    relations
        define viewer: [user] or editor
        define editor: [user]
    ```

    ```json
    [
      {
        "user": "user:anne",
        "relation": "editor",
        "object": "document:new-roadmap"
      }
    ]
    ```

- **Check request**: a call to OpenFGA check endpoint that returns whether the user has a certain relationship with an object.
- **A list objects request**: a call to OpenFGA check endpoint endpoint that returns all the objects of a given type that a user has specified relationship with.
- **Contextual tuple**: tuples that can be added to a **check request**, and only exist within the context of that particular request.
- **Type bound public access** (`<type>:*`): a special OpenFGA syntax meaning every object of that type when used as a user within a relationship tuple.
