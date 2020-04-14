# Prometheus WAL

WAL = Write-ahead-log

Source: https://www.robustperception.io/how-much-space-does-the-wal-take-up

All samples that are ingested by Prometheus are written to the WAL, so that on restart in-memory state which hasn't made it to a block yet can be reconstructed.

WAL files are stored in the `wal` directory in 128MB segments. These files contain raw data that has not been compacted yet, so they are significantly larger than regular block files. Prometheus will keep a minimum of 3 WAL files, however high-traffic servers may see more than three WAL files since it needs to keep at least two hours worth of raw data.

WAL format is composed of varous types of record.

- Each sample record represents one scrape or one recording rule output.
  - Each sample size (ignore the 23 bytes of overhead for simplicity)

    ```
    13 bytes (sample) = 1 byte (timestamp) + 8 bytes (value) + 4 bytes (churn)
    ```

- The series record are all the new time series from one scrape or recording rule.

    ```
    9 bytes (overhread) + size of all labels (a label <= 127 bytes)
    ```

- Tombstone records: ignore.

Concrette example numbers:

- Prometheus: ingests 100k samples/s & churns 1M series/2 hours with 100 bytes for series labels.
- `100000 * 13 = 1.3MB per second` for samples.
- `1000000  / 3600 / 2 * 100 = 13.8kB per second` for series.

Checkpoints which summarise older WAL entries down to just the series creations that may still be relevant.

> I am not really understand  this paragraph.

```
The checkpointing logic runs every two hours after head compaction, and will checkpoint the oldest third of segments. So summing the geometric series with a constant of 2 hours and a ratio of 2/3, we get about 4 hours worth of segments that will be kept around. Add then the 2 hours of WAL that'll build up until the next checkpoint, for 6 hours in total.
```

The size of checkpoint: 100k samples/s -> 1M old series -> 100 bytes each in the checkpoint -> 100MB checkpoint.

**Overall**: For the 100k samples/s Prometheus that's around 26GB of data, or around 10% of the size the blocks take for the default 2 week retention period.

**NOTE**: Prometheus >=2.11, WAL compression: `--storage.tsdb.wal-compression` flag. This should roughly half the size of the WAL, at the cost of some additional CPU.
