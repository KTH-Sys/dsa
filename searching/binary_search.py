from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Perform binary search to find target in sorted nums.
        Returns index of target if found, else -1.
        Time Complexity: O(log n)
        Space Complexity: O(1)
        """
        low, high = 0, len(nums) - 1   # search boundaries

        while low <= high:             # loop until search window collapses
            mid = (low + high) // 2    # midpoint index
            guess = nums[mid]          # value at midpoint

            if guess == target:        # found target
                return mid
            elif guess > target:       # target is in left half
                high = mid - 1
            else:                      # target is in right half
                low = mid + 1

        return -1   # target not found

s = Solution()
print(s.search([-1,0,3,5,9,12], 9))   # Output: 4
print(s.search([-1,0,3,5,9,12], 2))   # Output: -1
