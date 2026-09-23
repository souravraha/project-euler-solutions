# Project Euler Solutions

Solutions to [Project Euler](https://projecteuler.net/) problems in **Python** - **3** so far, more on the way.

> Profile: [projecteuler.net/profile/YOUR_USERNAME](https://projecteuler.net/profile/YOUR_USERNAME)

> Note: replace the placeholder profile link above with your real link before publishing.

## Solved

| # | Problem | Answer |
|---|---------|--------|
| 1 | Multiples of 3 or 5 (below 1000) | 233168 |
| 2 | Sum of even Fibonacci terms <= 4,000,000 | 4613732 |
| 8 | Largest product of 13 consecutive digits | 23514624000 |

## Highlights

A few problems I find particularly interesting, with notes on the approach:

| # | Problem | Approach | Notes |
|---|---------|----------|-------|
| 1 | Multiples of 3 or 5 | O(1) arithmetic series + inclusion-exclusion | 4 lines, no loops - [writeup](notes/001_multiples-of-3-and-5.md) |
| 2 | Even Fibonacci numbers | Parity cycle skips two of every three terms | Generate only the even terms via `E(n) = 4*E(n-1) + E(n-2)` - [writeup](notes/002_even-fibonacci-numbers.md) |
| 8 | Largest product in a series | Zero-aware sliding window | O(n) running product with a zero counter - [writeup](notes/008_largest-product-in-a-series.md) |

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

(`notes/022_amicable-numbers.md` is a sample showing the writeup format - swap it for a writeup you're proud of.)

Solutions follow a single convention: read the problem from `projecteuler.net`, compute the answer, and print it. Any non-trivial insight lives in a comment at the top of the file and (for highlighted problems) in `notes/`.

## How to Run

All current solutions are fast enough to verify locally:

```bash
python3 python/001_multiples_of_3_and_5.py      # -> 233168
python3 python/002_even_fibonacci_numbers.py    # -> 4613732
python3 python/008_largest_product_in_a_series.py  # -> 23514624000
```

## Conventions

- One file per problem, named `NNN_kebab-case-name.py`.
- No hardcoded answers - every file recomputes the result.
- Where a problem has multiple viable approaches, I implement the interesting one and explain the tradeoff in a header comment.
