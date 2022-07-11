# The Protocols

Source: <https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols>

- Git can use 4 distinct protocols to transfer data: local, HTTP, secure shell (SSH) and Git.

## 1. Local protocol

- Remote repository is in another directory on the same host.
- This is often used if everyone on team has access to a shared filesystem such as an NFS mount, or in the less likely case that everyone logs in to the same computer.
- For example:

```bash
# Clone
$ git clone /srv/git/project.git
$ git clone file:///srv/git/project.git
# Add a local repository
$ git remote add local_proj /srv/git/project.git
```

- Pros:
  - Simple and use existing file permissions and network access.
- Cons:
  - generally more difficult to set up and reach from multiple locations than basic network access.
  - A local repository is fast only if you have fast access to the data. A repository on NFS is often slower than the repository over SSH on the same server, allowing Git to run off local disks on each system.
  - Does not protect the repository against accidental damage.

## 2. HTTP protocols

- Git can communicate over HTTP using 2 different modes:
  - Dumb HTTP:
    - Dumb protocol exptects the bare Git repository to be served like normal files from the web server.
    - To allow read access to repository over HTTP:

    ```bash
    $ cd /var/www/htdocs/
    $ git clone --bare /path/to/git_project gitproject.git
    $ cd gitproject.git
    $ mv hooks/post-update.sample hooks/post-update
    $ chmod a+x hooks/post-update
    ```

  - Smart HTTP:
    - Run over standard HTTPS ports and can use various HTTP authentication mechanisms.
- Pros:
  - The simplicity of having a single URL for all types of access and having the server prompt only when authentication is needed makes things very easy for the end user.
  - Secure.
  - HTTP and HTTPS are such commonly used protocls that corporate firewalls are often se up to allow traffic through their ports.
- Cons:
  - Git over HTTPS can be a little more tricky to set up compared to SSH on some servers
  - If you’re using HTTP for authenticated pushing, providing your credentials is sometimes more complicated than using keys over SSH.

## 3. SSH protocol

- SSH is an authenticated network protocol and, because it’s ubiquitous, it’s generally easy to set up and use.

```bash
# Clone
$ git clone ssh://[user@]server/project.git
# Shorter scp-like syntax
$ git clone [user@]server:project.git
```

- Pros:
  - Relatively easy to set up.
  - Secure/
  - Efficient, making the data as compact as possible before transfering it.
- Cons:
  - Doesn't support anonymous access to Git repository.

## 4. Git protocol

- A special daemon that comes packaged with Git; it listens on a dedicated port 9418 that provides a service similar to the SSH protocol, but with absolutely no authentication.
- In order for a repository to be served over the Git protocol, you must create a git-daemon-export-ok file — the daemon won’t serve a repository without that file in it — but, other than that, there is no security.
- Pros:
  - Often the fastest network transfer protocol available.
- Cons:
  - The lack of authentication.
