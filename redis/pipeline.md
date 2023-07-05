# Redis pipeline

Source:

- <https://stackexchange.github.io/StackExchange.Redis/PipelinesMultiplexers>
- <https://redis.io/docs/manual/pipelining/>
- <https://buildatscale.tech/what-is-redis-pipeline/>
- <https://taswar.zeytinsoft.com/redis-pipeline-batching/>

## 1. Introduction

- Redis clients and servers communicate with each other using a protocol called [RESP (REdis Serialization Protocol)](https://redis.io/topics/protocol) which is TCP-based.
- In TCP-based protocol, server and client communicate with request/response model.
  - The client sends a request, the server processes the command.
  - The client waits for the response in a blocking way.
- This looks like:

```unknown
[req1]                         # client: the client library constructs request 1
     [c=>s]                    # network: request one is sent to the server
          [server]             # server: the server processes request 1
                 [s=>c]        # network: response one is sent back to the client
                      [resp1]  # client: the client library parses response 1
                            [req2]
                                 [c=>s]
                                      [server]
                                             [s=>c]
                                                  [resp2]

```

- Where the client is doing something:

```unknown
[req1]
     [====waiting=====]
                      [resp1]
                            [req2]
                                 [====waiting=====]
                                                  [resp2]
```

![](https://taswar.zeytinsoft.com/wp-content/uploads/2017/04/redis-client-server.png)

- Now consider a case, where we want to SET or GET 100s of commands, if we go by regular route, each command will take up some Round Trip Time(RTT) and that will be repeated for all the commands, which is not optimum. In cases like this, we can use Redis Pipeline.
- Redis pipelining is a technique for improving performance by issuing multiple commands at once without waiting for the response to each individual command.
  - Pipelining is basically a network optimization, where all commands are grouped from the client-side and sent at once.
  - While the client sends commands using pipelining, the server will be forced to queue the replies, using memory. So if you need to send a lot of commands with pipelining, it is better to send them as batches each containing a reasonable number, for instance 10k commands, read the replies, and then send another 10k commands again, and so forth.

![](https://taswar.zeytinsoft.com/wp-content/uploads/2017/04/redis-pipeline.png)

## 2. Benchmark

- Benchmark with StackExchange.Redis library.

```csharp
using StackExchange.Redis;
using System;

namespace RedisPipeline
{

    class Program
    {
        static readonly ConnectionMultiplexer redis = ConnectionMultiplexer.Connect(
                new ConfigurationOptions
                {
                    // Sammple REDIS_URI string: https://stackexchange.github.io/StackExchange.Redis/Configuration
                    EndPoints = { System.Environment.GetEnvironmentVariable("REDIS_URI") ?? "localhost" },
                });
        static void Main()
        {
            bench(withPipeline, 10000, "with Pipeine");
            bench(withoutPipeline, 10000, "without Pipeine");

            redis.Close();
        }

        static void bench(Action<int> benchedMethod, int loopNum, string desc)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            benchedMethod(loopNum);
            watch.Stop();
            Console.WriteLine($"Elapsed time {desc}: {watch.ElapsedMilliseconds} milliseconds");
        }

        static void withoutPipeline(int loopNum)
        {
            IDatabase db = redis.GetDatabase();
            for (int i = 0; i < loopNum; i++)
            {
                db.StringSet("key" + i, "value" + i);
                db.StringGet("key" + i);
            }
        }

        static void withPipeline(int loopNum)
        {
            IDatabase db = redis.GetDatabase();
            var pipeline = db.CreateBatch();
            for (int i = 0; i < loopNum; i++)
            {
                pipeline.StringSetAsync("key" + i, "value" + i);
                pipeline.StringGetAsync("key" + i);
            }
            pipeline.Execute();
        }
    }
}
```
