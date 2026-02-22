# YAQL: Yet Another Query Language

## Intro

- YAQL: an embeddable and extensible query language, that allows performing complex queries against arbitrary objects. It has a avast and comprehensive standard library of frequently used querying functions and can be extend even further with user-specified functions.
- YAQL - Yet Another Thing To Learn.

## YAQL grammar

### Data access

- `$<variable_name>`

### Strings

- strings can be enclosed " and '.
- \` is used to create a string where only one escape sysmbol \` is possible.
- If a string does not start with a digit or \_\_ and contains only digits, \_ and English letters, it is called identifier can be used without quotes at all. An identifier can be used as a name for function, parameter or property in $obj.property case.

### Functions

- `functionName(functionParameters)`. Brackets are necessary even if there are no parameters.
- Parameters:
  - Positional parmeters: `foo(1, 2, someValue)`.
  - Named parameters: `foo(paramName1 => value1, paramName2 => 123)`.
  - Mix: `foo(1, fals, param => null)`.

- Functions
  - Regular functions: `max(1, 2)`.
  - Method-like functions, which are called by specifying an object for which the function is called, followed by a dot and a function call: `stringValue.toUpper()`.
  - Extension methods, which can be called both ways: `len(string), string.len()`.

- YAQL standard library contains hundreds of functions which belong to one of these types.
- Applications can add new functions and override functions from the standard library.

### Operators

- Arithmetic: +. -, \*, /, mod
- Logical: =, !=, >=, <=, and, or, not
- Regexp operations: =~, !~
- Method call, call to the attribute: ., ?.
- Context pass: ->
- Indexing: [ ]
- Membership test operations: in

### Data structures

- Scalars: sring, int, boolean, Datetime and timespan.
- Lists: List creation [1, 2, value, true] or list(1, 2, value, true).
- Dictionaries: Dict creation: {key1 => value1, true => 1, 0 => false} or dict(key => value1, true => 1, 0 => false).
- Sets.

> NOTE: YAQL is designed to keep input data unchanged. All the functions that look as if they change data, actually return an updated copy and keep the original data unchanged. This is one reason why YAQL is thread-safe.

## Basic YAQL query operations

```yaml
customers_city:
  - city: New York
    customer_id: 1
  - city: Saint Louis
    customer_id: 2
  - city: Mountain View
    customer_id: 3
customers:
  - customer_id: 1
    name: John
    orders:
      - order_id: 1
        item: Guitar
        quantity: 1
  - customer_id: 2
    name: Paul
    orders:
      - order_id: 2
        item: Banjo
        quantity: 2
      - order_id: 3
        item: Piano
        quantity: 1
  - customer_id: 3
    name: Diana
    orders:
      - order_id: 4
        item: Drums
        quantity: 1
```

- Filtering

```
yaql> $.customers.where($.name = John)
```

- Ordering

```
yaql> $.customers.orderBy($.name)
```

- Grouping

```
yaql> $.customers.groupBy($.name)
```

- Selecting

```
yaql> $.customers.select([$.name, $.orders])
```

- Joining

```
yaql> $.customers.join($.customers_city, $1.customer_id = $2.customer_id, {customer=>$1.name, city=>$2.city, orders=>$1.orders})
```

- Take an element from collection

```
yaql> $.customers.skip(1).take(2)
```

- First element of collection

```
yaql> $.customers.first()
```
