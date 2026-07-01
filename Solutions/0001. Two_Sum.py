'''U- Given a list of integers (nums) and a target value,
        find the indices of two numbers that add up to the target.
        Each input will have exactly one solution, and
        the same element cannot be used twice.

        Example:
        nums = [2,7,11,15], target = 9  →  Output: [0,1]
        Because nums[0] + nums[1] = 2 + 7 = 9
'''
#M - Pattern: Array + Hash Map (for constant-time lookups)
# We’ll store seen numbers in a hash map (dictionary)
'''P
 - Loop through each number along with its index (enumerate)
 - Calculate the complement of the target
 - If the complement is already in hashmap, we found the pair
 - Return both indices: earlier one from the map, current one from this iteration.
 - Otherwise: Otherwise store the current number and its index ,so it can be found by future numbers.
'''

#I-
from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Create an empty dictionary (hash map) to store previously seen numbers.
        # Key   = number value
        # Value = its index in the array
        prevMap = {}

        # Loop through each number in the list, along with its index.
        for i, n in enumerate(nums):
            # Calculate the complement that we need to reach the target.
            # Example: if target = 9 and n = 2, then diff = 7
            diff = target - n

            # If the complement has already been seen (stored in prevMap),
            # we can immediately return the pair of indices.
            if diff in prevMap:
                # prevMap[diff] gives the index of the earlier number,
                # and i is the index of the current number.
                return [prevMap[diff], i]

            # Otherwise, store the current number and its index in the hash map.
            # This will let us find it quickly later if its complement appears.
            # prevMap = { n: i }
            prevMap[n] = i

nums = [2, 7, 11, 15]
target = 9
sol = Solution()
print (sol.twoSum(nums,target))

# E – Evaluate
        # Time Complexity: O(n)
        #   – one pass through nums, hash lookup is O(1)
        # Space Complexity: O(n)
        #   – may store all elements in prevMap

# R – Review
        # The algorithm uses a single hash map to remember what we've seen.
        # It avoids double loops (O(n²)) by trading space for speed.
