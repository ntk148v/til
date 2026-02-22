# PromQL Gotchas

## Instant vector & Range Vector

- **Instant vector**: One value per time series guaranteed.
- **Range vector**: Any number of values between two timestamps.

## Operators

- Aggregation Operators

```
instant vector -> instant vector
```

- Binary operators

```
instant vector <operator> instant vector = instant vector
```

## Functions

```
instant vector -> instant vector
range vector -> instant vector
```

### Gotchas

- Tell your aggregation operators about the label you care about.
- Never compare raw counters - use rate().
- Be careful with label sets when using binary operators.

<https://promcon.io/2019-munich/slides/promql-for-mere-mortals.pdf>

## Filtering by regexps on metric name

- Sometimes it is required returning all the time series for multiple metric names.
- Metric name is just an ordinary label with a special name - `__name__`.
- For instance, the following query returns all the time series with `node_network_receive_bytes_total` or `node_network_transmit_bytes_total`:

```
{__name__=~"node_network_(receive|transmit)_bytes_total"}
```

## Comparing current data with historical data

- PromQL allows querying historical data and combining / comparing it to the current data with `offset`.

```
node_network_receive_bytes_total offset 7d
go_memstats_gc_cpu_fraction > 1.5 * (go_memstats_gc_cpu_fraction offset 1h)
```

## Rate vs irate vs increase vs idelta

Source:

- <https://blog.devops.dev/prometheus-theory-rate-vs-irate-20e6243a3ab8#:~:text=The%20rate()%20function%20would,points%20given%20a%20time%20range.>
- <https://www.metricfire.com/blog/understanding-the-prometheus-rate-function/>

- **rate()**:
  - Use [first and last data points in the group, divide by query interval](https://github.com/prometheus/prometheus/blob/8849b7dcadc2960c70467734efce35d737be25f5/promql/functions.go#L71).
  - Best used for **slow moving counters and alerting rules**.

![](./imgs/rate.png)

```
(Vlast - Vfirst)/(Tlast - Tfirst)
```

- **irate()**:
  - Use [last 2 data points in the range, divide by scrape interval](https://github.com/prometheus/prometheus/blob/8849b7dcadc2960c70467734efce35d737be25f5/promql/functions.go#L272).
  - Give better representation of instant rate.
  - Used for graphing **volatile, fast-moving counters**.

![](./imgs/irate.png)

```
(Vlast - Vlast-1)/(Tlast - Tlast-1)
```

- For instance, if you have a _scrape interval = 15s_, a data point is pulled every 15 seconds. You're querying with a _1m_ interval (the '[1m]' suffix on your query), you will have 4 data points per interval. The `rate()` function would average using the **first and last** data points, averaged over the query interval (**1m**); whereas the `irate()` function would average using the `last two` data points, averaged over the scrape interval (**15s**).
- Notes:
  - Make sure there's at least 4 data points given a time range.
  - When combining rate with an aggregation operator, always take `rate()` first so `rate()` function can detect counter resets:

  ```promql
  sum without(code_handler) (rate(http_requests_total[5m]))
  ```

- Increase.

```
(Vcurr - Vprev)
```

- Idelta

```
(Vcurr-1 - Vcurr-2)
```

<https://github.com/prometheus/prometheus/blob/master/promql/functions.go#L135>

## Combining multiple series

- Combining multiple time series with arithmetic operations requires understanding [matching rules](https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching).
- The matching rules may be augmented with ignoring, on, group_left and group_right modifiers.

## Comparson with bool

```
rate(node_network_receive_bytes_total[5m]) < bool 2300
```

- 1 - true, 0 - false

## Returning multiple results from a single query

- Using `or` operator.

```
metric1 or metric2 or metric3
```

- There is a common trap when combining expression results: results with duplicate set of labels are skipped.

```
sum(a) or sum(b)
// sum(a) and sum(b) have identical label set --> skip sum(b)
```
