# IndexDB

Source: <https://victoriametrics.com/blog/vmstorage-how-indexdb-works/>

VictoriaMetrics identifies time series by `TSID` (time series ID) and stores raw samples sorted by `TSID`. Thus, the TSID is a primary index and could be used for searching and retrieving raw samples. However, the TSID is never exposed to the clients, i.e. it is for internal use only.

Instead, VictoriaMetrics maintains an **inverted index** that enables searching the raw samples by metric name, label name, and label value by mapping these values to the corresponding TSIDs.

VictoriaMetrics uses two types of inverted indexes:

- Global index. Searches using this index is performed across the entire retention period.
- Per-day index. This index stores mappings similar to ones in global index but also includes the date in each mapping. This speeds up data retrieval for queries within a shorter time range (which is often just the last day).

Mappings are added to the indexes during the data ingestion:

- In global index each mapping is created only once per retention period.
- In the per-day index each mapping is created for each unique date that has been seen in the samples for the corresponding time series.

When the search query is executed, VictoriaMetrics decides which index to use based on the time range of the query:

- Per-day index is used if the search time range is 40 days or less.
- Global index is used for search queries with a time range greater than 40 days.

Mappings are added to the indexes during the data ingestion:

- In global index each mapping is created only once per retention period.
- In the per-day index each mapping is created for each unique date that has been seen in the samples for the corresponding time series.

IndexDB respects retention period and once it is over, the indexes are dropped. For the new retention period, the indexes are gradually populated again as the new samples arrive.
