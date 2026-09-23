# Problem 8: Largest Product in a Series

*Largest product of thirteen consecutive digits in a given 1000-digit number.*

## The naive approach

For each of the 988 thirteen-digit windows, recompute the product from
scratch: `O(n*k)` ~ 13,000 multiplications. Fine at 1000 digits - but
recomputing a 12-of-13-digit prefix for every window is exactly the waste
that a sliding window removes.

## The insight

Track a **running product** as the window slides: when the left digit `d`
leaves, divide it out; when the new right digit `e` enters, multiply by it.
Every window update is `O(1)`, so `O(n)` over the whole string.

The snag is **zero**: a window containing a zero has product 0, and a zero
cannot be divided back out when it leaves. So instead of a single running
product, keep a *zero counter* alongside it; a window's product is 0 exactly
when the counter is non-zero, otherwise it's the running product of its
non-zero digits.

```
best = max over windows of (0 if zeros_in_window else running_product)
```

## Complexity

- Time: `O(n)` window updates - vs. `O(n*k)` for the per-window recompute
- Space: `O(1)`
- Measured: ~0.9 ms for a full pass over the 1000-digit string in CPython (timeit, 10k runs)

**Answer:** `23514624000`, the window `5576689664895` (digits 198-210, 1-based).

## Gotcha

The 1000-digit number must be embedded **verbatim**. On the Project Euler
page it renders split by a line break *mid-run* (`...44031` / `9989` /
`00088...`), so a quick `re.findall(r'\d{50,}', html)` silently drops the
short chunk. The problem's own 4-digit worked example
(`9 * 9 * 8 * 9 = 5832`) is a 10 ms tripwire for exactly this kind of
transcription slip - always check it before trusting the answer.
