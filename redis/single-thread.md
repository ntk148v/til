# Redis - Single thread

Source:

- <https://www.sobyte.net/post/2022-08/redis-single-thread/>

```
Redis is, mostly, a single-threaded server from the POV of commands execution (actually modern versions of Redis use threads for different things). It is not designed to benefit from multiple CPU cores. People are supposed to launch several Redis instances to scale out on several cores if needed. It is not really fair to compare one single Redis instance to a multi-threaded data store.
```
