from enum import Enum
from typing import TypeVar, Callable

T = TypeVar("T")


def parent(i):
    return i >> 1


def left(i):
    return i << 1


def right(i):
    return (i << 1) + 1


class HeapType(Enum):
    MAX = 0
    MIN = 1


class Heap:
    def __init__(
        self,
        A: list[T],
        heapType: HeapType = HeapType.MAX,
        key: Callable = lambda x: x,
    ) -> None:
        self._heap = [None] + list(A)  # Make the array 1-indexed
        self._key = key
        self.heap_size = len(A)
        self.type = heapType
        self.build_heap()

    def __repr__(self):
        return str(self._heap[1 : self.heap_size + 1])

    def _compare_eq(self, a, b) -> bool:
        return (
            self._key(a) >= self._key(b)
            if self.type == HeapType.MAX
            else self._key(a) <= self._key(b)
        )

    def assert_heap_property(self) -> None:
        for i in range(2, self.heap_size + 1):
            assert self._compare_eq(
                self._heap[parent(i)], self._heap[i]
            ), f"{self._heap[parent(i)]}, {self._heap[i]}, {self.type}"

    def heapify(self, i) -> None:
        l = left(i)
        r = right(i)
        largest_or_smallest = i

        if l <= self.heap_size and not self._compare_eq(self._heap[largest_or_smallest], self._heap[l]):
            largest_or_smallest = l
        if r <= self.heap_size and not self._compare_eq(self._heap[largest_or_smallest], self._heap[r]):
            largest_or_smallest = r

        if largest_or_smallest != i:
            self._heap[i], self._heap[largest_or_smallest] = self._heap[largest_or_smallest], self._heap[i]
            self.heapify(largest_or_smallest)

    def build_heap(self) -> None:
        for i in range(self.heap_size // 2, 0, -1):
            self.heapify(i)

    def get_heap(self) -> list[T]:
        return self._heap[1:self.heap_size + 1]


def heapsort(A: list[T], key: Callable = lambda x: x, reverse: bool = False) -> list[T]:
    heap_type = HeapType.MIN if reverse else HeapType.MAX
    H = Heap(A, heap_type, key)
    sorted_array = []

    for _ in range(len(A)):
        H._heap[1], H._heap[H.heap_size] = H._heap[H.heap_size], H._heap[1]
        sorted_array.append(H._heap[H.heap_size])
        H.heap_size -= 1
        H.heapify(1)

    sorted_array.reverse()  # because we extract max/min and append to the end
    return sorted_array


if __name__ == "__main__":
    H = Heap([3, 2, 5, 1, 9, 0, 8, 6, 7, 4], HeapType.MIN)
    print(H)
    H = Heap([3, 2, 5, 1, 9, 0, 8, 6, 7, 4], HeapType.MAX)
    print(H)

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    C = heapsort(A)
    print(C)
    C = heapsort(A, reverse=True)
    print(C)
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    C = heapsort(B)
    print(C)
    C = heapsort(B, key=lambda x: x[1])
    print(C)
