# OAuth2 vs. OpenID Connect

Source: <https://www.linkedin.com/advice/0/how-do-you-choose-between-oauth2-openid>

## 1. OAuth2: the authorization framework

A framework that allows a third-party application (called a client) to access resources from a resource server (such as an API) on behalf of a user (called a resource owner). The user grants the client a limited access token, which the client can use to request resources from the resource server. The access token is issued by an authorization server, which verifies the identity and consent of the user.

OAuth2 defines 4 roles (resource owner, client, resource server, and authorization server) and 4 grant types (authorization code, implicit, resource owner password credentials, and client credentials) for different scenarios of authorization.

![](https://assets.digitalocean.com/articles/oauth/abstract_flow.png)

## 2. OpenID Connect: The identity layer

OpenID Connect is an extension of OAuth2 that adds an identity layer to the authorization framework. It allows a client to verify the identity of the user and obtain basic profile information. The user logs in to an identity provider (such as Google or Facebook) using OpenID Connect, and the identity provider returns an ID token to the client. The ID token is a JSON Web Token (JWT) that contains information about the user, such as their name, email, and picture. The client can also request an access token and a refresh token from the identity provider, which can be used to access other resources.

![](https://curity.io/images/resources/openidconnect/openID-connect-overview.svg)

## 3. The differences between OAuth2 and OpenID Connect

The main difference between OAuth2 and OpenID Connect is that OAuth2 is only concerned with authorization while OpenID Connect is also concerned with authentication. Authorization means granting access to resources, while authentication means verifying the identity of a user. OAuth2 does not provide a standard way to obtain user information, while OpenID Connect does. OAuth2 relies on access token, which are opaque strings that can only be validated by the resource server, while OpenID Connect relies on ID tokens, which are self-contained and can be validated by the client. OAuth2 is more flexible and can be used for various types of applications, while OpenID Connect is more specific and can be used for single sign-on and social login.

## 4. How to choose between OAuth2 and OpenID Connect

The choice between OAuth2 and OpenID Connect on your web application's need and goals. If you only need to access from a resource server on behalf of a user, and you do not care about the user's identity or profile, then OAuth2 might be enough for you. You can use one of the OAuth2 grant types that suits your application's architecture and security requirements. If you need to verify the user's identity and obtain basic profile information, then OpenID Connect might be a better option for you. You can use the OpenID Connect authorization code flow or implicit flow, which are based on OAuth2, but also return an ID token along with an access token.

## 5. Tips for using OAuth2 and OpenID Connect

If you decide to use OAuth2 or OpenID Connect for your web application, here are some tips to help you implement them securely and effectively. You should use HTTPS for all communication between the client, the authorization server, the resource server, and the identity provider, as well as PKCE (Proof Key for Code Exchange) to prevent authorization code interception attacks. Additionally, you should use state and nonce parameters to prevent CSRF (Cross-Site Request Forgery) and replay attacks. Furthermore, you should validate the access token and the ID token according to their respective specifications. It is also important to store the access token and the refresh token securely in the client, and use them appropriately. Moreover, you should respect the scope and expiration of the access token and the ID token. Lastly, it is recommended that you update your client and server libraries to the latest versions.
