from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        U — Understand
        ----------------
        Given a sorted array `numbers`, find two distinct elements whose sum equals `target`.
        Return their indices using 1-based indexing.
        Exactly one valid solution exists.

        M — Match
        ----------------
        Pattern: Two Pointers
        Why: The array is sorted, so we can use left/right pointers to
        increase or decrease the sum deterministically in O(n) time.

        P — Plan
        ----------------
        1) Initialize two pointers:
           - left at the start (smallest value)
           - right at the end (largest value)
        2) While left < right:
           - Compute current sum = numbers[left] + numbers[right]
           - If sum is too large, move right pointer left
           - If sum is too small, move left pointer right
           - If sum equals target, return indices (1-based)
        3) Return empty list as a defensive fallback (though problem guarantees a solution)

        I — Implement
        ----------------
        """

        l, r = 0, len(numbers) - 1

        while l < r:
            currSum = numbers[l] + numbers[r]

            if currSum > target:
                # Sum too large → decrease by moving right pointer left
                r -= 1
            elif currSum < target:
                # Sum too small → increase by moving left pointer right
                l += 1
            else:
                # Found the exact target sum
                return [l + 1, r + 1]  # convert to 1-based indexing

        # E — Evaluate
        # ----------------
        # Time Complexity: O(n)
        #   - Each pointer moves at most n times
        # Space Complexity: O(1)
        #   - No extra data structures used

        # R — Review
        # ----------------
        # This solution relies on the sorted property of the input.
        # Two pointers allow us to eliminate impossible pairs efficiently.
        # Returning immediately avoids unnecessary iterations.

        return []  # defensive fallback
