import mmap
import os
from time import sleep

print("pid:", os.getpid())

with open("/var/tmp/file1.db", "rb") as f:
    with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
        sleep(10000)
