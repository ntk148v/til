# Join in PromQL

Sources:
- https://www.robustperception.io/left-joins-in-promql
- https://www.robustperception.io/using-group_left-to-calculate-label-proportions

PromQL doesn't have a feature called "joins", however does have "vector matching" which is a similar idea.

## Example

- Many-to-one matching

```
a * on (foo, bar) group_left(baz) b
|
|
|
v
SELECT a.value * b.value, a.*, b.baz
FROM a JOIN b ON (a.foo = b.foo AND a.bar == b.bar)
```

- A left join, but won't catch where the right hand side doesn't have a value to go with the left.

```
a * on (foo, bar) group_left(baz) b 
or on (foo, bar) a
|
|
|
v
SELECT a.value * COALESCE(b.value, 1), a.*, b.baz
FROM a LEFT OUTER JOIN b ON (a.foo == b.foo AND a.bar == b.bar)
```

## Use case: Using group\_left to add hostname label to a query result

Sometimes, the `instance` in Prometheus metric doesn't make any sense and we need something else to provide more information. A hostname for example, and our answer exist inside the `node_uname_info`. We just need to take the hostname from this metric and add the final value.

The solution is using `group_left`:

```
node_memory_Active_bytes * on(instance) group_left(nodename) (node_uname_info)
```

Prometheus gets the `nodename` from `node_uname_info` and add into the final results:

```
{instance="localhost:9100",job="node-exporter",nodename="your-first-vm"}	36917006336
```
