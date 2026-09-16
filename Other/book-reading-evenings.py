"""
BOOK READING EVENINGS  -  Google OA (intern), Easy
Source: fastprep.io/problems/google-book-reading-evenings
Note: source page is Pro-gated past Example 1 -- constraints, Example 2, and
the "book not finished" behavior are NOT confirmed. Treat those as assumptions,
flagged below, and re-verify against the real OA if you see this problem.

PROBLEM
    A book has chapters that must be read in order. chapter[i] = minutes to
    finish chapter i. evening[j] = minutes available on evening j.
    Each evening, read as many consecutive unread chapters as fully fit in the
    remaining budget. A chapter can only start if it can also finish that same
    evening -- never split across evenings. Leftover time at evening's end is
    discarded.
    Return the (1-indexed) evening number on which the last chapter is
    completed.

    Example: chapter=[30,20,10], evening=[50,10] -> 2
        evening 1 (budget 50): ch0(30) + ch1(20) = 50, exact fill. ch2(10)
            can't start (0 left).
        evening 2 (budget 10): ch2(10) finishes exactly.
        Last chapter finishes on evening 2 -> return 2.
"""

class Solution:
    def solve(self, chapter: list[int], evening: list[int]) -> int:
        """
        U — UNDERSTAND
            Return WHICH evening (1-indexed) finishes the last chapter.
            Order is fixed -- no choice, no optimization, pure simulation.
            A chapter starts only if it can finish in what's LEFT of that
            evening's budget; unread chapters roll into the next evening.
            ASSUMPTION (unconfirmed, page paywalled): if evening[] runs out
            before all chapters are read, return -1. Verify against the real
            problem if you draw this on the OA -- could also want a count of
            chapters finished, or be guaranteed to always finish.
            Q: can a single evening finish 0, 1, or many chapters? All three --
               0 if the next chapter alone exceeds the budget, many if several
               small chapters fit back to back.

        M — MATCH
            Two-pointer merge over two sequences with a running budget -- not
            binary search (nothing sorted, nothing to search for) and not DP
            (no overlapping subproblems, no choice to optimize over). Same
            family as merge-step-of-merge-sort or interval-scheduling sweeps:
            one pointer into chapter[], one loop over evening[], each chapter
            index visited exactly once across the WHOLE run.

        P — PLAN
            1. i = 0                      -- next unread chapter
            2. for j, budget in enumerate(evening):
                 while i < len(chapter) and chapter[i] <= budget:
                     budget -= chapter[i]
                     i += 1
                 if i == len(chapter): return j + 1   -- finished, 1-indexed
            3. loop over all evenings ends, book unfinished -> return -1

        I — IMPLEMENT
            (below)

        R — REVIEW
            [30,20,10], [50,10]
                j=0 budget=50: 30<=50 take,budget=20,i=1; 20<=20 take,budget=0,i=2
                    10<=0? no, stop. i=2 != 3, continue.
                j=1 budget=10: 10<=10 take, budget=0, i=3. i==3==len -> return 2 ✓
            [5], [5]                       -> j=0: 5<=5 take, i=1==len -> return 1
            [5,5], [10]                    -> j=0: both fit, i=2==len -> return 1
                (multiple chapters in one evening -- covered)
            [5,5], [3]                     -> j=0: 5<=3 false immediately, i=0
                loop ends, i!=len -> return -1  (chapter too big for any evening
                given -- ASSUMPTION path, unverified)
            [] , [10]                      -> len(chapter)==0; loop body: i==0==
                len already true before evening loop even starts conceptually --
                guard this: if not chapter: return 0  (no evenings needed)
            [10,10,10], [15,15]            -> j=0: 10<=15 take,budget=5,i=1;
                10<=5? no. i=1!=3, continue.
                j=1: budget=15, 10<=15 take,budget=5,i=2; 10<=5? no. i=2!=3.
                loop ends -> return -1  (third chapter never fits with only
                two evenings of 15 each, even though 10<=15 individually --
                catches the case where per-evening leftover doesn't carry over
                except within the same evening)

        E — EVALUATE
            Time  O(n + m): the inner while loop's total iterations across
              ALL evenings sum to at most n (each chapter index advances i
              exactly once, never revisited). The outer loop is O(m).
            Space O(1): two scalars beyond the input arrays.
            No sort, no auxiliary array -- optimal, since every chapter and
            every evening must be read at least once to know the answer.
        """
        if not chapter:
            return 0

        i = 0
        n = len(chapter)

        for evening_num, budget in enumerate(evening, start=1):
            while i < n and chapter[i] <= budget:
                budget -= chapter[i]
                i += 1
            if i == n:
                return evening_num

        return -1  # ASSUMPTION: book not finished within given evenings