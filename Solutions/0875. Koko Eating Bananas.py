import math

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        U — Understand
        ----------------
        Koko eats at a fixed speed k bananas/hour. Each hour she works on
        ONE pile, eating min(k, what's left) — leftover time in the hour
        is wasted. Find the SMALLEST k that finishes all piles within h
        hours. Hours for a pile = ceil(pile / k).

        M — Match
        ----------------
        Pattern: Binary Search on the ANSWER space (not on an input
        array). The key property is monotonicity: if speed k works, every
        speed above k also works — so "does this speed fit?" forms a
        sorted False...False True...True pattern, which binary search can
        cut in half each step.
        Search range: 1 (slowest) to max(piles) (fastest worth trying,
        since one-pile-per-hour means faster than the biggest pile
        changes nothing).

        P — Plan
        ----------------
        1) Set l = 1, r = max(piles). Seed res = r (guaranteed to work).
        2) While l <= r:
           - Guess the middle speed k.
           - Sum ceil(p / k) over all piles to get total hours.
           - If hours <= h: this speed works, so record it and search the
             SLOWER half (r = k - 1), hunting for something smaller.
           - Else it's too slow: discard it and everything below
             (l = k + 1).
        3) Return res — the smallest speed ever found that fit.
        """
        # I — Implement
        # ----------------
        l, r = 1, max(piles)
        res = r

        while l <= r:
            k = (l + r) // 2

            hours = 0
            for p in piles:
                # ceil, not plain division: leftover bananas still cost
                # a whole hour, since she can't start another pile
                hours += math.ceil(p / k)

            if hours <= h:
                res = k        # works — keep it, but look for slower
                r = k - 1
            else:
                l = k + 1      # too slow — speed up

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Monotonicity is what makes binary search valid here: a faster
        #   speed can never need MORE hours, so once a speed fits, all
        #   faster ones fit too. That guarantees discarding a half is safe.
        # - On a success we move r (not l), because a working speed might
        #   not be the SMALLEST working speed — there could be a slower
        #   one still untested below it.
        # - res is updated only on success, so it always holds a verified
        #   working speed; seeding it with max(piles) means it's valid
        #   even before the first comparison.
        # - r = max(piles) is a safe upper bound: beyond that, every pile
        #   already takes exactly 1 hour, so extra speed changes nothing.

        # E — Evaluate
        # ----------------
        # Time:  O(n * log m) — n = number of piles, m = max(piles).
        #        log m binary-search steps, each doing an O(n) pass to
        #        total up the hours.
        # Space: O(1) — only a few scalar variables.