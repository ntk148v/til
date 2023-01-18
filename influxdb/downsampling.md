# Downsample and retain data

```
more data points -> storage concerns -> downsample data
```

## 1. Definition

- [Continuous query (CQ)](https://docs.influxdata.com/influxdb/v1.8/query_language/continuous_queries/) is an InfluxQL query that runs automatically and periodically within a database. CQs require a function in the SELECT clause and must include a GROUP BY time() clause.

- [Retention policy (RP)](https://docs.influxdata.com/influxdb/v1.8/query_language/manage-database/#retention-policy-management) is the part of InfluxDB data structure that describes for how long InfluxDB keeps data.

## 2. ???
