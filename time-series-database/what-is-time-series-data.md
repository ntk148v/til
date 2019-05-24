# What is time-series data?

[Source](https://blog.timescale.com/what-the-heck-is-time-series-data-and-why-do-i-need-a-time-series-database-dcf3b1b18563/)

Time-series data is starting to play a larger role in our world.

## What is time-series data?

![basic-illustration](https://blog.timescale.com/content/images/2018/12/gif8.gif)


There are many other kinds of time-series data. To name a few: DevOps monitoring data, mobile/web application event streams, industrial machine data, scientific measurements.

These datasets primarily have 3 things in common:
1. The data that arrives is almost always recorded as a new entry.
2. The data typically arrives in time order.
3. Time is a primary axis (time-intervals can be either regular or irregular).

Simply put: time-series datasets track changes to the overall system as INSERTs, not UPDATEs.

It allows us to measure change: analyze how something changed in the past, monitor how something is changing in the present, predict how it may change in the future.

Of course, storing data at this resolution comes with an obvious problem: you end up with a lot of data, rather fast. Time-series data piles up very quickly.

Having a lot of data creates problems when both recording it and querying it in a performant way, which is why people are now turning to time-series database.

## Why do I need a time-series databbase?

1. **Scale**: Time-series data accumulates very quickly. Normal databases are not designed to handle that scale.

2. **Usability**: TSDBs also typically include functions and operations common to time-series data analysis such as data retention policies, continuous queries, flexible time aggregations, etc
