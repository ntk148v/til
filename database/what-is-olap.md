# What is OLAP?

Source:

- <https://en.wikipedia.org/wiki/Online_analytical_processing>
- <https://clickhouse.com/docs/concepts/olap>

OLAP stands for Online Analytical Processing:

- **Processing**: Some source data is processed ...
- **Analytical**: ... to produce some analytical reports and insights.
- **Online**: ... in real-time.

All database management systems could be classified into two groups:

- OLAP (Online Analytical Processing): focuses on building reports, each based on large volumes of historical data, but by doing its less frequently.
- OLTP (Online Transactional Processing): usually handles a continuous stream of transactions, constantly modifying the current state of data.

In practice OLAP and OLTP aren't viewed as binary categories, but more like a spectrum. Most real systems usually focus on one of them but provide some solutions or workarounds if the opposite kind of workload is also desired. This situation often forces businesses to operate multiple storage systems that are integrated. This might not be such a big deal, but having more systems increases maintenance costs, and as such the trend in recent years is towards [HTAP (Hybrid Transactional/Analytical Processing)](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) when both kinds of workload are handled equally well by a single database management system.

Even if a DBMS started out as a pure OLAP or pure OLTP, it is forced to move in the HTAP direction to keep up with the competition. ClickHouse is no exception. Initially, it has been designed as a fast-as-possible OLAP system and it still doesn't have full-fledged transaction support, but some features like consistent read/writes and mutations for updating/deleting data have been added.

The fundamental trade-off between OLAP and OLTP systems remains:

- To build analytical reports efficiently it's crucial to be able to read columns separately, thus most OLAP databases are columnar;
- While storing columns separately increases costs of operations on rows, like append or in-place modification, proportionally to the number of columns (which can be huge if the systems try to collect all details of an event just in case). Thus, most OLTP systems store data arranged by rows.
