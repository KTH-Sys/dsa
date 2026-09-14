def solution(A):
    """
    MINIMUM ABSOLUTE SUM  -  Google OA (intern / new grad)

    PROBLEM
        You are given an array A of N integers. Choose at most one element and
        multiply it by -1, so that the sum of the resulting array is as close to
        zero as possible. Return that minimum absolute sum.

        Example: A = [1, 3, 2, 5]  ->  1
            The total is 11. Negating 5 brings it to 1, which is the closest to
            zero any single flip can get.
    U — UNDERSTAND
        Choose AT MOST ONE element and multiply it by -1.
        Return the minimum possible |sum| of the resulting array.
        "At most one" => doing nothing is a legal choice, so |sum(A)| is a
        candidate answer and the array is never forced to change.
        Q: negatives in A? Yes -- flipping a negative makes it positive.
        Q: empty A? sum([]) == 0, answer 0. Loop is skipped, no crash.
        Q: N size? Assume up to 1e5, so O(N^2) is out.

    M — MATCH
        No data structure needed. The key algebra: flipping x removes x and
        adds -x, so the new total is
            S - x + (-x) = S - 2x
        No re-summing per candidate. That makes each of the N+1 options
        (flip each element, or flip nothing) O(1) to evaluate, so plain
        enumeration is already optimal.

        Trap: |S - 2x| is smallest when x is closest to S/2, which tempts a
        sort + binary search for S/2. That is O(N log N) -- strictly worse.
        Binary search only pays when the search space is bigger than the
        array; here the candidate set IS the array.

        Name collision: Codility's "MinAbsSum" lets you flip ANY SUBSET and is
        a subset-sum DP, O(N * sum). Different problem. "At most one" is the
        word doing all the work.

    P — PLAN
        1. total = sum(A)                      -- one pass
        2. best = abs(total)                   -- the no-flip candidate
        3. for each num: best = min(best, abs(total - 2*num))
        4. return best

    R — REVIEW
        [1,3,2,5] total=11
            no flip -> 11
            1 -> |11-2|=9   3 -> |11-6|=5   2 -> |11-4|=7   5 -> |11-10|=1
            => 1  (matches expected)
        [10,1] total=11 -> |11-20|=9, |11-2|=9, no-flip 11 => 9
            WITHOUT abs() this returns -9. That is the bug this line guards.
        [3,-3] total=0 -> no-flip wins with 0; every flip gives 6.
        [-1,-3] total=-4 -> flip -3: |-4+6|=2 => 2

    E — EVALUATE
        Time  O(N): one pass to sum, one pass to scan candidates.
        Space O(1): two scalars.
        Optimal -- every element must be read at least once to know the sum.
    """
    total = sum(A)
    best = abs(total)                  # candidate: flip nothing

    for num in A:
        # num -> -num  means  total - num + (-num)  ==  total - 2*num
        newSum = total - (2 * num)
        best = min(best, abs(newSum))  # abs() is load-bearing, see REVIEW

        # I — IMPLEMENT: single sweep, no sort, no auxiliary array

    return best