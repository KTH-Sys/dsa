from collections import defaultdict

class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        """
        U — Understand
        ----------------
        Determine whether a 9x9 Sudoku board is valid SO FAR (doesn't need
        to be solvable or fully filled — just check the rules aren't broken
        for whatever digits are already placed).
        Rules to check, for digits 1-9 only ('.' means empty, ignore it):
        1) Each ROW must not contain the same digit twice.
        2) Each COLUMN must not contain the same digit twice.
        3) Each of the nine 3x3 sub-BOXES must not contain the same digit twice.

        M — Match
        ----------------
        Pattern: Arrays & Hashing (duplicate detection via sets), applied
        to three overlapping groupings simultaneously: rows, columns, boxes.
        Tool: One hash set per row, one per column, one per 3x3 box —
        tracked via defaultdict(set) keyed by row index / col index / box index.
        Key insight: a cell at (r, c) belongs to exactly one row group r,
        one column group c, and one box group determined by (r//3, c//3).

        P — Plan
        ----------------
        1) Create three defaultdicts of sets: rows, cols, boxes.
        2) Scan every cell (r, c) on the board.
        3) Skip '.' (empty cells don't violate anything).
        4) Compute this cell's box id as (r // 3, c // 3) — integer division
           groups every 3 consecutive rows/cols into the same box bucket.
        5) If the digit is already in rows[r], cols[c], or boxes[(r//3,c//3)],
           it's a duplicate within that group -> return False immediately.
        6) Otherwise, add the digit to all three relevant sets and continue.
        7) If the scan completes with no duplicates found, return True.
        """
        # I — Implement
        # ----------------
        rows = defaultdict(set)   # rows[r] = set of digits seen in row r
        cols = defaultdict(set)   # cols[c] = set of digits seen in column c
        boxes = defaultdict(set)  # boxes[(r//3, c//3)] = set of digits seen in that box

        for r in range(9):
            for c in range(9):
                val = board[r][c]

                # Empty cells impose no constraint — skip them
                if val == ".":
                    continue

                # Identify which 3x3 box this cell belongs to
                box_id = (r // 3, c // 3)

                # Check all three groups this cell participates in
                if (val in rows[r] or
                    val in cols[c] or
                    val in boxes[box_id]):
                    return False

                # No conflict — record this digit in all three groups
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_id].add(val)

        return True

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - Every cell belongs to exactly one row, one column, and one box,
        #   so checking membership in all three sets before adding covers
        #   every rule the problem requires, with no group ever double-counted
        #   incorrectly.
        # - box_id = (r//3, c//3) correctly groups rows 0-2 -> 0, rows 3-5 -> 1,
        #   rows 6-8 -> 2 (same for columns), which exactly matches how a
        #   9x9 board partitions into nine 3x3 sub-grids.
        # - Checking BEFORE adding guarantees we catch the duplicate the
        #   moment a SECOND occurrence appears, rather than after the fact.
        # - defaultdict(set) means we never need to pre-initialize 9 empty
        #   sets manually — accessing rows[r] for a never-seen r auto-creates
        #   an empty set.

        # E — Evaluate
        # ----------------
        # Time:  O(1)  — board is always exactly 9x9 = 81 cells, so the
        #        double loop is a fixed 81 iterations, not dependent on
        #        variable input size. (Often described as O(n^2) where n=9,
        #        but since n is fixed, it's constant time/space in practice.)
        # Space: O(1)  — at most 9 rows * 9 digits + 9 cols * 9 digits +
        #        9 boxes * 9 digits, all bounded by the fixed board size.