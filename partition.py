# Implementation from: https://en.wikipedia.org/wiki/Quicksort
def straightforward(arr, lo, hi):
    pivot = arr[hi]

    i = lo - 1
    for j in range(lo, hi):
        # NOTE: I changed from `<=` to `<`
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


# Implementation from:
# Data Structures and Algorithms by M. Goodrich and others
def ds_book(arr, lo, hi):
    # Make sure to exclude the pivot from [i, j]
    pivot = arr[hi]
    i = lo
    j = hi - 1

    while i <= j:
        while i <= j and arr[i] < pivot:
            i += 1

        while i <= j and arr[j] > pivot:
            j -= 1

        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    # Put pivot into final place
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def lomuto(arr, lo, hi):
    pivot = arr[hi]

    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1

    arr[i], arr[hi] = arr[hi], arr[i]
    return i


# lo incl, hi incl
# Implementation from: https://en.wikipedia.org/wiki/Quicksort
def hoare_wiki(arr, lo, hi):
    # Make sure to exclude the pivot from [i, j]
    pivot = arr[lo]
    i = lo
    j = hi + 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            # NOTE: This line is my addition
            # Put pivot into final place
            arr[j], arr[lo] = arr[lo], arr[j]
            return j

        arr[i], arr[j] = arr[j], arr[i]


# Implementation based on original paper
def hoare(arr, lo, hi):
    L = (lo + hi) // 2  # "random pivot"
    pivot = arr[L]

    i = lo
    j = hi
    while True:
        while i < hi and arr[i] <= pivot:
            i += 1
        while j > lo and arr[j] >= pivot:
            j -= 1

        if i >= j:
            break

        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1

    if i < L:
        arr[i], arr[L] = arr[L], arr[i]
        i += 1
    elif L < j:
        arr[j], arr[L] = arr[L], arr[j]
        j -= 1

    return (j, i, pivot)


# Implementation based on original paper with median of medians
def hoare3(arr, lo, hi):
    """Partition arr in-place

    Returns:
        (j, i, pivot):

            arr[r] <= pivot for lo <= r <= j,
            arr[r] == pivot for j < r < i,
            arr[r] >= pivot for i <= r <= hi
    """
    x, y, z = arr[lo], arr[hi], arr[(lo + hi) // 2]
    pivot = x + y + z - min(x, y, z) - max(x, y, z)
    if pivot == x:
        L = lo
    elif pivot == y:
        L = hi
    else:
        L = (lo + hi) // 2

    i = lo
    j = hi
    while True:
        while i < hi and arr[i] <= pivot:
            i += 1
        while j > lo and arr[j] >= pivot:
            j -= 1

        if i >= j:
            break

        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1

    if i < L:
        arr[i], arr[L] = arr[L], arr[i]
        i += 1
    elif L < j:
        arr[j], arr[L] = arr[L], arr[j]
        j -= 1

    return (j, i, pivot)


def _validate_partition(part, pivot_idx, pivot):
    for i in range(pivot_idx):
        assert part[i] <= pivot

    for i in range(pivot_idx, len(part)):
        assert part[i] >= pivot


def _test():
    tests = [
        [5, 3, 2, 2, 2, 2, 6, 1],
        [2, 1, 2, 1, 2],
        [2, 1, 4, 1, 2],
        [5, 5, 5, 6, 4, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 8, 2],
    ]

    print("DS book")
    for test in tests:
        lst = test[:]
        pivot_idx = ds_book(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx, lst[pivot_idx])
        print(test, "->", lst)
        print(f"{pivot_idx=}, pivot_elt={test[-1]}")

    print()
    print("Straightforward")
    for test in tests:
        lst = test[:]
        pivot_idx = straightforward(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx, lst[pivot_idx])
        print(test, "->", lst)
        print(f"{pivot_idx=}, pivot_elt={test[-1]}")

    print()
    print("Hoare")
    for test in tests:
        lst = test[:]
        pivot_idx = hoare(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx[1], pivot_idx[-1])
        print(test, "->", lst)
        print(f"{pivot_idx=}")

    print()
    print("Hoare3")
    for test in tests:
        lst = test[:]
        pivot_idx = hoare3(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx[1], pivot_idx[-1])
        print(test, "->", lst)
        print(f"{pivot_idx=}")

    print()
    print("Hoare wiki")
    for test in tests:
        lst = test[:]
        pivot_idx = hoare_wiki(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx, lst[pivot_idx])
        print(test, "->", lst)
        print(f"{pivot_idx=}")


    print()
    print("Lomuto")
    for test in tests:
        lst = test[:]
        pivot_idx = lomuto(lst, 0, len(lst)-1)
        _validate_partition(lst, pivot_idx, lst[pivot_idx])
        print(test, "->", lst)
        print(f"{pivot_idx=}, pivot_elt={test[-1]}")


if __name__ == "__main__":
    _test()
