# SSH Agent Hijacking

Source: <https://www.clockwork.com/insights/ssh-agent-hijacking/>

SSH without passwords makes life with Unix-like OS much easier. If your network requires chained ssh sessions (to access a restricted network, for example), agent forwarding becomes extremely helpful.

But, this can be dangerous, though.

## How Passwordless authentication works?

When authenticating in normal mode, SSH uses your password to prove that you are who you say you are. The server compares a hash of this password to one it has on file, verifies that the hashes match, and lets you in.

If an attacker is able to break the encryption used to protect your password while it’s being sent to the server, they can steal the it and log in as you whenever they desire. If an attacker is allowed to perform hundreds of thousands of attempts, they can eventually guess your password.

A much safer authentication methocd is public key authentication, a away of logging in without a password. Public key authentication requires a matched pair of public and private keys. The public key encrypts messages that can only be decrypted with the private key. The remote computer uses its copy of your public key to encrypt a secret message to you. You prove you are you by decrypting the message using your private key and sending the message back to the remote computer. Your private key remains safely on your local computer the entire time, safe from attack.

![](https://www.thesslstore.com/blog/wp-content/uploads/2021/04/how-ssh-authentication-works.png)

The private key is valuable and must be protected, so by default it is stored in an encrypted format. Unfortunately this means entering your encryption passphrase before using it. Many articles suggest using passphrase-less (unencrypted) private keys to avoid this inconvenience. That’s a bad idea, as anyone with access to your workstation (via physical access, theft, or hackery) now also has free access to any computers configured with your public key.

OpenSSH includes [ssh-agent](http://www.openbsd.org/cgi-bin/man.cgi?query=ssh-agent), a daemon that runs on your local workstation. It loads a decrypted copy of your private key into memory, so you only have to enter your passphrase once. It then provides a local socket that the ssh client can use to ask it to decrypt the encrypted message sent bak by the remote server. Your private key stays safely ensconced in the ssh-agent process memory while still allowing you to ssh around without typing in passwords.

![](https://miro.medium.com/v2/resize:fit:720/format:webp/0*ct-6WRS_HNlW4ITz.png)

## How ForwardAgent works

Many tasks require "chaining" ssh sessions. For example:

- I ssh from my workstation to the dev server.
- I need to perform an svn update then, using the "svn+ssh" protocol.
- Since it would be silly to leave an unecrypted copy of my super-secret private key on a shared server, I'm now stuck with password authentication.
- If I enabled "ForwardAgent" in the ssh config on my workstation, ssh uses its built-in tunneling capabilities to create another socket on the dev server that is tunneled back to the ssh-agent socket on my local workstation. This means that the ssh client on the dev server can now send "decrypt this secret message" requests directly back to the ssh-agent running on my workstation, authenticating itself to the svn server without ever having access to my private key.

## Why this can be dangarous?

**TL;DR**: Anyone with root privilege on the intermediate server can make free use of your ssh-agent to authenticate them to other servers.

> Checkout the original post for the demonstration.

## Protect yourself!

- Don't let your ssh-agent store your keys indefinitely.
- Don't enable agent forwarding when connecting to untrustworthy hosts.

```text
Host trustworthyhost
  ForwardAgent yes

Host *
  ForwardAgent no
```
