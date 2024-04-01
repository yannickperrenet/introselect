import math
import sys

import partition


def hoare(arr, lo, hi, k):
    if lo < hi:
        i, j, _ = partition.hoare(arr, lo, hi)

        if k <= i:
            hoare(arr, lo, i, k)
        elif k >= j:
            hoare(arr, j, hi, k)


def hoare3(arr, lo, hi, k):
    if lo < hi:
        i, j, _ = partition.hoare3(arr, lo, hi)

        if k <= i:
            hoare3(arr, lo, i, k)
        elif k >= j:
            hoare3(arr, j, hi, k)


def introselect(arr, lo, hi, k):
    def helper(lo, hi, k, depth_limit):
        if lo < hi:
            if depth_limit == 0:
                # NOTE: Alternatively could do heap-select which also
                # has O(nlog n) worst-case. But since that is a pure Python
                # implementation it is likely slower than just sorting.

                # Only sort the section where the k-th element is located
                arr[lo:hi+1] = sorted(arr[lo:hi+1])
                return

            i, j, _ = partition.hoare3(arr, lo, hi)

            if k <= i:
                helper(lo, i, k, depth_limit-1)
            elif k >= j:
                helper(j, hi, k, depth_limit-1)

    depth_limit = min(2 * int(math.log2(hi-lo)), sys.getrecursionlimit())
    helper(lo, hi, k, depth_limit)


def lomuto(arr, lo, hi, k):
    if lo < hi:
        i = partition.lomuto(arr, lo, hi)

        if k < i:
            lomuto(arr, lo, i-1, k)
        elif k > i:
            lomuto(arr, i+1, hi, k)


if __name__ == "__main__":
    import random
    from timeit import default_timer as timer

    random.seed(14)

    data = random.choices(range(1_000), k=1_000_000)
    k = 58
    # N = 10_000_000
    # data = random.choices(range(1_000), k=N)
    # data = 10 * data
    # k = (10 * N) // 2

    print("Sorted")
    start = timer()
    ans = sorted(data)[k]
    end = timer()
    print(f"Time: {end - start:.3f}s")

    print("Intro")
    lst = data[:]
    start = timer()
    introselect(lst, 0, len(lst)-1, k)
    end = timer()
    print(f"Time: {end - start:.3f}s")
    assert lst[k] == ans

    print("Hoare")
    lst = data[:]
    start = timer()
    try:
        hoare(lst, 0, len(lst)-1, k)
    except RecursionError:
        print("Exceeded maximum recursion depth")
    else:
        end = timer()
        print(f"Time: {end - start:.3f}s")
        assert lst[k] == ans

    print("Hoare3")
    lst = data[:]
    start = timer()
    try:
        hoare3(lst, 0, len(lst)-1, k)
    except RecursionError:
        print("Exceeded maximum recursion depth")
    else:
        end = timer()
        print(f"Time: {end - start:.3f}s")
        assert lst[k] == ans

    print("Lumoto")
    lst = data[:]
    start = timer()
    try:
        lomuto(lst, 0, len(lst)-1, k)
    except RecursionError:
        print("Exceeded maximum recursion depth")
    else:
        end = timer()
        print(f"Time: {end - start:.3f}s")
        assert lst[k] == ans
