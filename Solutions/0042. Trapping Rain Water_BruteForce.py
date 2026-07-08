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
        Pattern: Brute force / direct simulation.
        For each index, directly answer the question "what's the tallest
        wall to my left, and what's the tallest wall to my right?" by
        scanning the array from scratch every time. No precomputation,
        no running totals — just the most literal translation of the
        problem statement into code.

        P — Plan
        ----------------
        1) For each index i, find left_wall = the tallest bar anywhere
           from index 0 up to and including i.
        2) Find right_wall = the tallest bar anywhere from index i to
           the end of the array.
        3) The water level at i is capped by the SHORTER of these two
           walls: min(left_wall, right_wall).
        4) Water trapped at i = that water level minus the bar's own
           height at i (the bar itself already fills part of that space).
        5) Sum water across every index.
        """
        # I — Implement
        # ----------------
        n = len(height)
        total = 0

        for i in range(n):
            # Rescan everything to the left (including i) for the tallest wall
            left_wall = max(height[0:i + 1])
            # Rescan everything to the right (including i) for the tallest wall
            right_wall = max(height[i:n])

            # Water level capped by the shorter wall, minus the bar's own height
            total += min(left_wall, right_wall) - height[i]

        return total

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - left_wall and right_wall both INCLUDE height[i] itself, so
        #   min(left_wall, right_wall) is always >= height[i] — the
        #   subtraction never goes negative.
        # - Every index is checked independently and directly against the
        #   problem's own definition of "trapped water" — there's no
        #   derived shortcut here, which is exactly why this version is
        #   easy to trust as a correctness baseline, even though it's slow.

        # E — Evaluate
        # ----------------
        # Time:  O(n^2)
        #   - For each of the n indices, max(height[0:i+1]) costs O(i) and
        #     max(height[i:n]) costs O(n-i) — these slices are RESCANNED
        #     from scratch every iteration, with no memory of prior work.
        #   - Summed across all n indices, this totals roughly O(n^2).
        # Space: O(n)
        #   - Each height[0:i+1] and height[i:n] call creates a NEW slice
        #     (a copy) before max() runs on it — so this isn't even O(1)
        #     space per call, unlike the optimized versions.