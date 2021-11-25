---
title: HTTP Headers
path: web-dev/http-headers.md
---

Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

**HTTP headers** let the client and the server pass additional information with an HTTP request or response.

I don't aim to list all headers here, just some interested me.

## 1. Accept-Ranges and Range

- When working with Golang HTTP client to download file, I find out these two headers.
- `Accept-Ranges` HTTP response header is a marker used by the server to advertise its support for partial requests from the client for file downloads. The value of this field indicates the unit that can be used to define a range.
- In the presence of an `Accept-Ranges` header, the browser may try to _resume_ an interrupted download instead of trying to restart the download.

```
Accept-Ranges: <range-unit>
Accept-Ranges: none
```

- If server implements partial downloads, client can use `Range` HTTP request header to indicate the part of a document that the server should return.
  - Several parts can be requested with one Range header at once, and the server may send back these ranges in a multipart document.
  - If the server sends back ranges --> `206 Partial Content` for the response.
  - If ranges are invalid --> `416 Range Not Statisfiable`.
  - The server can also ignore the Range header and return the _whole document_ with a `200`.

```
Range: <unit>=<range-start>-
Range: <unit>=<range-start>-<range-end>
Range: <unit>=<range-start>-<range-end>, <range-start>-<range-end>
Range: <unit>=<range-start>-<range-end>, <range-start>-<range-end>, <range-start>-<range-end>
Range: <unit>=-<suffix-length>
```

- So, what can I do with them? You can use them to implement a server that hosts files ([Golang http.ServeFile](https://pkg.go.dev/net/http#ServeFile) handles Range and Cache for you), then create a parallel download client.

// WIP: Add example here.