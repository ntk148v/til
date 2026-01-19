import mmap

with open("/var/tmp/file1.db", "r+b") as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        mm[:2] = b"ab"
