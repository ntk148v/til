# Uses of Elasticsearch

Source: <https://www.elastic.co/blog/found-uses-of-elasticsearch>

- Elasticsearch is used for a lot of different use cases:
    - Classical full text search
    - Analytics store
    - Auto completer
    - Spell checker
    - Alerting engine
    - General document store

## 1. You know, for search (and counting)

- Simple search `match`
- Inverted index
- Cache

## 2. Analytics

- Analytical workloads tend to count things and summarize your data - lots of data -> Elastisearch's aggregations.

## 3. Fuzzy searching

- A fuzzy search is one that is lenient forward spelling errors.
- Check out [Fuzzy searches](https://www.elastic.co/blog/found-fuzzy-search/).
- Fuzzy searches are simple to enable and can enhance “recall” a lot, but they can also be very expensive to perform. Fuzzy searches are CPU-intensive. Add them with care, and probably not to every field.
- `multi_field` and `fuzziness`

## 4. Autocompletion and Instant search

- Searching while the user types comes in many forms. It can be simple suggestions of e.g. existing tags, trying to predict a search based on search history, or just doing a completely new search for every (throttled) keystroke.
- `prefix` and `match_phrase_prefix`

## 5. Multi-tenancy

- Multiple customers/users with separate collections of documents -> every user has his own index -> too many indexes
  - The memory overhead is not negligible. Thousands of small indexes will consume a lot of heap space. The number of file descriptors can also explode.
  - A lot of duplication
  - Snapshot/Restore is currently a serial process, with an overhead per index.
- You probably should not make one index per user for your multi-tenant application.

## 6. Schema Free/User-defined schemas

- Elasticsearch's dynamic mapping. However, Elasticsearch will create a mapping for you behind the scenes, and it can be problematic when grows too big leading to a "mapping explosion".
- Even when not using a mapping, know what mapping Elasticsearch creates for you.

## 7. User-defined searches

- Be careful with user-defined search requests (CPU-intensive, memory hogging...)

## 8. Crawling and document processing

- Push processed data to Elasticsearch, don’t pull from and process within Elasticsearch.
