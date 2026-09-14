class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        """
        U — UNDERSTAND
            Find the leftmost index i where sum(nums[:i]) == sum(nums[i+1:]).
            nums[i] itself belongs to neither side. Return -1 if none exists.
            Q: can a side be empty? Yes -- sum of an empty slice is 0, and that
               counts as a valid match (e.g. [2,1,-1] pivots at i=0).
            Q: negatives? Yes -- sums aren't monotonic, so no early exit is
               possible; every index must be checked.
            Q: empty nums? Loop never runs, falls through to -1. No crash.

        M — MATCH
            Running prefix sum + a known total. If left = sum(nums[:i]), then
            right is never its own pass -- it's just whatever's left over:
                total = left + nums[i] + right  =>  right = total - left - nums[i]
            Same family as Split-and-Sort / LC 915: one running left-to-right
            aggregate, no suffix array needed here because sum (unlike max/min)
            can be derived from the total instead of precomputed backwards.

        P — PLAN
            1. total = sum(nums)          -- one pass
            2. left = 0
            3. for each i: derive right, compare to left, return i on match
            4. left += nums[i]  -- AFTER the check, since nums[i] is excluded
               from left at index i. Do this before the check and every
               answer shifts by one.
            5. no match anywhere -> return -1

        I — IMPLEMENT
            (below)

        R — REVIEW
            [1,7,3,6,5,6] total=28
                i=0 left=0  right=28-0-1=27   no   left->1
                i=1 left=1  right=28-1-7=20   no   left->8
                i=2 left=8  right=28-8-3=17   no   left->11
                i=3 left=11 right=28-11-6=11  YES -> return 3
            [2,1,-1] total=2, i=0: right=2-0-2=0, left=0  -> match at i=0
                (empty left side, legal)
            [-1,-1,-1,-1,-1,0] total=-4
                i=2: left=-2, right=-4-(-2)-(-1)=-1... trace confirms match at i=2
            [] -> loop skipped -> -1
            [1,2,3] -> no i satisfies it -> -1

        E — EVALUATE
            Time  O(n): single pass, sum() is also O(n) but separate.
            Space O(1): two scalars, no suffix array -- better than 915/
              Split-and-Sort because sum decomposes additively; max/min do not.
        """
        total = sum(nums)
        left = 0

        for i in range(len(nums)):
            right = total - left - nums[i]

            # at pivot i: total == left + nums[i] + right
            if left == right:
                return i

            left += nums[i]  # must happen AFTER the check -- see PLAN step 4

        return -1