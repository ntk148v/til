# The life of a metric

Source: <https://victoriametrics.com/blog/the-life-of-a-metric/>

The sample metric: an HTTP request counter

```text
http_requests_total{method="GET", status="200", path="/api/users"} 1027
```

## 1. Birth: the counter living in memory

When your code increments the counter, nothing leaves your process. No network call, no disk write, nothing. The metrics library just updates a number in memory.

```text
http_requests_total
  {method=GET,  status=200, path=/api/users}  -> 1027
  {method=POST, status=201, path=/api/users}  ->   84
  {method=GET,  status=500, path=/api/users}  ->    3
```

But those numbers are useless if they never leave the process. So on a fixed interval, the values are **exported**: either the process is _scraped_ or it _pushes_ a snapshot to a collector.

## 2. The journey over the wire

The moment the snapshot is taken, our series leaves home for the first time. It gets serialized (usually into Protocol Buffers) alongside its current value and the other metrics, and sent over HTTP to VictoriaMetrics.

Besides the metric name and its labels, our data point carries just two more things that matter later: an absolute timestamp and the cumulative value at that moment. It does not announce “+500”; it announces “the total is now 1527, as of this instant.” That is exactly what VictoriaMetrics stores.

## 3. Arrival: every protocol becomes the same shape

VictoriaMetrics does it translate it into one internal shape that the rest of the system understands: the request is decompressed, decoded, and flattened into simple (labels, timestamps, value) records. Part of that flattening is a small transformation that comes back to help us later: the metric name becomes a label. The name `http_requests_total` is stored as a special label called `__name__`, sitting right alongside method, status, and path. After this, a series really is just a set of labels.

```text
{__name__="http_requests_total", method="GET", status="200", path="/api/users"}  ts=...  value=1527
```

## 4. Naming the series: from labels to a tiny number

The labels get packed into a compact binary blob, the **MetricNameRaw**, roughly `[len][name][len][value]...`. For our series, the MetricNameRaw would look something like `[0][19]http_requests_total[6]method[3]GET[6]status[3]200[4]path[10]/api/users` (each length is really a 2-byte binary prefix, but you get the idea). This blob is just a lookup key, though, not the real identity of the series; VictoriaMetrics builds that identity (from the labels in sorted order) later, only when it actually needs it.

That blob is still a fair amount of data to carry around for every single sample on disk and in every index. So here is the trick: instead of storing the whole thing, we pick a number (a 64-bit integer called the `MetricID`); under the hood, an always-growing counter seeded from the clock at startup, so it is unique within one storage instance), and with that plus a few other details we build a tiny fixed-size identifier, the **TSID**. From here, _inside storage the series is just that numberL: the TSID_.

> [!NOTE]
> **Why a TSID and not just the MetricID?**
> The MetricID alone would be enough to identify the series uniquely. But data on disk is sorted by TSID, and the TSID puts three grouping fields before the MetricID: the metric name, a job-like label (job, cluster…), and an instance-like label (instance, host…). So series for the same metric, job, and instance land next to each other on disk, which compresses better and is cheaper to scan. The MetricID just breaks the final tie.

The catch, of course, is finding the right TSID for every sample that arrives, and finding it fast.

## 5. Resolving the TSID: four increasing expensive questions

VictoriaMetrics asks a series of increasingly expensive questions, and stops at the first one that answers. Here is the whole cascade at a glance:

