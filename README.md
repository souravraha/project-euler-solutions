# Project Euler Solutions

Solutions to [Project Euler](https://projecteuler.net/) problems in **Python** - **7** so far, still learning and more on the way.

## Solved

| # | Problem | Answer |
|---|---------|--------|
| 1 | Multiples of 3 or 5 (below 1000) | 233168 |
| 2 | Sum of even Fibonacci terms <= 4,000,000 | 4613732 |
| 8 | Largest product of 13 consecutive digits | 23514624000 |
| 301 | Nim, nim-sum of (n, 2n, 3n) below 2^30 | 2178309 |
| 310 | Nim Square, losing triples a<=b<=c<=100,000 | 2586528661783 |
| 560 | Coprime Nim, L(10^7, 10^7) mod 10^9+7 | 994345168 |
| 629 | Scatterstone Nim, g(200) mod 10^9+7 | 626616617 |

## Highlights

A few problems I find particularly interesting, with notes on the approach:

| # | Problem | Approach | Notes |
|---|---------|----------|-------|
| 1 | Multiples of 3 or 5 | O(1) arithmetic series + inclusion-exclusion | 4 lines, no loops - [writeup](notes/001_multiples-of-3-and-5.md) |
| 2 | Even Fibonacci numbers | Parity cycle skips two of every three terms | Generate only the even terms via `E(n) = 4*E(n-1) + E(n-2)` - [writeup](notes/002_even-fibonacci-numbers.md) |
| 8 | Largest product in a series | Zero-aware sliding window | O(n) running product with a zero counter - [writeup](notes/008_largest-product-in-a-series.md) |
| 301 | Nim | Nim-sum zero iff no two adjacent 1-bits in n | Count via Fibonacci `F(32)` - [writeup](notes/301_nim.md) |
| 310 | Nim Square | Grundy (square-subtraction) + Burnside orbits | `O(N sqrt N)` - [writeup](notes/310_nim-square.md) |
| 560 | Coprime Nim | Grundy closed form `pi(spf)` + Walsh-Hadamard | `O(n log log n)` - [writeup](notes/560_coprime-nim.md) |
| 629 | Scatterstone Nim | Grundy (k=2 parity, k=3 mex, k>=4 = s-1) + XOR partition DP | `O(n^3 + n^2 X)` - [writeup](notes/629_scatterstone-nim.md) |

Each highlight links to a short writeup in [`notes/`](notes/) covering:

1. What the naive approach is, and why it falls over.
2. The insight that makes a clean solution possible.
3. Complexity analysis and measured run time.

## Repository Layout

```
project-euler-solutions/
|-- README.md
|-- python/          # one file per problem: NNN_short-name.py
`-- notes/           # writeups for highlighted problems
```

Solutions follow a single convention: read the problem from `projecteuler.net`, compute the answer, and print it. Any non-trivial insight lives in a comment at the top of the file and (for highlighted problems) in `notes/`.

## How to Run

All current solutions are fast enough to verify locally:

```bash
python3 python/001_multiples_of_3_and_5.py      # -> 233168
python3 python/002_even_fibonacci_numbers.py    # -> 4613732
python3 python/008_largest_product_in_a_series.py  # -> 23514624000
python3 python/301_nim.py                        # -> 2178309
python3 python/310_nim_square.py                 # -> 2586528661783
python3 python/560_coprime_nim.py                # -> 994345168
python3 python/629_scatterstone_nim.py           # -> 626616617
```

## Conventions

- One file per problem, named `NNN_kebab-case-name.py`.
- No hardcoded answers - every file recomputes the result.
- Where a problem has multiple viable approaches, I implement the interesting one and explain the tradeoff in a header comment.
