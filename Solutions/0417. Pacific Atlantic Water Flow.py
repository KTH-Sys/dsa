from collections import deque

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """
        U — UNDERSTAND
            heights is a rows x cols grid of land heights.
            Pacific touches the top row and left column.
            Atlantic touches the bottom row and right column.
            Rain flows from a cell to a neighbor (up/down/left/right) if the
            neighbor is the SAME HEIGHT OR LOWER. Edge cells pour straight
            into the ocean(s) they touch.
            Return every [r, c] whose water can reach BOTH oceans (any order).
            Q: equal heights? Water flows across flat ground, so >= not >.
            Q: corners? (0, cols-1) and (rows-1, 0) touch both oceans.
            Q: size? Up to 200 x 200 = 40,000 cells.

        M — MATCH
            Attempt 1: from every cell, BFS downhill and check whether it
                reaches a Pacific edge and an Atlantic edge. Correct, but one
                search per cell: up to 40,000 x 40,000 = 1.6 billion steps,
                mostly repeating the same paths.
            Flip it: ask "which cells can reach THIS ocean?" instead of
                "where does THIS cell's water go?" Start at the ocean and
                CLIMB: step to a neighbor only if it's >= the current height
                (water could flow from it down to here). Everything you can
                climb to drains into that ocean.
            Two searches total, one per ocean, each starting from every
                edge cell of that ocean at once (multi-source BFS, like
                Rotting Oranges). Answer = cells in both.
            Can't sink the grid to mark visited: the second search needs the
                original heights. Each search keeps its own seen set.

        P — PLAN
            1. climb(starts): BFS from all starts at once.
               Step to (nr, nc) if it's on the grid, not seen, and
               heights[nr][nc] >= heights[r][c]. Return seen.
            2. pacific_starts  = top row + left column
               atlantic_starts = bottom row + right column
            3. pacific = climb(pacific_starts)
               atlantic = climb(atlantic_starts)
            4. Return every cell in both sets.
            Corners get added to a start list twice; set(starts) drops the
               duplicate, and the duplicate pop finds nothing new.

        I — IMPLEMENT
            (below)

        R — REVIEW
            1 2 3
            2 5 2        5 is a peak in the middle
            3 2 1
            Pacific  starts: (0,0) (0,1) (0,2) (1,0) (2,0)
                pop (0,1) h2: down (1,1) h5, 5 >= 2 -> climb
                pop (0,2) h3: down (1,2) h2, 2 <  3 -> blocked
                pop (2,0) h3: right (2,1) h2, 2 < 3 -> blocked
                pop (1,1) h5: (2,1), (1,2) both 2 < 5 -> blocked
                pacific = 6 cells: top row, left column, (1,1)
            Atlantic starts: (2,0) (2,1) (2,2) (0,2) (1,2)
                pop (2,0) h3: up (1,0) h2, 2 < 3 -> blocked
                pop (2,1) h2: up (1,1) h5, 5 >= 2 -> climb
                pop (0,2) h3: left (0,1) h2, 2 < 3 -> blocked
                pop (1,1) h5: (0,1), (1,0) both 2 < 5 -> blocked
                atlantic = 6 cells: bottom row, right column, (1,1)
            both = [[0,2], [1,1], [2,0]]
                two corners touch both oceans; the peak drains to both.
            Pit [[3,3,3],[3,1,3],[3,3,3]] -> center can't flow out, and
                neither ocean can climb DOWN into it -> 8 border cells.
            Single cell [[7]] -> touches all edges -> [[0,0]].
            LC example 1 (5 x 5) -> matches expected output.

        E — EVALUATE
            Time  O(rows * cols): each search visits each cell at most once,
                checking at most 4 neighbors; the final scan is one pass.
            Space O(rows * cols): two seen sets plus the queues.
            Follow-ups:
                Why not forward search per cell? 1.6 billion steps above;
                    reversing turns many searches into two.
                Why >= not >? Flat ground lets water through. Using > breaks
                    every flat region.
                Faster than sets? Two boolean grids,
                    [[False] * cols for _ in range(rows)], same idea.
                DFS instead of BFS? Same result; recursion can go 40,000
                    deep on a 200 x 200 grid, so BFS is the safer choice.
            Same "search backward from the goal" idea: LC 130 Surrounded
                Regions (start from the border), 542 01 Matrix,
                1020 Number of Enclaves.
        """
        rows, cols = len(heights), len(heights[0])
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))   # down, up, right, left

        def climb(starts):
            seen = set(starts)                   # cells that drain to this ocean
            queue = deque(starts)                # every edge cell starts at once
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):   # uphill or level
                        seen.add((nr, nc))
                        queue.append((nr, nc))
            return seen

        pacific_starts = []
        atlantic_starts = []
        for c in range(cols):
            pacific_starts.append((0, c))                # top row
            atlantic_starts.append((rows - 1, c))        # bottom row
        for r in range(rows):
            pacific_starts.append((r, 0))                # left column
            atlantic_starts.append((r, cols - 1))        # right column

        pacific = climb(pacific_starts)
        atlantic = climb(atlantic_starts)

        result = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pacific and (r, c) in atlantic:
                    result.append([r, c])
        return result 