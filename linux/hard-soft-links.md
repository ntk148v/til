# Hard links and soft links in Linux

Source:

- <https://www.redhat.com/en/blog/linking-linux-explained>
- <https://viblo.asia/p/hard-links-va-symbolic-links-tren-linux-07LKXJR2lV4>

## 1. Inode

On Linux, we can separate a file into 3 distinct sets of data:

- filename or filepath - **hard link**.
- metadata, such as when was the file created, last modified and accessed, which user owns the file, which user group is associated with the file, and what file permissions are set on the file—if it's an executable file, if it's read-only, etc. This is the **inode**.
- the actual data contained inside the file. For a plain text file encoded in ASCII, this data is the sequence of bytes that matches the characters in an ASCII table. For a PNG image, this data always starts with the bytes `89 50 4E 47 0D 0A 1A 0A`. So this data is always exactly what the program that saves the file outputs, and what a program that loads files expects. This data resists in one or more "blocks" in a disk.

![](https://www.virtualcuriosities.com/im/g4565)

```shell
ls -idl ipvs-lvs
19013717 drwxrwxr-x - kiennt 28 Feb  2024 ipvs-lvs
```

### 2. Hard links

- Every file on the Linux filesystem starts with a single hard link. The link is between the filename and the actual data stored on the filesystem. Creating an additional hard link to a file means a few different things.

```shell
ln (original file path) (new file path)
```

```shell
$ ls -il virtual-memory.md
19016335 .rw-rw-r-- 11k kiennt  5 Dec 17:17 virtual-memory.md

$ ln $PWD/virtual-memory.md /tmp/hard

$ cat /tmp/hard
# The same content as virtual-memory.md

$ ls -li virtual-memory.md /tmp/hard
19016335 .rw-rw-r-- 11k kiennt  5 Dec 17:17 /tmp/hard
19016335 .rw-rw-r-- 11k kiennt  5 Dec 17:17 virtual-memory.md
```

- When changes are made to one filename, the other reflects those changes. The permissions, link count, ownership, timestamps, and file content are the exact same. If the original file is deleted, the data still exists under the secondary hard link. The data is only removed from your drive when all links to the data have been removed. If you find two files with identical properties but are unsure if they are hard-linked, use the `ls -il` command to view the inode number. Files that are hard-linked together share the same inode number.
- If you delete/remove the source file, you can still access hard link file content.
- Hard limit: While useful, there are some limitations to what hard links can do. For starters, they can only be created for regular files (not directories or special files). Also, a hard link cannot span multiple filesystems. They only work when the new hard link exists on the same filesystem as the original.

![](https://images.viblo.asia/854df42c-5097-49cf-8c32-23fdd8be3484.png)

## 3. Soft links

- Commonly referred to as symbolic links, soft links link together non-regular and regular files. They can also span multiple filesystems. By definition, a soft link is not a standard file, but a special file that points to an existing file.

```shell
ln -s (file path you want to point to) (new file path)
```

```shell
$ ln -s $PWD/virtual-memory.md /tmp/soft
$ cat /tmp/soft

$ ls -li virtual-memory.md /tmp/soft
 5374107 lrwxrwxrwx   - kiennt 18 Dec 10:16 /tmp/soft -> /home/kiennt/Workspace/github.com/ntk148v/til/linux/virtual-memory.md
19016335 .rw-rw-r-- 11k kiennt  5 Dec 17:17 virtual-memory.md
```

- A symbolic link has its own inode, pointing to the original filepath.

![](https://images.viblo.asia/bf8c7003-1a2f-487d-89e9-a4c9f2ac608c.png)

- The biggest concern is data loss and data confusion. If the original file is deleted, the soft link is broken. This situation is referred to as a dangling soft link. If you were to create a new file with the same name as the original, your dangling soft link is no longer dangling at all. It points to the new file created, whether this was your intention or not, so be sure to keep this in mind.

## 4. Hard or soft?

There is no clear answer here. The best link is the type that fits your particular situation. While these concepts can be tricky to remember, the syntax is pretty straightforward, so that is a plus! To keep the two easily separated in your mind, I leave you with this:

- A hard link always points a filename to data on a storage device.
- A soft link always points a filename to another filename, which then points to information on a storage device.
