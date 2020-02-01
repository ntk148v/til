# Redis vs Memcached Note

Source: https://www.infoworld.com/article/3063161/why-redis-beats-memcached-for-caching.html

## The similarities

Both serve as in-memory, key-value stores, although Redis is more accurately described as a data structure store.

## When to use Memcached

* Cache relatively small and static data, such as HTMl code fragments.
* Internal memory management is more efficient in the simplest use cases because it consumes comparatively less memory resources for metadata.
* The only data type supported by Memcached: `string` - ideal for storing data that is only read.
* Cache management: data eviction - Least Recently Used.

## When to use Redis

* For storing the data structure.
* Cache management: by constrast, Redis allows for fine-grained control over eviction, letting you choose from six different eviction policies. Redis supports both lazy and active eviction, where data is evicted when more space is needed or proactively.
* Memcached limits key names to 250 bytes and works with plain strings only, Redis allows key names and values to be as large as 512MB each, and they are binary safe.
* Replicate the data that it manages.
* Has data persistence.

## Conclusion

Redis should be your first choice in nearly every case.
