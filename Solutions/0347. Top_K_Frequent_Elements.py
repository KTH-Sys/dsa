
def topKFrequent(self, nums: List[int], k: int) -> List[int]:
    # U — Understand
    # Input: list of integers nums, integer k
    # Output: k elements that appear most frequently in nums
    # Constraint: must be faster than O(n log n), order does not matter

    # M — Match
    # This problem matches the "bucket sort by frequency" pattern:
    # - Count occurrences with a hash map
    # - Use index = frequency to group numbers
    # - Traverse from highest frequency downward

    # P — Plan
    # 1. Build frequency map: number -> count
    # 2. Create buckets where index represents frequency
    # 3. Place each number into its frequency bucket
    # 4. Iterate buckets from high to low, collecting elements until k is reached

    # I — Implement
    fMap = {}                                   # frequency map
    bucket = [[] for i in range(len(nums) + 1)]# bucket[i] holds nums with freq = i

    for key in nums:                            # count frequencies
        fMap[key] = 1 + fMap.get(key, 0)
    
    for key, val in fMap.items():               # distribute into buckets
        bucket[val].append(key)

    result = []
    for i in range(len(bucket) - 1, 0, -1):     # scan from highest frequency
        for n in bucket[i]:
            result.append(n)
            if len(result) == k:                # stop once k elements collected
                return result

    # R — Review
    # - Buckets guarantee grouping by frequency
    # - Reverse traversal ensures highest frequency first
    # - Early return avoids unnecessary work

    # E — Evaluate
    # Time Complexity: O(n)
    #   - O(n) to count
    #   - O(n) to traverse buckets
    # Space Complexity: O(n)
    #   - Hash map + bucket array

