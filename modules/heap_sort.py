from modules.max_heap import heapify


def heap_sort(arr, n):
    for i in range(int(n / 2) - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr
