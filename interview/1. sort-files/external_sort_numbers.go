// filename: external_sort_numbers.go
package main

import (
	"bufio"
	"container/heap"
	"errors"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

const DefaultChunkLines = 1_000_000
const IOBufferSize = 1 << 20 // 1MB

type item struct {
	val int
	ri  int // run index
}
type minHeap []item

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i].val < h[j].val }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)        { *h = append(*h, x.(item)) }
func (h *minHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func parseIntLine(line string) (int, bool) {
	s := strings.TrimSpace(line)
	if s == "" {
		return 0, false
	}
	v, err := strconv.Atoi(s)
	if err != nil {
		return 0, false
	}
	if v < 0 {
		// nếu muốn chấp nhận số âm, bỏ điều kiện này
		return 0, false
	}
	return v, true
}

func writeRun(runPath string, nums []int) error {
	f, err := os.Create(runPath)
	if err != nil {
		return err
	}
	defer f.Close()
	w := bufio.NewWriterSize(f, IOBufferSize)
	for _, n := range nums {
		if _, err := w.WriteString(strconv.Itoa(n)); err != nil {
			return err
		}
		if err := w.WriteByte('\n'); err != nil {
			return err
		}
	}
	return w.Flush()
}

func createTempRun(tmpdir string) (string, *os.File, error) {
	// dùng os.CreateTemp để tên file tạm là duy nhất
	f, err := os.CreateTemp(tmpdir, "run_")
	if err != nil {
		return "", nil, err
	}
	return f.Name(), f, nil
}

func sortFilesIntoRuns(inputPaths []string, tmpdir string, chunkLines int) ([]string, error) {
	var runs []string

	for _, p := range inputPaths {
		f, err := os.Open(p)
		if err != nil {
			return nil, fmt.Errorf("open input %s: %w", p, err)
		}
		r := bufio.NewReaderSize(f, IOBufferSize)

		for {
			buf := make([]int, 0, chunkLines)
			for i := 0; i < chunkLines; i++ {
				line, err := r.ReadString('\n')
				if err != nil {
					// EOF hoặc lỗi: nếu còn nội dung trong line thì vẫn parse
					if len(line) == 0 {
						if errors.Is(err, os.ErrClosed) {
							return nil, fmt.Errorf("reader closed: %w", err)
						}
						// EOF thật sự: thoát vòng đọc chunk
						break
					}
				}
				// parse dòng (kể cả khi không có newline ở cuối file)
				if val, ok := parseIntLine(line); ok {
					buf = append(buf, val)
				}
				if err != nil {
					// EOF sau line cuối: thoát vòng đọc chunk
					break
				}
			}
			if len(buf) == 0 {
				// hết dữ liệu ở file này
				break
			}

			// sort numeric
			sort.Ints(buf)

			// tạo run file tạm và ghi
			runName, runFile, err := createTempRun(tmpdir)
			if err != nil {
				f.Close()
				return nil, err
			}
			runFile.Close() // chỉ cần tên, sẽ open lại với Create để ghi
			if err := writeRun(runName, buf); err != nil {
				f.Close()
				return nil, fmt.Errorf("write run %s: %w", runName, err)
			}
			runs = append(runs, runName)
		}
		f.Close()
	}

	return runs, nil
}

func kWayMerge(runFiles []string, outputPath string) error {
	type runState struct {
		file *os.File
		r    *bufio.Reader
	}
	states := make([]runState, len(runFiles))
	for i, p := range runFiles {
		f, err := os.Open(p)
		if err != nil {
			// cleanup mở trước đó
			for j := 0; j < i; j++ {
				_ = states[j].file.Close()
			}
			return fmt.Errorf("open run %s: %w", p, err)
		}
		states[i] = runState{file: f, r: bufio.NewReaderSize(f, IOBufferSize)}
	}

	out, err := os.Create(outputPath)
	if err != nil {
		for _, st := range states {
			_ = st.file.Close()
		}
		return fmt.Errorf("create output %s: %w", outputPath, err)
	}
	w := bufio.NewWriterSize(out, IOBufferSize)

	h := &minHeap{}
	heap.Init(h)

	// seed heap: đọc dòng đầu từ mỗi run
	for i := range states {
		line, err := states[i].r.ReadString('\n')
		if err != nil && len(line) == 0 {
			continue
		}
		if val, ok := parseIntLine(line); ok {
			heap.Push(h, item{val: val, ri: i})
		}
	}

	for h.Len() > 0 {
		it := heap.Pop(h).(item)
		if _, err := w.WriteString(strconv.Itoa(it.val)); err != nil {
			_ = w.Flush()
			_ = out.Close()
			for _, st := range states {
				_ = st.file.Close()
			}
			return fmt.Errorf("write output: %w", err)
		}
		if err := w.WriteByte('\n'); err != nil {
			_ = w.Flush()
			_ = out.Close()
			for _, st := range states {
				_ = st.file.Close()
			}
			return fmt.Errorf("write output newline: %w", err)
		}

		// lấy dòng kế tiếp từ cùng run
		line, err := states[it.ri].r.ReadString('\n')
		if err != nil && len(line) == 0 {
			// run này hết
		} else if val, ok := parseIntLine(line); ok {
			heap.Push(h, item{val: val, ri: it.ri})
		}
	}

	if err := w.Flush(); err != nil {
		_ = out.Close()
		for _, st := range states {
			_ = st.file.Close()
		}
		return fmt.Errorf("flush output: %w", err)
	}
	_ = out.Close()

	// đóng và xóa run files
	for i, st := range states {
		_ = st.file.Close()
		_ = os.Remove(runFiles[i])
	}
	return nil
}

func externalSortTwoFiles(fileA, fileB, outPath, tmpdir string, chunkLines int) error {
	runs, err := sortFilesIntoRuns([]string{fileA, fileB}, tmpdir, chunkLines)
	if err != nil {
		return err
	}
	return kWayMerge(runs, outPath)
}

func main() {
	// Flags cho tiện dụng
	var tmpdir string
	var chunkLines int
	flag.StringVar(&tmpdir, "tmpdir", os.TempDir(), "temporary directory for run files")
	flag.IntVar(&chunkLines, "chunk", DefaultChunkLines, "number of lines per chunk (controls RAM)")
	flag.Parse()

	if flag.NArg() < 3 {
		fmt.Println("Usage: external_sort_numbers <file_a> <file_b> <output_file> [-tmpdir /path] [-chunk N]")
		os.Exit(1)
	}
	fileA := flag.Arg(0)
	fileB := flag.Arg(1)
	outPath := flag.Arg(2)

	// đảm bảo tmpdir tồn tại
	if _, err := os.Stat(tmpdir); os.IsNotExist(err) {
		if err := os.MkdirAll(tmpdir, 0o755); err != nil {
			fmt.Fprintf(os.Stderr, "cannot create tmpdir %s: %v\n", tmpdir, err)
			os.Exit(1)
		}
	}
	absTmp, _ := filepath.Abs(tmpdir)
	fmt.Printf("Using tmpdir: %s, chunk lines: %d\n", absTmp, chunkLines)

	if err := externalSortTwoFiles(fileA, fileB, outPath, tmpdir, chunkLines); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Sorted merged output written to: %s\n", outPath)
}
