class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        U — Understand
        ----------------
        Given L0->L1->...->Ln, reorder in place into
        L0->Ln->L1->Ln-1->L2->Ln-2->... Modify the list's node
        connections directly; don't return a new list.

        M — Match
        ----------------
        Pattern: decompose into three sub-problems you already have
        tools for:
        1) Find the middle (fast/slow two-pointer technique)
        2) Reverse the second half (the exact Reverse Linked List
           algorithm, applied to a sub-list)
        3) Merge two lists by alternating nodes (careful pointer
           save-before-overwrite, same discipline as reversal)

        P — Plan
        ----------------
        1) Use slow/fast pointers: slow moves 1 step, fast moves 2
           steps, until fast reaches the end. slow lands on the middle.
        2) Split the list at slow: cut slow.next off and save it as the
           start of the second half; sever the first half by setting
           slow.next = None.
        3) Reverse the second half using the standard iterative
           reversal (prev/curr/temp).
        4) Merge: walk first-half pointer and reversed-second-half
           pointer together. At each step, save both lists' "next"
           references BEFORE rewiring, splice second's node in right
           after first's node, then advance both pointers into their
           saved "next" positions.
        """
        # I — Implement
        # ----------------

        # Step 1: find the middle using slow/fast pointers
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: split into two halves, then reverse the second half
        second = slow.next
        slow.next = None  # cut the first half off from the second

        prev = None
        while second:
            temp = second.next
            second.next = prev
            prev = second
            second = temp
        second = prev  # after reversal, prev is the new head of half 2

        # Step 3: merge the two halves, alternating nodes
        first = head
        while second:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first = temp1
            second = temp2

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - fast moving 2x speed guarantees slow lands on (or just
        #   before) the middle by the time fast exhausts the list,
        #   correctly splitting into a first half of length ceil(n/2)
        #   and second half of length floor(n/2).
        # - Reversing the second half turns "walk from the back" into
        #   "walk from the front of this reversed sub-list" — the exact
        #   Reverse Linked List algorithm, unchanged.
        # - In the merge step, temp1/temp2 save each list's next-node
        #   BEFORE any rewiring happens, so neither list's remaining
        #   nodes are ever lost mid-merge — same save-before-overwrite
        #   discipline as the reversal step itself.
        # - The merge loop runs while second exists; since the second
        #   half is always the same length or one shorter than the
        #   first, first always has a valid node to attach to even
        #   after second runs out.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — each of the three phases (find middle, reverse,
        #        merge) is a single O(n) pass, so total is O(n)
        # Space: O(1) — only a handful of pointer variables; the
        #        reordering happens by rewiring existing nodes, no new
        #        nodes or arrays created