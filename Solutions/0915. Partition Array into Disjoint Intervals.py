class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:
        """
        U — UNDERSTAND
            Split nums into left = nums[0:i], right = nums[i:], both non-empty.
            Every element of left must be <= every element of right.
            Return the smallest valid left length (= smallest valid i).
            Q: guaranteed to exist? Yes, problem states at least one valid split.
            Q: duplicates? Yes, and the condition is <=, so ties don't block a split.
            Q: negatives? Yes. Constraints: 2 <= n <= 1e5, so O(n^2) is out.

        M — MATCH
            "Every left elem <= every right elem" collapses to a seam condition:
                max(nums[0:i]) <= min(nums[i:])
            Prefix-aggregate / suffix-aggregate sweep. Same family as LC 238
            (prefix/suffix products) and the Split-and-Sort OA problem, which
            counts these boundaries instead of returning the first.

        P — PLAN
            1. suffix_min[i] = min of nums[i:], built right-to-left in one pass.
            2. Sweep left-to-right carrying left_max = max of nums[0:i+1].
            3. First i where left_max <= suffix_min[i+1] -> return i + 1.
            Right-to-left pass must finish before the left-to-right sweep starts,
            since step 2 reads suffix data that is ahead of it.

        I — IMPLEMENT
            (below)

        R — REVIEW
            [5,0,3,8,6] -> suffix_min = [0,0,3,6,6]
                i=0: left_max=5, suffix_min[1]=0  5<=0 no
                i=1: left_max=5, suffix_min[2]=3  5<=3 no
                i=2: left_max=5, suffix_min[3]=6  5<=6 YES -> return 3
            Edge n=2: suffix loop is empty, main loop runs once at i=0. OK.
            Edge all-equal [1,1,1]: hits at i=0, returns 1. OK.
            Trap: checking only nums[i-1] <= nums[i] is wrong -- [3,1,2,5] at
            i=2 passes adjacency (1<=2) but max(left)=3 > min(right)=2.

        E — EVALUATE
            Time  O(n): two independent linear passes.
            Space O(n): the suffix_min array.
            Can be reduced to O(1) space with the two-maxima one-pass variant
            (track committed left_max and running cur_max, extend on
            nums[i] < left_max). Same O(n) time, strictly better space.
        """
        n = len(nums)

        # suffix_min[i] = min(nums[i:]) -- must be built right-to-left
        suffix_min = [0] * n
        suffix_min[-1] = nums[-1]

        for i in range(n - 2, -1, -1):
            suffix_min[i] = min(nums[i], suffix_min[i + 1])

        left_max = nums[0]

        # split after index i, so left has length i + 1
        for i in range(n - 1):
            left_max = max(left_max, nums[i])

            if left_max <= suffix_min[i + 1]:
                return i + 1