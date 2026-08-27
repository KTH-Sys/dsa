class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        U — Understand
        ----------------
        Return the diameter of a binary tree: the number of EDGES on the
        longest path between any two nodes. The path need not pass
        through the root.

        M — Match
        ----------------
        Pattern: Recursive DFS with a side-channel result. Reuse the
        Maximum Depth recursion, but at every node also compute
        (left depth + right depth) — the length of the longest path
        bending at that node — and track the maximum of that across all
        nodes in a shared variable.

        P — Plan
        ----------------
        1) Keep a shared self.diameter, starting at 0.
        2) Define a helper depth(node) that returns the node's depth AND,
           as a side effect, updates self.diameter.
        3) At each node: the path bending here is left_depth + right_depth
           edges long — update self.diameter with the max.
        4) Return 1 + max(left, right) as this node's depth to its parent.
        5) After the traversal, self.diameter holds the answer.
        """
        # I — Implement
        # ----------------
        self.diameter = 0

        def depth(node):
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)

        depth(root)
        return self.diameter

        # R — Review
        # ----------------
        # - left + right (not +1) counts EDGES: a path from the deepest
        #   left node, through this node, to the deepest right node has
        #   exactly left + right edges.
        # - Checking left + right at EVERY node guarantees the best
        #   bending point is found, since every path bends at exactly one
        #   node and we test all of them.
        # - Depth is RETURNED (parent needs it); diameter is stored in a
        #   shared variable (it's a global best, not something a parent
        #   uses) — these are two separate results from one traversal.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — each node visited exactly once
        # Space: O(h) — recursion call stack, h = tree height