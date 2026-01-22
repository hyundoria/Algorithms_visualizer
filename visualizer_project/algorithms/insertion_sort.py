# stats: {'comp':0, 'swap: 0}

def insertion_sort(arr, stats):

    n = len(arr)

    # 1번째 인덱스부터 끝까지 시작 (0번은 이미 정렬된 것으로 간주)
    for i in range(1, n):
        j = i

        # j가 0보다 크고, 왼쪽(j-1) 값이 현재(j) 값보다 크다면 교환 (역순 탐색)
        while j > 0:

            # 1. 비교 시각화 (현재 비교 중인 두 막대 표시)
            stats['comp'] += 1
            yield arr, [j - 1, j]

            if arr[j - 1] > arr[j]:
                # 2. 교환 (Swap)
                arr[j - 1], arr[j] = arr[j], arr[j - 1]

                stats['swap'] += 1
                yield arr, [j - 1, j]  # 교환 후 상태 시각화

                j -= 1  # 한 칸 앞으로 이동해서 계속 비교
            else:
                # 왼쪽 값이 나보다 작거나 같으면, 내 자리를 찾은 것이므로 멈춤
                break

    yield None