# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        U — UNDERSTAND
            Return True if the tree is a valid binary search tree:
            at EVERY node, all values anywhere in its left subtree are
            strictly smaller, and all values anywhere in its right subtree
            are strictly larger.
            Q: duplicates? Invalid -- the rule is strict < on both sides.
               (If an interviewer allows duplicates on one side, loosen that
               side to <=.)
            Q: empty tree? Constraints say 1 <= nodes <= 10^4, so root is
               never None -- but None children exist under every leaf.
            Q: value range? -2^31 .. 2^31 - 1, so a "big number" sentinel can
               collide with a real value. Use float('-inf') / float('inf').

        M — MATCH
            Tree DFS that passes constraints DOWN from ancestors.
            Attempt 1 (wrong): compare each node only to its two children.
                    5
                   / \
                  3   7
                     / \
                    4   8
                Every parent/child check passes, but 4 sits in 5's right
                subtree and 4 < 5. Local checks miss rules from higher up.
            Attempt 2 (correct, slow): at each node, scan the entire left
                subtree for its max and the entire right subtree for its min.
                On a skewed chain this rescans n + (n-1) + ... + 1 = O(n^2).
            Fix: every ancestor contributes one limit. Going LEFT past X adds
                "must be < X"; going RIGHT past X adds "must be > X". So each
                node only needs the (low, high) range it inherits. Check it,
                narrow it, hand it to the children. One visit per node.

        P — PLAN
            1. Helper valid(node, low, high) answers: "does anything in this
               subtree break the rules?"
            2. Base case: node is None -> True. Nothing there, nothing broken.
               (Returning False here would reject every leaf, so every tree.
               True is also the neutral value for `and`: True and x == x.)
            3. If not (low < node.val < high) -> False.
            4. Left child inherits (low, node.val)  -- new upper limit.
               Right child inherits (node.val, high) -- new lower limit.
            5. Combine with `and`; it short-circuits on the first violation.
            6. Start at the root with (-inf, inf).

        I — IMPLEMENT
            (below)

        R — REVIEW
            Broken tree above, in call order:
                valid(5, -inf, inf)   -inf < 5 < inf   ok -> go left
                valid(3, -inf, 5)     -inf < 3 < 5     ok
                    valid(None, ...) x2 -> True, True  -> node 3 True
                valid(7, 5, inf)      5 < 7 < inf      ok -> go left
                valid(4, 5, 7)        5 < 4 ?          FAIL -> False
                `and` short-circuits: node 8 is never visited. Result False.
            Valid tree [2,1,3]:
                valid(2,-inf,inf) ok, valid(1,-inf,2) ok, valid(3,2,inf) ok -> True
            Single node [5]: in range, both children None -> True.
            Duplicate [2,2]: valid(2, -inf, 2) -> 2 < 2 fails -> False.
            Extreme value [2147483647]: -inf < 2^31-1 < inf -> True
                (an int sentinel like 2^31-1 would wrongly reject it).

        E — EVALUATE
            Time  O(n): each node checked once, O(1) work per node.
            Space O(h): recursion depth = tree height. O(log n) if balanced,
                O(n) on a skewed chain.
            Depth caveat: a 10^4-node chain recurses 10^4 deep; Python's
                default limit is 1000. LeetCode raises it, but in an interview
                the answer is an explicit stack of (node, low, high) tuples.
            Follow-up ("another way?"): in-order traversal of a valid BST
                yields strictly increasing values. Track the previous value;
                fail on the first val <= prev. Same O(n) time, O(h) space.
                Broken tree in-order = 3, 5, 4, ... -> fails at 4.
        """
        def valid(node, low, high):
            if not node:                        # empty subtree: nothing to break
                return True

            if not (low < node.val < high):     # outside the inherited range
                return False

            return (valid(node.left, low, node.val)        # left: new upper limit
                    and valid(node.right, node.val, high))  # right: new lower limit

        return valid(root, float('-inf'), float('inf'))