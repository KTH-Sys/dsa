class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        U — UNDERSTAND
            Count the number of CONTIGUOUS subarrays whose elements sum to
            exactly k. Return the count, not the subarrays themselves.
            Q: negatives allowed? Yes -- this rules out two pointers entirely
               (see M). Q: can k be 0 or negative? Yes, no special-casing
               needed, the algebra doesn't care about k's sign.
            Constraints: n up to ~2*10^4, values can be negative -- O(n^2) is
            borderline-risky, O(n) is the expected bar.

        M — MATCH
            First instinct off Sliding Window week: two pointers, expand
            right, shrink left when sum exceeds k. FAILS on [1,-1,1], k=1
            (true answer 3, pointer version returns 1) -- once l shrinks past
            an index, that state is gone forever, and negatives mean growing
            the window can DECREASE the sum, so there's no reliable direction
            to shrink or expand toward. Two pointers needs monotonic movement;
            negatives break that guarantee. Not a sliding window problem.

            Honest brute force: for every start i, walk forward summing until
            the end, checking against k. O(n^2) -- passes on small n, TLEs at
            n=10^4+. The waste: sum(i..j) and sum(i..j+1) share almost every
            term; brute force re-adds them from scratch for every new start.

            The fix: sum(i..j) = prefix[j+1] - prefix[i]. Want that == k, so
            rearranged: prefix[i] = prefix[j+1] - k. At each index the question
            becomes "how many earlier prefix sums equal running - k?" -- a
            LOOKUP against up to n prior values, not a recompute. A hash map
            answers "have I seen this exact value, how many times" in O(1),
            which is exactly what's needed and nothing more (no ordering
            queries required, so a hash map beats any sorted structure here).

        P — PLAN
            1. prefix_counts = {0: 1}  -- seed: empty prefix (sum 0) exists
               once, before any element is read. Without this, subarrays
               starting at index 0 are silently undercounted.
            2. prefix_sum = 0, total = 0
            3. for each num: prefix_sum += num
            4. total += prefix_counts[prefix_sum - k]   -- READ before WRITE
            5. prefix_counts[prefix_sum] += 1           -- register this sum
               Order matters: reading before writing prevents a subarray
               from counting itself against its own just-computed sum.
            6. return total

        I — IMPLEMENT
            (below)

        R — REVIEW
            [1,-1,1], k=1 (the sliding-window counterexample):
                seed {0:1}
                i=0 num=1  sum=1  key=0   hit=1  total=1  {0:1,1:1}
                i=1 num=-1 sum=0  key=-1  hit=0  total=1  {0:2,1:1,-1:0}
                i=2 num=1  sum=1  key=0   hit=2  total=3  {0:2,1:2,-1:0}
                -> 3, matches [1],[1,-1,1],[1]. Two pointers got this wrong;
                this doesn't.
            [1,2,3], k=3 -- clean case, no repeats:
                i=1: sum=3, key=0, hits seed -> [1,2]
                i=2: sum=6, key=3, hits i=1's insert -> [3]
                -> 2
            [3,4,7,2,-3,1,4,2], k=7 -- the repeated-prefix-sum case:
                prefix_sum returns to 14 at i=5 (first seen at i=2). The
                lookup at i=5 finds the count BEFORE this step's insert, so
                it correctly counts back to i=2's occurrence, not itself.
                -> 4, matches brute force exactly.

        E — EVALUATE
            Time  O(n): one pass, O(1) work per element (hash lookup/insert).
            Space O(n): up to one entry per distinct prefix sum -- PLUS a
              quirk if using defaultdict(int): a bracket READ on a missing
              key inserts it with value 0 (not just returns 0). Doesn't break
              correctness, but the dict can hold more keys than there are
              real prefix sums -- worth knowing if asked to justify the O(n)
              bound precisely, or if debugging by inspecting the dict directly.
            Optimal: every element must be read once to know any prefix sum,
              so O(n) is the floor. Same family as LC 525, 974, 1248 -- prefix
              sum + frequency map, distinct from this week's max/min seam
              pattern (Split-and-Sort, 915, 724) which never needed a map.
        """
        prefix_counts = defaultdict(int)
        prefix_counts[0] = 1            # empty prefix, sum 0, seen once
        prefix_sum = 0
        total = 0

        for num in nums:
            prefix_sum += num
            total += prefix_counts[prefix_sum - k]   # read first
            prefix_counts[prefix_sum] += 1           # then write

        return total