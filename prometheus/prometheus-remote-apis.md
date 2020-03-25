# Prometheus Remote APIs

- [Prometheus Remote APIs](#prometheus-remote-apis)
  - [1. Overview](#1-overview)
  - [2. Remote Write](#2-remote-write)
    - [2.1. WAL-based remote write](#21-wal-based-remote-write)
    - [2.2. Tunning](#22-tunning)
    - [2.3. Use cases](#23-use-cases)
  - [3. Remote read](#3-remote-read)
    - [3.1. The non-streamed version](#31-the-non-streamed-version)
    - [3.2. The chunked, streamed version](#32-the-chunked-streamed-version)
    - [3.3. Use cases](#33-use-cases)
  - [4. Source](#4-source)

## 1. Overview

Since version 1.x, Prometheus has the abilitiy to interact directly with its storage using the [remote APIs](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations).

This API allows 3rd party systems to interact with metrics data through two methods:

- **Write**: receive samples pushed by Prometheus.
- **Read**: pull samples from Prometheus.

Both methods are using HTTP with message encoded with [protobuf](https://github.com/protocolbuffers/protobuf). The request and response for both methods are compressed using [snappy](https://github.com/google/snappy).

## 2. Remote Write

### 2.1. WAL-based remote write

### 2.2. Tunning

### 2.3. Use cases

## 3. Remote read

The key idea of the remote read is to **allow querying Prometheus storage TSDB directly without PromQL evaluation**. It is similar to the Querier interface that the PromQL engine uses to retrieve data from storage.

### 3.1. The non-streamed version

Problems:

- No streaming capabilities within single HTTP request for the protobuf format.
- The response was including raw samples (`float64` value and `int64` timestamp) instead of an encoded, compressed batch of samples - chunks that are used to store metrics inside TSDB.

### 3.2. The chunked, streamed version

### 3.3. Use cases

## 4. Source

- https://prometheus.io/docs/practices/remote_write/
- https://prometheus.io/blog/2019/10/10/remote-read-meets-streaming/
