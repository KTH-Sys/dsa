class MinStack:
    """
    U — Understand
    ----------------
    Design a stack supporting push, pop, top, and getMin — all in O(1)
    time. A stack's minimum can change after every pop, and naively
    finding it requires scanning all remaining elements — this design
    avoids that scan entirely.

    M — Match
    ----------------
    Pattern: Auxiliary stack (two stacks in parallel), CONDITIONAL
    variant. Instead of pushing a min-snapshot on EVERY push (like the
    "always push min(val, prevMin)" version), this version only pushes
    to minStack when the new value is a NEW record-low (val <= current
    min). This makes minStack shorter in practice, but requires a
    matching check on pop() to know whether that popped value was
    actually the recorded minimum.

    P — Plan
    ----------------
    1) Keep two stacks: `stack` (real data) and `minStack` (only
       records NEW minimums, not every push).
    2) On push(val): always push to `stack`. Only push to `minStack`
       if minStack is empty OR val is <= the current minimum — meaning
       val becomes the new tied-or-lower minimum.
    3) On pop(): compare the top of `stack` to the top of `minStack`
       BEFORE removing anything. If they're equal, the value being
       removed WAS the current minimum, so minStack must also lose its
       top entry (the "next" minimum underneath gets exposed). If they
       differ, the popped value was never the minimum, so minStack is
       left untouched.
    4) top(): just look at stack[-1].
    5) getMin(): just look at minStack[-1] — O(1), no scanning needed.
    """
    # I — Implement
    # ----------------
    def __init__(self):
        # `stack` holds every value the user pushes, in order.
        self.stack = []
        # `minStack` only holds values that were a NEW minimum (or tied
        # with the current minimum) at the moment they were pushed.
        self.minStack = []

    def push(self, val: int) -> None:
        # Always add the new value to the real stack — normal stack behavior.
        self.stack.append(val)

        # Only add to minStack if there's no minimum yet (minStack is
        # empty), OR this value is less than or equal to the current
        # minimum — meaning it's a new (or tied) record-low.
        if not self.minStack or val <= self.minStack[-1]:
            self.minStack.append(val)

    def pop(self) -> None:
        # Check BEFORE removing anything: is the value about to be
        # removed from `stack` the SAME value currently sitting on top
        # of `minStack`? If so, that value was the recorded minimum,
        # and removing it means minStack must also drop its top entry
        # so the next-lowest recorded minimum becomes visible.
        if self.stack[-1] == self.minStack[-1]:
            self.minStack.pop()

        # Always remove the top of the real stack, regardless of
        # whether minStack was touched above.
        self.stack.pop()

    def top(self) -> int:
        # Just read the real stack's top value — ordinary stack behavior.
        return self.stack[-1]

    def getMin(self) -> int:
        # The whole point of the design: read the current minimum
        # directly, with no scanning or recomputation needed.
        return self.minStack[-1]

    # R — Review
    # ----------------
    # Correctness reasoning:
    # - minStack only ever contains values that WERE the minimum at
    #   some point, in the order they became the minimum — its top is
    #   always the CURRENT minimum of everything still in `stack`.
    # - The <= (not strict <) in push() matters: if a duplicate of the
    #   current minimum is pushed, it must ALSO go into minStack. If it
    #   didn't, popping one of the two equal minimum values later would
    #   incorrectly remove the minStack entry meant for the OTHER one
    #   (since pop() matches by VALUE, not by which specific push it
    #   was), causing minStack to lose track of the remaining duplicate.
    # - The equality check in pop() correctly identifies whether the
    #   departing value was "the" minimum: if stack[-1] != minStack[-1],
    #   the top of stack was never recorded as a minimum, so minStack
    #   must be left alone.

    # E — Evaluate
    # ----------------
    # Time:  O(1) for every operation — push, pop, top, getMin
    # Space: O(n) worst case (if values are non-increasing, minStack
    #        grows alongside stack), but O(1) extra in the common case
    #        where minStack only grows on genuine new lows