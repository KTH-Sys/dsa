class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        U — Understand
        ----------------
        Return True if subRoot appears inside root as a COMPLETE subtree:
        some node of root, together with all its descendants, is exactly
        identical to subRoot (same shape, same values, nothing extra
        hanging below).

        M — Match
        ----------------
        Pattern: Recursive DFS search, reusing the Same Tree comparison
        as a helper. Since subRoot could match at ANY node of root, walk
        every node and run the isSameTree check there. Uses `or` (one
        match anywhere is enough) rather than Same Tree's `and`.

        P — Plan
        ----------------
        1) Base case: an empty subRoot matches anything -> True.
        2) Base case: root exhausted but subRoot isn't empty -> False.
        3) At this node, run isSameTree(root, subRoot). If it matches,
           we've found it -> True.
        4) Otherwise recurse into the left subtree OR the right subtree —
           finding it in either one is sufficient.
        """
        # I — Implement
        # ----------------
        if not subRoot:
            return True
        if not root:
            return False
        if self.isSameTree(root, subRoot):
            return True

        return (self.isSubtree(root.left, subRoot) or
                self.isSubtree(root.right, subRoot))

    def isSameTree(self, p, q):
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return (self.isSameTree(p.left, q.left) and
                self.isSameTree(p.right, q.right))

        # R — Review
        # ----------------
        # - isSameTree demands a COMPLETE match (same shape all the way
        #   down), which is exactly what "subtree" requires — a partial
        #   value match with extra nodes below correctly returns False.
        # - `or` between the two recursive calls means the search stops
        #   as soon as ANY node matches; Python short-circuits, so the
        #   right subtree isn't even searched if the left already found it.
        # - The subRoot-empty check comes FIRST so that an empty pattern
        #   correctly returns True even when root is also empty.

        # E — Evaluate
        # ----------------
        # Time:  O(n * m) — n = nodes in root, m = nodes in subRoot. In
        #        the worst case, isSameTree (which costs O(m)) is run at
        #        every one of the n nodes.
        # Space: O(n) — recursion call stack depth, bounded by the height
        #        of root (O(n) worst case for a skewed tree)