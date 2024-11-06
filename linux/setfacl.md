# setfacl command

Source:

- <https://linux.die.net/man/1/setfacl>
- <https://www.geeksforgeeks.org/linux-setfacl-command-with-example/>

In Linux distributions, the `setfacl` sets Access Control Lists (ACLs) of files and directories. On the command line, a sequence of commands is followed by a sequence of files (which in turn can be followed by another sequence of commands, ...).

ACL is a set of rules implemeneted on the files and directories. The permission given to the users and Groups is based on their roles on perform certain actions or to execute certain tasks.

## Advantages of `setfacl`

- It allows the administrator to define specific permission for users and groups on specific files and directories.
- It has more flexibility than general file permission as we can assign multiple permissions at the same time.
- It helps to maintain specific permission without affecting others.
- It enhances the security level so that only authorized persons can access sensitive files and directories.
- It can modify or change the permission without interrupting the ongoing activities.

## Example

- Install:

```shell
$ sudo apt install acl -y
```

- Create a sample file:

```shell
$ touch test.txt
```

- Get the current ACL of file:

```shell
$ getfacl test.txt
# file: test.txt
# owner: kiennt
# group: kiennt
user::rw-
group::rw-
other::r--
```

- Set file permission to users:

```shell
$ setfacl -m u:nobody:rw test.txt
$ getfacl test.txt
# file: test.txt
# owner: kiennt98
# group: kiennt98
user::rw-
user:nobody:rw-
group::rw-
mask::rw-
other::r--
```

- Deny all permission:

```shell
$ setfacl -x u:nobody test.txt
$ getfacl test.txt
# file: test.txt
# owner: kiennt98
# group: kiennt98
user::rw-
group::rw-
mask::rw-
other::r--
```
