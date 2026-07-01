class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # ============================
        # U — Understand
        # We need the length of the longest sequence of consecutive integers.
        # Example: [100, 4, 200, 1, 3, 2] → longest = 1,2,3,4 → length = 4
        # Constraints allow up to 10^5 elements → need O(n).
        # ============================

        # ============================
        # M — Match
        # Pattern: HashSet for O(1) membership checks.
        # Key trick: Only start counting at the *beginning* of a sequence
        # (i.e., when num-1 is NOT in the set).
        # ============================

        # Convert list to set for O(1) lookups
        numSet = set(nums)

        # Tracks longest streak
        longest = 0

        # ============================
        # P — Plan
        # 1. Loop through each num in the set.
        # 2. If num-1 not in set → num is the start of a sequence.
        #    - Then expand from num upward: num+1, num+2, ...
        #    - Count how long the streak is.
        # 3. Update longest streak.
        # ============================

        for num in numSet:

            # Check if this is the start of a sequence
            if (num - 1) not in numSet:

                length = 1      # Current streak length
                curr = num      # Current number in streak

                # Extend the streak forward
                while (curr + 1) in numSet:
                    curr += 1
                    length += 1

                # Update global max
                longest = max(longest, length)

        # Return the final answer
        return longest

        # ============================
        # R — Review
        # - Handles duplicates naturally because set removes repeats.
        # - Each sequence is counted exactly once.
        # - No repeated scanning like the O(n^2) brute force solution.
        # ============================

        # ============================
        # E — Evaluate
        # Time Complexity: O(n)
        #   - Each number is considered once, and each chain grows only once.
        #
        # Space Complexity: O(n)
        #   - For storing the set of numbers.
        # ============================