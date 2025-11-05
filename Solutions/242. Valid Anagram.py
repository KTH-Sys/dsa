from typing import Dict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        U — Understand
        ----------------
        Determine whether s and t are anagrams:
        same multiset of characters (same letters with same counts), order irrelevant.

        M — Match
        ----------------
        Pattern: Arrays & Hashing (frequency counting).
        Tool: Two hash maps (dicts) mapping char -> count.

        P — Plan
        ----------------
        1) If lengths differ, return False.
        2) Build counts for s and t in one pass (two dicts).
        3) Return whether the two dicts are equal.
        """

        # I — Implement
        # ----------------
        # 1) Early length check (O(1))
        if len(s) != len(t):
            return False

        # 2) Build frequency maps
        countS = {}
        countT = {}

        # One pass through both strings (O(n))
        for i in range(len(s)):
            # Increment count for s[i]
            countS[s[i]] = 1 + countS.get(s[i], 0)
            # Increment count for t[i]
            countT[t[i]] = 1 + countT.get(t[i], 0)

        # 3) Compare maps (O(1) under lowercase-letters constraint)
        result = (countS == countT)

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - For each character, its count in s must equal its count in t.
        # - Dict equality checks exactly that.
        # - Length mismatch short-circuits obvious non-anagrams.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  (single pass + constant-time map compare over <=26 letters)
        # Space: O(1)  (at most 26 lowercase letters in each dict)
        return result
        