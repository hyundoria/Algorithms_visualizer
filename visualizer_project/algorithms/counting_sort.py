def counting_sort(arr, stats):

    n = len(arr)
    if n == 0:
        yield None
        return

    k = max(arr)
    b = [0] * n
    cnt = [0] * (k+1)

    for i in range(n):
        cnt[arr[i]] += 1
        stats['comp'] += 1  # 데이터 접근 비용
        yield arr, [i]

    # 2. 누적 합 계산
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i-1]

    # 3. 임시 배열에 정렬 (Build Output)
    for i in range(n-1,-1,-1):
        val = arr[i]
        b[cnt[val]-1] = val
        cnt[arr[i]] -= 1
        yield arr, [i]  # 역순으로 훑는 과정 시각화

    # 4. 원본 배열에 복사 (Copy back)
    for i in range(n):
        arr[i] = b[i]
        stats['swap'] += 1  # 값 덮어쓰기 비용
        yield arr, [i]  # 정렬된 값이 들어가는 과정 시각화

    yield None