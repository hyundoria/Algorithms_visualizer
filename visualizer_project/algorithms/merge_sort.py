def merge_sort(arr, stats):
    """
    외부에서 호출하는 진입점 함수 (Wrapper)
    """
    # 실제 재귀 함수 호출 (0 ~ len-1)
    yield from _merge_sort_recursive(arr, 0, len(arr) - 1, stats)
    yield None


def _merge_sort_recursive(arr, left, right, stats):
    if left < right:
        mid = (left + right) // 2

        # 1. 왼쪽 분할 (재귀 호출의 yield를 상위로 전달하기 위해 yield from 사용)
        yield from _merge_sort_recursive(arr, left, mid, stats)

        # 2. 오른쪽 분할
        yield from _merge_sort_recursive(arr, mid + 1, right, stats)

        # 3. 병합 (Merge)
        yield from merge(arr, left, mid, right, stats)


def merge(arr, left, mid, right, stats):
    temp = []
    i = left
    j = mid + 1

    #비교 및 임시 저장
    while i <= mid and j <= right:
        # 시각화: 현재 비교 중인 두 요소 표시
        stats['comp'] += 1
        yield arr, [i, j]

        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1

    # 남은 요소들 털어넣기
    while i <= mid:
        temp.append(arr[i])
        i += 1
    while j <= right:
        temp.append(arr[j])
        j += 1

    # 복사
    # 정렬된 temp 배열을 원본 arr에 덮어쓰기
    for t_idx, val in enumerate(temp):
        arr_idx = left + t_idx
        arr[arr_idx] = val

        stats['swap'] += 1

        yield arr, [arr_idx]