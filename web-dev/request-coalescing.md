# Request Coalescing

Source: <https://support.bunny.net/hc/en-us/articles/6762047083922-Understanding-Request-Coalescing>

- Request Coalescing combines multiple simultaneous requests to the same resource into a single request going to the origin. If multiple requests come in at the same time, they will be automatically merged. Once the request from the origin completes, the response will be streamed in real-time to all waiting connections for that request path.
- Request Coalescing works by using a special lock mechanism when sending requests to the origin. Traditionally, a CDN would send requests from the end-user to the origin and proxy the response back to that response. Request Coalescing on the other hand will, upon receiving a request, first, open a mutex lock. Then, the Request Coalescing system will send a single request to the origin. As soon as the origin responds, the mutex is released and all the waiting connections are automatically connected to the origin response.

![](https://bunny.net/blog/content/images/2022/06/bunnynet-cdn-request-coalescing-realtime-streaming-5.png)

- Benefits: the reduction of the load on your origin server, especially during large traffic spikes to the same resources such as live streaming, or very public APIs where the result can be cached to multiple users.
- How does Request Coalescing handle dynamic data? Request Coalescing will trigger on any uncached request hitting the CDN edge server. This is true for requests to both static and dynamic resources. It means that Request Coalescing should not be used in cases where the data being retrieved from the origin should be unique between users.
- Does Request Coalescing mean only one request will ever hit my server? No, Request Coalescing does not assure only a single request will ever be sent to the origin. It only combines uncached requests that are accessing a single resource at the same time. With Request Coalescing enabled, your origin could still receive a request to the same resource if the requests arrive sequentially. Coalescing also runs on each Edge Node/cluster independently, so you'll see 1 request for each file from each CDN PoP.
