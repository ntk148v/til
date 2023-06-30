# Why Kafka is so fast?

Source:

- <https://www.linkedin.com/pulse/why-kafka-so-fast-aman-gupta/>
- <https://blog.bytebytego.com/p/why-is-kafka-fast>
- <https://www.geeksforgeeks.org/why-apache-kafka-is-so-fast/>

Table of contents:

- [Why Kafka is so fast?](#why-kafka-is-so-fast)
  - [1. Sequential I/O](#1-sequential-io)
  - [2. Zero-copy principle](#2-zero-copy-principle)
  - [3. Optimal Data Structure](#3-optimal-data-structure)
  - [4. Horizontal Scaling](#4-horizontal-scaling)
  - [5. Compression \& Batching of Data](#5-compression--batching-of-data)

## 1. Sequential I/O

- When data is stored on a storage device, it is organized into blocks, and each block has a unique address. When a computer reads or writes data, it uses the block addresses to locate the data.
- Random I/O refers to the process of reading or writing data from non-contiguous addresses, which can cause the disk head to jump around to different locations, resulting in slower read and write speeds.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Random_vs_sequential_access.svg/1024px-Random_vs_sequential_access.svg.png)

- Sequential I/O refers to reading or writing data from contiguous blocks of memory -> the disk head can move in a straight line -> faster than random I/O.
- Kafka **uses sequential I/O** to improve the performance of its **log-based storage system**.
  - Kafka stores all the data it ingests in a log-structured format, which means that new data is appended to the end of the log.
  - Kafka also uses a technique called log compaction to clean up old data, which is also done in a sequential manner.

## 2. Zero-copy principle

- Zero-copy principle is a technique used in computer systems to minimize the number of time data is copied between different memory locations -> reduce the amoun of memory and CPU resources used.
- There are different ways to implement the zero-copy principles:
  - Memory mapping: this technique allows a process to access a file or other data source as if it were in its own memory space. This means that the process can read and write data to the file without the need to copy it to a separate buffer.
  - Direct memory access (DMA): this technique allows a device, such as a network card or disk controller, to transfer data directly to or from memory, without the need for the CPU to be involved in the transfer.
  - User-space libraries: Some user-space libraries like zero-copy libraries can help to implement zero-copy principles and eliminate the unnecessary data copies.
- Kafka uses the zero-copy principle to improve its performance by minimising the number of copies of data that are made as messages are produced and consumed.
  - This is achived using DMA.

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fff3743a9-915c-44c8-9bc3-562a754035f8_2469x2973.jpeg)

## 3. Optimal Data Structure

- Kafka uses a queue instead of tree since all the data is appended at the end and the reads are very simple by the use of pointers.

## 4. Horizontal Scaling

- Kafka has the ability to have multiple partitions for a single topic that can be spread across thousands of machines. This enables it to maintain the high-throughput and provide low latency.

## 5. Compression & Batching of Data

- Kafka batches the data into chunks which helps in reducing the network calls and converting most of the random writes to sequential ones.
- Kafka compresses a batch of messages and sends them to the server where they’re written in the compressed form itself. They are decompressed when consumed by the subscriber. GZIP & Snappy compression protocols are supported by Kafka.
