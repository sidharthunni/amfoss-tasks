# Task 04: The Pirate King's Challenge

All 5 Codeforces problems solved and accepted.

## Problems

1. **[2218D - The 67th OEIS Problem](https://codeforces.com/problemset/problem/2218/D)**
   Had to build a sequence where every consecutive gcd is different.
   Used distinct primes and multiplied neighbors together (a_i =
   p(i-1)*p(i)), so each gcd just comes out to be one of the primes,
   and primes are always different.

2. **[2230B - Digit String](https://codeforces.com/problemset/problem/2230/B)**
   Needed the fewest deletions so no subsequence makes a multiple of
   4. Any leftover 4 breaks it instantly, so those all go first. After
   that, only "1 then 2" or "3 then 2" patterns are a problem, so I
   just found the best point to split the string so all 2s come
   before the 1s/3s that are kept.

3. **[2238A - Another Puzzle from Papyrus](https://codeforces.com/problemset/problem/2238/A)**
   Compared two ways to turn array a into b - either don't reorder at
   all, or reorder (pay cost c) and pair up sorted a with sorted b.
   Picked whichever valid option costs less.

4. **[2241B - Good times Good times](https://codeforces.com/problemset/problem/2241/B)**
   Given a number x with at most 2 digits used, needed to find y so
   x*y also has at most 2 digits. Used y = 10^d + 1, which basically
   just copies x right next to itself when multiplied, so the digits
   never change.

5. **[2237C - Duck Surplus](https://codeforces.com/problemset/problem/2237/C)**
   Had to minimize the biggest pile after merging. Just went left to
   right keeping a running total, adding the next pile into it
   whenever it's smaller, otherwise starting fresh from that pile.

## Review
All 5 problems were pretty challenging, especially figuring out the
tricks behind a few of them. But it felt satisfying getting them all
accepted in the end. Still a lot for me to improve on when it comes
to spotting these patterns quickly.
