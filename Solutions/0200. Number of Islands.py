from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        U — UNDERSTAND
            grid is rows x cols of the STRINGS "1" (land) and "0" (water).
            Land cells connect only up/down/left/right, never diagonally.
            Count the connected groups of land (islands).
            Q: values are strings? Yes -- comparing to the int 1 is always
               False and silently returns 0.
            Q: can I modify grid? Ask first. If not, use a visited set.
            Q: size? Up to 300 x 300 = 90,000 cells -> O(rows*cols) needed,
               and recursion 90,000 deep is too deep for Python.

        M — MATCH
            Attempt 1: count every "1" -> overcounts. [[1,1],[1,0]] is one
                island, not three.
            Attempt 2: count only "top-left corners" (no land above or left)
                -> fails on a U shape:
                    1 0 1
                    1 1 1
                (0,2) looks like a new corner, but it connects to (0,0)
                through the bottom row. You can't tell connection locally.
            Fix: treat the grid as a graph (cell = point, edges to its 4
                neighbors). When the scan finds unclaimed land, flood the
                whole island at once and sink it. Each flood = one island.
            BFS with a queue instead of recursive DFS: same O(rows*cols),
                but no recursion-depth risk. (Recursive DFS fails at a
                40x40 all-land grid under Python's default 1000 limit.)

        P — PLAN
            1. directions = the four moves as (row change, col change).
            2. Scan every cell, row by row.
            3. On a "1": islands += 1, sink it, start a queue with it.
            4. While the queue has cells: pop the oldest, try each move.
               If the neighbor is on the grid AND is "1": sink it NOW,
               then add it to the back of the queue.
            5. Return islands.
            Order inside the check matters: bounds first, then the grid
               read. grid[-1] doesn't crash in Python -- it silently reads
               the last row and merges unrelated islands.
            Sink on ADD, not on pop: otherwise two neighbors can both add
               the same cell before it's popped (duplicates in the queue).

        I — IMPLEMENT
            (below)

        R — REVIEW
            1 1 0 0 1
            1 0 0 1 1
            0 0 1 0 0
            scan (0,0) land -> islands=1, flood sinks (0,0),(1,0),(0,1)
            scan (0,1) already "0" -> skip (this is the double-count guard)
            scan (0,4) land -> islands=2, flood sinks (0,4),(1,4),(1,3)
            scan (1,3),(1,4) already "0" -> skip
            scan (2,2) land -> islands=3, flood sinks (2,2) only
            -> return 3
            Edge checks hit: (0,0) up -> (-1,0) off top; (0,4) right ->
                (0,5) off right; (2,2) down -> (3,2) off bottom.
            U shape [[1,0,1],[1,1,1]] -> flood from (0,0) runs down,
                across, and up into (0,2) -> 1 island.
            All water -> 0. Single "1" -> 1.

        E — EVALUATE
            Time  O(rows * cols): each cell scanned once, sunk at most once,
                checked by at most 4 neighbors.
            Space O(rows * cols) worst case for the queue; no visited set
                because the grid itself records what's sunk.
            Follow-ups:
                Can't modify grid -> visited set of (r, c), same time,
                    O(rows*cols) extra space.
                Iterative DFS -> change popleft() to pop(). Same answer.
                Land added one cell at a time, count after each ->
                    union-find (LC 305 Number of Islands II).
            Same flood pattern: LC 695 Max Area, 463 Perimeter,
                1254 Closed Islands, 994 Rotting Oranges.
        """
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))   # down, up, right, left
        rows, cols = len(grid), len(grid[0])
        islands = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":            # land no flood has reached
                    islands += 1
                    grid[r][c] = "0"             # sink before enqueueing
                    queue = deque([(r, c)])

                    while queue:
                        cr, cc = queue.popleft()
                        for dr, dc in directions:
                            nr, nc = cr + dr, cc + dc
                            # bounds first, so the grid is never read off the edge
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                                grid[nr][nc] = "0"          # claim it now
                                queue.append((nr, nc))      # explore it later

        return islands