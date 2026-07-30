class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        U — Understand
        ----------------
        Given an array where prices[i] is the stock price on day i, find
        the maximum profit from buying on one day and selling on a LATER
        day (must buy before you sell). If no profit is possible, return 0.

        M — Match
        ----------------
        Pattern: Two Pointers (sliding window variant), where `l` tracks
        the best day to BUY so far and `r` scans forward looking for the
        best day to SELL. Unlike the classic two-pointer pattern (pointers
        converging from both ends), here both pointers move in the SAME
        direction — `l` only jumps forward when a new potential low is
        found, `r` always advances by one.

        P — Plan
        ----------------
        1) Start l at day 0 (candidate buy day) and r at day 1 (candidate
           sell day).
        2) For each r, compare prices[l] and prices[r]:
           - If prices[l] < prices[r], selling today would be profitable.
             Compute the profit and update maxP if it's a new best.
           - If prices[l] >= prices[r], today's price is a new LOW — it's
             a better buy day than the old l, so move l up to r (we'd
             never want to buy at the old, higher price when a cheaper
             day is available).
        3) Always advance r by one to look at the next day.
        4) Return maxP once r has scanned past the end of the array.
        """
        # I — Implement
        # ----------------
        l = 0
        r = 1
        maxP = 0

        while r < len(prices):
            if prices[l] < prices[r]:
                # Profitable if sold today — check if it beats the best so far
                profit = prices[r] - prices[l]
                maxP = max(profit, maxP)
            else:
                # Today's price is lower than our current buy day —
                # today becomes the new (better) buy day
                l = r
            r += 1

        return maxP

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - l always points to the LOWEST price seen so far in the
        #   current upward run, since any day with a price <= prices[l]
        #   immediately replaces l — there's never a reason to keep an
        #   old buy day once a cheaper one appears.
        # - Every day is checked as a potential sell day against the best
        #   buy day known up to that point, so the true maximum profit
        #   pair is guaranteed to be tested at some point during the scan.
        # - maxP only increases when a strictly better profit is found,
        #   and defaults to 0 if prices never rise (correctly reflecting
        #   "do nothing" as a valid, zero-profit choice).

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — single pass through prices; r visits every index
        #        once, l only ever moves forward, never backward
        # Space: O(1)  — only a few scalar variables (l, r, maxP), no
        #        auxiliary arrays or data structures