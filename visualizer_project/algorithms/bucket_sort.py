def bucket_sort(arr, stats):
    n = len(arr)
    if n == 0:
        yield None
        return

    num_buckets = 10
    buckets = [[] for _ in range(num_buckets)]
    max_val = max(arr)

    # 1. 분산 (Scatter)
    for i in range(n):
        if max_val == 0:
            idx = 0
        else:
            idx = int(arr[i] * num_buckets / (max_val + 1))

        buckets[idx].append(arr[i])
        stats['comp'] += 1
        yield arr, [i]

    # 2. 정렬 및 병합 (Sort & Gather)
    k = 0
    for i in range(num_buckets):
        buckets[i].sort()
        for val in buckets[i]:
            arr[k] = val
            stats['swap'] += 1
            yield arr, [k]
            k += 1

    yield None
