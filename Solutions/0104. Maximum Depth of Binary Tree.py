class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        U — Understand
        ----------------
        Return the maximum depth of a binary tree: the number of nodes
        along the longest path from the root down to the farthest leaf.

        M — Match
        ----------------
        Pattern: Recursive DFS. A node's depth is 1 + the max depth of
        its two subtrees. The problem is defined in terms of smaller
        copies of itself, which is the signal for recursion.

        P — Plan
        ----------------
        1) Base case: an empty node (None) contributes depth 0.
        2) Recursively find the depth of the left subtree and the right
           subtree.
        3) This node's depth = 1 + the larger of those two.
        """
        # I — Implement
        # ----------------
        if not root:
            return 0

        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)

        return 1 + max(left_depth, right_depth)

        # R — Review
        # ----------------
        # - Taking max (not sum) of the two subtree depths correctly
        #   follows the LONGER path, which is what "maximum depth" means.
        # - The +1 counts the current node itself.
        # - The None base case (depth 0) gives the recursion a solid
        #   floor to build the counts up from.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — every node is visited exactly once
        # Space: O(h) — h = height of tree, from the recursion call
        #        stack (worst case O(n) for a skewed tree)