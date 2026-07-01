from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        U — Understand
        ----------------
        Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]]
        such that:
            i != j != k
            nums[i] + nums[j] + nums[k] == 0
        The output must not contain duplicate triplets.

        M — Match
        ----------------
        Pattern: Sort + Two Pointers
        Reason:
        - After sorting, we can fix one number nums[i] and use two pointers (l, r)
          to find pairs that sum to -nums[i] in linear time.
        - Sorting also helps skip duplicates efficiently.

        P — Plan
        ----------------
        1) Sort nums.
        2) Loop i from 0 to n-3:
           - Skip duplicates for i.
           - If nums[i] > 0, break early (can't sum to 0).
        3) For each i:
           - Set l = i+1, r = n-1
           - While l < r:
             - Compute total = nums[i] + nums[l] + nums[r]
             - If total < 0, move l right (need bigger sum)
             - If total > 0, move r left (need smaller sum)
             - If total == 0, record triplet and skip duplicates for l and r
        4) Return the collected triplets.

        I — Implement
        ----------------
        """

        nums.sort()
        res: List[List[int]] = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicate "first" numbers to avoid duplicate triplets
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # If the current number is > 0, then all numbers to the right are >= it,
            # so the sum cannot be 0 anymore.
            if nums[i] > 0:
                break

            l, r = i + 1, n - 1

            while l < r:
                total = nums[i] + nums[l] + nums[r]

                if total < 0:
                    # Need a larger sum -> move left pointer right
                    l += 1
                elif total > 0:
                    # Need a smaller sum -> move right pointer left
                    r -= 1
                else:
                    # Found a valid triplet
                    res.append([nums[i], nums[l], nums[r]])

                    # Move both pointers inward
                    l += 1
                    r -= 1

                    # Skip duplicates on the left pointer
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1

                    # Skip duplicates on the right pointer
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1

        # E — Evaluate
        # ----------------
        # Time Complexity: O(n^2)
        #   - Sorting: O(n log n)
        #   - Outer loop runs O(n)
        #   - Inner two-pointer scan runs O(n) per i in worst case
        #   => O(n^2) dominates
        #
        # Space Complexity: O(1) extra (excluding output)
        #   - Sorting may use O(log n) stack depending on implementation
        #   - Result list is output space

        # R — Review
        # ----------------
        # - Sorting enables two-pointer search and duplicate skipping.
        # - Duplicate handling is essential: skip repeated i, and skip repeated l/r after finding a triplet.
        # - Early break when nums[i] > 0 improves performance.

        return res