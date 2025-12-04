# A sort question

> How to sort and merge two 700MB files on a server with only 1GB of RAM, where each line is a natural number, producing a single file in ascending order

## 1. Hướng dẫn (Tiếng Việt)

- Mục tiêu: Ghép hai file ~700MB, mỗi dòng là số tự nhiên, thành một file tăng dần.
- Ràng buộc: Server chỉ có 1GB RAM → dùng external sort (chia nhỏ, trộn trên đĩa).
- Cách 1 – GNU sort (khuyến nghị):
  - Numeric: `-n`; tăng tốc với LC_ALL=C; giới hạn RAM bằng `-S 300–500M`; thư mục tạm `-T`.
  - Sort từng file rồi trộn:

```shell
LC_ALL=C sort -n -S 400M -T /path/to/tmp -o A.sorted A
LC_ALL=C sort -n -S 400M -T /path/to/tmp -o B.sorted B
LC_ALL=C sort -n -S 400M -T /path/to/tmp -m -o AB.sorted A.sorted B.sorted
```

- Sort trực tiếp hai file:

```shell
LC_ALL=C sort -n -S 400M -T /path/to/tmp A B -o AB.sorted
```

- Cách 2 – Tự triển khai external merge:
  - Chia khối: đọc A, B theo từng khối vừa RAM (100–200MB), sort trong RAM, ghi “run files”.
  - K-way merge: dùng min-heap theo giá trị số, trộn các run thành `AB.sorted` theo luồng.

- Lưu ý: sạch dữ liệu (mỗi dòng một số, không khoảng trắng), cần vài GB trống ở `-T` (ưu tiên SSD), nếu OOM thì giảm `-S` xuống 300M.

Guide (English)

- Goal: Merge two ~700MB text files, one integer per line, into a single ascending-sorted file.
- Constraint: Only 1GB RAM → use external sorting (chunk-and-merge on disk).
- Method 1 – GNU sort (recommended):
  - Numeric: `-n`; speed up with LC_ALL=C; cap memory via `-S 300–500M`; temp dir `-T`.
  - Sort each then merge:LC_ALL=C sort -n -S 400M -T /path/to/tmp -o A.sorted A

```shell
LC_ALL=C sort -n -S 400M -T /path/to/tmp -o A.sorted A
LC_ALL=C sort -n -S 400M -T /path/to/tmp -o B.sorted B
LC_ALL=C sort -n -S 400M -T /path/to/tmp -m -o AB.sorted A.sorted B.sorted
```

- Sort both directly:

```shell
LC_ALL=C sort -n -S 400M -T /path/to/tmp A B -o AB.sorted
```

- Method 2 – Implement external merge:
  - Chunking: read A and B in RAM-sized chunks (100–200MB), sort in memory, write run files.
  - K-way merge: use a min-heap on numeric values, stream-merge runs into `AB.sorted`.

- Notes: ensure clean input (one integer per line, no whitespace), allocate several GB for `-T` (SSD preferred), lower `-S` to 300M if OOM.
