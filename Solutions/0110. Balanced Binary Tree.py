class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        U — Understand
        ----------------
        A binary tree is height-balanced if, at EVERY node, the heights
        of its two subtrees differ by at most 1. Return True if the whole
        tree is balanced, False otherwise.

        M — Match
        ----------------
        Pattern: Recursive DFS returning a dual-purpose value. One helper
        returns a subtree's HEIGHT if it's balanced, or a sentinel -1 if
        it (or anything below it) is NOT balanced. The -1 "alarm" bubbles
        straight to the top once any imbalance is found, giving one O(n)
        pass instead of the naive O(n^2) of recomputing heights everywhere.

        P — Plan
        ----------------
        1) Define height(node): returns 0 for an empty node.
        2) Recurse into left and right to get their heights (or -1).
        3) If either child returned -1 (already unbalanced), OR the two
           heights differ by more than 1 (unbalanced HERE), return -1.
        4) Otherwise return 1 + max(left, right) — the real height.
        5) The tree is balanced iff height(root) != -1.
        """
        # I — Implement
        # ----------------
        def height(node):
            if not node:
                return 0

            left = height(node.left)
            right = height(node.right)

            if left == -1 or right == -1 or abs(left - right) > 1:
                return -1

            return 1 + max(left, right)

        return height(root) != -1

        # R — Review
        # ----------------
        # - Returning -1 as an "unbalanced" sentinel lets a single
        #   traversal do double duty: report height AND flag imbalance,
        #   without a separate height() call at every node (which would
        #   be O(n^2)).
        # - Checking `left == -1 or right == -1` FIRST ensures that once
        #   imbalance is found anywhere below, it propagates to the root
        #   unchanged — no further real-height computation can override it.
        # - abs(left - right) > 1 catches lopsidedness in EITHER direction
        #   (left taller than right, or right taller than left).

        # E — Evaluate
        # ----------------
        # Time:  O(n) — each node visited exactly once (the -1 sentinel
        #        avoids re-measuring subtrees)
        # Space: O(h) — recursion call stack, h = tree height
