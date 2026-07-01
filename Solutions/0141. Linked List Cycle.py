# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        # U — Understand
        # Input: head of a singly linked list
        # Output: True if the list contains a cycle, otherwise False
        #
        # A cycle occurs when a node points back to a previously visited node,
        # causing infinite traversal.


        # M — Match Pattern
        # Pattern: Hash Set / Visited Nodes
        # Store each node we visit in a set.
        # If we encounter the same node again, a cycle exists.


        # P — Plan
        # 1. Create an empty set to store visited nodes.
        # 2. Start traversal from the head node.
        # 3. For each node:
        #       - check if it already exists in the set
        #       - if yes → cycle detected
        #       - if no → add it to the set
        # 4. Move to the next node.
        # 5. If traversal reaches None → no cycle.


        # I — Implement

        seen = set()       # store visited nodes
        cur = head         # start traversal at head

        while cur:         # continue while nodes exist

            if cur in seen:  # node already visited
                return True  # cycle detected

            seen.add(cur)    # record current node

            cur = cur.next   # move to next node


        # R — Review
        # Ensure:
        # - every node is checked exactly once
        # - cycle detection happens immediately when revisiting a node
        # - traversal moves correctly using cur.next


        # E — Evaluate
        # Time Complexity:  O(n)
        #   each node visited once
        #
        # Space Complexity: O(n)
        #   set stores visited nodes

        return False