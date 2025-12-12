# (Dumb) Question and Answer

## 1. The 2-Hour problem

Prometheus stores incoming data in a mutable in-memory structure called the Head Block. It keeps data here for 2 hours before compressing it and writing it to a permanent "Block" on the disk.

- Without a WAL: If Prometheus crashed, you would lose up to 2 hours of data (everything currently in RAM).
- With a WAL: Every single data point is written to the WAL on disk instantly as it arrives. If Prometheus crashes, it reads the WAL to restore those 2 hours of data into RAM.

## 2. Why doesn't Prometheus just flush to disk often (like VictoriaMetrics)?

The answer lies in **Indexing and Compression**.

- Prometheus Approach: It builds a heavy, highly optimized **Inverted Index** in RAM. This allows for extremely fast querying of massive datasets. However, this index is complex to construct. Writing this complex index to disk is an expensive operation. If Prometheus tried to write this to disk every second (or even every minute), the Disk I/O would be overwhelmed, and the server would stall.
- VictoriaMetrics Approach: It uses an architecture similar to an **LSM Tree (Log-Structured Merge-tree)**. It writes data in small, simple "parts" that are easy to flush to disk quickly. It merges them later in the background. This makes writing fast and frequent flushes possible, eliminating the need for a WAL, but it requires a different approach to indexing (which VM handles via distinct index structures like mergeset).

## 3. Why doesn't Prometheus use the WAL for everything?

The WAL is a simple sequential log (like a text file of "Event A, Event B, Event C").

- Terrible for Reading: To find "CPU usage for Server X at 2:00 PM," you would have to scan the entire WAL file from start to finish. This is incredibly slow.
- Terrible for Space: The WAL is uncompressed (or lightly compressed).
- The Solution: Every 2 hours, Prometheus takes that data, organizes it into columns (for speed), compresses it heavily (XOR/Gorilla compression), and saves it as a Block. This makes queries fast and disk usage low.
