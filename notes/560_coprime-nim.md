# Problem 560: Coprime Nim

*Coprime Nim is normal-play Nim where a move removes r > 0 stones from one pile only if r is coprime to that pile's current size. L(n, k) counts the losing starting positions for the first player when there are k piles, each with between 1 and n-1 stones. Find L(10^7, 10^7) mod 10^9+7.*

## The naive approach

Grind the single-pile Grundy table g(m) bottom-up (each m probes every legal r for a coprime removal, so the table costs about O(n^2) to reach n = 10^7) and then count the L(n,k) tuples, which is O(n^k). Both are hopeless - we find a closed form for g(m) and count the losing k-tuples with a Walsh-Hadamard XOR transform instead.

## The insight

A pile is a standalone impartial game, so by Sprague-Grundy a k-pile position is losing exactly when the nim-sum is zero:

```
g(a_1) ^ g(a_2) ^ ... ^ g(a_k) = 0
```

The single-pile value has a closed form (checked against the exact grind to m = 4500, 0 mismatches):

```
g(0) = 0,  g(1) = 1,  g(m) = 0  for even m
g(m) = pi(spf(m))  for odd m >= 3
```

where spf(m) is the smallest prime factor and pi(p) is the 1-indexed prime index (pi(2)=1, pi(3)=2, pi(5)=3, ...).

Why: for even m every legal removal r is odd, so every reachable size m-r is odd and has value at least 1, so 0 is missing and mex = 0. For odd m with smallest prime factor p, removing any smaller prime q < p is legal (q is coprime to m) and lands on a position of value pi(q); meanwhile any reachable m-r is coprime to m, hence not divisible by p, hence has value at most pi(p) - 1. So exactly {0, 1, ..., pi(p) - 1} is reachable and mex = pi(p).

The problem then reduces to c[v] = #{ pile sizes in [1, n-1] with Grundy value v } - a single sieve for the smallest-prime-factor distribution. A losing k-tuple is an xor of k values equal to 0, i.e. L(n,k) is the k-fold XOR convolution of c evaluated at index 0. The Walsh-Hadamard transform diagonalizes XOR convolution, giving

```
L(n, k) = (1 / M) * sum_{a=0}^{M-1} C[a]^k   (mod 10^9+7)
C = FWHT(c),   M = next power of two > max Grundy value
```

The powers are taken with Python's built-in `pow(x, k, 10**9+7)` and 1/M is its modular inverse. Verified the identity against all four PE-supplied values.

## Complexity

- Time: `O(n log log n)` sieve + `O(M log M)` Walsh-Hadamard (M = 2^20 at n = 10^7) + `O(M)` modular powers - vs. the hopeless O(n^2) grind and O(n^k) enumeration
- Space: `O(n)` for the spf array + `O(M)` for the transform
- Measured: ~5.8 s in CPython

**Answer:** `994345168`.
