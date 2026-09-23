# Problem 1: Multiples of 3 or 5

*Sum of the natural numbers below 1000 that are multiples of 3 or 5.*

## The naive approach

Loop over `1..999`, test `i % 3 == 0 or i % 5 == 0`, and accumulate. Correct
and trivially fast at this size, but the loop is pure overhead: the quantity
it computes has a closed form, so every iteration is wasted work.

## The insight

The multiples of `m` below `bound` form the arithmetic series
`m, 2m, ..., km` with `k = (bound - 1) // m`, summing to `m*k(k + 1)/2`.
The two sets overlap exactly in the multiples of 15, so inclusion-exclusion
gives

```
sum(3) + sum(5) - sum(15)
```

in **O(1)** - three divisions, no loop. (The earlier one-liner
`m * (bound - 1) // m * ((bound - 1) // m + 1) // m` looked equivalent by
eye, but operator precedence makes it compute `(bound - 1) * (k + 1) // m`
instead - a subtle bug that a brute-force sum caught.)

## Complexity

- Time: `O(1)` - vs. `O(bound)` if the numbers are listed
- Space: `O(1)`
- Measured: ~1-2 us per call in CPython (timeit, 100k runs; interpreter overhead dominates)

**Answer:** `233168` (for bound 1000).
