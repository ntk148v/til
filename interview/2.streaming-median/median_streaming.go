package main

import (
	"container/heap"
	"fmt"
	"sync"
)

// Number is the type supported by the median stream.
type Number float64

// -------- Max-Heap (store as positive, but invert comparison) --------

type maxHeap []Number

func (h maxHeap) Len() int            { return len(h) }
func (h maxHeap) Less(i, j int) bool  { return h[i] > h[j] } // reverse for max-heap
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(Number)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	n := len(old)
	val := old[n-1]
	*h = old[:n-1]
	return val
}

func (h maxHeap) Top() Number {
	if len(h) == 0 {
		return 0
	}
	return h[0]
}

// -------- Min-Heap --------

type minHeap []Number

func (h minHeap) Len() int            { return len(h) }
func (h minHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) { *h = append(*h, x.(Number)) }
func (h *minHeap) Pop() interface{} {
	old := *h
	n := len(old)
	val := old[n-1]
	*h = old[:n-1]
	return val
}

func (h minHeap) Top() Number {
	if len(h) == 0 {
		return 0
	}
	return h[0]
}

// -------- MedianStream --------

type MedianStream struct {
	low  maxHeap // max-heap
	high minHeap // min-heap
	mu   sync.Mutex
}

func NewMedianStream() *MedianStream {
	return &MedianStream{
		low:  maxHeap{},
		high: minHeap{},
	}
}

func (ms *MedianStream) Add(x Number) {
	ms.mu.Lock()
	defer ms.mu.Unlock()

	if ms.low.Len() == 0 {
		heap.Push(&ms.low, x)
	} else {
		if x <= ms.low.Top() {
			heap.Push(&ms.low, x)
		} else {
			heap.Push(&ms.high, x)
		}
	}

	// rebalance (low has same size or one more element)
	if ms.low.Len() > ms.high.Len()+1 {
		moved := heap.Pop(&ms.low).(Number)
		heap.Push(&ms.high, moved)
	} else if ms.high.Len() > ms.low.Len() {
		moved := heap.Pop(&ms.high).(Number)
		heap.Push(&ms.low, moved)
	}
}

func (ms *MedianStream) Median() *float64 {
	ms.mu.Lock()
	defer ms.mu.Unlock()

	total := ms.low.Len() + ms.high.Len()
	if total == 0 {
		return nil
	}

	if ms.low.Len() > ms.high.Len() {
		val := float64(ms.low.Top())
		return &val
	}

	lowTop := float64(ms.low.Top())
	highTop := float64(ms.high.Top())
	median := (lowTop + highTop) / 2.0
	return &median
}

func main() {
	ms := NewMedianStream()
	data := []float64{5, 15, 1, 3}
	expected := []float64{5, 10, 5, 4}

	out := make([]float64, 0)
	for _, x := range data {
		ms.Add(Number(x))
		m := ms.Median()
		out = append(out, *m)
	}

	fmt.Println("Data:", data)
	fmt.Println("Medians:", out)
	fmt.Println("Expected:", expected)
}
