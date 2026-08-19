class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        U — Understand
        ----------------
        Remove the n-th node from the END of the list, in a single pass,
        and return the (possibly new) head.

        M — Match
        ----------------
        Pattern: Two pointers with a fixed gap. Advance `right` n steps
        ahead of `left` FIRST, then walk both forward together — when
        `right` falls off the end, `left` is exactly n nodes short of
        the end. Combined with a DUMMY NODE so `left` always has a valid
        starting point even if the node to remove is the head itself.

        P — Plan
        ----------------
        1) Create a dummy node pointing at head; start BOTH left and
           right at dummy.
        2) Advance `right` forward n+1 times (not n) — this positions
           `right` such that when it becomes None, `left` lands on the
           node JUST BEFORE the one to remove (not on the target itself).
        3) Walk `left` and `right` forward together, one step each,
           until `right` becomes None.
        4) `left` is now sitting on the node before the target — unlink
           the target: left.next = left.next.next.
        5) Return dummy.next (the real head, skipping the placeholder).
        """
        # I — Implement
        # ----------------
        dummy = ListNode(0, head)
        left = dummy
        right = head

        # Advance right n steps ahead of left
        while n > 0 and right:
            right = right.next
            n -= 1

        # Walk both pointers together until right falls off the end
        while right:
            left = left.next
            right = right.next

        # left is now at the node BEFORE the target — unlink it
        left.next = left.next.next

        return dummy.next

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Starting right at head (not dummy) and advancing it n times
        #   (not n+1) creates exactly the right gap: when right becomes
        #   None after the second loop, left has moved exactly (length-n)
        #   steps from dummy, landing on the node immediately before the
        #   target — never on the target itself.
        # - dummy guarantees left always has a valid position to start
        #   from and walk from, even in the edge case where the node to
        #   remove IS the original head (in which case left never
        #   actually needs to move away from dummy).
        # - left.next = left.next.next is the standard single-node
        #   unlink: skip over the target entirely, relinking around it.

        # E — Evaluate
        # ----------------
        # Time:  O(L) — L = length of the list; single pass, each node
        #        visited a constant number of times
        # Space: O(1) — only a few pointer variables, no auxiliary
        #        arrays or a separate length-counting pass