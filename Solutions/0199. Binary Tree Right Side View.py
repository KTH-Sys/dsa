from collections import deque

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        U — Understand
        ----------------
        Standing to the right of a binary tree, return the values of the
        nodes visible from that side, top to bottom. A node is visible
        exactly when it's the RIGHTMOST node on its level — everything
        else on that level is blocked behind it.

        M — Match
        ----------------
        Pattern: BFS with a queue — the same level-by-level machinery as
        Level Order Traversal (102), with one change. Instead of
        collecting every value in a level, keep overwriting a single
        `rightmost` variable as we process left to right; whatever
        survives when the level's loop ends IS the rightmost node.

        P — Plan
        ----------------
        1) Start a queue with the root.
        2) While the queue isn't empty:
           - Reset `rightmost` to None for this level.
           - Snapshot qLen = len(q) BEFORE the inner loop, since the loop
             grows the queue with next-level nodes.
           - Loop exactly qLen times: pop from the front, and if the node
             is real, overwrite `rightmost` with it and enqueue both
             children.
           - After the loop, `rightmost` holds the last real node seen on
             this level — record its value.
        3) Return the collected values, one per level.
        """
        # I — Implement
        # ----------------
        res = []
        q = deque([root])

        while q:
            rightmost = None
            qLen = len(q)

            for i in range(qLen):
                node = q.popleft()
                if node:
                    # Keep overwriting — since we go left to right,
                    # the LAST assignment is the rightmost node
                    rightmost = node
                    q.append(node.left)
                    q.append(node.right)

            if rightmost:
                res.append(rightmost.val)

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Left children are enqueued before right children, and FIFO
        #   order preserves that, so each level is processed strictly
        #   left to right — making the final assignment the rightmost node.
        # - Snapshotting qLen before the inner loop keeps level boundaries
        #   clean; a live len(q) would consume next-level nodes and
        #   corrupt which node is "last" on this level.
        # - `if rightmost` correctly skips the phantom all-None pass below
        #   the deepest real level, and also handles an empty tree
        #   (root=None) with no separate guard needed.
        # - A level with only a LEFT child still records that child, since
        #   it's the rightmost node present on its level — correct, since
        #   nothing blocks it.

        # E — Evaluate
        # ----------------
        # Time:  O(n) — every node is enqueued once and dequeued once
        # Space: O(w) — w = the tree's maximum width; the queue holds at
        #        most one level at a time (O(n) worst case)