def shell_sort(arr, stats):

    n = len(arr)
    h = n // 2

    while h > 0:

        for i in range(h, n):

            temp = arr[i]
            j = i - h

            stats['comp'] += 1

            while j >= 0 and arr[j] > temp:

                yield arr, [j+h, j]
                arr[j + h] = arr[j]
                stats['swap'] += 1
                j -= h

            arr[j + h] = temp
            stats['swap'] += 1

        h //= 2



