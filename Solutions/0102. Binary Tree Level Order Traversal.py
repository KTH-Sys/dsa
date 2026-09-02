# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        U — Understand
        ----------------
        Return the tree's node values grouped by level: one inner list
        per depth, each read left to right, top level first.
        Example: the tree 3 / (9, 20) / (15, 7) returns
        [[3], [9, 20], [15, 7]].

        M — Match
        ----------------
        Pattern: BFS (Breadth-First Search) with a queue. Most tree
        problems use DFS (go deep), but this one is inherently LEVEL-based,
        which is exactly what BFS produces naturally.
        Two key mechanics:
        - A queue is FIFO (first in, first out), so children added to the
          BACK are always processed after everything currently in line —
          meaning the queue drains one full level before starting the next.
        - Snapshotting len(q) before each level gives that level's exact
          width, which is how we know where one level ends.
        This variant enqueues children UNCONDITIONALLY (even None) and
        filters them out on the way back out, rather than checking
        `if node.left` before appending.

        P — Plan
        ----------------
        1) Start a queue holding just the root (even if it's None).
        2) While the queue isn't empty:
           - Snapshot qLen = len(q) — the current level's width, captured
             BEFORE the inner loop grows the queue with the next level.
           - Loop exactly qLen times: pop from the FRONT. If the node is
             real, record its value and push BOTH children onto the BACK
             (None children included — they get skipped later).
           - If this level collected any values, append it to the result.
             The `if level` guard is what discards the all-None level that
             sits below the deepest real level.
        3) Return the list of levels.
        """
        # I — Implement
        # ----------------
        res = []
        q = collections.deque()

        # Root goes in even if it's None — the `if node` check inside the
        # loop handles that case, so no separate empty-tree guard is needed
        q.append(root)

        while q:
            # Snapshot the level's width BEFORE processing, since the loop
            # below appends next-level nodes and would otherwise blur the
            # boundary between levels
            qLen = len(q)
            level = []

            for i in range(qLen):
                node = q.popleft()   # take from the FRONT (FIFO)

                if node:
                    # Real node: record it, and queue BOTH children —
                    # including None ones, which get filtered on their turn
                    level.append(node.val)
                    q.append(node.left)
                    q.append(node.right)

            # Only keep levels that actually had real nodes. This skips the
            # final "phantom level" made entirely of the None children
            # enqueued by the deepest real level.
            if level:
                res.append(level)

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - FIFO order guarantees nodes are processed in discovery order;
        #   since children always go behind the current level, the queue
        #   drains one complete level before any next-level node is reached.
        # - Capturing qLen BEFORE the inner loop is essential: the loop
        #   itself grows the queue, so a live len(q) would consume past the
        #   level boundary and mash levels together.
        # - Left child is enqueued before the right child, preserving
        #   left-to-right order within each level.
        # - Enqueuing None children is safe because `if node` skips them on
        #   dequeue. The trade-off: the queue temporarily holds Nones, and
        #   one final all-None pass runs before the loop ends — which the
        #   `if level` guard correctly discards rather than appending [].
        # - An empty tree (root=None) works without a special guard: the
        #   queue starts as [None], the inner loop pops it and skips it,
        #   `level` stays empty, `if level` is False, and res stays [].

        # E — Evaluate
        # ----------------
        # Time:  O(n) — every real node is enqueued once and dequeued once;
        #        the None placeholders add a constant factor, not a
        #        complexity change
        # Space: O(w) — w = the tree's maximum width; the queue holds at
        #        most one level (plus its None children) at a time, which
        #        is O(n) worst case for the bottom level of a full tree