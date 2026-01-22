# stats: {'comp':0, 'swap: 0}
def selection_sort(arr, stats):

    n = len(arr)

    for i in range(n):

        min_idx = i

        for j in range(i + 1, n):

            stats['comp'] += 1
            yield arr, [i, j, min_idx]

            if arr[j] < arr[min_idx]:
                min_idx = j
                yield arr, [i, j, min_idx]

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            stats['swap'] += 1
            yield arr, [i, min_idx]
        else:
            yield arr, [i, i]

    yield None