from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        """
        U — Understand
        ----------------
        Given n non-negative integers representing an elevation map (bar
        width = 1), compute how much rainwater is trapped after it rains.
        A bar traps water only if there's a wall at least as tall on BOTH
        its left and right — the trapped depth at any index is capped by
        whichever surrounding wall is SHORTER.

        M — Match
        ----------------
        Pattern: Two Pointers, converging from both ends.
        Brute force (O(n^2)): for each index, rescan the whole left side
        and right side to find both walls — wasteful, since each rescan
        throws away the previous index's work.
        Optimized (O(n) time, O(1) space): track a running left_max and
        right_max as two SCALARS instead of two full arrays, using two
        pointers that walk toward each other.
        Key insight: whichever pointer currently sees the SHORTER height
        is safe to finalize immediately — because the opposite wall is
        already guaranteed to be at least that tall, and anything still
        unexplored between the pointers can only make that wall taller,
        never shorter. You never need the opposite side's EXACT max, only
        confirmation that it's "tall enough."

        P — Plan
        ----------------
        1) Place `left` at index 0 and `right` at the last index.
        2) Track left_max and right_max as running maximums seen so far
           from each side, starting at 0.
        3) While left < right, compare height[left] and height[right]:
           - If height[left] is the smaller of the two, that side is the
             one that's safe to resolve: update left_max, add
             (left_max - height[left]) to the water total, move left
             inward.
           - Otherwise, do the mirrored operation on the right side.
        4) Return the accumulated water total once the pointers meet.
        """
        # I — Implement
        # ----------------
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        water = 0

        while left < right:
            if height[left] < height[right]:
                # Left side is shorter — safe to resolve its water now,
                # since the right wall is already guaranteed taller.
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                # Right side is shorter (or equal) — mirror the logic.
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1

        return water

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - At any point where height[left] < height[right], we know
        #   right_max (whatever it ends up being) is AT LEAST height[right],
        #   which is already > height[left]. Since left_max is the tallest
        #   wall seen so far on the left, min(left_max, right_max) for
        #   index `left` is guaranteed to be left_max — so
        #   water = left_max - height[left] is safe to finalize without
        #   ever computing the exact right_max.
        # - The mirrored case holds symmetrically when the right side is
        #   shorter or equal.
        # - Each index is visited by exactly one pointer exactly once, so
        #   every position's water contribution gets added precisely once.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — left and right pointers together traverse the
        #        array once; each index is processed exactly one time.
        # Space: O(1)  — only left_max, right_max, and water are scalars;
        #        no auxiliary arrays are needed (unlike the O(n)-space
        #        prefix/suffix array version).