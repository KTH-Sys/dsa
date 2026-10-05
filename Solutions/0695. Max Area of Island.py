from collections import deque

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        U — UNDERSTAND
            grid is rows x cols of the NUMBERS 1 (land) and 0 (water).
            Land connects up/down/left/right only, never diagonally.
            Return the area (cell count) of the largest island; 0 if none.
            Q: ints or strings? INTS here -- the opposite of LC 200. Copying
               Number of Islands with == "1" silently returns 0 every time.
            Q: can I modify grid? Ask. If not, use a visited set.
            Q: size? Up to 50 x 50 = 2,500 cells. O(rows*cols) is the bar,
               and a 2,500-deep recursion exceeds Python's default 1,000.

        M — MATCH
            Attempt 1: count all land -> that's the SUM of every island,
                not the largest one.
            Attempt 2: flood from every land cell with a fresh visited set,
                keep the max -> correct, but an island of k cells is
                measured k times. All-land 50x50 = 2,500 floods of 2,500
                cells each.
            Fix: Number of Islands' flood fill, sinking as you go, so each
                island is measured exactly once. The only new idea: count
                cells during each flood and keep the max.
            Diff from LC 200 is three lines:
                islands += 1   ->   area = 0          (per-flood counter)
                (new)          ->   area += 1         (after each pop)
                (new)          ->   best = max(...)   (after each flood)

        P — PLAN
            1. Scan every cell, row by row.
            2. On a 1: sink it, start a queue with it, area = 0.
            3. While the queue has cells: pop one, area += 1, then for each
               of the 4 moves: if on the grid AND land -> sink it NOW,
               add it to the back of the queue.
            4. Queue empty -> island fully measured: best = max(best, area).
            5. Return best.
            Count on POP: every cell enters the queue exactly once (sinking
               on add guarantees it), so every cell is popped -- and counted
               -- exactly once. Counting on add also works, but then the
               starting cell needs its own +1, which is easy to forget.
            best = max(...) AFTER the while, not inside: inside, area is
               still a partial count.

        I — IMPLEMENT
            (below)

        R — REVIEW
            1 1 0 0
            0 0 0 1
            0 1 1 1
            0 0 0 1
            scan (0,0) land: pop (0,0) area=1, add (0,1)
                             pop (0,1) area=2
                             flood done: best = max(0, 2) = 2
            scan (0,1) already 0 -> skip (no double measurement)
            scan (1,3) land: pop (1,3) area=1, add (2,3)
                             pop (2,3) area=2, add (3,3), (2,2)
                             pop (3,3) area=3
                             pop (2,2) area=4, add (2,1)
                             pop (2,1) area=5
                             flood done: best = max(2, 5) = 5
            scan (2,1) already 0 -> skip: the flood reached it before the
                scan did, so no third island
            -> return 5
            All water -> no flood ever starts -> 0.
            Single 1 -> one pop -> 1.

        E — EVALUATE
            Time  O(rows * cols): each cell scanned once, popped at most
                once, checked by at most 4 neighbors.
            Space O(rows * cols) worst case for the queue; the grid itself
                records what's been sunk.
            Follow-ups:
                Can't modify grid -> visited set of (r, c), same time,
                    O(rows*cols) extra space.
                Recursive DFS -> return 1 + sum of the 4 neighbor calls;
                    clean, but 2,500 deep on an all-land grid.
                Return the island's cells -> append (cr, cc) on each pop
                    instead of incrementing, keep the best list.
                Flip one 0 to 1 for the biggest island -> LC 827: label
                    each island with an id and size, then sum distinct
                    neighbor ids around each water cell.
            Same flood skeleton: LC 200, 463, 1254, 994.
        """
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))   # down, up, right, left
        rows, cols = len(grid), len(grid[0])
        best = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:              # number, not "1"
                    grid[r][c] = 0               # sink before enqueueing
                    queue = deque([(r, c)])
                    area = 0                     # fresh count for this island

                    while queue:
                        cr, cc = queue.popleft()
                        area += 1                # each cell popped (and counted) once
                        for dr, dc in directions:
                            nr, nc = cr + dr, cc + dc
                            # bounds first, so the grid is never read off the edge
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                                grid[nr][nc] = 0           # claim it now
                                queue.append((nr, nc))     # count it when popped

                    best = max(best, area)       # flood done: area is final

        return best