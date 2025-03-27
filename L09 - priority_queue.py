from heapsort import *


class PriorityQueue(Heap):

    def __init__(self, A, queueType, key):
        super().__init__(A=A, heapType=queueType, key=key)

    def extremum(self):
        # Devuelve el elemento en la cima del heap
        return self._heap[1] if self.heap_size >= 1 else None

    def extract_extremum(self):
        # Extrae y devuelve el elemento extremo (mínimo o máximo)
        if self.heap_size < 1:
            return None
        extreme = self._heap[1]
        self._heap[1], self._heap[self.heap_size] = self._heap[self.heap_size], self._heap[1]
        self.heap_size -= 1
        self.heapify(1)
        return extreme

    def upsert(self, e):
        # Inserta un nuevo elemento o actualiza uno existente
        for i in range(1, self.heap_size + 1):
            if self._heap[i][0] == e[0]:
                self._heap[i] = e
                self.build_heap()
                return
        self._heap.append(e)
        self.heap_size += 1
        i = self.heap_size
        while i > 1 and not self._compare_eq(self._heap[parent(i)], self._heap[i]):
            self._heap[i], self._heap[parent(i)] = self._heap[parent(i)], self._heap[i]
            i = parent(i)


if __name__ == "__main__":
    A = [
        ("a", 4),
        ("b", 1),
        ("1", 3),
        ("Z", 2),
        ("@", 16),
        ("d", 9),
        ("A", 10),
        ("BB", 14),
        ("X", 8),
        ("-", 7),
    ]
    pq = PriorityQueue(A=A, queueType=HeapType.MAX, key=lambda x: x[1])
    print(pq.heap_size)
    # 10
    print(pq)
    # [('@', 16), ('BB', 14), ('A', 10), ('X', 8), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('a', 4), ('b', 1)]
    print(pq.extremum())
    # ('@', 16)
    e = pq.extract_extremum()
    print(e)
    # ('@', 16)
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('b', 1)]
    pq.upsert(("@", 5))
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('b', 1), ('@', 5)]
    pq.upsert(("@", 12))
    print(pq)
    # [('BB', 14), ('@', 12), ('A', 10), ('a', 4), ('X', 8), ('d', 9), ('1', 3), ('Z', 2), ('b', 1), ('-', 7)]
