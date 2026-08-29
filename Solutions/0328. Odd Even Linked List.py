class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        U — Understand
        ----------------
        Group all nodes at ODD positions together, followed by all nodes
        at EVEN positions — where "position" means the 1-indexed spot in
        the list (1st, 2nd, 3rd...), NOT the node's value. Keep the
        relative order within each group. Must be done in O(1) extra space.
        Example: 1->2->3->4->5  becomes  1->3->5->2->4
        (positions 1,3,5 first, then positions 2,4).

        M — Match
        ----------------
        Pattern: Linked-list pointer weaving with two "braided" pointers.
        Walk two pointers down the list at once — one stitching together
        the odd-position nodes, one stitching together the even-position
        nodes — then join the tail of the odd chain to the head of the
        even chain. Same save-the-reference-before-rewiring discipline as
        Reverse/Reorder List, but here we're un-interleaving one list
        into two chains rather than reversing.

        P — Plan
        ----------------
        1) Handle tiny lists: 0 or 1 node needs no reordering — return as-is.
        2) Set odd = 1st node, even = 2nd node, and remember even_head
           (the 2nd node) so we can attach the even chain on at the end.
        3) While there are still even nodes with something after them:
           - Point odd at the node after even (the next ODD-position node),
             then advance odd to it.
           - Point even at the node after the new odd (the next
             EVEN-position node), then advance even to it.
           This "leap-frogs" both pointers two steps down the list each
           loop, weaving the two chains apart.
        4) Attach the tail of the odd chain to even_head, joining the two
           groups: all odds, then all evens.
        5) Return head (still the 1st node, now front of the odd chain).
        """
        # I — Implement
        # ----------------

        # 1) A list of length 0 or 1 is already trivially grouped
        if not head or not head.next:
            return head

        # 2) odd starts at position 1, even at position 2
        odd = head
        even = head.next
        even_head = even   # save the even chain's head to reattach later

        # 3) Weave the two chains apart, leap-frogging two steps per loop
        while even and even.next:
            # Link current odd to the NEXT odd-position node (skip the even)
            odd.next = even.next
            odd = odd.next          # advance odd onto that node

            # Link current even to the NEXT even-position node (skip the odd)
            even.next = odd.next
            even = even.next        # advance even onto that node

        # 4) Odd chain is complete — stitch the even chain onto its tail
        odd.next = even_head

        # 5) head is unchanged: still the front of the odd chain
        return head

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - odd.next = even.next always skips exactly one node (the current
        #   even) to land on the next odd-position node, and vice versa —
        #   so the two chains are pulled apart cleanly without losing any
        #   node, because each rewire reads the "next" reference just
        #   before overwriting it.
        # - even_head is captured BEFORE any rewiring, so the even chain's
        #   start is never lost even though even.next gets overwritten
        #   repeatedly during the weave.
        # - The loop guard `even and even.next` stops exactly when there's
        #   no further even-position node to process, leaving odd sitting
        #   on the last odd node — the correct place to attach even_head.
        # - Relative order within each group is preserved because both
        #   pointers only ever move FORWARD, never reordering within a group.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — each node is visited and rewired a constant number
        #        of times in a single pass
        # Space: O(1) — only a handful of pointers (odd, even, even_head);
        #        nodes are rewired in place, nothing new allocated