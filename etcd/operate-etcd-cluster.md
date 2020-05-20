# Operate Etcd cluster

https://ntk148v.github.io/blog/posts/operate-etcd-cluster/

> **NOTE**: This is my perspective aggregation. You can easily find these such of knowledges in [the references](#5-references).

## 1. Context

Etcd Version `v3.4.0`.

## 2. Requirements

### 2.1. Number of nodes

* \>= 3 nodes. A etcd cluster needs a majority of nodes, a quorum to agree on updates to the cluster state. For a cluster with **n-members**, quorum is **(n/2)+1**.

### 2.2. CPUs

* Etcd doesn't require a lot of CPU capacity.
* Typical clusters need **2-4 cores** to run smoothly.

### 2.3. Memory

* Etcd performance depends on having enough memory (cache key-value data, tracking watchers...).
* Typical **8GB** is enough.

### 2.4. Disk

* An etcd cluster is very sensitive to disk latencies. Since etcd must persist proposals to its log, disk activity from other processes may cause long `fsync` latencies. The upshot is etcd may miss heartbeats, causing request timeouts and temporary leader loss. An etcd server can sometimes stably run alongside these processes when given a high disk priority.
* Check whether a disk is fast enough for etcd using [fio](https://github.com/axboe/fio). If the 99th percentile of fdatasync is **<10ms**, your storage is ok.

```bash
$ fio --rw=write --ioengine=sync --fdatasync=1 --directory=test-data \
    --size=22m --bs=2300 --name=mytest
```
* **SSD** is recommended.

### 2.5. Network

* Etcd cluster should be deployed in a fast and reliable network. Low latency ensures etcd members can communicate fast. High bandwidth can reduce the time to recover a failed etcd member.
* **1GbE** is sufficient for common etcd.
* Note that the network isn't the only source of latency. Each request and response may be impacted by slow disks on both the leader and followers.

## 3. Tuning

### 3.1. Time parameters

* `Heartbeat interval`.
  * The frequency with which the leader will notify followers that it is still the leader.
  * Default: **100ms**.
  * Best practice: **Around 0.5-1.5 x round-trip time (RTT) between members**. Measure RTT with `ping`.
  * Tradeoff: Too low -> etcd will send unnecessary messages -> increase the usage of CPU and network resources. Too high -> leads to high election timeout.
* `Election timeout`.
  * How long a follower node will go without hearing a heartbeat before attempting to become leader itself.
  * Default: **1000ms**.
  * Best practice: **>= 10 x RTT and < 50s**.
* The heartbeat interval and election timeout value should be **the same for all members in one cluster**.
  
```bash
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

### 3.2. Disk

* An etcd server can sometimes stably run alongside these processes when given a high disk priority using [ionice](https://linux.die.net/man/1/ionice).

```bash
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

### 3.3. Snapshot

* etcd appends all key changes to a log file -> huge log that grows forever :point_up:
* Solution: Make periodic snapshots (save the current and remove old logs).
* Default: make snapshots after every **10 000 changes**.
* Tuning: Just in case that etcd's memory and disk usage is too high, lower threshold.
  
```bash
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## 4. Maintenance

### 4.1. History compaction

* Etcd keeps an exact history of its keyspace, the history should be periodically compacted to avoid performance degradation and eventual storage space exhaustion.
* Etcd can be set to automatically compact the keyspace with the `--auto-compaction-*` option with a period of hours.

```bash
# keep one hour of history
$ etcd --auto-compaction-retention=1 --auto-compaction-mode=periodic
```

* Compaction modes:
  * Revision-based: `--auto-compaction-mode=revision --auto-compaction-retention=1000` automatically Compact on "latest revision" - 1000 every 5-minute (when latest revision is 30000, compact on revision 29000). Use this when having a large keyspace.
  * Periodic: `--auto-compaction-mode=periodic --auto-compaction-retention=72h` automatically Compact with 72-hour retention window every 1-hour. Use this when having a huge number of revisions for a key-value pair.

### 4.2. Defragmentation

* Compacting old revisions internally fragments etcd by leaving gaps in backend database - `internal fragmentation`.
* Internal fragmentation space is available for use by etcd but unavailable to the host filesystem.
* Solution: Release this space back to the filesystem with defrag.

```bash
$ etcdctl defrag
```

* It should be run rather infrequently, as there is always going to be an unavoidable pause.

## 5. References

* Etcd hardware: https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/hardware.md
* Etcd tuning: https://github.com/etcd-io/etcd/blob/master/Documentation/tuning.md
* Etcd maintainence: https://etcd.io/docs/v3.4.0/op-guide/maintenance/
