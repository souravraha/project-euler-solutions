"""Problem 1: Multiples of 3 or 5.

Arithmetic-series solution; O(1) in the bound, no loops.
Inclusion-exclusion handles the overlap of the two sets.
Answer for 1000: 233168.
"""


def multiples_sum(bound: int) -> int:
    def multiples(m: int) -> int:
        k = (bound - 1) // m          # number of multiples of m below bound
        return m * k * (k + 1) // 2   # sum of the arithmetic series m, 2m, ..., km

    return multiples(3) + multiples(5) - multiples(15)


if __name__ == "__main__":
    print(multiples_sum(1000))
