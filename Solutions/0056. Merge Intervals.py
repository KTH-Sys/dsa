class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        U — UNDERSTAND
            Given ranges [start, end], combine every group that overlaps and
            return the combined ranges (any order).
            [[1,3], [2,6], [8,10], [15,18]] -> [[1,6], [8,10], [15,18]]
            Q: do touching ranges merge? Yes: [1,4] + [4,5] -> [1,5].
            Q: is the input sorted? No -- overlapping ranges can be anywhere.
            Q: single-point ranges like [3,3]? Allowed.
            Q: may I modify the input? Ask. This version sorts it in place.
            Q: size? Up to 10^4 ranges.

        M — MATCH
            Attempt 1: merge neighbors in input order -> fails on
                [[1,3], [8,10], [2,6]]: [1,3] and [2,6] overlap but aren't
                next to each other.
            Attempt 2: compare every pair, merge, repeat until nothing
                changes -> O(n^2) per pass, and merges can create new
                overlaps, so many passes.
            Notice: after sorting by start, a range can only overlap the
                block currently being built. Everything earlier already
                ended before that block began.
            Greedy sweep: each range either extends the current block or
                starts a new one. A closed block is never reopened, which
                is safe because every later range starts even further right.
            Plain intervals.sort() works: lists compare by first item
                (start), then second (end). No lambda needed.

        P — PLAN
            1. Sort by start.
            2. merged = [first range]
            3. For each remaining [start, end]:
                 last = merged[-1]
                 if start <= last end -> last end = max(last end, end)
                 else                 -> append [start, end] as a new block
            4. Return merged.
            <= (not <) so touching ranges merge.
            max (not just end) so a range inside the block can't shrink it.
            last = merged[-1] is the SAME list as the one inside merged, so
                last[1] = ... updates merged directly.

        I — IMPLEMENT
            (below)

        R — REVIEW
            [[8,10], [1,3], [2,6], [15,18], [6,7], [2,4], [9,9]]
            sorted: [1,3] [2,4] [2,6] [6,7] [8,10] [9,9] [15,18]
            [1,3]                  first block           [[1,3]]
            [2,4]   2 <= 3   stretch to max(3,4)=4       [[1,4]]
            [2,6]   2 <= 4   stretch to 6                [[1,6]]
            [6,7]   6 <= 6   touching, stretch to 7      [[1,7]]
            [8,10]  8 >  7   new block                   [[1,7], [8,10]]
            [9,9]   9 <= 10  inside: max(10,9)=10        [[1,7], [8,10]]
            [15,18] 15 > 10  new block          [[1,7], [8,10], [15,18]]
            [[1,10], [2,3]] -> [[1,10]]   (max matters)
            [[1,4], [4,5]]  -> [[1,5]]    (<= matters)
            [[5,7]]         -> [[5,7]]    (loop never runs)

        E — EVALUATE
            Time  O(n log n): the sort dominates; the sweep is O(n).
            Space O(n) for merged (plus the sort's own memory).
            Optimal: merging single-point ranges [x,x] answers "are there
                duplicates?", which needs O(n log n) comparisons, so no
                comparison-based method can beat O(n log n).
            Follow-ups:
                Don't modify input -> intervals = sorted(intervals) and
                    start with merged = [intervals[0][:]] (a copy).
                Counting version: +1 at each start, -1 at each end, sweep
                    sorted points; a block closes when the count hits 0.
                    Same O(n log n); the running count also answers "most
                    overlapping at once" (LC 253 Meeting Rooms II).
                One new range into an already-merged list -> LC 57 Insert
                    Interval, O(n) with no re-sort.
            Same "sort, then sweep" pattern: LC 57, 435, 252, 253.
        """
        intervals.sort()                          # by start (ties broken by end)
        merged = [intervals[0]]                   # first block

        for start, end in intervals[1:]:
            last = merged[-1]                     # the block being built
            if start <= last[1]:                  # overlaps or touches
                last[1] = max(last[1], end)       # stretch the end
            else:                                 # gap
                merged.append([start, end])       # start a new block

        return merged
    