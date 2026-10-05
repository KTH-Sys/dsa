from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        U — UNDERSTAND
            grid holds the NUMBERS 0 (empty), 1 (fresh), 2 (rotten).
            Each minute, every fresh orange touching a rotten one
            (up/down/left/right) rots -- all at the same time.
            Return minutes until no fresh orange remains, or -1 if some
            fresh orange can never rot.
            Q: no fresh at the start? Return 0.
            Q: fresh but no rotten? Nothing can ever spread -> -1.
            Q: empty cells (0) block the spread? Yes -- rot only moves
               orange to orange.
            Q: size? Up to 10 x 10, but aim for O(rows * cols) anyway.

        M — MATCH
            Attempt 1: each minute, scan the grid and rot in place.
                [2,1,1] -> (0,1) rots, then (0,2) sees it and rots in the
                SAME scan -> returns 1, true answer 2. An orange that rots
                this minute must not spread until next minute.
            Attempt 1b: collect changes, apply at the end of each minute
                -> correct, but rescans the whole grid every minute:
                O((rows*cols)^2) when the rot snakes one orange per minute.
            Notice: only the oranges that JUST rotted can spread next
                minute. Everything older is done spreading.
            Fix: multi-source BFS. All rotten oranges start in the queue
                together (every fire starts at once), and the queue is
                processed one ROUND per minute.
            Why all sources at once: [2,1,1,1,2] -> both ends spread
                together -> 2 minutes. One source alone would give 4.

        P — PLAN
            1. One setup pass: queue every rotten orange, count fresh.
            2. While the queue isn't empty AND fresh > 0:
                 for _ in range(len(queue)):   <- measured ONCE per minute
                     pop an orange; for each of the 4 moves:
                     if on the grid and fresh -> rot it, fresh -= 1,
                     queue it (it spreads NEXT minute)
                 minutes += 1
            3. Return minutes if fresh == 0, else -1.
            range(len(queue)) is evaluated once at the start of the round,
               so oranges appended mid-round wait for the next round.
            `fresh > 0` in the loop condition: the last orange to rot is
               still in the queue. Without this check, one extra empty
               round runs and minutes is off by one.
            Rot (set to 2) on ADD, same as sinking in Islands -- it's the
               visited mark, so no orange is queued twice.

        I — IMPLEMENT
            (below)

        R — REVIEW
            2 1 1      fresh = 6, queue = [(0,0)]
            1 1 0
            0 1 1
            min 1: pop (0,0)        rots (1,0),(0,1)   fresh 4
            min 2: pop (1,0)        rots (1,1)         fresh 3
                   pop (0,1)        rots (0,2)         fresh 2
                   ((1,1) rotted this minute but waits in the queue --
                    exactly the Attempt 1 bug, fixed)
            min 3: pop (1,1)        rots (2,1)         fresh 1
                   pop (0,2)        rots nothing
            min 4: pop (2,1)        rots (2,2)         fresh 0
            loop check: fresh == 0 -> stop ((2,2) still queued, no extra
                minute) -> return 4
            [[0,2]] -> fresh 0, loop never runs -> 0
            [[1]] -> queue empty, fresh 1 -> -1
            [[2,1,1],[0,1,1],[1,0,1]] -> bottom-left walled off -> -1
            [[2,1,1,1,2]] -> 2

        E — EVALUATE
            Time  O(rows * cols): one setup pass; each orange rotted and
                queued at most once, checked by at most 4 neighbors.
            Space O(rows * cols) worst case for the queue.
            Follow-ups:
                Why not DFS? DFS goes deep on one path; it has no rounds,
                    so it can't tell which minute anything rotted.
                No inner loop? Queue (r, c, minute) triples and track the
                    largest minute seen.
                Can't modify grid? Visited set, same as Islands.
            Same level-by-level BFS: LC 542 01 Matrix, 1091 Shortest Path
                in Binary Matrix, 286 Walls and Gates, 752 Open the Lock.
        """
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))   # down, up, right, left
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0

        for r in range(rows):                    # setup: every fire starts now
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0
        while queue and fresh > 0:
            for _ in range(len(queue)):          # exactly this minute's frontier
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # bounds first, so the grid is never read off the edge
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2         # rot now: marks it visited
                        fresh -= 1
                        queue.append((nr, nc))   # spreads next minute
            minutes += 1

        return minutes if fresh == 0 else -1