# Caching Header Best Practices

Source: <https://simonhearne.com/2022/caching-header-best-practices/>

Table of contents:

- [Caching Header Best Practices](#caching-header-best-practices)
  - [1. Introduction](#1-introduction)
  - [2. The solution](#2-the-solution)
  - [3. Caching Headers](#3-caching-headers)
  - [4. Caching Behaviors](#4-caching-behaviors)
    - [4.1. Not Cacheable](#41-not-cacheable)
    - [4.2. Immutable](#42-immutable)

## 1. Introduction

- Caching headers are one of those deceptively complex web technologies which are so often overlooked or misconfigured.
- The focus of this post is on client-side (or downstream) caching - in the client device. Caching in proxies, load balancers and CDNs adds some more complexity, and is not covered here.

## 2. The solution

- Use versioned assets wherever possible (e.g.`main.v123.min.css` or `main.min.css?v=123`) and set a single caching header allowing the maximum cache duration of one year:

```http
Cache-Control: max-age=31536000, immutable
```

- For non-versioned assets which may change, combine the Cache-Control header with an ETag for asynchronous revalidation in the client:

```http
Cache-Control: max-age=604800, stale-while-revalidate=86400
ETag: "<file-hash-generated-by-server>"
```

- For HTML files, set a low TTL and private cache flags:

```http
Cache-Control: max-age:300, private
```

![](https://simonhearne.com/img/_dzUob7MLk-900.avif)

## 3. Caching Headers

- [Expires](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expires): a date (in GMT) after which this asset may no longer be used from the browsers cache and must be re-fetched.
- [Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control): a combination of features in one header, including how long the resource can be cached by the client (in seconds) as well as whether proxies can cache it, whether to force revalidation and more.
- [ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag): a string that uniquely identifies an asset version, generally a server-generated hash of the file.
- [Last-Modified](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Last-Modified): a timestamp which allows browsers to validate the freshness of cached assets.
- [Pragma](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Pragma): a hangover from HTTP/1.0, this should generally not be used in preference for Cache-Control except where HTTP/1.0 clients must be supported.

> **Recommendation**: use `Cache-Control` and `ETag`.

## 4. Caching Behaviors

### 4.1. Not Cacheable

- For assets that are dynamically generated.
- Client can cache the asset, but it can't use the cached asset without revalidating with the server.

```http
Cache-Control: no-cache
```

- Client may not store asset at all.

```http
Cache-Control: no-store
```

### 4.2. Immutable

- For versioned asset.
- The asset can be stored for a year and never needs to be revalidated.

```http
Cache-Control: max-age=31536000, immutable
```

### 4.3. Time-restricted

- For asset which should be stored for the duration of a session (e.g.one day or one week) but should be refreshed or revalidated if the visitor returns later.

```http
Cache-Control: max-age=86400
```

### 4.4. Revalidate

- When combined with Time-restricted, this allow browsers to use a cached asset for a period of time (from zero seconds up to a year) and then revalidate the object with origin once that period has expired.

```http
Cache-Control: max-age=604800, stale-while-revalidate=86400
```

// WIP
