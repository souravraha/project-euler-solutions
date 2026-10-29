# Problem 629: Scatterstone Nim

*A position is a partition of n into piles (heaps). A move replaces one pile of
size >= 2 by any partition of it into between 2 and k non-empty piles (k is
fixed). Normal play: the first player with no move loses. Let F_k(n) be the
number of winning positions for n; find g(n) = sum over k = 2..n of F_k(n) at
n = 200, modulo 10^9+7. Given F_2(5)=3, F_3(5)=5, g(7)=66, g(10)=291.*

## The naive approach

For every k in 2..n: grind the single-pile Grundy table G_k(s) by enumerating
all 2..k-way splits of each s (costs O(n^k) and blows up for k ~ n = 200), then
count the F_k(n) partitions - of which there are p(200) ~ 4e12 - one by one.
Both the Grundy grind and the partition enumeration are hopeless.

## The insight

Sprague-Grundy collapses the whole game to the single-pile value. A position
(partition lambda) is winning exactly when the xor of the Grundy numbers of its
heaps is non-zero:

```
G_k(s_1) ^ G_k(s_2) ^ ... ^ G_k(s_t)  !=  0
```

So F_k(n) = p(n) - L_k(n), where L_k(n) is the number of partitions of n whose
heap xor is zero. Everything hinges on the single-heap table G_k(s), which has
only **three distinct shapes**:

```
k = 2   ->  G_2(s) = 1 if s is even else 0        (parity)
k = 3   ->  tabulate: G_3(1..10) = 0,1,2,3,1,4,3,2,4,5, ...
k >= 4  ->  G_k(s) = s - 1   for every s
```

The k = 2 rule is by parity induction: an even s splits into two parts of the
same parity (both reachable nims are 0, so mex = 1); an odd s splits into one
odd and one even part (all reachable nims are 1, so mex = 0).

The k >= 4 case **saturates**. Any move replaces a pile of size s by r >= 2
piles of sizes x_1..x_r, so the option's nim is `(x_1-1) ^ ... ^ (x_r-1)`,
which is at most their sum `s - r <= s - 2`. So `s - 1` is *never* a reachable
nim. Meanwhile the four-way regime is rich enough to reach every nimber
`0..s-2`, forcing the mex to be exactly `s-1`. Because the Grundy number is
non-decreasing in the set of allowed moves, every k >= 4 lands on this same
table. This is the decisive simplification: instead of solving n-1 different
games we solve three.

A partition is a **multiset** of heaps, so to count L_k(n) we do an unbounded
count over heap sizes, threading an xor-state. With D[t][x] = "number of ways
to partition total t with heap xor x" (D[0][0] = 1) and the increasing-sum
unbounded update

```
D[t][x ^ G(s)] += D[t - s][x]        (t >= s)
```

(allowing the same size s to recur any number of times), the losing count is
simply L_k(n) = D[n][0]. The xor dimension has width X = 256, enough for every
Grundy value below heap size 200. This completely avoids enumerating the 4e12
partitions.

Finally the sum over k collapses (n >= 4):

```
g(n) = F_2(n) + F_3(n) + (n - 3) F_4(n)
```

## Complexity

- Time: `O(n^2)` partition numbers + `O(n^3)` for the k=3 Grundy table + `3 * O(n^2 X)` XOR DPs (X = 256) - vs. the hopeless `O(n^k)` grind and `p(n)` enumeration
- Space: `O(n * X)` for the partition/xor tables
- Measured: ~2.5 s in CPython (verified against all four given values, and
  cross-checked by an independent brute-force game simulation out to n = 18)

**Answer:** `626616617`.
