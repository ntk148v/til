# GraphQL

Source: https://www.howtographql.com/

- [GraphQL](#graphql)
  - [1. Introduction](#1-introduction)
  - [2. GraphQL vs REST](#2-graphql-vs-rest)
  - [3. Core concepts](#3-core-concepts)
  - [4. Architecture](#4-architecture)

## 1. Introduction

- New **API** standard. A more efficient Alternative to REST:
  - Increased mobile usage creates need for efficient data loading.
  - Variety of different frontend frameworks and platforms.
  - Fast development & expectation for rapid feature development.
- Enables **declarative data fetching** where a client can specify what data it needs from an API.
- GraphQL server exposes **single endpoint** and respond to **queries**.
- A **query language** for APIs.
- Can be used with any programming language and framework.

## 2. GraphQL vs REST

- Scenario: An app needs to display the titles of the posts of a specific user. The same screen also displays the names of the last 3 followers of that user.
- REST API: Access multiple endpoints.
  - `/users/<id>` fetchs the initial user data.
  - `/users/<id>/posts` returns all the posts for a user.
  - `/users/<id>/followers` returns a list of followers per user.

![](https://imgur.com/VRyV7Jh.png)

- GraphQL: Send a single query to the GrahQL server that includes the concrete data requirements. The server then responds with a JSON object where thee requirements are fulfilled.

![](https://imgur.com/z9VKnHs.png)

- No more Over/Underfetching.
  - Overfetching: Downloading unnecessary data.
  - Underfetching: An endpoint doesn't return enough of the right information, need to send multiple requests (n+1-requests problem).

## 3. Core concepts

- Schema Definition Language (SDL): GraphQL has its own type system that’s used to define the schema of an API. The syntax for writing schemas is called Schema Definition Language (SDL).

```graphql
type Person {
  name: String! # the ! - this field is required.
  age: Int!
  posts: [Post!]! # relation - one-to-many-relationship
  # between Person and Post since the
  # posts field is an array of posts
}

type Post {
  title: String!
  author: Person!
}
```

- Fetching data with **queries**.

```graphql
# Query
{
  allPersons {
    name
  }
}
# Response
{
  "allPersons": [
    { "name": "Johnny" },
    { "name": "Sarah" },
    { "name": "Alice" }
  ]
}

# Query with arguments
{
  allPersons(last: 2) {
    name
  }
}
```

- Writing data with **mutations** (create/update/delete).

```graphql
mutation { # Always need to start with mutation keyword
  createPerson(name: "Bob", age: 36) {
    name
    age
  }
}
# Response
"createPerson": {
  "name": "Bob",
  "age": 36,
}
# GraphQL types have unique IDs that are generated
# by the server when new objects are created
# Extending Person type from before, add an id:
type Person {
  id: ID!
  name: String!
  age: Int!
}
```

- Realtime updates with **subscriptions**.

```graphql
# client <---steady connection--> server
subscription {
  newPerson {
    name
    age
  }
}
# Whenever a new mutation is performed that creates a new Person
# the server sends the information about this person over to client
{
  "newPerson": {
    "name": "Jane",
    "age": 23
  }
}
```

- Defining a **schema**.
  - Defines capabilities of the API by specifying how a client and fetch and update data.
  - Reprents contract between client and server.
  - Collection of GrapQL types with special _root types_.

```graphql
# root types
type Query {
  ...
}

type Mutation {
  ...
}

type Subscription {
  ...
}
# query type
{
  allPersons {
    name
  }
}

type Query {
  allPersons (last: Int): [Person!]!
}
# mutation type
mutation {
  createPerson(name: "Bob", age: 36) {
    id
  }
}

type Mutation {
  createPerson(name: String!, age: String!): Person!
}

# subscription type
subscription {
  newPerson {
    name
    age
  }
}

type Subscription {
  newPerson: Person!
}
```

## 4. Architecture

- Use cases:

  - GraphQL server with a connected database.

  ![](https://imgur.com/cRE6oeb.png)

  - GraphQL server that is a thin layer in front of a number of third party or legacy systems and integrates them through a single GraphQL API.

  ![](https://imgur.com/zQggcSX.png)

  - A hybrid approach of a connected database and third party or legacy systems that can all be accessed through the same GraphQL API

  ![](https://imgur.com/73dByTz.png)

- Resolver functions:
  - The sole purpose of a resolver function is to fetch data for its field.
  - When the server receives a query, it will call all the functions for the fields that are specified in the query's payload.
  - It thus resolves the query and is able to retrieve the correct dataa for each field. One all resolvers returned, the server will package data up in the format that was described by the query and send it back to the client.
