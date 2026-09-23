"""Problem 2: Even Fibonacci Numbers.

Sum of the even-valued terms in the Fibonacci sequence (starting 1, 2)
not exceeding four million. Answer: 4613732.

Insight: parity cycles odd, even, odd, even, ... since an even term is
the sum of the two preceding odds, so exactly every third term is even.
The even subsequence alone obeys E(n) = 4*E(n-1) + E(n-2) (because two
steps of Fibonacci add up that way), letting us generate only the even
terms and skip two thirds of the series.
"""

LIMIT = 4_000_000


def sum_even_fibonacci(limit: int) -> int:
    total = 0
    prev, curr = 0, 2  # 0 is a sentinel so 4*curr + prev yields the whole sequence: 2, 8, 34, ...
    while curr <= limit:
        total += curr
        prev, curr = curr, 4 * curr + prev
    return total


if __name__ == "__main__":
    print(sum_even_fibonacci(LIMIT))
