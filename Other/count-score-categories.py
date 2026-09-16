"""
PROBLEM: Count Score Categories - GOOGLE OA

You are given an integer array `scores`.
Classify every score into exactly one category:

    score < 50         -> Unsuccessful
    50 <= score <= 80  -> Ordinary Pass
    score > 80         -> Excellent

Return:
    [unsuccessful_count, ordinary_count, excellent_count]

Example:
    scores = [49, 50, 80, 81, 100]

    49       -> Unsuccessful
    50, 80   -> Ordinary
    81, 100  -> Excellent

    Output: [1, 2, 2]
"""


def solution(scores):

    # ============================================================
    # U — UNDERSTAND
    # ============================================================
    # We need to examine every score exactly once and count how
    # many belong to each of the three categories.
    #
    # Important boundaries:
    #   49 -> unsuccessful
    #   50 -> ordinary
    #   80 -> ordinary
    #   81 -> excellent


    # ============================================================
    # M — MATCH
    # ============================================================
    # Pattern: Linear traversal + counting/classification.
    #
    # No sorting, hashmap, prefix sum, etc. is necessary.
    # We can maintain three counters while scanning the array.
    #
    # Time:  O(n)
    # Space: O(1)


    # ============================================================
    # P — PLAN
    # ============================================================
    # 1. Initialize three counters.
    # 2. Loop through every score.
    # 3. If score < 50:
    #       increment unsuccessful.
    # 4. Else if score <= 80:
    #       increment ordinary.
    #    Since the first condition failed, score is already >= 50.
    # 5. Otherwise:
    #       increment excellent.
    # 6. Return the three counts.


    # ============================================================
    # I — IMPLEMENT
    # ============================================================

    unsuccessful = 0
    ordinary = 0
    excellent = 0

    for score in scores:

        if score < 50:
            unsuccessful += 1

        elif score <= 80:
            ordinary += 1

        else:
            excellent += 1

    result = [unsuccessful, ordinary, excellent]


    # ============================================================
    # R — REVIEW
    # ============================================================
    # Example:
    #
    # scores = [49, 50, 80, 81, 100]
    #
    # score = 49
    #   49 < 50
    #   unsuccessful = 1
    #
    # score = 50
    #   not < 50
    #   50 <= 80
    #   ordinary = 1
    #
    # score = 80
    #   not < 50
    #   80 <= 80
    #   ordinary = 2
    #
    # score = 81
    #   not < 50
    #   not <= 80
    #   excellent = 1
    #
    # score = 100
    #   excellent = 2
    #
    # result = [1, 2, 2]


    # ============================================================
    # E — EVALUATE
    # ============================================================
    # Time Complexity:
    #   O(n) — every score is examined once.
    #
    # Space Complexity:
    #   O(1) — only three counters are maintained.
    #
    # Edge cases:
    #   []             -> [0, 0, 0]
    #   [50]           -> [0, 1, 0]
    #   [80]           -> [0, 1, 0]
    #   [49]           -> [1, 0, 0]
    #   [81]           -> [0, 0, 1]

    return result