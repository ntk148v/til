# IndexDB

Source: <https://victoriametrics.com/blog/vmstorage-how-indexdb-works/>

VictoriaMetrics IndexDB is the inverted index component that enables efficient searching of time series by metric names, label names, and label values [1](#0-0) .

## Overview

IndexDB maintains an inverted index that maps metric names, label names, and label values to corresponding Time Series IDs (TSIDs) [2](#0-1) . Since TSIDs are internal-only identifiers, the inverted index serves as the primary mechanism for querying time series data.

## Index Types

VictoriaMetrics uses two types of inverted indexes:

1. **Global Index**: Searches across the entire retention period, with each mapping created only once per retention period [3](#0-2)
2. **Per-day Index**: Includes date in each mapping and is used for queries within shorter time ranges (40 days or less) [4](#0-3)

The system automatically chooses which index to use based on the query's time range [5](#0-4) .

## Implementation Details

### Search Process

The core search functionality is implemented in `searchMetricIDs` which:

- Takes tag filters and time range as input
- Returns sorted metric IDs that match the criteria
- Filters out deleted metric IDs from results [6](#0-5)

### Caching

IndexDB uses multiple caches for performance optimization:

- `metricIDCache`: Maps metric IDs to TSIDs for fast lookups [7](#0-6)
- `dateMetricIDCache`: Tracks (date, metricID) pairs to avoid duplicate index entries [8](#0-7)

### Data Updates

When new data arrives, the system:

- Updates per-date data by checking if (date, metricID) pairs already exist in cache
- Pre-populates the next day's index during the last hour of the current day to reduce resource spikes [9](#0-8)

## Configuration

Key configuration options include:

- `-disablePerDayIndex`: Disables per-day index to improve performance and reduce disk usage for fixed time series sets [10](#0-9)
- `-storage.idbPrefillStart`: Controls how early IndexDB pre-filling starts before rotation (default: 1 hour) [11](#0-10)
- Various cache size flags for tuning performance [12](#0-11)

## Performance Considerations

- IndexDB respects retention periods and drops indexes when retention expires [13](#0-12)
- High churn rate (frequently changing time series) can significantly increase index size [14](#0-13)
- For low churn scenarios, disabling per-day index is recommended [15](#0-14)

## Notes

The IndexDB is a critical component that bridges the gap between human-readable metric queries and internal TSID-based storage. Its dual-index design provides optimal performance for both recent queries (using per-day index) and long-term historical queries (using global index). The implementation focuses heavily on caching strategies to minimize disk I/O during query execution.

Wiki pages you might want to explore:

- [Architecture (VictoriaMetrics/VictoriaMetrics)](/wiki/VictoriaMetrics/VictoriaMetrics#2)

### Citations

**File:** docs/victoriametrics/README.md (L1465-1478)

```markdown
## IndexDB

VictoriaMetrics identifies
[time series](https://docs.victoriametrics.com/victoriametrics/keyconcepts/#time-series) by
`TSID` (time series ID) and stores
[raw samples](https://docs.victoriametrics.com/victoriametrics/keyconcepts/#raw-samples) sorted
by TSID (see [Storage](#storage)). Thus, the TSID is a primary index and could
be used for searching and retrieving raw samples. However, the TSID is never
exposed to the clients, i.e. it is for internal use only.

Instead, VictoriaMetrics maintains an **inverted index** that enables searching
the raw samples by metric name, label name, and label value by mapping these
values to the corresponding TSIDs.
```

**File:** docs/victoriametrics/README.md (L1481-1496)

```markdown
- Global index. Searches using this index is performed across the entire
  retention period.
- Per-day index. This index stores mappings similar to ones in global index
  but also includes the date in each mapping. This speeds up data retrieval
  for queries within a shorter time range (which is often just the last day).

When the search query is executed, VictoriaMetrics decides which index to use
based on the time range of the query:

- Per-day index is used if the search time range is 40 days or less.
- Global index is used for search queries with a time range greater than 40
  days.

Mappings are added to the indexes during the data ingestion:

- In global index each mapping is created only once per retention period.
```

**File:** docs/victoriametrics/README.md (L1500-1502)

```markdown
IndexDB respects [retention period](#retention) and once it is over, the indexes
are dropped. For the new retention period, the indexes are gradually populated
again as the new samples arrive.
```

**File:** docs/victoriametrics/README.md (L1519-1521)

```markdown
But if your use case assumes low or no churn rate, then you might benefit from disabling the per-day index by setting
the flag `-disablePerDayIndex`{{% available_from "v1.112.0" %}}. This will improve the time series ingestion speed and decrease disk space usage,
since no time or disk space is spent maintaining the per-day index.
```

**File:** lib/storage/index_db.go (L341-361)

```go
func (db *indexDB) getFromMetricIDCache(dst *TSID, metricID uint64) error {
	// There is no need in checking for deleted metricIDs here, since they
	// must be checked by the caller.
	buf := (*[unsafe.Sizeof(*dst)]byte)(unsafe.Pointer(dst))
	key := (*[unsafe.Sizeof(metricID)]byte)(unsafe.Pointer(&metricID))
	tmp := db.s.metricIDCache.Get(buf[:0], key[:])
	if len(tmp) == 0 {
		// The TSID for the given metricID wasn't found in the cache.
		return io.EOF
	}
	if &tmp[0] != &buf[0] || len(tmp) != len(buf) {
		return fmt.Errorf("corrupted MetricID->TSID cache: unexpected size for metricID=%d value; got %d bytes; want %d bytes", metricID, len(tmp), len(buf))
	}
	return nil
}

func (db *indexDB) putToMetricIDCache(metricID uint64, tsid *TSID) {
	buf := (*[unsafe.Sizeof(*tsid)]byte)(unsafe.Pointer(tsid))
	key := (*[unsafe.Sizeof(metricID)]byte)(unsafe.Pointer(&metricID))
	db.s.metricIDCache.Set(key[:], buf[:])
}
```

**File:** lib/storage/index_db.go (L2194-2210)

```go
// The returned metricIDs are sorted.
func (is *indexSearch) searchMetricIDs(qt *querytracer.Tracer, tfss []*TagFilters, tr TimeRange, maxMetrics int) (*uint64set.Set, error) {
	metricIDs, err := is.searchMetricIDsInternal(qt, tfss, tr, maxMetrics)
	if err != nil {
		return nil, err
	}
	if metricIDs.Len() == 0 {
		// Nothing found
		return nil, nil
	}

	// Filter out deleted metricIDs.
	dmis := is.db.s.getDeletedMetricIDs()
	metricIDs.Subtract(dmis)

	return metricIDs, nil
}
```

**File:** lib/storage/storage.go (L2305-2367)

```go
func (s *Storage) updatePerDateData(idb *indexDB, rows []rawRow, mrs []*MetricRow, hmPrev, hmCurr *hourMetricIDs) error {
	if s.disablePerDayIndex {
		return nil
	}

	var date uint64
	var hour uint64
	var prevTimestamp int64
	var (
		// These vars are used for speeding up bulk imports when multiple adjacent rows
		// contain the same (metricID, date) pairs.
		prevDate     uint64
		prevMetricID uint64
	)

	hmPrevDate := hmPrev.hour / 24
	nextDayMetricIDs := &s.nextDayMetricIDs.Load().metricIDs
	ts := fasttime.UnixTimestamp()
	// Start pre-populating the next per-day inverted index during the last hour of the current day.
	// pMin linearly increases from 0 to 1 during the last hour of the day.
	pMin := (float64(ts%(3600*24)) / 3600) - 23
	type pendingDateMetricID struct {
		date uint64
		tsid *TSID
		mr   *MetricRow
	}
	var pendingDateMetricIDs []pendingDateMetricID
	var pendingNextDayMetricIDs []uint64
	for i := range rows {
		r := &rows[i]
		if r.Timestamp != prevTimestamp {
			date = uint64(r.Timestamp) / msecPerDay
			hour = uint64(r.Timestamp) / msecPerHour
			prevTimestamp = r.Timestamp
		}
		metricID := r.TSID.MetricID
		if metricID == prevMetricID && date == prevDate {
			// Fast path for bulk import of multiple rows with the same (date, metricID) pairs.
			continue
		}
		prevDate = date
		prevMetricID = metricID
		if hour == hmCurr.hour {
			// The row belongs to the current hour. Check for the current hour cache.
			if hmCurr.m.Has(metricID) {
				// Fast path: the metricID is in the current hour cache.
				// This means the metricID has been already added to per-day inverted index.

				// Gradually pre-populate per-day inverted index for the next day during the last hour of the current day.
				// This should reduce CPU usage spike and slowdown at the beginning of the next day
				// when entries for all the active time series must be added to the index.
				// This should address https://github.com/VictoriaMetrics/VictoriaMetrics/issues/430 .
				if pMin > 0 {
					p := float64(uint32(fastHashUint64(metricID))) / (1 << 32)
					if p < pMin && !nextDayMetricIDs.Has(metricID) {
						pendingDateMetricIDs = append(pendingDateMetricIDs, pendingDateMetricID{
							date: date + 1,
							tsid: &r.TSID,
							mr:   mrs[i],
						})
						pendingNextDayMetricIDs = append(pendingNextDayMetricIDs, metricID)
					}
				}
```

**File:** lib/storage/storage.go (L2376-2384)

```go
		// Slower path: check the dateMetricIDCache if the (date, metricID) pair
		// is already present in indexDB.
		//
		// TODO(@rtm0): indexDB.dateMetricIDCache should not be used directly
		// since its purpose is to optimize is.hasDateMetricID(). See if this
		// function could be changed so that it does not rely on this cache.
		if idb.dateMetricIDCache.Has(date, metricID) {
			continue
		}
```

**File:** app/vmstorage/main.go (L79-82)

```go
	disablePerDayIndex = flag.Bool("disablePerDayIndex", false, "Disable per-day index and use global index for all searches. "+
		"This may improve performance and decrease disk space usage for the use cases with fixed set of timeseries scattered across a "+
		"big time range (for example, when loading years of historical data). "+
		"See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#index-tuning")
```

**File:** app/vmstorage/main.go (L89-91)

```go
	idbPrefillStart = flag.Duration("storage.idbPrefillStart", time.Hour, "Specifies how early VictoriaMetrics starts pre-filling indexDB records before indexDB rotation. "+
		"Starting the pre-fill process earlier can help reduce resource usage spikes during rotation. "+
		"In most cases, this value should not be changed. The maximum allowed value is 23h.")
```

**File:** docs/victoriametrics/victoria_metrics_flags.md (L552-572)

```markdown
-storage.cacheSizeIndexDBDataBlocks size
Overrides max size for indexdb/dataBlocks cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeIndexDBDataBlocksSparse size
Overrides max size for indexdb/dataBlocksSparse cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeIndexDBIndexBlocks size
Overrides max size for indexdb/indexBlocks cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeIndexDBTagFilters size
Overrides max size for indexdb/tagFiltersToMetricIDs cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeMetricNamesStats size
Overrides max size for storage/metricNamesStatsTracker cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeStorageMetricName size
Overrides max size for storage/metricName cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
-storage.cacheSizeStorageTSID size
Overrides max size for storage/tsid cache. See https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/#cache-tuning
Supports the following optional suffixes for size values: KB, MB, GB, TB, KiB, MiB, GiB, TiB (default 0)
```

**File:** docs/victoriametrics/FAQ.md (L369-371)

```markdown
- Increased total number of time series stored in the database.
- Increased size of inverted index, which is stored at `<-storageDataPath>/indexdb`, since the inverted index contains entries for every label of every time series with at least a single ingested sample.
- Slow-down of queries over multiple days.
```
