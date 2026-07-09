class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """
        U — Understand
        ----------------
        Return True if s2 contains a contiguous substring that is a
        permutation of s1 (same letters, same counts, any order).
        Constraint assumed: lowercase English letters only.

        M — Match
        ----------------
        Pattern: Sliding Window + frequency counting (Valid Anagram's
        counting technique, reused inside a fixed-size window).
        Brute force (O(n*m)): rebuild the window's letter counts from
        scratch at every position — wasteful, since only 2 letters
        actually change (one slides out, one slides in) per shift.
        Optimized (O(n)): maintain ONE running count array for the
        window, updating just the sliding-in and sliding-out characters
        each step — plus a `matches` counter tracking how many of the
        26 letters currently have EQUAL counts between s1 and the
        window, so checking "is this a match" is an O(1) check
        (matches == 26) instead of comparing all 26 counts every time.

        P — Plan
        ----------------
        1) If s1 is longer than s2, no window could ever fit -> False.
        2) Build s1Count (fixed) and s2Count for the FIRST window of
           s2 (length len(s1)) — one-time O(m) setup.
        3) Compute `matches`: how many of the 26 letter positions
           already agree between s1Count and s2Count.
        4) Slide the window one step at a time across the rest of s2:
           - Before sliding, check if matches == 26 (found it).
           - Add the new right-edge character to s2Count; update
             `matches` by comparing ONLY that letter's before/after count.
           - Remove the old left-edge character from s2Count; update
             `matches` the same way for that letter.
        5) After the loop, do one final matches == 26 check (for the
           last window position, which the loop doesn't check inside it).
        """
        # I — Implement
        # ----------------
        if len(s1) > len(s2):
            return False

        s1Count = [0] * 26
        s2Count = [0] * 26

        # Build counts for s1 and the FIRST window of s2 in one pass
        for i in range(len(s1)):
            s1Count[ord(s1[i]) - ord('a')] += 1
            s2Count[ord(s2[i]) - ord('a')] += 1

        # Count how many of the 26 letters already match between the two
        matches = 0
        for i in range(26):
            if s1Count[i] == s2Count[i]:
                matches += 1

        # Slide the window across the rest of s2
        l = 0
        for r in range(len(s1), len(s2)):
            if matches == 26:
                return True

            # Character entering the window on the right
            index_r = ord(s2[r]) - ord('a')
            s2Count[index_r] += 1
            if s1Count[index_r] == s2Count[index_r]:
                matches += 1                    # case 1: counts now equal → gained a match
            elif s1Count[index_r] + 1 == s2Count[index_r]:
                matches -= 1                    # case 2: counts WERE equal, now off by one → lost a match

            # Character leaving the window on the left
            index_l = ord(s2[l]) - ord('a')
            s2Count[index_l] -= 1
            if s1Count[index_l] == s2Count[index_l]:
                matches += 1
            elif s1Count[index_l] - 1 == s2Count[index_l]:
                matches -= 1

            l += 1

        return matches == 26

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - matches only ever tracks EQUALITY at each of the 26 letter
        #   slots, so matches == 26 means every single letter count
        #   agrees between s1 and the window — exactly the definition
        #   of "the window is a permutation of s1."
        # - Each shift only changes 2 letters (one in, one out), so the
        #   matches counter only ever needs to re-examine those 2
        #   letters, never all 26 — this is what makes each shift O(1).
        # - The final `return matches == 26` after the loop covers the
        #   LAST window position, since the in-loop check only verifies
        #   matches BEFORE sliding to a new window, not after the final slide.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — n = len(s2); initial setup is O(m), then each
        #        of the remaining (n-m) window shifts does O(1) work
        # Space: O(1)  — two fixed 26-element arrays, independent of
        #        input size