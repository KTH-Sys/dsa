class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """
        U — Understand
        ----------------
        Given a BST and two nodes p and q, return their Lowest Common
        Ancestor — the deepest node having both p and q as descendants
        (a node may be a descendant of itself).

        M — Match
        ----------------
        Pattern: BST traversal exploiting the ordering property. In a BST,
        left subtree < node < right subtree, so comparing p.val and q.val
        against the current node tells you which single direction to go —
        no need to search both subtrees like in a general binary tree.
        The LCA is the FIRST node where p and q's paths diverge.

        P — Plan
        ----------------
        1) Start at the root.
        2) At each node, compare both p.val and q.val to the current value:
           - Both greater -> both live right, move right.
           - Both smaller -> both live left, move left.
           - Otherwise (they split, or one equals the current node) ->
             this node is the LCA, return it.
        3) Iterative loop, since we only ever follow ONE path down.
        """
        # I — Implement
        # ----------------
        cur = root

        while cur:
            if p.val > cur.val and q.val > cur.val:
                cur = cur.right
            elif p.val < cur.val and q.val < cur.val:
                cur = cur.left
            else:
                return cur

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - The BST property guarantees that if both values are greater
        #   than cur, BOTH nodes must be in cur's right subtree (nothing
        #   larger can exist on the left), so descending right can't skip
        #   past the LCA.
        # - The first node where the "both same direction" condition FAILS
        #   is exactly where p and q's root-to-node paths diverge — which
        #   is the definition of the lowest common ancestor.
        # - The `else` branch also correctly handles the case where one of
        #   p or q IS the current node: the strict > / < comparisons both
        #   fail on equality, so we return cur — correct, since a node is
        #   its own descendant.

        # E — Evaluate
        # ----------------
        # Time:  O(h) — h = height of the tree; we walk one path down,
        #        never backtracking (O(log n) for a balanced BST,
        #        O(n) worst case for a skewed one)
        # Space: O(1) — iterative, only one pointer variable; no
        #        recursion stack needed since we never branch