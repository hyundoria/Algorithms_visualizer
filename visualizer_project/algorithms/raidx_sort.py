def radix_sort(arr, stats):
    n = len(arr)
    if n == 0:
        yield None
        return

    max1 = max(arr)
    exp = 1

    while max1 // exp > 0:
        yield from counting_sort_for_radix(arr, exp, stats)
        exp *= 10

    yield None


def counting_sort_for_radix(arr, exp, stats):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp)
        count[index % 10] += 1
        stats['comp'] += 1
        yield arr, [i]

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (arr[i] // exp)
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        yield arr, [i]  # 역순 탐색 시각화

    for i in range(n):
        arr[i] = output[i]
        stats['swap'] += 1
        yield arr, [i]  # 결과 복사 시각화
