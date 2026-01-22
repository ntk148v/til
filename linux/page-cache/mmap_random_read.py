import mmap
import os
from random import randint
from time import sleep

with open("/var/tmp/file1.db", "r") as f:
    fd = f.fileno()
    size = os.stat(fd).st_size
    with mmap.mmap(fd, 0, prot=mmap.PROT_READ) as mm:
        try:
            while True:
                pos = randint(0, size - 4)
                print(mm[pos : pos + 4])
                sleep(0.05)
        except KeyboardInterrupt:
            pass
