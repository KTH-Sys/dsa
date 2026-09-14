"""
Split and Sort Array  -  Google OA

PROBLEM
    Given an array A of N integers, split it into two non-empty parts
    left = A[0:i] and right = A[i:] for some 1 <= i <= N-1.
    Sort each part independently, then concatenate them back.
    Count the number of split points i that yield a non-decreasing array.

    Example: A = [1, 3, 2, 4]
        i=1 -> [1] + [2,3,4] = [1,2,3,4]   sorted   OK
        i=2 -> [1,3] + [2,4] = [1,3,2,4]   not sorted
        i=3 -> [1,2,3] + [4] = [1,2,3,4]   sorted   OK
    Answer: 2

KEY INSIGHT
    Sorting fixes all ordering *within* each part for free, so the only thing
    that can break monotonicity is the seam. A split at i is valid iff

        max(A[0:i]) <= min(A[i:])

    Precompute suffix minima right-to-left, then sweep left-to-right carrying a
    running prefix max.  O(N) time, O(N) space.  O(1) space is impossible:
    min(right) cannot be known without a right-to-left pass.

RELATED (these ARE on LeetCode, same invariant)
    769  Max Chunks To Make Sorted      (values are a permutation of 0..n-1)
    915  Partition Array into Disjoint Intervals  (smallest valid left length)
    768  Max Chunks To Make Sorted II   (answer == this count + 1)

TRAP
    Checking only the adjacent pair A[i-1] <= A[i] is wrong.
    A = [3, 1, 2, 5], i = 2: adjacency sees 1 <= 2 and says valid, but
    max(left) = 3 > min(right) = 2.  True answer 1, shortcut returns 2.
    Covered by test case "adjacent_pair_trap" below.
"""

import random
import time


# ---------------------------------------------------------------- solution

def solution(A):
    n = len(A)
    if n < 2:
        return 0

    suffix_min = [0] * n
    suffix_min[-1] = A[-1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(A[i], suffix_min[i + 1])

    count = 0
    left_max = A[0]
    for i in range(n - 1):
        left_max = max(left_max, A[i])
        if left_max <= suffix_min[i + 1]:
            count += 1

    return count


# ------------------------------------------------- brute-force oracle O(N^2 log N)

def brute(A):
    n = len(A)
    count = 0
    for i in range(1, n):
        joined = sorted(A[:i]) + sorted(A[i:])
        if all(joined[j] <= joined[j + 1] for j in range(n - 1)):
            count += 1
    return count


# ---------------------------------------------------------------- test table

CASES = [
    ("given_sample",        [1, 3, 2, 4],      2),
    ("already_sorted",      [1, 2, 3],         2),   # every split works
    ("reverse_sorted",      [3, 2, 1],         0),
    ("all_duplicates",      [1, 1, 1],         2),   # <= not <
    ("dup_blocks_split",    [2, 2, 1],         0),
    ("single_element",      [5],               0),   # both parts must be non-empty
    ("empty",               [],                0),   # guard, not a real input
    ("two_sorted",          [1, 2],            1),
    ("two_unsorted",        [2, 1],            0),
    ("negatives",           [-3, -1, -2, 0],   2),
    ("adjacent_pair_trap",  [3, 1, 2, 5],      1),
    ("big_dip_at_end",      [1, 2, 3, 0],      0),
    ("plateau_seam",        [1, 2, 2, 3],      3),
]


def run_table():
    print("test table")
    failures = 0
    for name, arr, expected in CASES:
        got = solution(list(arr))
        ok = got == expected
        failures += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<20} {arr}  ->  got {got}, want {expected}")
    return failures


def run_stress(trials=2000, max_n=9, lo=-3, hi=3):
    """Small arrays, tiny value range -> lots of duplicates and ties."""
    print(f"\nstress vs brute force  ({trials} trials, n<={max_n}, values {lo}..{hi})")
    for _ in range(trials):
        n = random.randint(1, max_n)
        arr = [random.randint(lo, hi) for _ in range(n)]
        fast, slow = solution(list(arr)), brute(list(arr))
        if fast != slow:
            print(f"  [FAIL] mismatch on {arr}: solution={fast}, brute={slow}")
            return 1
    print("  [PASS] no mismatches")
    return 0


def run_timing(n=100_000):
    print(f"\ntiming  (n={n:,})")
    arr = [random.randint(-10**9, 10**9) for _ in range(n)]
    t0 = time.perf_counter()
    result = solution(arr)
    elapsed = time.perf_counter() - t0
    print(f"  [{'PASS' if elapsed < 1.0 else 'SLOW'}] {elapsed*1000:.1f} ms, returned {result}")
    print("  (brute force here would be ~10^10 ops -> guaranteed TLE)")
    return elapsed >= 1.0


if __name__ == "__main__":
    random.seed(42)
    failures = run_table() + run_stress() + run_timing()
    print(f"\n{'ALL GREEN' if failures == 0 else str(failures) + ' FAILURE(S)'}")