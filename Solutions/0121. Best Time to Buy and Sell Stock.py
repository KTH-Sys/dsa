from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        U — Understand
        ----------------
        Given an array prices where prices[i] is the price on day i,
        choose one day to buy and a later day to sell.
        Return the maximum profit possible. If no profit is possible, return 0.

        M — Match
        ----------------
        Pattern: One-pass / Greedy (also interpretable as Sliding Window)
        Idea:
        - Track the minimum price seen so far (best buy point)
        - For each day as a potential sell day, compute profit = sell - minBuy
        - Keep the maximum profit across all days

        P — Plan
        ----------------
        1) Initialize minBuy as the first day's price
        2) Initialize maxPro = 0 (best profit so far)
        3) Iterate through prices as "sell" price:
           - Update maxPro using sell - minBuy
           - Update minBuy if current sell price is a new minimum
        4) Return maxPro

        I — Implement
        ----------------
        """

        # Minimum price observed so far (best day to buy up to current day)
        minBuy = prices[0]

        # Maximum profit observed so far
        maxPro = 0

        # Treat each price as a potential sell price
        for sell in prices:
            # If we sold today, profit would be today's price - best buy so far
            maxPro = max(maxPro, sell - minBuy)

            # Update best buy price if today's price is lower
            minBuy = min(minBuy, sell)

        # E — Evaluate
        # ----------------
        # Time Complexity: O(n)
        #   - Single pass through prices
        # Space Complexity: O(1)
        #   - Only two variables (minBuy, maxPro)

        # R — Review
        # ----------------
        # Correctness intuition:
        # - For each day, the best profit selling today is achieved by buying at
        #   the lowest price seen before (or on) today.
        # - We keep updating that minimum and track the best profit over all days.

        return maxPro
