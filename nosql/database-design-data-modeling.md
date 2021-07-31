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
- Document databases stores data in the document data type, which is similar to a JSON document or object. Queries are used to retrieve field values.
- Key-value database, the simplest type of database. Data is retrieved using the direct request method rather than through the use of a query language.
- Wide-column stores use a table form but in a flexible and scalable way. Data is retrieved using a query language.
- Graph databases consist nodes connected by edges. Node and relationship information is retrieved using specialized query language.