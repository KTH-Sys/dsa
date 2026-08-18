# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        U — Understand
        ----------------
        Given two SORTED linked lists, merge them into one sorted list by
        rewiring existing nodes (not creating new ones). Return the head
        of the merged list.

        M — Match
        ----------------
        Pattern: Two-pointer merge (the merge step of merge sort), plus
        the DUMMY NODE technique to avoid special-casing "what's the
        first node of the result."

        P — Plan
        ----------------
        1) Create a dummy node, and a `tail` pointer starting at dummy —
           tail always points to the LAST node currently attached to
           the result.
        2) While both list1 and list2 still have nodes:
           - Compare their current values. Attach whichever is smaller
             to tail.next, then advance THAT list's pointer forward.
           - Always advance tail to the node just attached.
        3) Once one list is exhausted, the other list's REMAINING nodes
           are already sorted among themselves — just attach the whole
           remaining chain directly, no need to walk it node by node.
        4) Return dummy.next (skipping the placeholder itself).
        """
        # I — Implement
        # ----------------
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # One list may still have remaining nodes — attach the whole tail
        tail.next = list1 if list1 else list2

        return dummy.next

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Both lists are individually sorted, so at every step, the
        #   smaller of the two CURRENT nodes is guaranteed to be the
        #   smallest unattached value across BOTH lists combined —
        #   nothing smaller could still be hiding further down either list.
        # - dummy sidesteps the "no previous node exists yet" problem for
        #   the very first attachment — tail always has somewhere valid
        #   to point from, even before any real merging has happened.
        # - Once one list runs out, the other's remaining nodes are
        #   already in sorted order relative to each other AND are all
        #   >= everything already attached, so splicing the whole
        #   remainder in one line is safe and correct.

        # E — Evaluate
        # ----------------
        # Time:  O(n + m) — n, m = lengths of list1, list2; each node
        #        from both lists is visited and attached exactly once
        # Space: O(1) — no new nodes created, only a dummy placeholder
        #        and pointer variables; existing nodes are rewired