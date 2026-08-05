class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        U — Understand
        ----------------
        For each day, find how many days until a WARMER day appears. If
        none exists, output 0 for that day.

        M — Match
        ----------------
        Pattern: Monotonic Stack. Maintain a stack of day-indices that
        are still "waiting" for a warmer day, kept in DECREASING
        temperature order from bottom to top. When a new day arrives
        that's warmer than the stack's top, that resolves the wait for
        every day on the stack it's warmer than — pop and record each one.

        P — Plan
        ----------------
        1) Create a result array of zeros, same length as temperatures.
        2) Keep a stack of [temperature, index] pairs for days still
           awaiting a warmer future day.
        3) For each new day (i, t):
           - While the stack isn't empty AND t is warmer than the
             stack's top temperature: pop that day off, grab its index,
             and record (current index - popped index) as its answer.
           - Push the current day onto the stack (it's now "waiting").
        4) Any day never popped by the end simply keeps its default 0
           (no warmer day ever came).
        """
        # I — Implement
        # ----------------
        res = [0] * len(temperatures)
        stack = []  # each entry: [temperature, index]

        for i, t in enumerate(temperatures):
            # Resolve every waiting day that this new day is warmer than
            while stack and t > stack[-1][0]:
                popped = stack.pop()
                stackInd = popped[1]
                res[stackInd] = i - stackInd

            # This day is now waiting for its own warmer day
            stack.append([t, i])

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - The stack only ever holds days that HAVEN'T found a warmer
        #   day yet, so every pop represents a genuine resolution.
        # - Checking stack[-1] (most recent waiting day) first, and
        #   continuing to pop with `while` (not `if`), ensures a single
        #   warm day resolves EVERY waiting day it's warmer than, not
        #   just the most recent one.
        # - i - stackInd correctly computes "how many days later" the
        #   resolution happened, since both are array indices and no
        #   warmer day could have appeared in between (it would have
        #   already resolved stackInd earlier if it had).
        # - Days left on the stack when the loop ends never get a warmer
        #   day, so their res[] entry correctly stays at the default 0.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — each index is pushed onto the stack exactly once
        #        and popped at most once, so total stack operations
        #        across the whole run are bounded by 2n, not n^2.
        # Space: O(n) — worst case (strictly decreasing temperatures),
        #        every day ends up on the stack simultaneously.