# Redis Benchmark

Source:

- <https://redis.io/docs/management/optimization/benchmarks/>

Table of contents:

- [Redis Benchmark](#redis-benchmark)
  - [1. Key factors and gotchas](#1-key-factors-and-gotchas)
  - [2. Setup](#2-setup)
  - [3. Latency](#3-latency)
  - [4. redis-benchmark](#4-redis-benchmark)
  - [5. memtier benchmark](#5-memtier-benchmark)

## 1. Key factors and gotchas

- Redis is a single-threaded server from the POV of commands execution. It is not designed to benefit from multiple CPU cores.
- Natively iterating on synchronous Redis commands does not benchmark Redis itself, but rather measure your network (or IPC) latency and the client library intrinsic latency. To really test Redis, you need multiple connections (like redis-benchmark) and/or to use pipelining to aggregate several commands and/or multiple threads or processes.
- Network bandwidth and latency usually have a direct impact to the performance.
  - Check network latency with `ping` before launching the benchmark.
  - Estimate the throughput in Gbit/s and compare it to the theoretical bandwidth of the network.
- CPU: Being single-threaded, Redis favors fast CPUs with large caches and not many cores.
- Speed of RAM and memory bandwidth seem less critical for global performance especially for small objects
- Redis runs slower on a VM compared to running without virtualization using the same hardware.
- Run tests on isolated hardware as much as possible.
- The system must have enough RAM and must not swap.
- If you plan to use RDB or AOF for benchmark, please check there is no other I/O activity in the system.
- Set Redis logging level to warning or notice.
- Avoid using monitoring tools which can alter the result of the benchmark (MONITOR command).

## 2. Setup

- Cause the limitation of resource, I will launch benchmark in a single host with docker-compose.

```shell
# Setup Redis cluster
docker compose -p bench up -d
```

- Redis cluster with 4 master, replicas 1 and disabled persistence.

## 3. Latency

- In the context of Redis, latency is a measure of how long does a `ping` command take to receive a response from the server.
- Check latency:

```shell
docker run -it --rm --net bench_default bitnami/redis:7.0 redis-cli -h redis-node-0 -a bitnami --latency

min: 0, max: 1, avg: 0.27 (9194 samples)
```

- If you’d like to measure the system latency only, you can use `--intrinsic-latency` for that.
  - The intrinsic latency is inherent to the environment, depending on factors such as hardware, kernel, server neighbors, and other factors that aren't controlled by Redis.
  - You need to run this command in the server, not in the client.

```shell
docker exec -it redis-node-0 redis-cli -h redis-node-0 -a bitnami --intrinsic-latency 100

Max latency so far: 1 microseconds.
Max latency so far: 2 microseconds.
Max latency so far: 3 microseconds.
Max latency so far: 14 microseconds.
Max latency so far: 50 microseconds.

45067127 total runs (avg latency: 2.2189 microseconds / 2218.91 nanoseconds per run).
Worst run took 23x longer than the average latency.
```

- Read more about [latency here](https://redis.io/docs/management/optimization/latency/).

## 4. redis-benchmark

- Redis comes with a benchmark tool called `redis-benchmark`. This program can be used to simulate an arbitrary number of clients connecting at the same time and performing actions on the server, measuring how long it takes for the requests to be completed. The resulting data will give you an idea of the average number of requests that your Redis server is able to handle per second.

```shell
redis-benchmark --help

...
 -h <hostname>      Server hostname (default 127.0.0.1)
 -p <port>          Server port (default 6379)
 -s <socket>        Server socket (overrides host and port)
 -a <password>      Password for Redis Auth
 --user <username>  Used to send ACL style 'AUTH username pass'. Needs -a.
 -u <uri>           Server URI.
 -c <clients>       Number of parallel connections (default 50)
 -n <requests>      Total number of requests (default 100000)
 -d <size>          Data size of SET/GET value in bytes (default 3)
 --dbnum <db>       SELECT the specified db number (default 0)
 -3                 Start session in RESP3 protocol mode.
 --threads <num>    Enable multi-thread mode.
 --cluster          Enable cluster mode.
                    If the command is supplied on the command line in cluster
                    mode, the key must contain "{tag}". Otherwise, the
                    command will not be sent to the right cluster node.
 --enable-tracking  Send CLIENT TRACKING on before starting benchmark.
 -k <boolean>       1=keep alive 0=reconnect (default 1)
 -r <keyspacelen>   Use random keys for SET/GET/INCR, random values for SADD,
                    random members and scores for ZADD.
                    Using this option the benchmark will expand the string
                    __rand_int__ inside an argument with a 12 digits number in
                    the specified range from 0 to keyspacelen-1. The
                    substitution changes every time a command is executed.
                    Default tests use this to hit random keys in the specified
                    range.
                    Note: If -r is omitted, all commands in a benchmark will
                    use the same key.
 -P <numreq>        Pipeline <numreq> requests. Default 1 (no pipeline).
 -q                 Quiet. Just show query/sec values
 --precision        Number of decimal places to display in latency output (default 0)
 --csv              Output in CSV format
 -l                 Loop. Run the tests forever
 -t <tests>         Only run the comma separated list of tests. The test
                    names are the same as the ones produced as output.
                    The -t option is ignored if a specific command is supplied
                    on the command line.
 -I                 Idle mode. Just open N idle connections and wait.
 -x                 Read last argument from STDIN.
 --tls              Establish a secure TLS connection.
 --sni <host>       Server name indication for TLS.
 --cacert <file>    CA Certificate file to verify with.
 --cacertdir <dir>  Directory where trusted CA certificates are stored.
                    If neither cacert nor cacertdir are specified, the default
                    system-wide trusted root certs configuration will apply.
 --insecure         Allow insecure TLS connection by skipping cert validation.
 --cert <file>      Client certificate to authenticate with.
 --key <file>       Private key file to authenticate with.
 --tls-ciphers <list> Sets the list of preferred ciphers (TLSv1.2 and below)
                    in order of preference from highest to lowest separated by colon (":").
                    See the ciphers(1ssl) manpage for more information about the syntax of this string.
 --tls-ciphersuites <list> Sets the list of preferred ciphersuites (TLSv1.3)
                    in order of preference from highest to lowest separated by colon (":").
                    See the ciphers(1ssl) manpage for more information about the syntax of this string,
                    and specifically for TLSv1.3 ciphersuites.
...
```

- Run test on Redis cluster:
  - Number of (parallel) connections: 100
  - Number of requests: 20000
  - Number of threads: 50
  - Data size of SET/GET value in bytes: 32 bytes
  - Enable pipeline with 10.

```shell
# Don't forget to change host address and password
# Assume bench_default is the Redis cluster network
# The result can be different
docker run -it --rm --net bench_default bitnami/redis:7.0 redis-benchmark -h redis-node-0 -a bitnami --cluster -t set,get -c 100 --threads 50 -n 20000 -d 32 -P 10

...
99.150% <= 274.175 milliseconds (cumulative count 198300)
99.200% <= 289.279 milliseconds (cumulative count 198400)
99.300% <= 299.263 milliseconds (cumulative count 198600)
99.400% <= 362.239 milliseconds (cumulative count 198800)
99.500% <= 368.127 milliseconds (cumulative count 199000)
99.550% <= 455.167 milliseconds (cumulative count 199100)
99.600% <= 502.271 milliseconds (cumulative count 199200)
99.700% <= 601.599 milliseconds (cumulative count 199400)
99.800% <= 614.399 milliseconds (cumulative count 199600)
99.900% <= 638.463 milliseconds (cumulative count 199800)
100.000% <= 648.191 milliseconds (cumulative count 200000)

Summary:
  throughput summary: 201207.23 requests per second
  latency summary (msec):
          avg       min       p50       p95       p99       max
       93.030     0.776    89.087   169.855   259.199   648.191
```

## 5. memtier benchmark

- [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark) is a high-throughput benchmark tool for Redis and Memcached created by Redis Labs.

```shell
Usage: memtier_benchmark [options]
A memcache/redis NoSQL traffic generator and performance benchmarking tool.

Connection and General Options:
  -h, --host=ADDR                Server address (default: localhost)
  -s, --server=ADDR              Same as --host
  -p, --port=PORT                Server port (default: 6379)
  -S, --unix-socket=SOCKET       UNIX Domain socket name (default: none)
  -4, --ipv4                     Force IPv4 address resolution.
  -6  --ipv6                     Force IPv6 address resolution.
  -P, --protocol=PROTOCOL        Protocol to use (default: redis).
                                 other supported protocols are resp2, resp3, memcache_text and memcache_binary.
                                 when using one of resp2 or resp3 the redis protocol version will be set via HELLO command.
  -a, --authenticate=CREDENTIALS Authenticate using specified credentials.
                                 A simple password is used for memcache_text
                                 and Redis <= 5.x. <USER>:<PASSWORD> can be
                                 specified for memcache_binary or Redis 6.x
                                 or newer with ACL user support.
      --tls                      Enable SSL/TLS transport security
      --cert=FILE                Use specified client certificate for TLS
      --key=FILE                 Use specified private key for TLS
      --cacert=FILE              Use specified CA certs bundle for TLS
      --tls-skip-verify          Skip verification of server certificate
      --sni=STRING               Add an SNI header
  -x, --run-count=NUMBER         Number of full-test iterations to perform
  -D, --debug                    Print debug output
      --client-stats=FILE        Produce per-client stats file
  -o, --out-file=FILE            Name of output file (default: stdout)
      --json-out-file=FILE       Name of JSON output file, if not set, will not print to json
      --hdr-file-prefix=FILE     Prefix of HDR Latency Histogram output files, if not set, will not save latency histogram files
      --show-config              Print detailed configuration before running
      --hide-histogram           Don't print detailed latency histogram
      --print-percentiles        Specify which percentiles info to print on the results table (by default prints percentiles: 50,99,99.9)
      --cluster-mode             Run client in cluster mode
  -h, --help                     Display this help
  -v, --version                  Display version information

Test Options:
  -n, --requests=NUMBER          Number of total requests per client (default: 10000)
                                 use 'allkeys' to run on the entire key-range
  -c, --clients=NUMBER           Number of clients per thread (default: 50)
  -t, --threads=NUMBER           Number of threads (default: 4)
      --test-time=SECS           Number of seconds to run the test
      --ratio=RATIO              Set:Get ratio (default: 1:10)
      --pipeline=NUMBER          Number of concurrent pipelined requests (default: 1)
      --reconnect-interval=NUM   Number of requests after which re-connection is performed
      --multi-key-get=NUM        Enable multi-key get commands, up to NUM keys (default: 0)
      --select-db=DB             DB number to select, when testing a redis server
      --distinct-client-seed     Use a different random seed for each client
      --randomize                random seed based on timestamp (default is constant value)

Arbitrary command:
      --command=COMMAND          Specify a command to send in quotes.
                                 Each command that you specify is run with its ratio and key-pattern options.
                                 For example: --command="set __key__ 5" --command-ratio=2 --command-key-pattern=G
                                 To use a generated key or object, enter:
                                   __key__: Use key generated from Key Options.
                                   __data__: Use data generated from Object Options.
      --command-ratio            The number of times the command is sent in sequence.(default: 1)
      --command-key-pattern      Key pattern for the command (default: R):
                                 G for Gaussian distribution.
                                 R for uniform Random.
                                 S for Sequential.
                                 P for Parallel (Sequential were each client has a subset of the key-range).

Object Options:
  -d  --data-size=SIZE           Object data size in bytes (default: 32)
      --data-offset=OFFSET       Actual size of value will be data-size + data-offset
                                 Will use SETRANGE / GETRANGE (default: 0)
  -R  --random-data              Indicate that data should be randomized
      --data-size-range=RANGE    Use random-sized items in the specified range (min-max)
      --data-size-list=LIST      Use sizes from weight list (size1:weight1,..sizeN:weightN)
      --data-size-pattern=R|S    Use together with data-size-range
                                 when set to R, a random size from the defined data sizes will be used,
                                 when set to S, the defined data sizes will be evenly distributed across
                                 the key range, see --key-maximum (default R)
      --expiry-range=RANGE       Use random expiry values from the specified range

Imported Data Options:
      --data-import=FILE         Read object data from file
      --data-verify              Enable data verification when test is complete
      --verify-only              Only perform --data-verify, without any other test
      --generate-keys            Generate keys for imported objects
      --no-expiry                Ignore expiry information in imported data

Key Options:
      --key-prefix=PREFIX        Prefix for keys (default: "memtier-")
      --key-minimum=NUMBER       Key ID minimum value (default: 0)
      --key-maximum=NUMBER       Key ID maximum value (default: 10000000)
      --key-pattern=PATTERN      Set:Get pattern (default: R:R)
                                 G for Gaussian distribution.
                                 R for uniform Random.
                                 S for Sequential.
                                 P for Parallel (Sequential were each client has a subset of the key-range).
      --key-stddev               The standard deviation used in the Gaussian distribution
                                 (default is key range / 6)
      --key-median               The median point used in the Gaussian distribution
                                 (default is the center of the key range)

WAIT Options:
      --wait-ratio=RATIO         Set:Wait ratio (default is no WAIT commands - 1:0)
      --num-slaves=RANGE         WAIT for a random number of slaves in the specified range
      --wait-timeout=RANGE       WAIT for a random number of milliseconds in the specified range (normal
                                 distribution with the center in the middle of the range)
```

- Run test on Redis cluster:
  - Number of client per thread: 100
  - Number of requests: 20000
  - Number of threads: 50
  - Data size of SET/GET value in bytes: 32 bytes
  - Enable pipeline with 10.
  - Ratio between SET and GET: 1:5.

```shell
docker run -it --rm --net bench_default -v /tmp/results:/tmp/test redislabs/memtier_benchmark:2.0.0 -h redis-node-0 -a bitnami --cluster-mode -c 100 --threads 50 -n 20000 -d 32 --pipeline=10 --ratio=1:5 --hdr-file-prefix=/tmp/test/test
```

- Check result files in `/tmp/results`:

```shell
ls /tmp/results
test_FULL_RUN_1.hgrm  test_FULL_RUN_1.txt  test_GET_command_run_1.hgrm  test_GET_command_run_1.txt  test_SET_command_run_1.hgrm  test_SET_command_run_1.txt
```

- Visualize in [online formatter](http://hdrhistogram.github.io/HdrHistogram/plotFiles.html), choose your .txt file:

![](./images/Histogram.png)
