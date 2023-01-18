---
title: Differences Between OpenAPI 2.0 and 3.0
path: web-dev/openapi-2-and-3.md
---

## Specification Restructured to Increase Reusability

![image](https://user-images.githubusercontent.com/10803803/132095470-174c98bf-a7bb-4d9c-964f-e5556685a3a7.png)

## Extended JSON Schema Support

The 3.0 release includes extended support for JSON Schema, which means you can use more JSON Schema keywords than with version 2.0. Some keywords supported in version 3.0 are handled slightly differently than in JSON Schema, including:

- oneOf
- anyOf
- allOf

OpenAPI 2.0 does not support the oneOf or anyOf keywords, but you can use these keywords with version 3.0.

## Examples Overhauled for Easy Reusability

## Improved Parameter Descriptions

Version 3.0 includes improvements to parameter descriptions. The `body` and `formData` parameter types have been removed and replaced with `requestBody`. The specification supports arrays and objects in operation parameters, and you can specify the method of serialization. Operation parameters include path, query, header, and cookie.

## More

Source: <https://blog.stoplight.io/difference-between-open-v2-v3-v31>
