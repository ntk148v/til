import heapq
import threading
from typing import Optional, Union

Number = Union[int, float]


class MedianStream:
    """
    Thread-safe two-heap median structure using a single mutex.
    low:  max-heap via negative values
    high: min-heap
    """

    def __init__(self) -> None:
        self.low = []    # max-heap (store negatives)
        self.high = []   # min-heap
        self._lock = threading.Lock()

    def add(self, x: Number) -> None:
        """Insert x in O(log n)."""
        xf = float(x)
        with self._lock:
            if not self.low:
                heapq.heappush(self.low, -xf)
            else:
                low_top = -self.low[0]
                if xf <= low_top:
                    heapq.heappush(self.low, -xf)
                else:
                    heapq.heappush(self.high, xf)

            # rebalance
            if len(self.low) > len(self.high) + 1:
                moved = -heapq.heappop(self.low)
                heapq.heappush(self.high, moved)
            elif len(self.high) > len(self.low):
                moved = heapq.heappop(self.high)
                heapq.heappush(self.low, -moved)

    def median(self) -> Optional[float]:
        """Return current median in O(1)."""
        with self._lock:
            total = len(self.low) + len(self.high)
            if total == 0:
                return None

            if len(self.low) > len(self.high):
                return -self.low[0]

            return (-self.low[0] + self.high[0]) / 2.0


if __name__ == "__main__":
    # Basic tests
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
