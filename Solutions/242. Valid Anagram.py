from typing import Dict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        U — Understand
        ----------------
        Determine whether s and t are anagrams:
        same multiset of characters (same letters with same counts), order irrelevant.
        Constraint assumed: both strings contain only lowercase English letters (a-z).

        M — Match
        ----------------
        Pattern: Arrays & Hashing (frequency counting), optimized with a fixed-size array.
        Tool: Single array of size 26 acting as a combined counter for both strings.

        P — Plan
        ----------------
        1) If lengths differ, return False.
        2) Walk both strings by index, incrementing the count for s[i] and
           decrementing the count for t[i] in the same array slot.
        3) Scan the array — if any slot is nonzero, the strings aren't anagrams.
           If every slot is 0, they are.
        """
        # I — Implement
        # ----------------
        # 1) Early length check (O(1))
        if len(s) != len(t):
            return False

        # 2) Single array tracks net frequency difference per letter
        count = [0] * 26

        # One pass through both strings by index (O(n))
        for i in range(len(s)):
            # Increment for s's character
            count[ord(s[i]) - ord('a')] += 1
            # Decrement for t's character
            count[ord(t[i]) - ord('a')] -= 1

        # 3) Check that every letter's net count balanced out to zero
        for n in count:
            if n != 0:
                return False
        return True

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Each letter has one slot; +1 for appearing in s, -1 for appearing in t.
        # - If s and t are anagrams, every letter's contributions cancel to 0.
        # - If any letter's count is nonzero, s and t disagree on that letter's frequency.
        # - Length mismatch short-circuits obvious non-anagrams before the scan.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  (single pass to build counts + O(26) pass to verify, n = len(s))
        # Space: O(1)  (fixed 26-element array, independent of input size)
        
