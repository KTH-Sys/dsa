class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """
        U — Understand
        ----------------
        Find all UNIQUE triplets [a, b, c] in nums such that a+b+c == 0.
        No duplicate triplets in the result, even if the same values
        appear at different indices.

        M — Match
        ----------------
        Pattern: Sort + Two Pointers, built on top of the "Two Sum II
        (sorted array)" pattern. Fix one number as an anchor, then use
        two pointers to find pairs in the remainder that sum to the
        negation of the anchor. Sorting ALSO makes duplicate-skipping
        trivial, since equal values become adjacent.

        P — Plan
        ----------------
        1) Sort nums. This enables both the two-pointer technique and
           cheap duplicate detection.
        2) For each index i (the anchor):
           - If nums[i] > 0, no triplet is possible (smallest number in
             the remaining sorted suffix is already positive) -> break.
           - If nums[i] equals the previous anchor, skip it (avoids
             duplicate triplets starting with the same first value).
        3) Set l = i+1, r = len(nums)-1. While l < r:
           - If the three-sum is too big, move r left (shrink toward
             smaller values).
           - If too small, move l right (grow toward larger values).
           - If exactly zero, record the triplet, then move BOTH
             pointers inward, skipping over any duplicate values at the
             new l and r positions before the next comparison.
        """
        # I — Implement
        # ----------------
        nums.sort()
        res = []

        for i in range(len(nums)):
            # No valid triplet possible once the anchor itself is positive
            if nums[i] > 0:
                break

            # Skip duplicate anchors (adjacent after sorting)
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = nums[i] + nums[l] + nums[r]

                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    # Skip duplicate values on the left pointer's new position
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Sorting guarantees: if nums[i] > 0, every number from i onward
        #   is also >= nums[i] > 0, so no three of them can sum to 0 ->
        #   safe to break entirely, not just skip this i.
        # - Skipping i when nums[i]==nums[i-1] avoids re-finding the exact
        #   same set of triplets that anchor already produced.
        # - After recording a match, advancing l and r past duplicates
        #   prevents the same (l,r) VALUES from producing a duplicate
        #   triplet with the same anchor.

        # E — Evaluate
        # ----------------
        # Time:  O(n^2)  — O(n log n) sort + O(n) outer loop, each with an
        #        O(n) two-pointer sweep inside
        # Space: O(1) to O(n) — depends on sort implementation; output
        #        space for res not counted as extra