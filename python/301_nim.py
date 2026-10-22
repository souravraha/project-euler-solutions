"""Problem 301: Nim.

Count the positive integers n <= 2**30 for which the normal-play
three-heap Nim position X(n, 2n, 3n) is a losing position, i.e. has
nim-sum 0. Answer: 2178309.

Insight: the nim-sum is 0 exactly when n XOR 2n XOR 3n = 0. Because
3n = n + 2n, that holds exactly when adding n and 2n produces no carry,
i.e. when n and 2n have no bit set in common. Since 2n is just n
shifted left by one, two such bits coincide exactly when n has two
adjacent 1-bits. So the answer is the count of n in [1, 2**30] with no
two adjacent 1-bits in binary, a Fibonacci number F(L + 2) over
L-bit strings. For L = 30 that is F(32) = 2178309; adding 2**30 (a
single set bit, so valid) while dropping n = 0 (also valid) nets out,
leaving the answer equal to the L-bit count.
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
