def quick_sort(arr, state):

    yield from _quicksort(arr, 0,len(arr) - 1, state)

def partition(arr,low,high,stats):
    pivot = arr[high]
    i = low-1

    for j in range(low,high):

        stats['comp'] += 1
        if arr[j] < pivot:

            i = i+1
            stats['swap'] += 1
            yield arr, [i, j]
            arr[i],arr[j] = arr[j],arr[i]


    i = i+1
    arr[i],arr[high] = arr[high],arr[i]
    stats['swap'] += 1
    yield arr, [i, high]
    return i


def _quicksort(arr,low,high,state):

    if low < high:

        p = yield from partition(arr,low,high,state)

        yield from _quicksort(arr,low,p-1,state)

        yield from _quicksort(arr,p+1,high,state)

