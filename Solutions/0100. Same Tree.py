class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        U — Understand
        ----------------
        Given the roots of two binary trees, return True if they are
        structurally identical AND have the same value at every
        corresponding node. Same shape + same values everywhere.

        M — Match
        ----------------
        Pattern: Recursive DFS comparing two trees in lockstep. Two trees
        are the same if their roots match (both empty, or both present
        with equal values) AND their left subtrees match AND their right
        subtrees match — a definition made of smaller copies of itself.

        P — Plan
        ----------------
        1) If both nodes are None, they match → True.
        2) If exactly one is None, shapes differ → False.
        3) If both exist but values differ → False.
        4) Otherwise, recursively check that BOTH the left subtrees match
           AND the right subtrees match (using `and`).
        """
        # I — Implement
        # ----------------
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
        # - The three base checks cover every root-pair case: both empty
        #   (match), one empty (mismatch in shape), both present with
        #   different values (mismatch in value).
        # - `and` between the two recursive calls means a single mismatch
        #   ANYWHERE in either subtree makes the whole result False, and
        #   that False propagates up through every ancestor.
        # - Order matters: the None checks run BEFORE p.val is accessed,
        #   so we never touch .val on a None node (which would crash).

        # E — Evaluate
        # ----------------
        # Time:  O(n) — n = number of nodes in the smaller tree; each
        #        pair of corresponding nodes is compared once (comparison
        #        stops early on the first mismatch)
        # Space: O(h) — recursion call stack, h = tree height