class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:

        #if length of hashset is less than list, duplicate exist
        return len(set(nums)) < len(nums)