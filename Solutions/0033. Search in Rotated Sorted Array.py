class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        U — Understand
        ----------------
        Given a rotated sorted array (originally ascending, then rotated
        at some unknown pivot) with all unique elements, find the index
        of `target`. Return -1 if it doesn't exist. Must run in O(log n).

        M — Match
        ----------------
        Pattern: Modified Binary Search. Like Find Minimum in Rotated
        Sorted Array, the array is made of two sorted runs joined at a
        rotation point. At every step, ONE of the two halves (l..mid or
        mid..r) is guaranteed to be a clean, unbroken sorted run — the
        other half contains the rotation break. Identify which half is
        clean, then check if target could possibly live in that clean
        half's value range; if so search there, otherwise search the
        other (broken) half.

        P — Plan
        ----------------
        1) Standard binary search skeleton: l=0, r=len(nums)-1.
        2) At each step, compute mid. If nums[mid] is the target, return
           mid immediately.
        3) Determine which side is the "clean" (unbroken sorted) half:
           - If nums[l] <= nums[mid], the LEFT half (l..mid) is clean.
           - Otherwise, the RIGHT half (mid..r) is clean.
        4) If the left half is clean:
           - If target falls WITHIN nums[l]..nums[mid]'s range, search
             left (r = mid-1).
           - Otherwise, target must be in the right half -> search
             right (l = mid+1).
        5) If the right half is clean, do the mirrored check.
        6) If the loop ends without finding target, return -1.
        """
        # I — Implement
        # ----------------
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2

            # Found it — return immediately
            if target == nums[mid]:
                return mid

            # Determine which half is the "clean" sorted run
            if nums[l] <= nums[mid]:
                # LEFT half (l..mid) is sorted with no rotation break
                if target > nums[mid] or target < nums[l]:
                    # target is OUTSIDE the clean left half's range,
                    # so it must be in the right half
                    l = mid + 1
                else:
                    # target IS within the left half's range
                    r = mid - 1
            else:
                # RIGHT half (mid..r) is sorted with no rotation break
                if target < nums[mid] or target > nums[r]:
                    # target is OUTSIDE the clean right half's range,
                    # so it must be in the left half
                    r = mid - 1
                else:
                    # target IS within the right half's range
                    l = mid + 1

        # Loop ended without finding target
        return -1

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - "nums[l] <= nums[mid]" reliably detects an unbroken sorted
        #   left half: if the rotation break were inside l..mid, the
        #   values would DROP somewhere in that range, making nums[l]
        #   greater than nums[mid] — so this comparison being true
        #   guarantees no break exists between l and mid.
        # - Once a half is known to be clean/sorted, a simple range
        #   check (target compared against that half's min and max)
        #   correctly determines whether target COULD be hiding there —
        #   if target is outside that range, it's impossible for it to
        #   be in the clean half, so the other (broken) half must be
        #   searched instead.
        # - Every iteration eliminates at least half the remaining
        #   search space, exactly like standard binary search.

        # E — Evaluate
        # ----------------
        # Time:  O(log n) — each step discards roughly half the
        #        remaining search space
        # Space: O(1) — only a few scalar variables (l, r, mid)