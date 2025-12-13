# Log structured merge (LSM) tree

Source:

- <https://www.geeksforgeeks.org/dsa/introduction-to-log-structured-merge-lsm-tree/>
- <https://www.youtube.com/watch?v=I6jB0nM9SKU>
- <https://system.farmerboy95.com/ByteByteGo/lsm-tree/>
- <https://docs.yugabyte.com/stable/architecture/docdb/lsm-sst/>

LSM Trees are the data structure underlying many highly scalable NoSQL distributed key-value type databases such as Amazon's DynamoDB, Cassandra, and ScyllaDB.

A simple version of LSM Trees comprises 2 levels of tree-like data structure:

- Memtable and resides completely in memory (let's say T0)
- SStables stored in disk (Let's say T1)
- Typically in LSMs there is a third component - WAL (Write ahead log)

![](<https://media.geeksforgeeks.org/wp-content/uploads/20230618122313/Android-UML---Algorithm-flowchart-example-(1).png>)

## 1. Comparison to B-tree

Most traditional databases (for example, MySQL, PostgreSQL, Oracle) have a [B-tree](https://en.wikipedia.org/wiki/B-tree)-based storage system

- Write operations (insert, update, delete) are more expensive in a B-tree, requiring random writes and in-place node splitting and rebalancing. In LSM-based storage, data is added to the memtable and written onto a SST file as a batch.
- The append-only nature of LSM makes it more efficient for concurrent write operations.

## 2. Memtable

All new write operations (inserts, updates, and deletes) are written as key-value pairs to an in-memory data structure called a memtable, which is essentially a sorted map or tree. The key-value pairs are stored in sorted order based on the keys. When the memtable reaches a certain size, it is made immutable, which means no new writes can be accepted into that memtable.

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure3.png)

## 3. Flush to SST

The immutable memtable is then flushed to disk as an SST (Sorted String Table) file. This process involves writing the key-value pairs from the memtable to disk in a sorted order, creating an SST file

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure4.png)

## 4. SST (Sorted String Table)

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure5.png)

- Each SST file is an immutable, sorted file containing key-value pairs
- The data is organized into data blocks, which are compressed using configurable compression algorithms (for example, Snappy, Zlib).
- Index blocks provide a mapping between key ranges and the corresponding data blocks, enabling efficient lookup of key-value pairs.
- Filter blocks containing **bloom filters** allow for quickly determining if a key might exist in an SST file or not, skipping entire files during lookups.
  - A [bloom filter](https://systemdesign.one/bloom-filters-explained/) is a space-efficient data structure that helps quickly determine whether a key might exist in that file or not, avoiding unnecessary disk reads.
    - The bloom filter data structure is a bit array of length n. The position of the buckets is indicated by the index (0–9) for a bit array of length ten. All the bits in the bloom filter are set to zero when the bloom filter is initialized (an empty bloom filter). The bloom filter discards the value of the items but stores only a set of bits identified by the execution of hash functions on the item.

    ![empty bloom filter](https://systemdesign.one/bloom-filters-explained/empty-bloom-filter.webp)
    - The following operations are executed to add an item to the bloom filter:
      - the item is hashed through k hash functions
      - the modulo n (length of bit array) operation is executed on the output of the hash functions to identify the k array positions (buckets)
      - the bits at all identified buckets are set to one

      ![adding an item](https://systemdesign.one/bloom-filters-explained/add-item-bloom-filter.webp)
      - The items red and blue are added to the bloom filter. The buckets that should be set to one for the item red are identified by the execution of the modulo operator on the computed hash value.

      ```text
      h1(red) mod 10 = 1
      h2(red) mod 10 = 3
      h3(red) mod 10 = 5
      ```

    - The following operations are executed to check if an item is a member of the bloom filter:
      - the item is hashed through the same k-hash functions
      - the modulo n (length of bit array) operation is executed on the output of the hash functions to identify the k array positions (buckets)
      - verify if all the bits at identified buckets are set to one

    ![check membership](https://systemdesign.one/bloom-filters-explained/item-membership-bloom-filter.webp)
    - If any of the identified bits are set to zero, the item is not a member of the bloom filter. If all the bits are set to one, the item **might** be a member of the bloom filter. The uncertainty about the membership of an item is due to the possibility of some bits being set to one by different items or due to hash function collisions.

    ```text
    h1(blue) mod 10 = 4
    h2(blue) mod 10 = 5
    h3(blue) mod 10 = 9
    ```

    - The item blue might be a member of the bloom filter as all the bits are set to one.

- The footer section of an SST file contains metadata about the file, such as the number of entries, compression algorithms used, and pointers to the index and filter blocks.

## 5. Write path

- When new data is written to the LSM system, it is first inserted into the active memtable.
- As the memtable fills up, it is made immutable and written to disk as an SST files.
- Each SST file is sorted by key and contains a series of key-value pairs organized into data blocks, along with index and filter blocks for efficient lookups.

## 6. Read path

- To read a key, the LSM tree first checks the memtable for the most recent value.
- If not found, it checks the SST files and finds the key or determines that it doesn't exist. During this process, LSM uses the index and filter blocks in the SST files to efficiently locate the relevant data blocks containing the key-value pairs.

## 7. Delete path

Rather than immediately removing the key from SSTs, the delete operation marks a key as deleted using a tombstone marker, indicating that the key should be ignored in future reads. The actual deletion happens during compaction, when tombstones are removed along with the data they mark as deleted.

## 8. Compaction

- As data accumulates in SSTs, a process called compaction merges and sorts the SST files with overlapping key ranges producing a new set of SST files.
- The merge process during compaction helps to organize and sort the data, maintaining a consistent on-disk format and reclaiming space from obsolete data versions.
- There are two types of compaction: Size Tiered Compaction and Level Based Compaction.

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure9.png)

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure10.png)

![](https://system.farmerboy95.com/assets/ByteByteGo/lsm-tree/figure11.png)
