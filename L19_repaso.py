# 1a) Preprocesamiento en tiempo Θ(n + k)
def preprocess(L, k):
    count = [0] * (k + 1)
    for num in L:
        count[num] += 1
    prefix_sum = [0] * (k + 1)
    for i in range(1, k + 1):
        prefix_sum[i] = prefix_sum[i - 1] + count[i]
    return prefix_sum

# 1b) Consulta en tiempo O(1)
def query_range(prefix_sum, a, b):
    if a > b:
        return 0
    return prefix_sum[b] - (prefix_sum[a - 1] if a > 0 else 0)

# 2) Ordenar enteros en el rango [0, n^3 - 1] en O(n)
def sort_n_cubed(arr, n):
    exp = 1
    while exp <= n**3:
        counting_sort(arr, exp, n)
        exp *= n

def counting_sort(arr, exp, base):
    count = [0] * base
    output = [0] * len(arr)
    for num in arr:
        index = (num // exp) % base
        count[index] += 1
    for i in range(1, base):
        count[i] += count[i - 1]
    for num in reversed(arr):
        index = (num // exp) % base
        output[count[index] - 1] = num
        count[index] -= 1
    for i in range(len(arr)):
        arr[i] = output[i]

# 3a) Ordenar enteros con un total de n dígitos en O(n)
def radix_sort(arr):
    max_digits = max(len(str(num)) for num in arr)
    for d in range(max_digits):
        arr.sort(key=lambda x: (x // (10**d)) % 10)
    return arr

# 3b) Ordenar cadenas de texto lexicográficamente en O(n)
def radix_sort_strings(arr):
    max_length = max(len(s) for s in arr)
    for i in range(max_length - 1, -1, -1):
        arr.sort(key=lambda x: x[i] if i < len(x) else "")
    return arr

# 4) Quicksort mejorado con insertion sort
def hybrid_quicksort(arr, k):
    def quicksort(left, right):
        if right - left < k:
            return
        pivot = arr[right]
        i = left - 1
        for j in range(left, right):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        quicksort(left, i)
        quicksort(i + 2, right)
    
    quicksort(0, len(arr) - 1)
    insertion_sort(arr)

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# 5) Multiplicación de matrices con Strassen
def add_matrix(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

def sub_matrix(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

def strassen_matrix_multiply(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    M1 = strassen_matrix_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_matrix_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_matrix_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_matrix_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_matrix_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_matrix_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_matrix_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))
    
    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)
    
    return [C11[i] + C12[i] for i in range(mid)] + [C21[i] + C22[i] for i in range(mid)]

# 6) Máxima suma de elementos no adyacentes en O(n)
def max_non_adjacent_sum(arr):
    incl, excl = 0, 0
    for num in arr:
        new_excl = max(incl, excl)
        incl = excl + num
        excl = new_excl
    return max(incl, excl)

# 7) Implementación de un Treap
import random

class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(1, 100)
        self.left = None
        self.right = None

def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    return x

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y

def treap_insert(root, key):
    if root is None:
        return TreapNode(key)
    if key < root.key:
        root.left = treap_insert(root.left, key)
        if root.left.priority > root.priority:
            root = rotate_right(root)
    else:
        root.right = treap_insert(root.right, key)
        if root.right.priority > root.priority:
            root = rotate_left(root)
    return root

def treap_delete(root, key):
    if root is None:
        return root
    if key < root.key:
        root.left = treap_delete(root.left, key)
    elif key > root.key:
        root.right = treap_delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        if root.left.priority > root.right.priority:
            root = rotate_right(root)
            root.right = treap_delete(root.right, key)
        else:
            root = rotate_left(root)
            root.left = treap_delete(root.left, key)
    return root