![](https://victoriametrics.com/blog/the-life-of-a-metric/tsid-resolution.webp)

- _was the previous row in this batch the exact same series?_ If the MetricNameRaw is byte-identical to the row right before it, VictoriaMetrics simply reuses that TSID.
- _have we seen this series recently?_ VictoriaMetrics keeps an in-memory `MetricNameRaw → TSID`s cache (the tsidCache). This is the single most important cache in the whole system, and on a warm instance our metric is almost certainly in there, so the answer usually costs a single cheap lookup.
- `do we have it written down anywhere?` This is where the sorting finally happens: the labels are put into canonical order to build the canonical **MetricName**, and VictoriaMetrics goes to disk to search on-disk inverted index for it.
- `this is a series nobody has ever seen before.` VictoriaMetrics mints a fresh MetricID for our metric and creates all the index entries for the new series.

## 6. The price of being born: the inverted index

Before anyone can query it, VictoriaMetrics has to make it findable, and that means writing it into the **inverted index**, which lives in its own store, the `indexdb`.

The easiest way to understand the index is to look at the questions it will have to answer later. Every kind of entry exists to answer exactly one of them:

| Entry                                              | Question it answers                                   |
| -------------------------------------------------- | ----------------------------------------------------- |
| MetricName → TSID                                  | I have the full labels; which series is this?         |
| MetricID → MetricName                              | I have a series number; what are its name and labels? |
| MetricID → TSID                                    | I have a series number; where does its data live?     |
| (label name, label value) → MetricIDs              | Which series have status="500"?                       |
| (metric name, label name, label value) → MetricIDs | Which series match http_requests_total{status="500"}? |

The real cost lives in the last two rows, the **posting lists**: for one specific label pair, the list of every series that carries it.

- Being findable by any label means joining all the relevant lists (`__name__="http_request_total"`, `method="GET"`, `status="200"`, `path="/api/users"`). Then three more for the composite name + label entries (`http_request_total` with `status="200"`, and so on), which exist because the most common query shape (a metric name filtered by a label) can then be answered from one single list. Seven updates for one new series.
- VictoriaMetrics also maintains **per-day indexes**: the same posting lists, but scoped to a single date.

![](https://victoriametrics.com/blog/the-life-of-a-metric/index-fanout.webp)

Fourteen writes for our newborn series; now compare that to its millionth sample later on, which costs almost nothing: it reuses a cached TSID and just appends a value. Being born is the expensive part of our metric’s life; growing up is cheap.

> [!IMPORTANT]
> That asymmetry is the whole reason **cardinality** (the number of distinct series), not raw sample volume, is what stresses a time series database.

Once the index entries exist and the TSID is cached, our metric is officially “known”. But notice that everything so far has been about identity; we have not stored a single sample yet. Now its actual value needs to go somewhere.

## 7. The write path: an LSM tree

VictoriaMetrics organizes data into **monthly partitions**, directories named `YYYY_MM`, and routes each sample to a partition by its timestamp. Within a partition, the write path follows a design known as an **LSM tree** (Log-Structured Merge Tree). The name sounds fancy, but the idea is simple: never modify existing data; always write new immutable files, and keep merging them into bigger ones in the background. It is a design tuned above all for one thing: **ingesting an enormous number of samples per second**.

- The part, VictoriaMetrics's unit of physical storage (an immutable bundle of sorted, compressed samples). Every part has exactly the same internal format; the only things that change over its life are wherer it lives (RAM or disk) and hoow big it is.
- An in-memory part is a part still living in RAM, a small part is a freshly written one on disk, a big part is the result of merging many smaller ones.
- A **rawRows shard**: a plain in-memory buffer of a few megabytes, enough for a couple hundred thousand rows. There is one shard per CPU core, so ingestion threads never fight over a lock (a big deal when you are swallowing millions of samples per second).
- When the shard fills up, or after a couple of seconds at most, everything in it gets sorted by `(TSID, timestamp)` and grouped into **blocks**: consecutive samples of the _same series_, up to 8192 of them, sitting physically next to each other.
- The blocks are then compressed into our sample's first part, one still living in RAM: an **in-memory part**. This is the moment our sample stops being a loose row and takes on the columnar, compressed shape we will dig into next. It is also the moment it becomes visible to queries.
- A background flusher writes that in-memory part to disk as a **small part**, forcing the operating system to physically write the files rather than just promise to.
- Dedicated workers continuously fold parts into bigger ones (in-memory parts into small parts, small parts into big parts, big parts into bigger ones), always keeping everything sorted by `(TSID, timestamp)`.

## 8. The shape on disk: columnar storage and compression

The heart of a part is just two files:

```text
timestamps.bin   all the timestamps, compressed
values.bin       all the values, compressed
```

Two companion files, `index.bin` and `metaindex.bin`, act as the table of contents: they record which slice of those two files belongs to which series and time range, so a query can jump straight to the right bytes. But the interesting story is in the two big files.

Notice that **timestamps and values are stored separately**. This is columnar storage, and it is the foundation everything else builds on. Instead of storing records like `(ts1, v1), (ts2, v2), ...` interleaved, you store all the timestamps together and all the values together. Why does that help? Because the numbers within a column are far more similar to each other than a timestamp is to its value, and similarity is exactly what compression feeds on.

### 8.1. Compressing timestamps

Metrics are usually sampled on a regular schedule: every 15 seconds, every 60 seconds. So a column of timestamps looks like:

```text
1700000000000, 1700000015000, 1700000030000, 1700000045000, ...
```

Each of those is a big thirteen-digit number, but look closer: every one is exactly 15000 milliseconds after the previous one. All the interesting information is in the difference between neighbors, so why store the full numbers at all? Store the **delta** between consecutive timestamps instead and the column becomes 15000, 15000, 15000, .... Take the delta of the deltas (delta-of-delta) and you get 0, 0, 0, .... A column of zeros compresses to almost nothing.

The encoder is even smart enough to recognize the common cases explicitly. If every delta is identical, a whole block of thousands of timestamps is stored as just the first timestamp and the step. That A cou’s it.

### 8.2. Compressing values

Values get a two-part treatment.

- Floating-point values are converted into integers using **decimal scaling**: a small value like 1.27 becomes a mantissa 127 with an exponent -2. Working with integers instead of raw floats makes the subsequent delta encoding far more effective.
- The integers are delta-encoded, and here the shape of the series matches:
  - A counter mostly climb steadily, so delta-of-delta turns its values into a sequence of small, similar numbers, just like the timestamps.
  - A gauge wanders up and down, so plain delta compresses it best.

After the delta encoding there is one final squeeze - zstd. At this point our metric is at rest: a few bytes inside a compressed block, inside a values.bin, inside a part, inside a monthly partition, on a disk. It is durable, it is tiny, and it is ready to be read.

## 9. Reading it back: the query

```text
rate(http_requests_total{status="500"}[5m])

--> “How many 500 errors per second, over the last 5 minutes?”
```

Before doing any heavy lifting, VictoriaMetrics checks whether it has answered this question recently. Query results are cached. The cache really decides how much raw data must be fetched: if it has nothing, the whole time range; if it has a partial answer, only the missing slice. Either way, for that missing piece the engine has to go get the raw data (walking the same path ingestion took, but backwards):

![](https://victoriametrics.com/blog/the-life-of-a-metric/query-read-path.webp)

## 10. Growing old: downsamplings

Downsampling thins the data out as it ages, riding on the same background-merge machinery we already met. You might keep 15-second data for a week, then collapse it to 1-minute resolution for a month, then 15-minute resolution for a year. Each step throws away points but keeps the shape of the curve, so old data takes a fraction of the space while remaining correct for the questions you would actually ask of it.

There is no averaging or clever math involved. During merges, for each series, VictoriaMetrics keeps the last sample of each downsampling interval and simply discards the rest.

## 11. Death: retention

Nothing lives forever, and you do not want it to; unbounded data means unbounded disk bills. VictoriaMetrics enforces a **retention period** (`-retentionPeriod`, one month by default) and removes data older than that.

This is where the monthly-partition layout pays off one last time. Because all the data for a given month lives in its own YYYY_MM directory, expiring old data is mostly a matter of _deleting whole partition directories_ once every sample inside them is past the retention period. There is no expensive row-by-row scan to find what to delete; you just drop the month. As a finer backstop, merges also skip individual blocks whose newest timestamp has already fallen past the retention deadline, so expired data is not even carried forward into new parts.
