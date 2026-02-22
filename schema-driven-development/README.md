# Schema-driven development

Source: <https://99designs.com/blog/engineering/schema-driven-development/>

Table of contents:

- [Schema-driven development](#schema-driven-development)
  - [1. Introduction](#1-introduction)
  - [2. SDD technologies](#2-sdd-technologies)
    - [2.1. GraphQL](#21-graphql)
    - [2.2.gRPC/Twirp](#22grpctwirp)
    - [2.3. Prisma](#23-prisma)

## 1. Introduction

- The _schema_ is a contract between two sides of a system.
  - The schema communicates the type of requests that can be made and the expected type of response.

  ![](https://99designs-blog.imgix.net/blog/wp-content/uploads/2021/07/013zl5qonwt38590jxr7-e1626161750821.png?auto=format&q=60&fit=max&w=930)
  - A schema follows a specific, unambiguous type of language defined by the technology that you use.
  - Schema language is usually programming-language agnostic that communicates common software ideas such as objects, enumeration, field types.

- Schema-driven development (SDD):
  - SDD prioritises the design of the schema and uses it as the first-class citizen to communicate the responsibilities of the client and the server. This contract usually becomes the API.
  - Benefits:
    - Better cross-team communications
    - Better API design
    - Independent client and server development
    - Clear entity relationships
    - Type-safety: Type-safety is important when building medium to large applications. A lot of bugs can be caught at compile time by using languages like Go or TypeScript.

## 2. SDD technologies

### 2.1. GraphQL

- [GraphQL](https://graphql.org/)'s schema is called Schema Definition Language (SDL).
- Checkout [GraphQL til](../graphql/README.md)
- Common use case: Browser/Mobile to Server/s communication.
- Schema-first development, Schema Definition Language First (SDL-first) and code-first:
  - Schema-first development: the process of building software where schema-design is prioritised.
  - SDL-first: an implementation approach where code is often generated from the schema.
  - Code-first: an implementation approach where resolvers are created first and the schema is generated from the code.

![](https://99designs-blog.imgix.net/blog/wp-content/uploads/2021/07/aa-4.png?auto=format&q=60&fit=max&w=930)

### 2.2.gRPC/Twirp

- [gRPC](https://grpc.io/), [Twirp](https://twitchtv.github.io/twirp/docs/intro.html) are Remote Procedure Call frameworks.
- gRPC, Twirp use Protocol Buffers (protobuf) as the Interface Definition Language. Protobuf is also the serialization protocol for structured data.
- They are commonly used in a micro-service architecture. The client is the service making the request and the server is the service returning the response. Services can choose to send data encoded using Protobuf or JSON. Protobuf can be serialized and sent faster than JSON. JSON is useful if you need to debug calls between services.
- Check out [gRPC til](../grpc/README.md).
- Common use case: Server to server communication.

### 2.3. Prisma

- [Prisma](https://www.prisma.io/) is an Object-relational mapping (ORM) library which represents database models through a central schema written in Prisma Schema Language (PSL).
- The Prisma schema is effortlessly easy to read. It clearly shows model relationships and field types. On top of that, other important information such as database connection is also stored in the schema.

```prisma
datasource db {
  provider = "mysql"
  url      = env("PRISMA_DATABASE_URL")
}

generator client {
  provider        = "prisma-client-js"
}

model Bull {
  id     String @id @default(uuid())
  name   String
  farm   Farm
  farmId String
}

model Farm {
  id   String @id @default(uuid())
  name String
  bulls Bull[]
}
```

- Prisma is the only ORM that is easy to see the relationships of entities without connecting to the database and click through 200 tables to build up a mental map to connect all the pieces together.
- Common use case: Server to database communication.
