from typing import List

class Solution:
    def maxArea(self, heights: List[int]) -> int:
        """
        U — Understand
        ----------------
        We are given an array where each value represents the height of a vertical line.
        Two lines form a container that can hold water.
        The amount of water is determined by:
            area = min(height[left], height[right]) * (right - left)
        We must find the maximum possible area.

        M — Match
        ----------------
        Pattern: Two Pointers
        Reason:
        - The width depends on distance between pointers
        - The height is limited by the shorter line
        - A sorted-like structure (indices from left to right) allows greedy pointer movement

        P — Plan
        ----------------
        1) Start with the widest container: left at 0, right at n-1
        2) Compute area using current pointers
        3) Move the pointer pointing to the shorter line
           - Moving the taller line cannot increase area
        4) Repeat until pointers meet
        5) Track and return the maximum area found

        I — Implement
        ----------------
        """

        # Initialize two pointers at the ends
        l, r = 0, len(heights) - 1

        # Store the maximum area found
        res = 0

        # Continue while there is width between pointers
        while l < r:
            # Calculate current container area
            area = min(heights[l], heights[r]) * (r - l)

            # Update maximum area
            res = max(res, area)

            # Move the pointer at the shorter height
            # Reason: area is limited by the shorter wall
            if heights[l] <= heights[r]:
                l += 1
            else:
                r -= 1

        # E — Evaluate
        # ----------------
        # Time Complexity: O(n)
        #   - Each pointer moves at most n times total
        # Space Complexity: O(1)
        #   - Only constant extra variables used

        # R — Review
        # ----------------
        # The greedy choice of moving the shorter pointer is correct because:
        # - Width always decreases
        # - Only increasing the limiting height can improve area
        # This guarantees all optimal candidates are explored in linear time.

        return res
