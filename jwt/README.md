# JSON Web Token (JWT)

- [JSON Web Token (JWT)](#json-web-token-jwt)
  - [What is it?](#what-is-it)
  - [What is its structure?](#what-is-its-structure)
    - [Header](#header)
    - [Payload](#payload)
    - [Signature](#signature)
  - [How it works?](#how-it-works)
  - [Implementation in <put-a-programming-language-here>](#implementation-in-put-a-programming-language-here)

## What is it?

JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

Want more, check the [official JWT introduction](https://jwt.io/introduction/).

## What is its structure?

```
<header>.<payload>.<signature>
```

### Header

```json
{
	"alg": "HS256", # The signing algorithm being used (HMAC SHA256/RSA)
	"typ": "JWT" # The type of token
}
```

JSON --> Base64Url encoded --> `<header>`

### Payload

Contains the **claims**:

- **Registered claims**:
  - A set of predefined claims.
  - Provide a set of useful, interoperable claims.
  - iss (issuer), exp (expiration time), sub (subject), aud (audience)...
- **Public claims**:
  - Should be defined in the [IANA JSON Web Token registry](https://www.iana.org/assignments/jwt/jwt.xhtml).
- **Private claims**:
  - Custom.
  - Share information between parties that agree on using them.
  - Are neither registered nor public claims.

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

JSON --> Base64Url encoded --> `<*payload*>`

### Signature

```
<alg>(base64UrlEncode(<header> + "." + <payload>), <secret>)
```

The signature is used to verify the message wasn't changed along the way and in the case of tokens signed with a private key, it can also verify that the sender of the JWT is who it says it is.

## How it works?

![](https://miro.medium.com/max/1480/1*tW-8Y2edq04b4__zF0Jm9Q.png)

Image source [here](https://medium.com/@siddharthac6/json-web-token-jwt-the-right-way-of-implementing-with-node-js-65b8915d550e)

Whenever the user wants to access a protected route or resource, the user agent should send the JWT, typically in the **Authorization** header using the **Bearer** schema.

```
Authorization: Bearer <token>
```

## Implementation in <put-a-programming-language-here>

<WIP>
