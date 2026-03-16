# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:

        # U — Understand
        # Input: two sorted linked lists (list1 and list2)
        # Output: one merged sorted linked list
        # Example:
        # list1: 1 → 3 → 5
        # list2: 2 → 4 → 6
        # result: 1 → 2 → 3 → 4 → 5 → 6


        # M — Match Pattern
        # Pattern: Two-pointer merge
        # Same idea used in the merge step of Merge Sort.
        # Always attach the smaller node to the merged list.


        # P — Plan
        # 1. Create a dummy node to simplify list construction.
        # 2. Use a pointer (node) to build the result list.
        # 3. Compare the current nodes of list1 and list2.
        # 4. Attach the smaller node to node.next.
        # 5. Move the pointer forward.
        # 6. Continue until one list is empty.
        # 7. Attach the remaining nodes from the non-empty list.


        # I — Implement

        # dummy node helps avoid special case for first node
        dummy = node = ListNode()

        # traverse both lists
        while list1 and list2:

            # compare node values
            if list1.val < list2.val:

                # attach list1 node
                node.next = list1

                # move list1 forward
                list1 = list1.next

            else:

                # attach list2 node
                node.next = list2

                # move list2 forward
                list2 = list2.next

            # move node forward in merged list
            node = node.next


        # attach remaining nodes
        # only one of these will be non-empty
        node.next = list1 or list2


        # R — Review
        # Check:
        # - All nodes connected
        # - Order preserved
        # - Dummy node skipped in final result


        # E — Evaluate
        # Time Complexity: O(n + m)
        #   n = length of list1
        #   m = length of list2
        #
        # Space Complexity: O(1)
        #   No extra data structures used
        #   Only pointer manipulation


        # return the real head (skip dummy node)
        return dummy.next