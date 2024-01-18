# Google Zanzibar in a Nutshell

Source: <https://www.permify.co/post/google-zanzibar-in-a-nutshell/>

Table of content:

- [Google Zanzibar in a Nutshell](#google-zanzibar-in-a-nutshell)
  - [1. Why is Zanzibar needed?](#1-why-is-zanzibar-needed)
    - [1.1. Different permission structures of various product](#11-different-permission-structures-of-various-product)
    - [1.2. Downside of Centralized authz system at scale](#12-downside-of-centralized-authz-system-at-scale)
  - [2. What is Zanzibar?](#2-what-is-zanzibar)
    - [2.1. Data model](#21-data-model)
    - [2.2. Access control checks](#22-access-control-checks)
    - [2.3. Functionality](#23-functionality)
    - [2.4. Data consistency](#24-data-consistency)
    - [2.5. Providing Low Latency at High Scale](#25-providing-low-latency-at-high-scale)

[Zanzibar](https://research.google/pubs/pub48190/) is the global authorization system used at Google for handling authorization for hundreds of its services and products including; YouTube, Drive, Calendar, Cloud and Maps.

## 1. Why is Zanzibar needed?

- Google uses Zanzibar for its product to handle authorization. But what is Authorization? Simply, it is the process of controlling who can do, own or access a system in a application. Authorization systems can branch off due to application and user needs. Eventually, when things grow, authorization is a hard piece to solve for various reasons.
- Let's examine the two major problem Google encoutered to understand why they need Zanzibar and eventually build it.

### 1.1. Different permission structures of various product

- Modeling authorization: simple with few roles and permissions -> growth and never ending user requirements -> get uglier over time.
- In Google's case, they have a large number of applications and services with different permission needs: Drive has its own sharing authorization, Youtune has private/public video access controls, etc.
- Also access checks between resources from one application in another is every common: Google Calendar might have the right authorization for Google Meets.
- So, Google needs a flexible modeling structure where they can create and extend the combinations of different access control approaches in a unified system that makes it easier for application to interoperate.

### 1.2. Downside of Centralized authz system at scale

- First approach: build a permission system for each individual application that is connected directly with the database -> design these systems as abstract entities, such as a library or a centralized engine, that cater to many individual applications and services -> "centralized permission engine" -> stateless (don't store data), behave as an engine to manage functionality such as performing "access checks".
- In order to make an access check and compute a decision, you need to load authorization data and relations from the database and other services -> downside in terms of performance and scalability.
- Google needs a solution that is super fast, secure, and scalable while providing consistency and reliability across all applications.
  - "Correctness"
  - "Low latency"
  - "High availability"
  - "Large scale"

## 2. What is Zanzibar?

- Zanzibar is an authorization service that stores permissions as ACL styled relationships and performs access decisions according to these relations. Zanzibar unifies authorization to serve individual applications and services.

### 2.1. Data model

- Abstracting authorization data elimnates data loading issues on each enforcement action. "Can User X view document Y".
  - Traditional way: check our policy or access rules and then needed to load the necessary data for the decision.
  - Zanzibar way: you already have all of the information stored as relational tuples to make decisions quickly.
- When using Zanzibar, you tell Zanzibar about the activities that are related to authorization data:
  - We have a rule: "only document creators can view the document".
  - In that case, you need to feed Zanzibar with actions in your systems about document creation: "user X created document Y", etc. Then Zanzibar stores this information as a **relational tuple** in the centralized data source.
- Relational tuples are similar to individual ACL collections of object user or object relations and take the form of "**user U has relation R to object O**".

```text
⟨tuple⟩ ::= ⟨object⟩ # ⟨relation⟩ @ ⟨user⟩

-> When user 1 created document 2 you need to send the object and the subject relation. If the Zanzibar system were a person you'd say "Hey Zanzibar user:1 is owner of document:2". And this data stored as `document:2#owner@user:1`

⟨object⟩ ::= ⟨namespace⟩ : ⟨object id⟩

⟨user⟩ ::= ⟨user id⟩ | ⟨userset⟩

⟨userset⟩ ::= ⟨object⟩ # ⟨relation⟩
```

- So the Zanzibar derived system unifies and stores a collection of relational tuples as authorization data.

### 2.2. Access control checks

- All of these relational tuples and authorization model combines and build up a relations graph, which is mainly used for the access control check.

![](https://user-images.githubusercontent.com/34595361/213842820-8920066c-eec8-468b-9465-202464813a44.png)

- Evaluating access decisions operate as a walkthrough of this directed graph.

### 2.3. Functionality

- Zanzibar has five core methods: **read, write, watch, check, expand**.
- The read, write, and watch methods are used for interacting directly with the authorization data (relation tuples), while the check and expand methods are focused specifically on authorization.

### 2.4. Data consistency

- Zanzibar avoids the inconsistent data with an approach of snapshot reads. Basically it ensures that enforcement is evaluated at a consistent point of time to prevent inconsistency. Zanzibar team developed tokens called Zookies that consist of a timestamp which is compared in access checks to ensure that the snapshot of the enforcement is at least as fresh as the resource version’s timestamp.

### 2.5. Providing Low Latency at High Scale

- Zanzibar replicates all ACL data in tens of geographically distributed data centers and distributes load across thousands of servers around the world.
