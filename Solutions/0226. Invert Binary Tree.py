class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        U — Understand
        ----------------
        Given the root of a binary tree, mirror it: swap the left and
        right child of EVERY node, top to bottom. Return the root.

        M — Match
        ----------------
        Pattern: Recursive tree traversal (DFS). Inverting a whole tree
        = swap the root's two children, then invert each subtree the
        same way. The problem is made of smaller copies of itself, which
        is the signal for recursion.

        P — Plan
        ----------------
        1) Base case: if the node is None (empty), there's nothing to
           invert — return None.
        2) Swap this node's left and right children.
        3) Recursively invert the left subtree and the right subtree.
        4) Return this node.
        """
        # I — Implement
        # ----------------
        if not root:
            return None

        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root

        # R — Review
        # ----------------
        # - Swapping at every node, all the way down, produces a full
        #   mirror image — because the swap happens at every level via
        #   the recursion reaching every node exactly once.
        # - The base case (None) stops the recursion cleanly at the
        #   bottom, where there are no children to swap.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — every node is visited exactly once
        # Space: O(h) — h = height of the tree, from the call stack of
        #        nested recursive calls (worst case O(n) for a skewed
        #        tree, O(log n) for a balanced one)