# The Plan for InfluxDB 3.0 Open Source

Source: <https://www.influxdata.com/blog/the-plan-for-influxdb-3-0-open-source/>

- **InfluxDB 3.0 open source will be called `InfluxDB Edge`**.
- **After InfluxDB Edge is released, we will create a free community edition named InfluxDB Communit**y with additional features not in Edge (this development effort will not be in the InfluxDB repo).
- **InfluxDB Community will be upgradeable to a commercial version of InfluxDB** with features not available in either Edge or Community.

![](https://images.ctfassets.net/o7xu9whrs0u9/2DWxhgploHpf8vt9qcenGZ/586d31e90a0733b3d9884b11c4ff9634/Offering-Graphic-02.png)

- **The InfluxDB IOx repo has been copied over to the InfluxDB repo** [under this commit](https://github.com/influxdata/influxdb/commit/aa458ed1661a9e0ea58e5f999d383c08f8309c36). The IOx repo will be made private in a week.
- **Flux is in maintenance mode**. We will continue to support and run it for our customers with security and critical fixes, but our current focus is on our core SQL and InfluxQL query engine.
