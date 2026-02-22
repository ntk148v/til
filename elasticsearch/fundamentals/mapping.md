# Introduction to Mapping

## 1. Overview

- Mapping describes how documents and their fields are indexed and stored (defining the data types and formats of fields).
- Each document is a collection of fields, which each have their own **data type**. When mapping your data, you create a mapping definition, which contains a list of fields that are pertinent to the document. A mapping definition also includes **metadata fields**, like the `_source` field, which customize how a document's associated metadata is handled.
  - Field data type: This type indicates the kind of data the field contains, such as strings or boolean values, and its intended use
  - Metadata fields: Each document has metadata associated with it, such as the `_index`, mapping `_type`, and `_id` metadata fields.

## 2. Define mapping

- Use dynamic mapping and explicit mapping to define your data.

### 2.1. Dynamic mapping

- When Elasticsearch detects a new field in a document, it dynamically adds the field to the type mapping by default.
- Elasticsearch uses the rules in the [table](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-field-mapping.html) to determine how to map data types for each field.
- Use [dynamic template](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html) to define custom mappings.

### 2.2. Explicit mapping

- Allows you to precisely choose how to define the mapping definition, such as:
  - Which string fields should be treated as full text fields.
  - Which fields contain numbers, dates or geolocations.
  - The format of date values.
  - Custom rules to control the mapping for dynamically added fields.

## 3. Gotchas

- Existing type and field mappings cannot be updated.
- Fields are shared across mapping types. What this mean, is that if a `title` field exists in both an `employee` and `article` mapping type, then the fields must have exactly the same mapping in each type.
