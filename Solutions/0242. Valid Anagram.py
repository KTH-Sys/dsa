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
        Tool: Two hash maps (dicts) mapping char -> count, built in a
        single pass over both strings simultaneously.

        P — Plan
        ----------------
        1) If lengths differ, return False immediately (can't be
           anagrams if they don't even have the same number of characters).
        2) Build countS and countT in one pass, using each character
           itself as the dictionary key.
        3) Return whether the two dicts are equal.
        """
        # I — Implement
        # ----------------
        if len(s) != len(t):
            return False

        countS, countT = {}, {}
        for i in range(len(s)):
            # Increment count for s[i] — .get(s[i], 0) looks up the SAME
            # key we're about to write to, so repeats correctly accumulate
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)

        return countS == countT

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - For each character, its count in s must equal its count in t.
        # - Dict equality checks exactly that — Python compares dicts by
        #   key-value pairs, not by insertion order, so {'a':2,'b':1} ==
        #   {'b':1,'a':2} correctly evaluates to True.
        # - Using s[i]/t[i] (the character itself) as the key, consistently
        #   for both the read (.get) and the write, guarantees every
        #   repeat of a character finds and increments its own existing
        #   count rather than colliding with an unrelated key or never
        #   being found at all.
        # - Length mismatch short-circuits obvious non-anagrams before
        #   any counting work happens.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — single pass building both dicts, O(1) dict
        #        equality check afterward (bounded by alphabet size)
        # Space: O(1)  — at most 26 lowercase letters in each dict,
        #        independent of input length n