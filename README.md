# Introselect

Get the `nth_element` of an array, i.e. the element that would be in the `nth` position if the array
where sorted.

C++ has an implementation for
[`nth_element`](https://en.cppreference.com/w/cpp/algorithm/nth_element), which is linear on average
with respect to the length of the array (by using the [introselect
algorithm](https://en.wikipedia.org/wiki/Introselect)). However, Python does not ([`statistics`
package source code](https://github.com/python/cpython/blob/3.12/Lib/statistics.py#L600)).

The reason Python never opted to implement any `nth_element` function based on a variant of a
selection algorithm, is clearly explained by Raymond Hettinger
([source](https://bugs.python.org/msg309909)):

    While variants of quick-select have a nice O(n) theoretical time, the variability is very-high
    and has really bad worst cases. The existing sort() is unbelievably fast, has a reasonable worst
    case, exploits existing order to great advantage, has nice cache performance, and has become
    faster still with the recently added type-specialized comparisons.  This sets a very high bar
    for any proposed patches.

Nevertheless, having an implementation at hand seemed like a good idea to me. Depending on your
data, using a selection algorithm may very well outperform Python's native `sort()`. Although the
cost of using `sort()` is much lower, then inspecting your data to decide whether a selection
algorithm is faster on average.

As C++ opted for introselect, this package does as well.

## Background

Introselect was hinted at by David R. Musser in his [introsort
paper](https://webpages.charlotte.edu/rbunescu/courses/ou/cs4040/introsort.pdf).

Introsort bypasses the $O(n^2)$ worst-case runtime of quicksort (originally named `find` and
introcuded by R. Hoare in [this paper](https://dl.acm.org/doi/10.1145/366622.366647)), by limiting
the stack depth (i.e. recursion depth) by $\log n$ and instead runs an $O(n\log n)$ worst-case (but
worse average runtime complexity) sorting algorithm, such as heap-sort, on the remaining
subproblems. Thereby obtaining an $O(n\log n)$ worst-case runtime with similar average runtimes to
quicksort.

To improve the runtime of quickselect, Musser proposed introselect which uses the same tactic as
introsort, i.e. limiting the stack depth. The depth can be limited by a logarithmic bound giving a
worst case runtime of $O(n\log n)$. Musser even mentions limiting the depth such that one ends up
with an overall linear worst-case runtime, however he retired before publishing that paper.

There are published $O(n)$ selection algorithms such as BFPRT ([original
paper](https://people.csail.mit.edu/rivest/pubs/BFPRT73.pdf)), which was later improved by A.
Alexandrescu in his [ninthers paper](https://arxiv.org/abs/1606.00484) ([source
code](https://github.com/andralex/MedianOfNinthers)). However, BFPRT has a high constant factor
making it slower than quickselect (and introselect) in practice.

An important part of a selection algorithms is its underlying partitioning scheme. There is
extensive literature on the comparison of these partitioning schemes, e.g. researching the actual
number of comparisons, however we won't go into them here. Partitioning schemes rely on different
techniques for their pivot selection as poor pivot selection leads to slow runtimes. For example, if
you coincidentally select the median to be the pivot element, then the number of recursive calls is
minimized whereas selecting the minimum would result in $O(n)$ recursive calls (hence the $O(n^2)$
worst-case of most selection algorithms).

## Implementation

When opting for a selection algorithm, you are met with the following choices:

-   How to select a pivot element for partitioning?
-   Which partitioning scheme performs best?
-   Which selection algorithm to use?

    Of course the actual selection algorithm has already made the previous choices, but its good to
    know what the different components of a selection algorithm are.

Therefore, I opted to implemented multiple partitioning schemes and selection algorithms to make a
quick comparison.

You can find the partitioning functions in [`partition.py`](partition.py), selection algorithms
in [`find.py`](find.py) and comparison code in [`test.py`](test.py).

```python
import find

arr = [8, 5, 9, 1, 66, 7, 3]
find.introselect(arr, 0, len(arr)-1, 1)
# -> arr = [1, 3, 9, 8, 66, 7, 5]
assert arr[1] == sorted(arr)[1] == 3
```

## Example timings

As you can see, `sort()` provides the most reliable runtime (in addition to subsequent calls for
different `n` being $O(1)$ ). However, in some cases, selection algorithms do run faster.

```plain
N        sort     Lomuto   Intro    Hoare3   Hoare
-------- -------- -------- -------- -------- --------
    5000    0.000    0.000    0.000    0.000    0.000
   10000    0.000    0.001    0.000    0.000    0.001
   50000    0.002    0.003    0.002    0.002    0.002
  100000    0.006    0.005    0.004    0.004    0.005
  500000    0.039    0.033   *0.027    0.027    0.047
 1000000    0.084    0.120   *0.056    0.074    0.077
 2000000    0.187    0.263   *0.126    0.171    0.211
 3000000   *0.292    0.420    0.301    0.436    0.331
 4000000   *0.419    0.770    0.534    0.591    0.468
 5000000   *0.524    1.154    0.558    0.550    0.578
 6000000   *0.664    1.397    0.762    1.114    0.843
 7000000    0.782    1.725    0.915    1.289   *0.693
 8000000    0.925    0.995   *0.506    0.535    0.874
 9000000    1.036    0.969    0.913   *0.732    1.140
10000000    1.171    1.412    0.823    0.606   *0.604
11000000    1.375    2.127    1.883    1.384   *0.932
```
