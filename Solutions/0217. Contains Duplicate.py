class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # ============================
        # U — Understand
        # Goal: return True if any number appears twice.
        # Input constraints: up to 10^5 elements → need O(n) or O(n log n).
        # ============================

        # ============================
        # M — Match
        # Pattern: Hashing / HashSet
        # Reason: O(1) average lookup for duplicates.
        # ============================

        hashset = set()

        # ============================
        # P — Plan
        # Loop through nums:
        #   If n already seen → return True
        #   Else add n to set
        # End → return False
        # ============================

        for n in nums:
            if n in hashset:
                # Found a duplicate
                return True
            hashset.add(n)

        # No duplicates found
        return False

        # ============================
        # R — Review
        # Handles empty? Yes.
        # Handles negatives? Yes.
        # Handles large n? O(n) time, OK.
        # ============================

        # ============================
        # E — Evaluate
        # Time Complexity: O(n)
        #   - One pass
        #   - O(1) average lookup per element
        #
        # Space Complexity: O(n)
        #   - Worst case store all elements in the set
        # ============================
