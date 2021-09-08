# Best practices for REST API design

Source: https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/

- [Best practices for REST API design](#best-practices-for-rest-api-design)
  - [1. Accept and respond with JSON](#1-accept-and-respond-with-json)
  - [2. Use nouns instead of verbs in endpoint paths](#2-use-nouns-instead-of-verbs-in-endpoint-paths)
  - [3. Use logical nesting on endpoints](#3-use-logical-nesting-on-endpoints)
  - [4. Handle errors gracefully and return standard error codes](#4-handle-errors-gracefully-and-return-standard-error-codes)
  - [5. Allow filtering, sorting, and pagination](#5-allow-filtering-sorting-and-pagination)
  - [6. Maintain good security practices](#6-maintain-good-security-practices)
  - [7. Cache data to improve performance](#7-cache-data-to-improve-performance)
  - [8. Versioning our APIs](#8-versioning-our-apis)

## 1. Accept and respond with JSON

- REST APIs should accept JSON for request payload and also send responses to JSON.
- To make sure that when our REST API app responds with JSON that clients interpret it as such, we should set Content-Type in the response header to application/json after the request is made.

## 2. Use nouns instead of verbs in endpoint paths

- Should use the nouns which represent the entity that the endpoint that we’re retrieving or manipulating as the pathname.
- The action should be indicated by the HTTP request method that we're making.
  - GET retrieves resources.
  - POST submits new data to the server.
  - PUT updates existing data.
  - DELETE removes data.
- For example, GET /articles/ for getting news articles. Likewise, POST /articles/ is for adding a new article , PUT /articles/:id is for updating the article with the given id. DELETE /articles/:id is for deleting an existing article with the given ID.

## 3. Use logical nesting on endpoints

- When designing endpoints, it makes sense to group those that contain associated information. That is, if one object can contain another object, you should design the endpoint to reflect that.
- For example, if we want an endpoint to get the comments for a news article, we should append the /comments path to the end of the /articles path.

## 4. Handle errors gracefully and return standard error codes

- Common error HTTP status codes include:
  - 400 Bad Request – This means that client-side input fails validation.
  - 401 Unauthorized – This means the user isn’t not authorized to access a resource. It usually returns when the user isn’t authenticated.
  - 403 Forbidden – This means the user is authenticated, but it’s not allowed to access a resource.
  - 404 Not Found – This indicates that a resource is not found.
  - 500 Internal server error – This is a generic server error. It probably shouldn’t be thrown explicitly.
  - 502 Bad Gateway – This indicates an invalid response from an upstream server.
  - 503 Service Unavailable – This indicates that something unexpected happened on server side (It can be anything like server overload, some parts of the system failed, etc.).

## 5. Allow filtering, sorting, and pagination

- The databases can get very large.
- We need ways to filter items, paginate data.

## 6. Maintain good security practices

- Most communication between client and server should be private -> using SSL/TLS for security is a must.
- People shouldn't be able to access more information that they requested -> least priviledge -> Add role checks for a single role, have more granular roles for each user.

## 7. Cache data to improve performance

- Add caching to return data from the local memory instead of querying the database to get the data every time.
- If you are using caching, you should also include Cache-Control information in your headers. This will help users effectively use your caching system.

## 8. Versioning our APIs

- Should have different versions of APIs if we're making any changes to them that may break items.
