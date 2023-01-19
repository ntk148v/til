# PostgreSQL vs. MySQL

Source:

- <https://phoenixnap.com/kb/postgres-vs-mysql>
- <https://www.turing.com/blog/postgresql-vs-mysql-comparison/>
- <https://www.ibm.com/cloud/blog/postgresql-vs-mysql-whats-the-difference>
- <https://www.guru99.com/postgresql-vs-mysql-difference.html>

There are many available RDBMS on the market, MySQL and PostgreSQL are the two most prominent solutions. This article focuses on the main distinctions and provides a detailed comparison of MySQL and PostgreSQL.

| Categories                              | MySQL                                                                                         | PostgreSQL                                                                        |
| --------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Open source                             | Both open-source (GNU License) and paid commerical                                            | Fully open-source and free of charge ()                                           |
|                                         | RDMS                                                                                          | Object-relational database management system (ORDBMS)                             |
| ACID compliance                         | ACID compliant only when it is used with InnoDB and NDB Cluster Storage engines               | Complete ACID compliant                                                           |
| SQL compliant                           | partially SQL compliant                                                                       | largely SQL compliant                                                             |
| Performance                             | Mostly used for web-based projects that need a database for straightforward data transactions | Highly used in large systems where to read and write speeds are important         |
| Best suited                             | Perform well in OLAP & OLTP systems when only read speeds are needed                          | Perform well when executing complex queries                                       |
| Materialized view                       | Support temporary tables but does not offer materialized views                                | Support materialized views and temporary tables                                   |
| B-Tree indexes                          | Two or more B-tree indexes can be used when it is appropriate                                 | B-tree indexes merged at runtime to evaluate are dynamically converted predicates |
|                                         |
| Multiversion concurrency control (MVCC) | Support (InnoDB only)                                                                         | Support                                                                           |
