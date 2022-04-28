# NewSQL

Source:

- <https://en.wikipedia.org/wiki/NewSQL>
- <https://phoenixnap.com/kb/newsql>

- NewSQL is a class of relational database management systems that seek to provide the scalability of NoSQL systems for online transaction processing ([OLTP](https://phoenixnap.com/kb/oltp-database)) workloads while maintaining the [ACID](https://phoenixnap.com/kb/acid-vs-base) guarantees of a traditional database system.
- NewSQL bridges the gap between SQL and NoSQL. NewSQL databases aim to scale and stay consistent.
- Main features:
  - In-memory storage and data processing
  - Partitioning
  - ACID properties
  - Secondary indexing
  - High availability
  - A built-in crash recovery mechanism
- Difference between SQL, NoSQL, and NewSQL

|                   | SQL                    | NoSQL                   | NewSQL                      |
| ----------------- | ---------------------- | ----------------------- | --------------------------- |
| Schema            | Relational (table)     | Schema-free             | Both                        |
| SQL               | Yes                    | Depends on the system   | Yes, with enhanced features |
| ACID              | Yes                    | No (BASE)               | Yes                         |
| OLTP              | Partial support        | Not supported           | Full support                |
| Scaling           | Vertical               | Horizontal              | Horizontal                  |
| Distributed       | No                     | Yes                     | Yes                         |
| High availability | Custom                 | Auto                    | Built-in                    |
| Queries           | Low complexity queries | High complexity queries | Both                        |
