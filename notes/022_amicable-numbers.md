# Problem 22: Names Scores

*Sample writeup - replace this with a problem you actually solved and are proud of.*

## The naive approach

A straightforward reading suggests, for each name, computing `length * (a + b + c)` as a
string sum and multiplying by position in the sorted list. That's fine - but the real cost on
this problem family is **enumerating candidates** (here: every 1-21 digit string). A brute
force over 200 million candidates in Python takes hours.

## The insight

**Digit DP.** The sum condition only depends on the multiset of digits used, not their
order. So instead of enumerating strings, count how many distinct digit *multisets* sum to
each residue `s in {0..9}`, multiply by `9^k` arrangements, and take the difference between
"not divisible by 11" and "divisible by 11."

```
count(n) = total_distinct_digit_sets(n) - divisible_by_11(n)
```

The divisible-by-11 part also becomes a small DP over the alternating-sum state,
so the whole solution is `O(n * n * 10)` - microseconds, not hours.

## Complexity

- Time: `O(n*n)` table fills per query, constant in string length
- Space: `O(n)`
- Measured: `0.003 s` locally vs. the ~90 min a naive scan takes to hit its first answer

## Measured run time

| n | Time |
|---|------|
| 100 000 | 2.1 ms |
| 1 000 000 | 21 ms |

*(Sample numbers - swap in your real benchmark.)*
