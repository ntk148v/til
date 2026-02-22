# What is time-series data?

Source:

- <https://blog.timescale.com/what-the-heck-is-time-series-data-and-why-do-i-need-a-time-series-database-dcf3b1b18563/>)
- <https://www.alibabacloud.com/blog/key-concepts-and-features-of-time-series-databases_594734>

Time-series data is starting to play a larger role in our world.

- [What is time-series data?](#what-is-time-series-data)
  - [1. What is time-series data?](#1-what-is-time-series-data)
  - [2. Why do I need a time-series databbase?](#2-why-do-i-need-a-time-series-databbase)
  - [3. Time series data models](#3-time-series-data-models)
  - [4. Processing of Time series data](#4-processing-of-time-series-data)
    - [4.1. Filter](#41-filter)
    - [4.2. Aggregation](#42-aggregation)
    - [4.3. Downsampling, Rollup and Auto-Rollup](#43-downsampling-rollup-and-auto-rollup)

## 1. What is time-series data?

![basic-illustration](https://blog.timescale.com/content/images/2018/12/gif8.gif)

Time series data is used to describe the state change information of an object in the historical time dimension.

There are many other kinds of time-series data. To name a few: DevOps monitoring data, mobile/web application event streams, industrial machine data, scientific measurements.

These datasets primarily have 3 things in common:

1. The data that arrives is almost always recorded as a new entry.
2. The data typically arrives in time order.
3. Time is a primary axis (time-intervals can be either regular or irregular).

Simply put: time-series datasets track changes to the overall system as INSERTs, not UPDATEs.

It allows us to measure change: analyze how something changed in the past, monitor how something is changing in the present, predict how it may change in the future.

Of course, storing data at this resolution comes with an obvious problem: you end up with a lot of data, rather fast. Time-series data piles up very quickly.

Having a lot of data creates problems when both recording it and querying it in a performant way, which is why people are now turning to time-series database.

## 2. Why do I need a time-series databbase?

1. **Scale**: Time-series data accumulates very quickly. Normal databases are not designed to handle that scale.

2. **Usability**: TSDBs also typically include functions and operations common to time-series data analysis such as data retention policies, continuous queries, flexible time aggregations, etc

## 3. Time series data models

- A data model of time series data mainly consists of the following parts:
  - Subject: The subject to be measured.
  - Measurements: A subject may have one or more measurements, each corresponding to a specific metric.
  - Timestamp: The measurement report is always attached with a timestamp attributeto indicate the time.

- Modeling by Data source:

![](https://yqintl.alicdn.com/db4bdf7212932ecf87a82d26b6a18c5a07f9c7ae.png)

- Modeling by metrics:

![](https://yqintl.alicdn.com/96206056bbc41827577a9a434d5cb7c0577db962.png)

## 4. Processing of Time series data

In addition to the basic data writing and storage, query and analysis are the most important features of a TSDB. The processing of time series data mainly includes filter, aggregation, groupby and downsampling.

### 4.1. Filter

![](https://yqintl.alicdn.com/ebaa5c55bd4db820e544d3b1da1ad81308fd77d5.png)

Query for all data that meets the given conditions of different dimesions.

### 4.2. Aggregation

![](https://yqintl.alicdn.com/d398477b6336253484e7f490d4a11299b267f2fb.png)

GroupBy is the processing of converting low-dimensional time series data into high-dimensional statistics. After the original data is queried, we obtain the result through real-time computation. Mainstream TSDBs optimize this process through pre-aggregation.

### 4.3. Downsampling, Rollup and Auto-Rollup

Downsampling is the process of converting high-resolution time series data into low-resolution time series data. This process is called rollup. Downsampling is to aggregate data of the same dimension at different time levels.

Downsampling is divided into:

- Storage downsampling: to reduce storage costs of data, especially historical data.
- Query downsampling: for queries with a larger time range to reduce the returned data points.
