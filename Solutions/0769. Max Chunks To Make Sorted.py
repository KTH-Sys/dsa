class Solution:
    def maxChunksToSorted(self, arr: List[int]) -> int:
        """
        U — UNDERSTAND
            arr is a PERMUTATION of 0..n-1 (stated in constraints, load-bearing).
            Cut into chunks, sort each chunk, concatenate -> must equal sorted(arr).
            Return the max chunk count.
            Q: can chunks be empty? No, and max count means cut as often as legal.
            Q: duplicates? No -- that's LC 768, a different problem.
            Constraints: 1 <= n <= 10, values distinct in [0, n-1].
            Note: n is tiny here, but the O(n) solution is the same length as any
            hack, so don't let the small bound tempt you into brute force.

        M — MATCH
            Same seam invariant as LC 915 / Split-and-Sort:
                boundary after i is valid  iff  max(arr[0:i+1]) <= min(arr[i+1:])
            The permutation constraint collapses it. If the first i+1 elements
            occupy positions 0..i after sorting, they must be exactly the set
            {0..i}; with distinct values in [0, n-1], i+1 values whose max is i
            can only be that set. So the whole test reduces to:
                prefix_max == i
            No suffix array needed.

        P — PLAN
            1. Sweep left-to-right carrying prefix_max.
            2. Every i where prefix_max == i closes a chunk -> increment.
            3. i = n-1 always satisfies it (max of a full permutation is n-1),
               so the final mandatory boundary is counted automatically.

        I — IMPLEMENT
            (below)

        R — REVIEW
            [1,0,2,3,4]
                i=0 v=1 pmax=1  1==0 no
                i=1 v=0 pmax=1  1==1 YES -> 1
                i=2 v=2 pmax=2  YES -> 2
                i=3 v=3 pmax=3  YES -> 3
                i=4 v=4 pmax=4  YES -> 4   => [1,0][2][3][4]
            [4,3,2,1,0] -> pmax=4 from i=0, matches only at i=4 -> 1 chunk.
            [0] -> i=0, pmax=0, matches -> 1.
            Trap: prefix_max = 0 as the initializer is safe ONLY because values
            start at 0. In any non-permutation variant use float('-inf').

        E — EVALUATE
            Time  O(n), single pass.
            Space O(1), two scalars -- better than the O(n) suffix_min version,
            and only because the permutation removed the need for suffix data.
            LC 768 (duplicates, no permutation) loses this shortcut and goes back
            to prefix-max vs suffix-min, i.e. the Split-and-Sort sweep + 1.
        """
        chunks = 0
        prefix_max = 0

        for i, v in enumerate(arr):
            prefix_max = max(prefix_max, v)

            # first i+1 elements are exactly {0..i} -> safe to cut here
            if prefix_max == i:
                chunks += 1

        return chunks