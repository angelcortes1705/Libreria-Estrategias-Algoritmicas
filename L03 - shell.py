from typing import TypeVar, Callable
from math import ceil, log

T = TypeVar("T")


def shell_sort(
    A: list[T], key: Callable = lambda x: x, reverse: bool = False
) -> list[T]:
    """
    Sorts (in place) list A using the shell sort algorithm.

    Parameters
    ----------
    A: list[T]
        List of comparable elements.
    key: Callable
        Function used to compare elements in A. Defaults to comparing the elements themselves.
    reverse: bool
        Whether to sort in decreasing order or not. Defaults to False.
    """
    n = len(A)
    gap = n // 2  # Salto de n/2

    while gap > 0:
        for i in range(gap, n):
            temp = A[i]
            j = i

            # Determinar la comparación según reverse
            while j >= gap and (key(A[j - gap]) > key(temp) if not reverse else key(A[j - gap]) < key(temp)):
                A[j] = A[j - gap]
                j -= gap

            A[j] = temp

        gap //= 2  # Reducir el salto


if __name__ == "__main__":

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    shell_sort(A)
    print(A)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    shell_sort(A, reverse=True)
    print(A)
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    shell_sort(B)
    print(B)
    # [(0, 2), (1, 6), (2, 0), (3, 8), (4, 7), (5, 5), (6, 4), (7, 9), (8, 1), (9, 3)]
    shell_sort(B, key=lambda x: x[1])
    print(B)
    # [(2, 0), (8, 1), (0, 2), (9, 3), (6, 4), (5, 5), (1, 6), (4, 7), (3, 8), (7, 9)]
