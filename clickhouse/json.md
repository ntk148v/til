# Using JSON

Source: <https://clickhouse.com/docs/best-practices/use-json-where-appropriate>

ClickHouse now offers a native JSON column type designed for semi-structured and dynamic data. **This is a column type, not data format**. You should only use the JSON type when the structure of your data is dynamic, not when you simply happen to store JSON.

Important trade-offs:

- Slower `INSERT`s - splitting into sub-columns, performing type inference, and managing flexible storage structures makes inserts slower compared to storing JSON as a simple `String` column.
- Slower when reading entire objects - If you need to retrieve complete `JSON` documents (rather than specific fields), the `JSON` type is slower than reading from a `String` column. The overhead of reconstructing objects from separate sub-columns provides no benefit when you're not doing field-level queries.
- Storage overhead - Maintaining separate sub-columns adds structural overhead compared to storing JSON as a single string value.

**Use the JSON type when**:

- Your data has a dynamic or unpredictable structure with varying keys across documents
- Field types or schemas change over time or vary between records
- You need to query, filter, or aggregate on specific paths within JSON objects whose structure you can't predict upfront
- Your use case involves semi-structured data like logs, events, or user-generated content with inconsistent schemas

**Use a String column (or structured types) when**:

- Your data structure is known and consistent - in this case, use normal columns, Tuple, Array, Dynamic, or Variant types instead
- JSON documents are treated as opaque blobs that are only stored and retrieved in their entirety without field-level analysis
- You don't need to query or filter on individual JSON fields within the database
- The JSON is simply a transport/storage format, not analyzed within ClickHouse
