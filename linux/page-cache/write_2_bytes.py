with open("/var/tmp/file1.db", "br+") as f:
    print(f.write(b"ab"))
