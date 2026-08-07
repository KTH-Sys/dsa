class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        U — Understand
        ----------------
        Given a rotated sorted array (originally ascending, then rotated
        at some unknown pivot) with all unique elements, find the
        minimum value in O(log n) time.

        M — Match
        ----------------
        Pattern: Modified Binary Search. The array isn't globally sorted,
        but it's made of two sorted runs joined at the rotation point.
        Compare nums[m] to nums[r] to determine which half currently
        contains the "break" (and therefore the minimum).

        P — Plan
        ----------------
        1) Set l=0, r=len(nums)-1, and track the running minimum found.
        2) While l <= r:
           - Compute m as the midpoint.
           - If nums[l] <= nums[r], this SUBARRAY is already fully
             sorted (no rotation break inside it) — nums[l] is the
             smallest value in this range; update result and stop early.
           - Otherwise, compare nums[m] to nums[r]:
             - If nums[m] > nums[r], the break is to the right of m,
               so search l = m+1 onward.
             - Else, the break is at or before m, so search up to r=m-1
               (m itself might be the answer, but nums[m] gets recorded
               as a candidate minimum before narrowing).
        3) Return the smallest value discovered across all narrowing steps.
        """
        # I — Implement
        # ----------------
        l, r = 0, len(nums) - 1
        result = nums[0]

        while l <= r:
            # If this slice is already sorted, its first element IS the
            # minimum of the slice — no need to search further within it.
            if nums[l] <= nums[r]:
                result = min(result, nums[l])
                break

            m = l + ((r - l) // 2)
            result = min(result, nums[m])

            if nums[m] >= nums[l]:
                # Left half (l..m) is sorted and doesn't contain the
                # break, so the break (and true min) is to the right.
                l = m + 1
            else:
                # nums[m] < nums[l] means the break is at or before m,
                # so narrow into the left half.
                r = m - 1

        return result

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - "nums[l] <= nums[r]" being true means the CURRENT search
        #   range has no rotation break inside it (it's a clean ascending
        #   run), so its first element is trivially its minimum.
        # - Comparing nums[m] to nums[l] (not nums[r]) determines which
        #   side of m the break sits on: if nums[m] >= nums[l], the left
        #   portion (l..m) is itself sorted (no break there), so the
        #   break must be strictly after m.
        # - result is updated with every midpoint visited, so even
        #   though the search space shrinks, no candidate minimum is
        #   ever missed.

        # E — Evaluate
        # ----------------
        # Time:  O(log n) — each step discards roughly half the
        #        remaining search space
        # Space: O(1) — only a few scalar variables