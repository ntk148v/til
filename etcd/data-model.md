# Etcd V3 data model

<https://etcd.io/docs/v3.4.0/learning/data_model/>

- Infrequently updated data.
- Muti-version.
- Persistent.

## Logical view

- Flat binary key space.
- The key space maintains multiple revisions.
  - Each atomic mutative operation creates a new revision on the key space.
  - All data held by previous revisions remains unchanged and be accessed.
  - Store is compacted -> revisions > the compact revision - removed.
- A key's life spans a generation, from creation to deletion.
- Each key may have one or multiple generations.

## Physical view

- Stores as key-value pairs in a persistent [b+tree](https://en.wikipedia.org/wiki/B%2B_tree).
- Each revision of the store's state only contains the delta from its previous revision.
- The key of key-value pair is a 3-tuple (major, sub, type).

```
key = major + sub + type
        |      |      |
        |      |      |
        v      |      |
store revision holding the key
               |      |
               |      |
               v      |
differentiates among keys within the same revision
                      |
                      |
                      v
optional suffex for special value.
```
