from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        """
        U — Understand
        ----------------
        Given n non-negative integers representing an elevation map where
        the width of each bar is 1, compute how much rainwater can be
        trapped after it rains.
        Key insight: water sits on top of a bar only if there's a TALLER
        (or equal) wall on BOTH its left and right — the water level at
        any position is capped by whichever of those two walls is shorter.

        M — Match
        ----------------
        Pattern: Prefix / Suffix arrays — the exact same shape as Product
        of Array Except Self. Instead of prefix/suffix PRODUCTS, track
        prefix/suffix MAXIMUMS.
        Formula: water[i] = min(leftMax[i], rightMax[i]) - height[i]
        (clipped at 0, since a bar taller than both walls holds no water).

        P — Plan
        ----------------
        1) Build left_max[i] = tallest bar from index 0 to i (inclusive),
           via a single left-to-right pass.
        2) Build right_max[i] = tallest bar from index i to n-1 (inclusive),
           via a single right-to-left pass.
        3) For each index, the water level is capped by the SHORTER of its
           two surrounding walls: min(left_max[i], right_max[i]).
        4) Water trapped at i = that capped level minus the bar's own
           height (never negative, since a bar can't be taller than its
           own value in either max array).
        5) Sum water across all indices.
        """
        # I — Implement
        # ----------------
        if not height:
            return 0

        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        # Pass 1: tallest wall seen so far, walking left to right
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Pass 2: tallest wall seen so far, walking right to left
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Pass 3: water at each index is capped by the shorter wall
        water = 0
        for i in range(n):
            water += min(left_max[i], right_max[i]) - height[i]

        return water

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - left_max[i] and right_max[i] both INCLUDE height[i] itself, so
        #   min(left_max[i], right_max[i]) is always >= height[i] — the
        #   subtraction never goes negative.
        # - A bar can only hold water up to the height of its shorter
        #   surrounding wall; anything above that would simply overflow
        #   off that shorter side.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — three linear passes over height
        # Space: O(n)  — two auxiliary arrays of size n
        # (A two-pointer variant collapses this to O(1) space — see below)