# Storing Passwords securely using pass (GPG2)

## Why Pass?

Why Pass? Why not other password manager like KeePass, LastPass...?

- It's simple and lightweight.
- It uses existing tools like GnuPG, tree and Git.
- I can play with it through terminal. It looks cool :relieved: :relieved:

## Introduce

From [official website](https://www.passwordstore.org/):

```
Password management should be simple and follow Unix philosophy. With pass, each password lives inside of a gpg encrypted file whose filename is the title of the website or resource that requires the password. These encrypted files may be organized into meaningful folder hierarchies, copied from computer to computer, and, in general, manipulated using standard command line file management utilities.
```

`pass` is a simple password manager for the command line. Pass is a shell script that makes use of existing tools like GnuPG, tree and Git.

## Installation

Nothing much to write here, install `pass` is quite simple. Just follow the official website, you can get it.

## Basic usage

> **NOTE**: To be able to use ass, set up GnuPG2 (Not GnuPG, please keep in mind)

For the first time, I've followed [Pass man page](https://git.zx2c4.com/password-store/about/) like this:

```
$ pass init "Kien-Nguyen Password Storage"
# Return Password store initialized... Ha! gotcha, easy
$ pass insert Gmail/my-fancy-email
# Return gpg: Kien-Nguyen Password Storage: skipped: No public key
# gpg: [stdin]: encryption failed: No public key
# Uh oh what happened?
```

Double check man page, figure out that I have to use gpg-id, but I haven't had one yet.

```
$ gpg2 --list-keys
# Nothing....
```

To remedy this, let's create a GPG(2) key. Pass uses GnuPG2, which does not share its keyring with GnuPG. So remember to use `gpg2` instead of `gpg`.

### Create GPG key

```
$ gpg2 --full-gen-key
# Follow the instruction
$ gpg2 --list-keys
/home/kiennt/.gnupg/pubring.kbx
-------------------------------
pub   rsa2048/C8DC0750 2018-09-03 [SC]
uid         [ unknown] Kien Nguyen Tuan <kiennt2609@gmail.com>
sub   rsa2048/E5F492AB 2018-09-03 [E]
```

Now I have one GPG key with the ID C8DC0750. Re-initializing pass

```
pass init C8DC0750
```

### Insert a Password into Pass

```
pass insert Working/secret-thing
```

### Generate a new random password

```
pass generate Working/secret-thing-2
```

### Retrieve a password

```
pass Working/secret-thing
```

### Remove a password

```
pass remove Working/secret-thing
```

### Central git server for Pass in combination with GnuPG

```
# Enable management for local changes through Git
$ pass git init
# Add the remote git repository as 'origin'
$ pass git remote add origin path-or-link-to-git-repository-that-i-wont-tell-you
# Push your local Pass history
$ pass git push -u --all
```

Now you can use standard Git commands, prefixed by `pass`. For example: `pass git push`, `pass git pull`. Pass will automatically create commits when you use it to modify your password store.`
