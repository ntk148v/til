# Prometheus Long term storage solutions

## Problem

Prometheus's local storage isn't intended as a long term data store, rather as
more of an ephemeral cache.

If your local storage becomes corrupted for whatever reason, your best bet is
to shutdown Prometheus & remove the entire storage directory. However, you can
also try removing individual block directories to resolve the problem. This
means losing a time window of around two hours worth of data per block
directory. Prometheus's local storage is not meant as durable long-term
storage. It is limited in its scalability & durability.

So the problem is how to solve the durable trouble?

## Option 1: Still use local storage

- We use local storage, increase retention time (When to remove old data.
  Defaults to `15d`) with option `--storage.tsdb.retention` if you want.
- Write some scripts to backup data to object storage (like AWS S3 or OpenStack
  Swift). Rsync, rclone... are possible options. [Thanos](https://github.com/improbable-eng/thanos)
  as its description - **Highly available Prometheus setup with long term
  storage capabilities.** looks interesting. It does backup task that a bit
  more automatically.
- That strategy stills has drawback: when to backup data? If local storage is
  corrupted right before the backup, how is it going?

## Option 2: Remote storage

### Option 2.1: InfluxDB

### Option 2.2: PostgreSQL/TimescaleDB

### Option 2.3: Cortex
