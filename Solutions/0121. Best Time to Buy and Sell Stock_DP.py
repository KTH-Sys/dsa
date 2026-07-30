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
        Pattern: Single-pass running minimum (a simplified two-pointer
        idea). Instead of tracking pointer POSITIONS for buy/sell days,
        just carry forward the LOWEST price value seen so far — the
        problem only asks for the profit amount, not which specific days
        achieved it, so the day index itself is unnecessary state.

        P — Plan
        ----------------
        1) Start minPrice at the first day's price (the only candidate
           buy day known so far) and maxProfit at 0.
        2) For each day's price:
           - Compute the profit if selling TODAY, using the lowest price
             seen up through YESTERDAY (today hasn't updated minPrice yet).
           - Update maxProfit if this profit beats the current best.
           - THEN update minPrice if today's price is a new low, making
             it available as a buy day for future iterations.
        3) Return maxProfit after scanning every day.
        """
        # I — Implement
        # ----------------
        maxProfit = 0
        minPrice = prices[0]

        for price in prices:
            # Profit if we sold today, having bought at the lowest price
            # seen so far (does NOT yet include today as a buy candidate)
            profit = price - minPrice
            maxProfit = max(maxProfit, profit)

            # Now let today's price become the new low, if it is one —
            # done AFTER the profit check, so today can't be used as
            # both its own buy and sell day
            minPrice = min(minPrice, price)

        return maxProfit

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - minPrice always holds the lowest price encountered up to and
        #   including the current day by the END of each iteration, so
        #   every later day's profit calculation is checked against the
        #   best possible buy day available before it.
        # - Checking profit BEFORE updating minPrice guarantees a day is
        #   never used as its own buy-and-sell pair (profit would be 0
        #   anyway in that case, so this ordering costs nothing but
        #   keeps the logic conceptually clean).
        # - maxProfit only grows when a strictly better profit appears,
        #   correctly defaulting to 0 if prices never rise (doing
        #   nothing is always a valid, zero-profit option).

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — single pass through prices, one comparison and
        #        one update per element
        # Space: O(1)  — only two scalar variables (maxProfit, minPrice),
        #        no auxiliary arrays or pointer bookkeeping needed