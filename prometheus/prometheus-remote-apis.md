# Prometheus Remote APIs

- [Prometheus Remote APIs](#prometheus-remote-apis)
  - [1. Overview](#1-overview)
  - [2. Remote Write](#2-remote-write)
    - [2.1. WAL-based remote write](#21-wal-based-remote-write)
    - [2.2. Tunning](#22-tunning)
  - [3. Remote read](#3-remote-read)
    - [3.1. The non-streamed version](#31-the-non-streamed-version)
    - [3.2. The chunked, streamed version](#32-the-chunked-streamed-version)
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

## 3. Remote read

### 3.1. The non-streamed version

### 3.2. The chunked, streamed version

## 4. Source

- https://prometheus.io/docs/practices/remote_write/
- https://prometheus.io/blog/2019/10/10/remote-read-meets-streaming/
