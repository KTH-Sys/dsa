# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:

        # U — Understand
        # Input: head of a singly linked list
        # Output: head of the reversed list
        # Example:
        # 1 → 2 → 3 → 4 → None
        # becomes
        # 4 → 3 → 2 → 1 → None


        # M — Match Pattern
        # This is a classic Linked List pointer manipulation problem.
        # Pattern: Reverse pointers using three variables.
        # Use prev, curr, and temp.


        # P — Plan
        # 1. Initialize prev = None
        # 2. Start curr at head
        # 3. Iterate through the list
        # 4. Save next node
        # 5. Reverse pointer
        # 6. Move both pointers forward
        # 7. When curr becomes None, prev is the new head


        # I — Implement
        prev, curr = None, head

        while curr:

            temp = curr.next   # store next node
            curr.next = prev   # reverse the pointer

            prev = curr        # move prev forward
            curr = temp        # move curr forward


        # R — Review
        # Ensure:
        # - All pointers reversed
        # - No nodes lost
        # - prev becomes the new head


        # E — Evaluate
        # Time Complexity:  O(n)  (traverse list once)
        # Space Complexity: O(1)  (no extra data structures)

        return prev