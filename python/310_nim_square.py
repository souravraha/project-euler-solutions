"""Problem 310: Nim Square.

Nim Square is the three-heap, normal-play Nim variant in which a move
may remove only a square number of stones from one heap. Count the
losing positions (a, b, c) with 0 <= a <= b <= c <= N. Answer for
N = 100000 below (the PE-supplied N = 29 -> 1160 is used to check).

Insight: a single heap is the impartial 'remove a square' subtraction
game with Grundy value g(m) = mex { g(m - s) : s a square, s <= m }.
The three-heap game is the disjunctive sum, so it is losing exactly
when g(a) ^ g(b) ^ g(c) = 0 (Sprague-Grundy). Since a <= b <= c asks
for *multisets* of three heap sizes, Burnside's lemma turns the orbit
count into a simple function of how many sizes carry each Grundy value.
"""

from math import isqrt


def grundy(n: int) -> list[int]:
    """g[0..n] for the 'remove a square number of stones' subtraction game."""
    squares = [s * s for s in range(1, isqrt(n) + 1)]
    g = [0] * (n + 1)
    seen = [0] * (n + 2)       # generation table indexed by Grundy value
    gen = 0
    for m in range(1, n + 1):
        gen += 1
        for s in squares:
            if s > m:
                break
            seen[g[m - s]] = gen
        mex = 0
        while seen[mex] == gen:
            mex += 1
        g[m] = mex
    return g


def losing_positions(n: int) -> int:
    """Losing (a, b, c), 0 <= a <= b <= c <= n, with g(a)^g(b)^g(c) = 0.

    With f[v] = #{m in [0, n] : g(m) = v}, the number of *ordered*
    losing triples is T = sum_{u, v} f[u] f[v] f[u ^ v]. Burnside's
    lemma on the symmetric group (whose orbits are the a <= b <= c
    multisets) gives M = (T + 3*(n+1)*f[0] + 2*f[0]) / 6.
    """
    g = grundy(n)
    gmax = max(g)
    freq = [0] * (gmax + 1)
    for v in g:
        freq[v] += 1
    f0 = freq[0]

    ordered = 0
    for u in range(gmax + 1):
        fu = freq[u]
        if fu:
            for v in range(gmax + 1):
                w = u ^ v
                if w <= gmax:
                    ordered += fu * freq[v] * freq[w]

    return (ordered + 3 * (n + 1) * f0 + 2 * f0) // 6


if __name__ == "__main__":
    assert losing_positions(29) == 1160   # PE: N = 29 is 1160
    print(losing_positions(100_000))
