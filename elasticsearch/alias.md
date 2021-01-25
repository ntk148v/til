# Index alias

## 1. What is an index alias?

An index alias is another name you can put on one or several indices.

```
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-logs-*",
        "alias": "my-logs"
      }
    }
  ]
}
```

## 2. Use cases

### 2.1. Scoping requests



## 1. TL;DR

- An alias is acting exactly like an index.
- You can query an ingest on an alias with normal API calls.
- An alias can be set on several indices.
- Aliases can be changed whenever you want.
- Alias helps maintaining Index with no downtime.
