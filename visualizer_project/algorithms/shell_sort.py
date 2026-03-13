def shellSort(arr):

    n = len(arr)
    h = n // 2
    while h > 0:
        for i in range(h, n):
            temp = arr[i]
            j = i - h
            while j >= 0 and arr[j] > temp:
                arr[j + h] = arr[j]
                j -= h
            arr[j + h] = temp
        h //= 2

    print(arr)

arr = [8,1,4,2,7,6,3,5]
shellSort(arr)

