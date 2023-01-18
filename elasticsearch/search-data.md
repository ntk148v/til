# Search data

## Near real-time search

- A document is stored in Elasticsearch, it is indexed and fully searchable in _near real-time_ - within 1 second.
- Lucene introduced the concept of per-segment search. A _segment_ is similar to an inverted index. After a commit, a new segment is added to the commit point and the buffer is cleared.
- Documents in the in-memory indexing buffer are written to new segment.

  - A lucene index with new documents in the in-memory buffer - filesystem cache (cheap).

  ![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/lucene-in-memory-buffer.png)

  - The buffer conents are written to a segment, which is searchable, but is not yet commited.

  ![](https://www.elastic.co/guide/en/elasticsearch/reference/current/images/lucene-written-not-committed.png)

- This process of writing and opening a new segment is called a _refresh_. A referesh makes all operations performed on an index since the last refresh avaiable for search, but it doesn't make sure that they are written to disk to a persistent storage, as it doesn't call fsync, thus doesn't guarantee durability (lucene commit, way more expensive).
  - Waiting for the refresh interval.
  - Setting [refresh](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-refresh.html) option.
  - Using the [Refresh API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-refresh.html) to explicity complete a refresh.
- By default, Elasticsearch periodically refreshes indices every second, but only on indices that have received one search request or more in the last 30 seconds.

![](https://i.stack.imgur.com/8tkrD.png)
