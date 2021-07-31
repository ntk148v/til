---
title: NoSQL Database Design & Data Modeling
path: nosql/database-design-data-modeling.md
---
Source: https://www.mongodb.com/nosql-explained/data-modeling

## Schema Design for NoSQL Databases

- NoSQL databases are designed to store data that does not have a fixed structure.
- Fundamental property: the need to optimize data access.
- How users will query the data and how often.
- How often will data be updated?

## NoSQL Data Modeling

- Each of the 4 main types of NoSQL databases is based on a specific way of storing data.
- Document Store: Data and metadata are stored hierarchically in JSON-based documents inside the database. (query language)
- Key Value Store: The simplest of the NoSQL databases, data is represented as a collection of key-value pairs. (direct request method)
- Wide-Column Store: Related data is stored as a set of nested-key/value pairs within a single column. (direct language)
- Graph Store: Data is stored in a graph structure as node, edge, and data properties. (specialized query language)