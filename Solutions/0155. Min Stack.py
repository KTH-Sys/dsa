class MinStack:
    """
    U — Understand
    ----------------
    Design a stack supporting push, pop, top, and getMin — all in O(1)
    time. The challenge is getMin: a stack's minimum can change after
    every pop, and naively finding it requires scanning all elements.

    M — Match
    ----------------
    Pattern: Auxiliary stack (two stacks in parallel). Maintain a second
    stack that tracks the RUNNING MINIMUM at each point in the main
    stack's history — not just the overall minimum, but what the minimum
    WAS at the moment each element was pushed.

    P — Plan
    ----------------
    1) Keep two stacks: `stack` (the real data) and `minStack` (the
       running minimum, one entry per push).
    2) On push(val): push val onto `stack`. Compute the new minimum as
       min(val, current top of minStack) and push THAT onto minStack.
    3) On pop(): pop from BOTH stacks together, keeping them in sync.
    4) top(): just look at stack[-1].
    5) getMin(): just look at minStack[-1] — O(1), no scanning needed.
    """
    # I — Implement
    # ----------------
    def __init__(self):
        self.stack = []
        self.minStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # New minimum is the smaller of (this value) and (previous minimum)
        val = min(val, self.minStack[-1] if self.minStack else val)
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]

    # R — Review
    # ----------------
    # Correctness reasoning:
    # - minStack[i] always holds "the minimum of stack[0..i]" at the time
    #   element i was pushed — a complete historical record, not just a
    #   single cached value.
    # - Popping both stacks together means minStack[-1] always correctly
    #   reflects the minimum of whatever elements REMAIN in stack, because
    #   it's rewinding to exactly the minimum that was true at that
    #   earlier moment — no rescanning needed.

    # E — Evaluate
    # ----------------
    # Time:  O(1) for every operation — push, pop, top, getMin
    # Space: O(n) — minStack stores one entry per element in stack,
    #        so it doubles space usage but stays linear