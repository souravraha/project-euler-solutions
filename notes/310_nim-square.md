# Problem 310: Nim Square

*Nim Square: three-heap, normal-play Nim where each move removes a square number of stones from one heap. Count the losing positions (a, b, c) with 0 <= a <= b <= c <= 100,000.*

## The naive approach

Recursively explore every game state, or for each of the ~10^15 triples
(a, b, c) with a <= b <= c test whether it is losing. Both are hopeless
at N = 100,000 - we never enumerate positions at all.

## The insight

Each heap is a standalone impartial game: starting with m stones, a move
takes m to m - s for some square s <= m. Its Grundy value is

```
g(m) = mex { g(m - s) : s a square, s <= m }
```

A position is losing (a P-position) iff the nim-sum is zero. By
Sprague-Grundy the three-heap sum is losing exactly when

```
g(a) ^ g(b) ^ g(c) = 0
```

So only the *frequencies* of the Grundy values matter. Let
f[v] = #{ heap sizes in [0, N] with Grundy v }.

The catch is that a <= b <= c counts *multisets* of three heap sizes,
not ordered triples. Burnside's lemma (symmetric group S_3 acting on
ordered triples, orbits = multisets) fixes this:

```
ordered   T = sum_{u,v}  f[u] f[v] f[u ^ v]
         M = ( T + 3*(N+1)*f[0] + 2*f[0] ) / 6
```

The `3*(N+1)*f[0]` and `2*f[0]` terms are the fixed-point counts of the
transpositions (both equal heap sizes coincide, reducing the xor to a
single component) and the 3-cycles (all three coincide). Verified the
identity against a direct O(N^3) enumeration for N = 5, 10, 29, 40, and
against the PE-supplied N = 29 -> 1160.

## Complexity

- Time: `O(N sqrt(N))` for the Grundy table (each m scans ~sqrt(m) squares) + `O(G^2)` for the Burnside sum, G = max Grundy - vs. the hopeless O(N^3) enumeration
- Space: `O(N)` for the Grundy table
- Measured: ~1.3 s for N = 100,000 in CPython

**Answer:** `2586528661783`.
