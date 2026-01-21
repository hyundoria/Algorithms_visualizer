# stats: {'comp':0, 'swap: 0}
def bubble_sort(arr, stats):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            # 비교 시각화
            yield arr, [j, j + 1]

            stats['comp'] += 1  # 비교 횟수 증가

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                stats['swap'] += 1  # 교환 횟수 증가
                # 교환 시각화
                yield arr, [j, j + 1]

    yield None