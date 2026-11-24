"""Problem 301: Nim.

Count the positive integers n <= 2**30 for which the three-heap,
normal-play Nim position X(n, 2n, 3n) has nim-sum 0 (a losing position).
Answer: 2178309 (= F(32)).

Insight: n ^ 2n ^ 3n = 0 because 3n = n + 2n, and a sum equals the xor
exactly when no carry is produced. So the nim-sum vanishes iff adding n
and 2n creates no carry, i.e. n and 2n share no set bit. Since 2n = n << 1,
two such bits coincide exactly when n has two adjacent 1-bits. Hence the
losing n are exactly those with no two adjacent 1-bits.

Counting: L-bit binary strings with no adjacent 1-bits number F(L + 2)
(recurrence f(1) = 2, f(2) = 3, f(L) = f(L-1) + f(L-2)), so [0, 2**30)
holds F(32) of them. The range [1, 2**30] differs by dropping n = 0 (valid)
and adding 2**30 (a single set bit, also valid) - the swap cancels, so the
answer is exactly F(32) = 2178309.
"""


def count_no_adjacent(bits: int) -> int:
    """Number of integers in [0, 2**bits) with no two adjacent 1-bits.

    This is the Fibonacci number F(bits + 2); equivalently the little
    recurrence f(1) = 2, f(2) = 3, f(L) = f(L - 1) + f(L - 2).
    """
    if bits == 1:
        return 2
    a, b = 2, 3
    for _ in range(3, bits + 1):
        a, b = b, a + b
    return b


def nim_zero_positions(limit_bits: int = 30) -> int:
    """Count positive n <= 2**limit_bits with X(n, 2n, 3n) = 0.

    Equivalent to the number of n in [1, 2**limit_bits] with no two
    adjacent 1-bits. [0, 2**limit_bits) already has that many (counting
    n = 0); dropping n = 0 and adding the single set-bit value
    2**limit_bits cancel, so the total is just the L-bit count.
    """
    return count_no_adjacent(limit_bits)


if __name__ == "__main__":
    print(nim_zero_positions(30))
