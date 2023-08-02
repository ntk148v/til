# JSON Web Token (JWT)

Source:

- <https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/>
- <https://jwt.io/introduction/>

Table of contents:

- [JSON Web Token (JWT)](#json-web-token-jwt)
  - [1. Introduction](#1-introduction)
    - [1.1. What is JWT?](#11-what-is-jwt)
    - [1.2. Security considerations](#12-security-considerations)
    - [1.3. JWT structure?](#13-jwt-structure)
      - [1.3.1. Header](#131-header)
      - [1.3.2. Payload](#132-payload)
      - [1.3.3. Signature](#133-signature)
  - [2. How it works?](#2-how-it-works)
    - [2.1. Basic login](#21-basic-login)
    - [2.2. Basic logout](#22-basic-logout)
    - [2.3. Silent refresh](#23-silent-refresh)
  - [3. Implementation in `<put-a-programming-language-here>`](#3-implementation-in-put-a-programming-language-here)

## 1. Introduction

### 1.1. What is JWT?

JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

Want more, check the [official JWT introduction](https://jwt.io/introduction/).

### 1.2. Security considerations

- But can't a client just create a random JSON payload an impersonate a user?
  - Good question! That’s why a JWT also contains a signature. This signature is created by the server that issued the token (let’s say your login endpoint) and any other server that receives this token can independently verify the signature to ensure that the JSON payload was not tampered with, and has information that was issued by a legitimate source.
- But if I have a valid and signed JWT and someone steals it from the client, can’t they use my JWT forever?
  - Yes! If a JWT is stolen, then the thief can can keep using the JWT. An API that accepts JWTs does an independent verification without depending on the JWT source so the API server has no way of knowing if this was a stolen token! This is why JWTs have an expiry value. And these values are kept short. Common practice is to keep it around 15 minutes, so that any leaked JWTs will cease to be valid fairly quickly. But also, make sure that JWTs don’t get leaked.
  - That’s why it’s also really important not to store the JWT on the client persistently. Doing so you make your app vulnerable to CSRF & XSS attacks, by malicious forms or scripts to use or steal your token lying around in cookies or localStorage.

### 1.3. JWT structure?

- A JWT is not encrypted. It is based64 encoded and signed. So anyone can decode the token and use its data. A JWT's signature is used to verify that it is in fact from a legitimate source.
- A JWT looks something like this, when it's serialized:

```unknown
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2o
```

- If you decode that base64, you'll get JSON in 3 important parts: header, payload and signature.

```
<header>.<payload>.<signature>
```

#### 1.3.1. Header

```json
{
 "alg": "HS256", # The signing algorithm being used (HMAC SHA256/RSA)
 "typ": "JWT" # The type of token
}
```

JSON --> Base64Url encoded --> `<header>`

#### 1.3.2. Payload

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

#### 1.3.3. Signature

```
<alg>(base64UrlEncode(<header> + "." + <payload>), <secret>)
```

The signature is used to verify the message wasn't changed along the way and in the case of tokens signed with a private key, it can also verify that the sender of the JWT is who it says it is.

## 2. How it works?

![](https://miro.medium.com/max/1480/1*tW-8Y2edq04b4__zF0Jm9Q.png)

Image source [here](https://medium.com/@siddharthac6/json-web-token-jwt-the-right-way-of-implementing-with-node-js-65b8915d550e)

Whenever the user wants to access a protected route or resource, the user agent should send the JWT, typically in the **Authorization** header using the **Bearer** schema.

```
Authorization: Bearer <token>
```

- Here is the diagram of how a JWT is issued (`/login`) and then used to make an API call to another service (`/api`) in a nutshell:

![](https://hasura.io/blog/content/images/2019/08/Screen-Shot-2019-08-29-at-12.54.53.png)

- Ugh! This seems complicated. Why shouldn’t I stick to good old session tokens?
  - Painful discussions on the internet, but Backend developers like using JWTs because a) microservices b) not needing a centralized token database.
  - In a microservices setup, each microservice can independently verify that a token received from a client is valid. The microservice can further decode the token and extract relevant information without needing to have access to a centralized token database.

![](https://hasura.io/blog/content/images/2019/08/Screen-Shot-2019-08-29-at-12.54.53.png)

### 2.1. Basic login

![](https://hasura.io/blog/content/images/2022/01/jwt-blogpost-1-login.png)

- The login process:
  - A login form that submits a username/password to an auth endpoint and grabs the JWT token from the response. This could be login with an external provider, an OAuth or OAuth2 step.
  - It really doesn't matter, as long as the client finally gets a JWT token in the response of the final login success step.
  - Where do we store this token? We need to save JWT Token somewhere, so that we can forward it to API as a header.
    - _Do not persist in localstorage, or do not create cookies on the client._
    - The [OWASP JWT Cheatsheet](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.md) and [OWASP ASVS (Application Security Verification Standard)](https://github.com/OWASP/ASVS) prescribe guidelines for handling and storing tokens.
      - Store the token using the browser `sessionStorage` container.
      - Add it as a Bearer HTTP `Authentication` header with JavaScript when calling services.
      - Add `fingerprint` information to the token.
- Now that we have the token what can we do with it?
  - Using in API client to pass it as a header to every API call
  - Check if a user is logged in by seeing if the JWT variable is set
  - Optionally, we can even decode the JWT on the client to access data in the payload. Let's say we need the user-id or the username on the client, which we can extract from the JWT.

### 2.2. Basic logout

- With JWTs, a "logout" is simply deleting the token on the client side so that it can't be used for subsequent API calls.

![](https://hasura.io/blog/content/images/2022/01/jwt-blogpost-2-check-token-flow.png)

- The token is still valid and can be used. What if I need to ensure that the token cannot be used ever again?

  - This is why keeping JWT expiry values to a small value is important. And this is why ensuring that your JWTs don't get stolen is even more important. The token is valid (even after you delete it on the client), but only for short period to reduce the probability of it being used maliciously.
  - In addition, you can add a deny-listing workflow to your JWTs. In this case, you can have a `/logout` API call and your auth server puts the tokens in a "invalid list". However, all the API services that consume the JWT now need to add an additional step to their JWT verification to check with the centralized "deny-list". This introduces central state again, and brings us back to what we had before using JWTs at all.

  ![](https://hasura.io/blog/content/images/2022/01/jwt-blogpost-3-check-token-flow-serverside.png)

### 2.3. Silent refresh

- There are 2 major problems that users of our JWT based app will still face:
  - Given our short expiry times on the JWTs, the user will be logged out every 15 minutes. This would be a fairly terrible experience. Ideally, we'd probably want our user to be logged in for a long time.
  - If a user closes their app and opens it again, they'll need to login again. Their session is not persisted because we're not saving the JWT token on the client anywhere.
- To solve this problem, most JWT providers, provide a refresh token. A refresh token has 2 properties:
  - It can be used to make an API call (say, `/refresh_token`) to fetch a new JWT token before the previous JWT expires.
  - It can be safely persisted across sessions on the client!
- How does a refersh token work?
  - This token is issued as part of authentication process along with the JWT. The auth server should saves this refresh token and associates it to a particular user in its own database, so that it can handle the renewing JWT logic.
  - On the client, before the previous JWT token expires, we wire up our app to make a `/refresh_token` endpoint and grab a new JWT.
- How is a refresh token safely persisted on the client?
  - Same as the first JWT Token (`access_token`).
    - Store the token using the browser `sessionStorage` container.
    - Add it as a Bearer HTTP `Authentication` header with JavaScript when calling services.
    - Add `fingerprint` information to the token.
- What does the new "login" process look like?

![](https://hasura.io/blog/content/images/2022/01/jwt-blogpost-4-login-refresh-flow.png)

- What does the silent refresh look like?

![](https://hasura.io/blog/content/images/2022/01/jwt-blogpost-5-silent-refresh.png)

## 3. Implementation in `<put-a-programming-language-here>`

> <WIP>
