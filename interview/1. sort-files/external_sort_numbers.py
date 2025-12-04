# filename: external_sort_numbers.py
import heapq
import os
import tempfile

# Cấu hình chunk theo số dòng để kiểm soát RAM.
# Với số tự nhiên dạng text, 1_000_000 dòng/chunk thường ~100–200MB tùy độ dài.
CHUNK_LINES = 1_000_000

def parse_int_line(line: str):
    # Loại bỏ khoảng trắng và newline; bỏ qua dòng trống
    s = line.strip()
    if not s:
        return None
    # Chỉ chấp nhận số tự nhiên (>=0)
    # Nếu muốn hỗ trợ âm, thay đổi logic tại đây.
    return int(s)

def write_run(run_path: str, numbers):
    # Ghi mỗi số thành một dòng
    with open(run_path, "w", encoding="utf-8") as f:
        for n in numbers:
            f.write(f"{n}\n")

def sort_file_into_runs(input_paths, tmpdir=None, chunk_lines=CHUNK_LINES):
    if tmpdir is None:
        tmpdir = tempfile.gettempdir()
    run_files = []

    for path in input_paths:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            while True:
                buf = []
                for _ in range(chunk_lines):
                    line = f.readline()
                    if not line:
                        break
                    val = parse_int_line(line)
                    if val is not None:
                        buf.append(val)
                if not buf:
                    break
                # Sort numeric trong RAM
                buf.sort()
                # Tạo run file tạm
                run_fd, run_path = tempfile.mkstemp(prefix="run_", dir=tmpdir, text=True)
                os.close(run_fd)
                write_run(run_path, buf)
                run_files.append(run_path)

    return run_files

def k_way_merge(run_files, output_path):
    # Mở tất cả run files
    fps = [open(p, "r", encoding="utf-8") for p in run_files]
    heap = []

    # Đọc số đầu từng run và đẩy vào heap
    for i, fp in enumerate(fps):
        line = fp.readline()
        if line:
            val = parse_int_line(line)
            if val is not None:
                heap.append((val, i))
    heapq.heapify(heap)

    with open(output_path, "w", encoding="utf-8") as out:
        while heap:
            val, i = heapq.heappop(heap)
            out.write(f"{val}\n")
            nxt = fps[i].readline()
            if nxt:
                nval = parse_int_line(nxt)
                if nval is not None:
                    heapq.heappush(heap, (nval, i))

    # Đóng và xóa run files
    for fp in fps:
        fp.close()
    for p in run_files:
        try:
            os.remove(p)
        except OSError:
            pass

def external_sort_two_files(file_a, file_b, output_file, tmpdir=None, chunk_lines=CHUNK_LINES):
    # Bước 1: Tạo các run files đã sort từ A và B
    runs = sort_file_into_runs([file_a, file_b], tmpdir=tmpdir, chunk_lines=chunk_lines)
    # Bước 2: K-way merge thành một file duy nhất
    k_way_merge(runs, output_file)

if __name__ == "__main__":
    # Ví dụ sử dụng:
    # python external_sort_numbers.py A B AB.sorted
    import sys
    if len(sys.argv) < 4:
        print("Usage: python external_sort_numbers.py <file_a> <file_b> <output_file> [tmpdir] [chunk_lines]")
        sys.exit(1)
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    output_file = sys.argv[3]
    tmpdir = sys.argv[4] if len(sys.argv) >= 5 else None
    chunk_lines = int(sys.argv[5]) if len(sys.argv) >= 6 else CHUNK_LINES

    external_sort_two_files(file_a, file_b, output_file, tmpdir=tmpdir, chunk_lines=chunk_lines)
    print(f"Sorted merged output written to: {output_file}")
