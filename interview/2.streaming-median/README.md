# Streaming Median (Two-Heaps)

A scalable data structure to maintain the median of a stream of integers with:

- `add(x)`: O(log n)
- `median()`: O(1)
- Handles up to ~10 million inserts
- Memory: O(n)

## Table of Contents

- [Streaming Median (Two-Heaps)](#streaming-median-two-heaps)
  - [Table of Contents](#table-of-contents)
  - [Concept](#concept)
    - [Invariants](#invariants)
    - [Median Logic](#median-logic)
    - [Insert Algorithm (`add(x)`)](#insert-algorithm-addx)
  - [Operations](#operations)
  - [Complexity](#complexity)
  - [Thread Safety](#thread-safety)
  - [Python Implementation](#python-implementation)
  - [Go Implementation](#go-implementation)
  - [Notes for Large Streams](#notes-for-large-streams)
  - [Assumptions](#assumptions)

## Concept

Use two heaps:

- `low`: max-heap for the lower half of numbers
- `high`: min-heap for the upper half

### Invariants

- Size balance: `len(low) == len(high)` or `len(low) == len(high) + 1`
- Order property: `max(low) ≤ min(high)`

### Median Logic

- If sizes equal: `median = (top(low) + top(high)) / 2`
- Else: `median = top(low)`

### Insert Algorithm (`add(x)`)

1. If `low` is empty or `x ≤ top(low)`, push to `low`; otherwise push to `high`.
2. Rebalance:
   - If `len(low) > len(high) + 1`: move `top(low)` → `high`
   - If `len(high) > len(low)`: move `top(high)` → `low`

## Operations

- `add(x)`: O(log n) due to heap push/pop
- `median()`: O(1) by reading heap tops

## Complexity

- Time: `add(x)` O(log n), `median()` O(1)
- Space: O(n), store all elements across both heaps

## Thread Safety

- Recommended: single RW lock protecting both heaps
  - `add(x)`: acquire write lock (exclusive)
  - `median()`: acquire read lock (shared)
- Avoid partial locking—both heaps must be mutated atomically.
- For even-size average, use widened arithmetic (e.g., float64) to avoid integer overflow.

## Python Implementation

```python
# median_stream.py
import heapq
import threading
from typing import Optional, Union

Number = Union[int, float]

class MedianStream:
    def __init__(self) -> None:
        self.low = []   # max-heap via negatives
        self.high = []  # min-heap
        self._lock = threading.Lock()

    def add(self, x: Number) -> None:
        with self._lock:
            if not self.low:
                heapq.heappush(self.low, -float(x))
            else:
                low_top = -self.low[0]
                if x <= low_top:
                    heapq.heappush(self.low, -float(x))
                else:
                    heapq.heappush(self.high, float(x))

            # Rebalance
            if len(self.low) > len(self.high) + 1:
                moved = -heapq.heappop(self.low)
                heapq.heappush(self.high, moved)
            elif len(self.high) > len(self.low):
                moved = heapq.heappop(self.high)
                heapq.heappush(self.low, -moved)

    def median(self) -> Optional[float]:
        with self._lock:
            total = len(self.low) + len(self.high)
            if total == 0:
                return None

            if len(self.low) > len(self.high):
                return -self.low[0]
            else:
                low_top = -self.low[0]
                high_top = self.high[0]
                return (low_top + high_top) / 2.0

if __name__ == "__main__":
    ms = MedianStream()
    data = [5, 15, 1, 3]
    expected = [5.0, 10.0, 5.0, 4.0]
    out = []
    for x in data:
        ms.add(x)
        out.append(ms.median())
    print("Data:", data)
    print("Medians:", out)
    print("Expected:", expected)
    assert out == expected

    ms2 = MedianStream()
    for x in range(1, 11):
        ms2.add(x)
    assert ms2.median() == 5.5

    ms3 = MedianStream()
    for x in range(10, 0, -1):
        ms3.add(x)
    assert ms3.median() == 5.5

    ms4 = MedianStream()
    for v in [2, 2, 2, 2, 2]:
        ms4.add(v)
    assert ms4.median() == 2.0

    print("All tests passed.")
```

## Go Implementation

```go
// median_stream.go
package main

import (
	"container/heap"
	"fmt"
	"math"
	"sync"
)

type FloatMinHeap []float64
func (h FloatMinHeap) Len() int           { return len(h) }
func (h FloatMinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h FloatMinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *FloatMinHeap) Push(x interface{}) { *h = append(*h, x.(float64)) }
func (h *FloatMinHeap) Pop() interface{} {
	old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x
}
func (h FloatMinHeap) Peek() float64 { return h[0] }

type FloatMaxHeap []float64
func (h FloatMaxHeap) Len() int           { return len(h) }
func (h FloatMaxHeap) Less(i, j int) bool { return h[i] > h[j] } // max-heap
func (h FloatMaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *FloatMaxHeap) Push(x interface{}) { *h = append(*h, x.(float64)) }
func (h *FloatMaxHeap) Pop() interface{} {
	old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x
}
func (h FloatMaxHeap) Peek() float64 { return h[0] }

type MedianStream struct {
	low  FloatMaxHeap
	high FloatMinHeap
	mu   sync.RWMutex
}

func NewMedianStream() *MedianStream {
	ms := &MedianStream{low: make(FloatMaxHeap, 0), high: make(FloatMinHeap, 0)}
	heap.Init(&ms.low); heap.Init(&ms.high)
	return ms
}

func (ms *MedianStream) Add(x float64) {
	ms.mu.Lock()
	defer ms.mu.Unlock()

	if ms.low.Len() == 0 {
		heap.Push(&ms.low, x)
	} else if x <= ms.low.Peek() {
		heap.Push(&ms.low, x)
	} else {
		heap.Push(&ms.high, x)
	}

	if ms.low.Len() > ms.high.Len()+1 {
		moved := heap.Pop(&ms.low).(float64)
		heap.Push(&ms.high, moved)
	} else if ms.high.Len() > ms.low.Len() {
		moved := heap.Pop(&ms.high).(float64)
		heap.Push(&ms.low, moved)
	}
}

func (ms *MedianStream) Median() (float64, bool) {
	ms.mu.RLock()
	defer ms.mu.RUnlock()

	total := ms.low.Len() + ms.high.Len()
	if total == 0 { return 0, false }

	if ms.low.Len() > ms.high.Len() {
		return ms.low.Peek(), true
	}
	lowTop := ms.low.Peek()
	highTop := ms.high.Peek()
	return (lowTop + highTop) / 2.0, true
}

func main() {
	ms := NewMedianStream()
	data := []float64{5, 15, 1, 3}
	expected := []float64{5, 10, 5, 4}
	out := make([]float64, 0, len(data))

	for _, x := range data {
		ms.Add(x)
		m, ok := ms.Median()
		if !ok { panic("median not available") }
		out = append(out, m)
	}
	fmt.Println("Data:    ", data)
	fmt.Println("Medians: ", out)
	fmt.Println("Expected:", expected)

	eq := func(a, b float64) bool { return math.Abs(a-b) < 1e-9 }
	for i := range out {
		if !eq(out[i], expected[i]) {
			panic(fmt.Sprintf("median mismatch at %d: got %v want %v", i, out[i], expected[i]))
		}
	}

	ms2 := NewMedianStream()
	for i := 1.0; i <= 10.0; i++ { ms2.Add(i) }
	m2, _ := ms2.Median(); if !eq(m2, 5.5) { panic("median incorrect for 1..10") }

	ms3 := NewMedianStream()
	for i := 10.0; i >= 1.0; i-- { ms3.Add(i) }
	m3, _ := ms3.Median(); if !eq(m3, 5.5) { panic("median incorrect for 10..1") }

	ms4 := NewMedianStream()
	for i := 0; i < 5; i++ { ms4.Add(2.0) }
	m4, _ := ms4.Median(); if !eq(m4, 2.0) { panic("median incorrect for duplicates") }

	fmt.Println("All tests passed.")
}
```

## Notes for Large Streams

- Memory: ~160 MB for 10M `float64` total across two heaps (plus overhead). Use `int64` for integers.
- For exact rational median on even counts (no floating rounding), return the two middles and compute externally.

## Assumptions

- Inputs fit in 64-bit numeric types.
- Even-count median returns a floating average. Adjust if your API requires integer or rational results.
