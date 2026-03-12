def heap_sort(arr, stats):
    yield from _heap_sort(arr, stats)
    yield None

def heapify(arr, n, i, stats):
    largest = i        # 루트
    left    = 2*i + 1  # 왼쪽 자식
    right   = 2*i + 2  # 오른쪽 자식

    if left < n:
        stats['comp'] += 1
        yield arr, [largest, left]
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        stats['comp'] += 1
        yield arr, [largest, right]
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        stats['swap'] += 1
        yield arr, [i, largest]
        yield from heapify(arr, n, largest, stats)  # 재귀적으로 힙 속성 유지
    else:
        yield arr, [i]


def _heap_sort(arr, stats):
    n = len(arr)


    # 1단계: 최대 힙(Max-Heap) 구성
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i, stats)

    # 2단계: 루트(최댓값)를 끝으로 이동 후 힙 재구성
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        stats['swap'] += 1
        yield arr, [0, i]
        yield from heapify(arr, i, 0, stats)

    yield None