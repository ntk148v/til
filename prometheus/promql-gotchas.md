# PromQL Gotchas

## Instant vector & Range Vector

* **Instant vector**: One value per time series guaranteed.
* **Range vector**: Any number of values between two timestamps.

## Operators

* Aggregation Operators
    
```
instant vector -> instant vector
```

* Binary operators

```
instant vector <operator> instant vector = instant vector
```

## Functions

```
instant vector -> instant vector
range vector -> instant vector
```

### Gotchas

* Tell your aggregation operators about the label you care about.
* Never compare raw counters - use rate().
* Be careful with label sets when using binary operators.

https://promcon.io/2019-munich/slides/promql-for-mere-mortals.pdf
