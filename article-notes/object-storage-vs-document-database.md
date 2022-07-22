# Object storage or Document database?

Source: <https://serverless.pub/s3-or-dynamodb/>

- AWS S3 = Object storage
- AWS DynamoDB = Document database

- [Object storage or Document database?](#object-storage-or-document-database)
  - [1. Key feature differences](#1-key-feature-differences)
  - [2. Quick rules of thumb](#2-quick-rules-of-thumb)

## 1. Key feature differences

- S3 is an _object store_
  - Designed for large binary unstructured data.
  - Store individual objects up to 5TB.
  - The objects are aggregated into _buckets_ - like a namespace or a database table.
  - Designed for throughput, not nescessarily predictable (or very low) latency.
  - Work on entire items. Atomic batch operations on groups of objects are not possible, and it's difficult to work with parts of an individual object.
  - Useful for extract-transform-load data warehouse sceniarios than for ad-hoc or online request.
  - Provides eventual consistency.
  - Support automatic versioning.
- DynamoDB is a _document database_, a NoSQL database.
  - Designed for storing structured textual (JSON) data, supporting individual items up to 400KB.
  - Stores items in _tables_, which can either be in a particular region or globally replicated.
  - Designed for low latency and sustained usage patterns. If the average item is relatively small, espacially if items are less than 4KB, DynamoDB is significantly faster than S3 for individual operations.
  - Works with structured documents, so its smalltest atom of operation is a property inside an item.
  - Can handle batch operations and conditional updates, even atomic transactions on multiple items.
  - Able to setup indexes for efficiently querying properties of items.
  - Can enfore strong read consistency.
  - Does not provide object versioning out of the box.

## 2. Quick rules of thumb

![](https://serverless.pub/img/s3ordynamo.png)

- For example:
  - Use S3 to store files and most user requests, such as share invitations and conversion requests.
  - Use DynamoDB to store account information, such as subscription data and payment references.
