# TIme Series Benchmark Suite (TSBS)

[A new framework released by TimescaleDB engineers](https://github.com/timescale/tsbs) to generate time-series database datasets and compare read/write performance of various database.

Using TSBS for benchmarking involves 3 phases:

1. **Data & query a priori generation**: allows you to generate data and queries you want to benchmark first, and then you can re-use it as input to the benchmarking phases. Benchmarking results are not affected by generating data or queries on-the-fly.
2. **Data loading**: measures insert/write performance by taking the data generated in the previous step and using it as input to a database-specific command line program.
3. **Query execution**: measures query execution performancein TSBS by first loading the data using the previous section and generating the queries as described earlier. This gives you an output with the description of the query and multiple groupings of measurements.
