# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """
        U — UNDERSTAND
            Given the root of a BST and an integer k, return the kth smallest
            value in the tree. k is 1-indexed: k=1 is the smallest.
            Input like [2,1,3] is LeetCode's level-by-level drawing of the
            tree (root, then left child, then right child), NOT sorted order.
            [2,1,3], k=1 -> sorted order is 1,2,3 -> answer 1.
            Q: k out of range? LC guarantees 1 <= k <= n. Without that
               guarantee, return a sentinel (-1) rather than crash.
            Q: duplicates? A valid BST here has distinct values.

        M — MATCH
            A BST is a sorted list folded into a tree. In-order traversal
            (left subtree, node, right subtree) unfolds it in sorted order.
            Attempt 1: collect all values, sort, index -> O(n log n). Ignores
                that the tree is already sorted.
            Attempt 2: full in-order into a list, return values[k-1] -> O(n)
                time and space. Correct, but for k=1 it still visits all n
                nodes when the answer is known after the first.
            Fix: in-order ONE node at a time, counting, and stop at k.
                Early exit is awkward in recursion (the answer has to bubble
                up through every call), so use an explicit stack.
            Stack holds TreeNode objects, not values: after visiting a node
                you still need node.right. A bare int has no links.

        P — PLAN
            Stack = ancestors walked past but not yet visited.
            Repeat while there is anything left to visit:
            1. Dive left: push node, move to node.left, until None.
               The top of the stack is now the smallest unvisited node.
            2. Visit: pop it, k -= 1. If k == 0, return its value.
            3. Turn right: node = node.right, then back to step 1.
               After turning right you MUST dive left again: the next
               smallest is the right subtree's leftmost node, not its top.
            Loop condition: unvisited nodes live either under `node` or on
               the stack. Both empty -> traversal finished.

        I — IMPLEMENT
            (below)

        R — REVIEW
                      8
                    /   \
                   3     10
                  / \      \
                 1   6      14
                    / \     /
                   4   7   13          k = 5, sorted: 1,3,4,6,7,8,...
            iter 1: push 8,3,1  pop 1  k=4  right None      stack [8,3]
            iter 2: (no dive)   pop 3  k=3  right -> 6      stack [8]
            iter 3: push 6,4    pop 4  k=2  right None      stack [8,6]
            iter 4: (no dive)   pop 6  k=1  right -> 7      stack [8]
            iter 5: push 7      pop 7  k=0  -> return 7
            8 stays on the stack unvisited; 10, 13, 14 never touched.

            Why the condition needs BOTH halves ([2,1,3], k=4):
            iter 2 pops 2 -> stack EMPTY, but node = 3 still unvisited.
                `while stack` alone would stop early and skip 3.
            iter 2 of the k=5 trace: node None but stack non-empty.
                `while node` alone would stop early too.
            After 3 is visited, both empty -> exit -> return -1.
            With `while True`, that case crashes: pop from empty stack.

            pop() can never fail: if the loop runs because node is set, the
            dive pushes at least one node first; otherwise the stack is
            non-empty by the loop condition.

        E — EVALUATE
            Time  O(h + k): dive about h nodes to reach the smallest, then k
                pops. Worst case O(n) when k = n or the tree is a chain.
            Space O(h): the stack holds at most one root-to-leaf path.
            Follow-up (asked by LC itself): tree modified often, kth queried
                often. Store `size` (subtree node count) in every node. At a
                node with left size L:
                    k <= L      -> go left
                    k == L + 1  -> this node is the answer
                    else        -> k -= L + 1, go right
                O(h) per query regardless of k; inserts/deletes update sizes
                along their path.
            Same iterative in-order pattern: LC 173 (BST Iterator), LC 98
                (validate by checking the in-order sequence is increasing).
        """
        stack = []
        node = root

        while node is not None or stack:   # anything left to visit?
            while node:                    # 1. dive left, remember ancestors
                stack.append(node)         #    the node, not node.val
                node = node.left

            node = stack.pop()             # 2. visit next smallest
            k -= 1
            if k == 0:
                return node.val

            node = node.right              # 3. turn right, then dive again

        return -1                          # only reached if k > n