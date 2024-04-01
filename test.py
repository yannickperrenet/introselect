import random

import find


def select_by_sorting(a, rank):
    """Return rank'th item of list a by sorting. May modify a."""
    assert 0 <= rank < len(a)
    a.sort()
    return a[rank]


def validate():
    """Confirm that all select functions give the correct result."""
    ranks = list(range(500))
    data = [1000 + r for r in ranks]
    random.shuffle(ranks)  # Test in random order.
    for rank in ranks:
        random.shuffle(data)
        assert select_by_sorting(data, rank) == 1000+rank
        random.shuffle(data)
        find.hoare(data, 0, len(data)-1, rank)
        assert data[rank] == 1000+rank
        random.shuffle(data)
        find.lomuto(data, 0, len(data)-1, rank)
        assert data[rank] == 1000+rank
        random.shuffle(data)
        find.hoare3(data, 0, len(data)-1, rank)
        assert data[rank] == 1000+rank
        random.shuffle(data)
        find.introselect(data, 0, len(data)-1, rank)
        assert data[rank] == 1000+rank


# From: https://bugs.python.org/file35423/select.py
# Helper class for timings. Since we mostly care about large data sets,
# the times will be moderately large (e.g. in excess of a second). In
# that case, we don't bother with timeit, which is designed for timing
# small snippets with millisecond timings.

class Stopwatch:
    """Time hefty or long-running block of code using a ``with`` statement:

    >>> with Stopwatch() as sw:  #doctest: +SKIP
    ...     do_this()
    ...     do_that()
    ...
    >>> print(sw.elapsed)  #doctest: +SKIP
    1.234567

    """
    def __init__(self, timer=None):
        if timer is None:
            from timeit import default_timer as timer
        self.timer = timer
        self._start = self._end = self._elapsed = None

    def __enter__(self):
        self._start = self.timer()
        return self

    def __exit__(self, *args):
        self._end = self.timer()

    @property
    def elapsed(self):
        return self._end - self._start


HEADER = """\
N        sort     Lomuto   Intro    Hoare3   Hoare
-------- -------- -------- -------- -------- --------"""


def run_test(size, single=True):
    """Run a timing test against all select* functions, and print the
    results. Smaller times are faster, hence better.

    Argument <size> is the number of data points in the list argument.

    If <single> is true, each function is called once. If <single> is
    false, each function is called three times, using different ranks,
    and the total time taken is averaged.

    These timing tests assume that each test takes an appreciable amount of
    time (e.g. seconds rather than milliseconds), and do not take heroic
    measures to reduce the measurement overhead. Consequently, for very
    small <size> and very low timings, the results shown may be inaccurate.
    """
    data = list(range(size))
    random.shuffle(data)
    if single:
        ranks = (size//2,)
        results = ([],)  # List to hold results of calling select functions.
    else:
        # Pick three semi-arbitrary ranks.
        ranks = (size//2, size//3, 4*size//5)
        results = ([], [], [])  # One list per rank.
    print("%8d" % size, end = ' ', flush=True)

    a = data[:]
    with Stopwatch() as sw:
        for r, L in zip(ranks, results):
            L.append(select_by_sorting(a, r))
    print("%8.3f" % (sw.elapsed/3), end=' ', flush=True)

    a = data[:]
    with Stopwatch() as sw:
        for r, L in zip(ranks, results):
            find.lomuto(a, 0, len(a)-1, r)
            L.append(a[r])
    print("%8.3f" % (sw.elapsed/3), end=' ', flush=True)

    a = data[:]
    with Stopwatch() as sw:
        for r, L in zip(ranks, results):
            find.introselect(a, 0, len(a)-1, r)
            L.append(a[r])
    print("%8.3f" % (sw.elapsed/3), end=' ', flush=True)

    a = data[:]
    with Stopwatch() as sw:
        for r, L in zip(ranks, results):
            find.hoare3(a, 0, len(a)-1, r)
            L.append(a[r])
    print("%8.3f" % (sw.elapsed/3), end=' ', flush=True)

    a = data[:]
    with Stopwatch() as sw:
        for r, L in zip(ranks, results):
            find.hoare(a, 0, len(a)-1, r)
            L.append(a[r])
    print("%8.3f" % (sw.elapsed/3), flush=True)

    # Verify that all the functions gave the same result.
    for rank, L in zip(ranks, results):
        if any(x != L[0] for x in L):
            print("test for rank %d failed" % rank, L)


def drive(single=True):
    with Stopwatch() as sw:
        if single:
            print("== Single call mode ==")
        else:
            print("== Average of three calls mode ==")
        print(HEADER)
        for i in range(4, 7):
            size = 10**i
            run_test(size//2, single)
            run_test(size, single)
        for i in range(2, 12):
            size = i*10**6
            run_test(size, single)
    print("Total elapsed time: %.2f minutes" % (sw.elapsed/60))
    print()


if __name__ == "__main__":
    validate()
    drive()
