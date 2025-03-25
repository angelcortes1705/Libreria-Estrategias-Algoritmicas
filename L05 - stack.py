class Stack:
    def __init__(self, s=None) -> None:
        self._stack = s

    def __repr__(self) -> str:
        return str(self._stack)

    def top(self):
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self._stack[-1]

    def pop(self):
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self._stack.pop()

    def push(self, e) -> None:
        self._stack.append(e)

    def is_empty(self) -> bool:
        #True vacia - False contrario
        return len(self._stack) == 0

    def clear(self) -> None:
        self._stack.clear()


if __name__ == "__main__":

    S = Stack([3, 2, 5, 1, 9, 0, 8, 6, 7, 4])
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    print(S.top())
    # 4
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    e = S.pop()
    print(e)
    # 4
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7]
    S.push(-1)
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, -1]
    print(S.is_empty())
    # False
    S.clear()
    print(S.is_empty())
    # True