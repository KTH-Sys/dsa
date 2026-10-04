"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from collections import deque

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        """
        U — UNDERSTAND
            Given one node of a connected, undirected graph, return a DEEP
            copy: brand-new Node objects, connected the same way, sharing
            nothing with the original.
            The input [[2,4],[1,3],[2,4],[1,3]] only DESCRIBES the graph; the
            function receives one Node object (node 1) and must discover the
            rest by following .neighbors.
            Q: empty graph? node is None -> return None.
            Q: values unique? Yes, 1..n, n <= 100. (Key by object anyway.)
            Q: undirected? Yes -- each edge appears in BOTH nodes' lists.

        M — MATCH
            Attempt 1: Node(node.val, node.neighbors) -> shallow copy. The
                new node's list still points at ORIGINAL nodes.
            Attempt 2: recursively copy each neighbor with no memory ->
                1 -> 2 -> 1 -> 2 ... infinite recursion, because undirected
                edges are loops. Even without the loop, it would create a
                fresh copy of a node every time it's reached again.
            Root cause: no memory of what's already been copied.
            Fix: a hash map, original -> copy. Check it before creating
                anything. One map stops cycles AND prevents duplicate copies.
            Walk the graph with BFS. Creating a node's copy IS the visited
                mark, done at discovery time (same as sinking a cell when
                it's enqueued in Number of Islands).

        P — PLAN
            1. If node is None, return None.
            2. clones = {node: copy of node}; queue = [node].
            3. While the queue has originals:
                 pop cur
                 for each original neighbor nb:
                   if nb not in clones: copy it, record it, queue it
                   clones[cur].neighbors.append(clones[nb])
            4. Return clones[node].
            The wiring line sits OUTSIDE the if: it runs for every neighbor,
                new or already copied. Inside the if, edges to
                already-copied nodes would never be wired.
            Every node on the wiring line goes through clones[...]: a bare
                cur or nb there would be an original, tangling the graphs.

        I — IMPLEMENT
            (below)

        R — REVIEW
            1 --- 2        1:[2,4]  2:[1,3]  3:[2,4]  4:[1,3]
            |     |
            4 --- 3
            init:  clones {1:1'}            queue [1]
            pop 1: nb 2 new -> 2', queue    wire 1'->2'    queue [2]
                   nb 4 new -> 4', queue    wire 1'->4'    queue [2,4]
            pop 2: nb 1 seen                wire 2'->1'    queue [4]
                   nb 3 new -> 3', queue    wire 2'->3'    queue [4,3]
            pop 4: nb 1 seen                wire 4'->1'
                   nb 3 seen                wire 4'->3'    queue [3]
            pop 3: nb 2 seen                wire 3'->2'
                   nb 4 seen                wire 3'->4'    queue []
            return 1'.  Copy adjacency matches; zero shared node objects.
            Totals: 4 copies, 4 pops (each node queued once), 8 wirings
                (one per neighbor-list entry: 4 edges x 2 directions).
            None -> None.  Single node, no neighbors -> 1' with [].

        E — EVALUATE
            Time  O(V + E): each node popped once; each edge seen once from
                each end.
            Space O(V): the clones map plus the queue.
            Follow-ups:
                Recursive DFS -> same map; register the copy BEFORE
                    recursing into neighbors or the cycle returns.
                    Depth is fine here (n <= 100).
                Directed graph -> same code; it never assumed paired edges.
                Disconnected graph -> one start node only reaches its own
                    component; you'd need every node and an outer loop
                    (the Number of Islands scan, applied to a graph).
            Same original -> copy map idea: LC 138 Copy List with Random
                Pointer.
        """
        if not node:
            return None

        clones = {node: Node(node.val)}      # original -> copy
        queue = deque([node])                # originals still to explore

        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors:
                if nb not in clones:                 # first time seeing nb
                    clones[nb] = Node(nb.val)        # copy it, mark it seen
                    queue.append(nb)                 # explore it later
                clones[cur].neighbors.append(clones[nb])   # wire copy to copy

        return clones[node]