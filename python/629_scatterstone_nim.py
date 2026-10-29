"""Problem 629: Scatterstone Nim.

A position is a partition lambda = (s_1, ..., s_t) of n, the s_i being heap
sizes.  A move replaces one heap of size >= 2 by any partition of that heap
into between 2 and k non-empty heaps (k is fixed for the game).  Normal play:
the player with no move loses.

Let F_k(n) = number of positions (partitions of n) that are winning for the
first player;  g(n) = sum over k = 2..n of F_k(n).  Find g(200) mod (10^9+7).

Sprague-Grundy:
  A position wins iff its nim-sum is non-zero, the nim-sum being the XOR of
  the single-heap Grundy numbers G_k(s) of its heaps.

Single-heap Grundy G_k(s) = mex of { xor of G_k over the parts of a split },
where a split has between 2 and k parts.  Three regimes:

  * k = 2  ->  G_2(s) = 1 if s is even else 0  (parity rule).
  * k = 3  ->  tabulate G_3 from the mex definition (2- and 3-way splits).
      G_3(1..10) = 0,1,2,3,1,4,3,2,4,5, ...
  * k >= 4 ->  G_k(s) = s - 1  for all s.
      Every move to r >= 2 parts gives a nim value (x_i-1) that is at most
      their sum, s - r <= s - 2, so s - 1 is never reachable; the four-way
      regime realises every nimber 0..s-2, forcing the mex to be s - 1.
      Grundy is non-decreasing in the set of allowed moves, so all
      k >= 4 give the same G table.

Counting losing positions:
  A partition is a multiset of heaps, so each heap size can occur any number
  of times; each use of size s adds G_k(s) to the nim (an even number of uses
  cancels out).  D[t][x] = number of partitions of total t with nim x, with
  D[0][0] = 1 and the unbounded update (sum in increasing order allows reuse)

      D[t][x ^ G(s)] += D[t - s][x]      (t >= s),

  gives the losing count L_k(n) = D[n][0] directly -- no need to enumerate
  the ~4e12 partitions of 200.

Therefore (n >= 4)

      g(n) = F_2(n) + F_3(n) + (n - 3) F_4(n),

where F_j(n) = p(n) - L_j(n) and p(n) is the ordinary partition number.

Compute g(200) mod (10^9+7), checking the given F_2(5)=3, F_3(5)=5,
g(7)=66, g(10)=291 first.
"""

import time

MOD = 10 ** 9 + 7
X = 256  # every G_k(s) with s <= 200 is < 256, hence every xor of them is too


def partition_numbers(n, mod):
    """p[0..n] = number of integer partitions, each value taken mod.`"""
    p = [0] * (n + 1)
    p[0] = 1
    for s in range(1, n + 1):
        for t in range(s, n + 1):
            p[t] = (p[t] + p[t - s]) % mod
    return p


def grundy_k2(n):
    """G(s),  split into exactly 2 parts: 1 if s is even else 0."""
    sg = [0] * (n + 1)
    for s in range(2, n + 1):
        sg[s] = 1 if s % 2 == 0 else 0
    return sg


def grundy_k3(n):
    """G(s),  split into 2 or 3 parts: mex of the reachable nims."""
    sg = [0] * (n + 1)
    sg[1] = 0
    for s in range(2, n + 1):
        seen = [False] * X
        # exactly 2 parts: (a, s-a)
        for a in range(1, s):
            seen[sg[a] ^ sg[s - a]] = True
        # exactly 3 parts: a, b, c >= 1, a+b+c = s
        for a in range(1, s - 1):
            for b in range(1, s - a):
                c = s - a - b
                seen[sg[a] ^ sg[b] ^ sg[c]] = True
        g = 0
        while seen[g]:
            g += 1
        sg[s] = g
    return sg


def grundy_k4(n):
    """G(s),  split into 2..k parts with k >= 4:  equals s - 1."""
    sg = [0] * (n + 1)
    for s in range(2, n + 1):
        sg[s] = s - 1
    return sg


def losing_count(n, sg, mod):
    """# partitions of n whose nim-sum (xor of sg[heap] over heaps) is 0."""
    dp = [[0] * X for _ in range(n + 1)]
    dp[0][0] = 1
    for s in range(1, n + 1):
        g = sg[s]
        for t in range(s, n + 1):
            cur = dp[t]
            prev = dp[t - s]
            for x in range(X):
                cur[x ^ g] = (cur[x ^ g] + prev[x]) % mod
    return dp[n][0]


def f(n, k, p):
    """F_k(n) = winning partitions = p(n) - losing,  all mod MOD."""
    if k == 2:
        sg = grundy_k2(n)
    elif k == 3:
        sg = grundy_k3(n)
    else:
        sg = grundy_k4(n)
    return (p[n] - losing_count(n, sg, MOD)) % MOD


def g_of(n):
    """g(n) = sum over k = 2..n of F_k(n)."""
    p = partition_numbers(n, MOD)
    if n < 4:
        return sum(f(n, k, p) for k in range(2, n + 1)) % MOD
    return (f(n, 2, p) + f(n, 3, p) + (n - 3) * f(n, 4, p)) % MOD


def main():
    # Given in the problem statement -- sanity-check the whole model.
    p5 = partition_numbers(5, MOD)
    checks = [
        (f(5, 2, p5), 3),
        (f(5, 3, p5), 5),
        (g_of(7), 66),
        (g_of(10), 291),
    ]
    for got, want in checks:
        assert got == want, f"self-check failed: got {got}, expected {want}"
        print(f"  OK: computed {got}")

    answer = g_of(200)
    print(f"  g(200) mod 10^9+7 = {answer}")
    return answer


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"  ({time.time() - t0:.2f}s)")
