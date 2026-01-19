import mmap

with open("/var/tmp/file1.db", "r") as f:
    with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
        mm.madvise(mmap.MADV_RANDOM)
        print(mm[:2])
