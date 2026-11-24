"""Problem 560: Coprime Nim.

Coprime Nim: N piles; a move removes r > 0 stones from one pile where
r is coprime to the current pile size; last to move wins. L(n, k) is the
number of losing (first-player) k-positions with each pile in [1, n-1].

Insight 1 (Grundy closed form). A pile is the impartial game "remove a
number coprime to the current size". A little Grundy analysis shows the
pile value never needs a case split:
  g(0) = 0,  g(1) = 1,  g(m) = 0 for even m,
  and for odd m >= 3 the reachable Grundy set skips exactly the ordinal
  of m's smallest prime factor, so
      g(m) = pi(spf(m)),
where pi(p) is the (1-indexed) ordinal of the odd prime p among all
primes (pi(3)=2, pi(5)=3, pi(7)=4, ...) and spf(m) is the smallest
prime factor of (odd) m.  Hence only the *distribution* of spf(m) over
the odd piles matters - a single sieve gives it, no O(n^2) grind.

Insight 2 (counting). A k-position is losing iff the xor of its k
Grundy values is 0, so with freq[v] = #{ pile sizes in [1, n-1] having
Grundy value v },
      L = (1 / M) * sum_{a=0}^{M-1} S(a)^k,   M = next power of two
  where S(a) = sum_v freq[v] * (-1)^{popcount(a & v)}.  The vector
  S(a) is exactly the Walsh--Hadamard (XOR) transform of freq, which
  is an O(M log M) fast transform.

Given: L(5,2)=6, L(10,5)=9964, L(10,10)=472400303,
       L(10^3, 10^3) mod 1e9+7 = 954021836.
Find  L(10^7, 10^7) mod 1e9+7.
"""

from array import array
import math

MOD = 1_000_000_007


def ordinal_by_spf(n: int):
    """Return (max_ordinal, ord_arr, spf) for m in [0, n].

    spf[m]       = smallest prime factor of m (0 for m < 2)
    ord_arr[m]   = pi(spf(m)), the 1-indexed ordinal of spf(m) among the
                   primes (pi(2)=1, pi(3)=2, pi(5)=3, ...); 0 otherwise
    max_ordinal  = pi(largest prime <= n)
    """
    spf = array("I", range(n + 1))
    if n >= 1:
        spf[0] = spf[1] = 0
    for i in range(2, math.isqrt(n) + 1):
        if spf[i] == i:                         # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    ord_arr = array("I", [0]) * (n + 1)
    ordinal = 0
    for v in range(2, n + 1):
        if spf[v] == v:                         # v is prime
            ordinal += 1
            ord_arr[v] = ordinal                # pi(v), 1-indexed
    return ordinal, ord_arr, spf


def grundy_frequency(n: int):
    """freq[v] = #{ pile sizes m in [1, n] with Grundy value v }.

    freq[0] = n // 2 (the even sizes), freq[1] = 1 (the single size 1),
    and every odd m >= 3 lands in the bin pi(spf(m)).
    """
    max_ordinal, ord_arr, spf = ordinal_by_spf(n)
    size = 1
    while size <= max_ordinal:
        size <<= 1                              # power of two > max ordinal
    freq = [0] * size
    freq[0] = n // 2                            # even piles -> Grundy 0
    if n >= 1:
        freq[1] = 1                             # the single pile of size 1
    for m in range(3, n + 1, 2):                # odd piles -> pi(spf(m))
        freq[ord_arr[spf[m]]] += 1
    return freq


def losing_positions(n: int, k: int) -> int:
    """L(n, k) for piles in [1, n-1]: count of losing k-positions mod MOD."""
    freq = grundy_frequency(n - 1)
    size = len(freq)
    # Walsh-Hadamard (XOR) transform: S(a) = sum_v freq[v]*(-1)^{popcount(a&v)}
    h = 1
    while h < size:
        for i in range(0, size, 2 * h):
            base = i
            for j in range(base, base + h):
                x = freq[j]
                y = freq[j + h]
                freq[j] = x + y
                freq[j + h] = x - y
        h <<= 1
    inv_m = pow(size, MOD - 2, MOD)
    total = 0
    for a in range(size):
        total = (total + pow(freq[a] % MOD, k, MOD)) % MOD
    return total * inv_m % MOD


def _selfcheck() -> None:
    assert losing_positions(5, 2) == 6
    assert losing_positions(10, 5) == 9964
    assert losing_positions(10, 10) == 472_400_303
    assert losing_positions(1000, 1000) == 954_021_836


if __name__ == "__main__":
    _selfcheck()
    print(losing_positions(10_000_000, 10_000_000))
