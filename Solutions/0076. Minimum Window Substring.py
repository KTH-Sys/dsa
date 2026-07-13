class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        U — Understand
        ----------------
        Find the smallest substring of s that contains every character of t,
        including matching duplicate counts (if t has two 'a's, the window
        needs at least two 'a's too). Return "" if no such window exists.

        M — Match
        ----------------
        Pattern: Sliding Window with a GROW/SHRINK two-pointer (variable
        size), not a fixed-size window like Permutation in String.
        Track `have` (how many of t's DISTINCT characters are currently
        satisfied in the window) against `need` (how many distinct
        characters t requires). Expand right until have == need, then
        greedily shrink left as far as possible while it stays valid,
        recording the smallest valid window seen along the way.

        P — Plan
        ----------------
        1) Count each character's required frequency in t (countT), and
           set need = number of DISTINCT characters required.
        2) Walk r across s, adding s[r] to a running window count.
        3) Whenever a character's window count reaches EXACTLY its
           required count in countT, increment have.
        4) Whenever have == need, the window is currently valid — shrink
           from the left as far as possible while it stays valid,
           recording the smallest valid window seen so far each time.
        5) Return the smallest recorded window, or "" if none was found.
        """
        # I — Implement
        # ----------------

        # If `t` is empty, return an empty string.
        if t == "":
            return ""

        # Builds a dictionary counting how many times each character appears in `t`
        countT = {}
        for c in t:
            countT[c] = 1 + countT.get(c, 0)

        # `have` starts at 0. `need` is the number of keys in `countT`.
        have, need = 0, len(countT)

        # dictionary for character counts for the current window in `s`
        window = {}

        # `res` will store the [left, right] indices of the best (smallest)
        # valid window found so far. `resLen` tracks its length.
        res, resLen = [-1, -1], float("infinity")

        # window left edge at 0, `r` walks through every index of `s`,
        # one at a time. (the main loop)
        l = 0
        for r in range(len(s)):

            # Grabs the character currently at the right edge, and
            # increments its count in the `window` dictionary
            c = s[r]
            window[c] = 1 + window.get(c, 0)

            # Checks two things: (1) is this character one that `t`
            # actually needs at all, and (2) does the window's count for
            # it just now reach exactly the required amount? If both are
            # true, increment have
            if c in countT and window[c] == countT[c]:
                have += 1

            # Whenever the window currently contains everything `t`
            # requires, enter a shrink loop.
            while have == need:

                # Computes the current window's length (r - l + 1), and
                # if it's smaller than the best one recorded so far,
                # saves it as the new best.
                if (r - l + 1) < resLen:
                    res = [l, r]
                    resLen = r - l + 1

                # Removes the leftmost character from the window's count.
                # Checks whether removing that character just caused its
                # count to drop below what's required. If so, a
                # previously-satisfied requirement is now broken, so have
                # ticks down.
                window[s[l]] -= 1
                if s[l] in countT and window[s[l]] < countT[s[l]]:
                    have -= 1

                # Moves the left edge one step forward
                l += 1

        # Unpacks the best recorded window's indices, and returns that
        # substring — unless resLen is still infinity, meaning no valid
        # window was ever found, in which case return an empty string.
        l, r = res
        return s[l:r + 1] if resLen != float("infinity") else ""

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - `have` only increments when a count reaches EXACTLY the
        #   required value — extra duplicates beyond that don't
        #   re-trigger it, and it only decrements when a count drops
        #   BELOW the required value (checked via window[s[l]] < countT[s[l]]).
        # - The while loop always shrinks as far as validity allows before
        #   the next expansion, guaranteeing every valid window's minimal
        #   left edge is tested — no shorter valid window is skipped.
        # - res/resLen start as "nothing found yet" sentinels (infinity is
        #   guaranteed larger than any real window length), so the first
        #   valid window found is always recorded without special-casing.

        # E — Evaluate
        # ----------------
        # Time:  O(n + m)  — n = len(s), m = len(t). Each index of s is
        #        added to the window once (by r) and removed at most once
        #        (by l), so total pointer movement is O(n).
        # Space: O(m)  — countT and window store at most the distinct
        #        characters appearing in t (and briefly in s).