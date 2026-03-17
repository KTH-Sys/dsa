class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # U — Understand
        # We need the maximum sum of any contiguous subarray.
        # Contiguous means elements must stay next to each other.

        # M — Match Pattern
        # This is Kadane's Algorithm.
        # Pattern: DP over array where we track the best sum ending at each index.

        # P — Plan
        # 1. Let current_sum = best subarray sum ending at current index.
        # 2. Let max_sum = best subarray sum seen overall.
        # 3. For each number:
        #       either start new subarray at this number
        #       or extend previous subarray
        # 4. Update global maximum.

        # I — Implement
        current_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            # Either start fresh from num,
            # or extend the previous subarray.
            current_sum = max(num, current_sum + num)

            # Track the best answer seen so far.
            max_sum = max(max_sum, current_sum)

        # R — Review
        # Handles all-negative arrays correctly because we initialize
        # from nums[0], not 0.

        # E — Evaluate
        # Time: O(n)
        # Space: O(1)
        return max_sum