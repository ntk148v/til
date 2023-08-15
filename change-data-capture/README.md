# Change Data Capture (CDC)

Source: <https://www.qlik.com/us/change-data-capture/cdc-change-data-capture>

## 1. Introduction

- Change data capture (CDC) refers to the process of identifying and capturing changes made to data in a database and then delivering those changes in real-time to a downstream process or system.
- Capturing every change from transactions in a source database and moving them to the target in real-time keeps the systems in sync and provides for reliable data replication and zero-downtime cloud migrations.
- Change data capture is a method of ETL (Extract, Transform, Load) where data is extracted from a source, transformed, and then loaded to a target repository such as a data lake or data warehouse.

![](https://www.qlik.com/us/-/media/images/global/etl/etl-vs-elt_etl-process-diagram.png?rev=f9f43db03f494c5d8fce01ea101f0dcf&h=971&w=1376&hash=34CC77EDF9575EF0E6B4AD767FEA1BCE)

- Benefits:
  - Eliminates the need for bulk load updating and inconvenient batch windows by enabling incremental loading or real-time streaming of data changes into your target repository.
  - Log-based CDC is a highly efficient approach for limiting impact on the source extract when loading new data.
  - Since CDC moves data in real-time, it facilitates zero-downtime database migrations and supports real-time analytics, fraud protection, and synchronizing data across geographically distributed systems.
  - CDC is a very efficient way to move data across a wide area network, so it's perfect for the cloud.
  - CDC is also well suited for moving data into a stream processing solution like Apache Kafka.
  - CDC ensures that data in multiple systems stays in sync. This is especially important if you're making time-sensitive decisions in a high-velocity data environment.

## 2. CDC Methods

The most popular method is to use a transaction log which records changes made to the database data and metadata.

### 2.1. Log-based CDC

- When a new transaction comes into a database, it gets logged into a log file with no impact on the source system.
- You can pick up those changes and then move those changes from the log.

![](https://www.qlik.com/us/-/media/images/global-us/site-content/change-data-capture/cdc-change-data-capture/02changedatacaptureinfographic2x.png)

### 2.2. Query-based CDC

- Here you query the data in the source to pick up changes. This approach is more invasive to the source systems because you need something like a timestamp in the data itself.

### 2.3. Trigger-based CDC

- You change the source application to trigger the write to a change table and then move it. This approach reduces database performance because it requires multiple writes each time a row is updated, inserted, or deleted.
