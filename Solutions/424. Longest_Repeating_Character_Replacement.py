class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # U — Understand
        # We need the length of the longest substring that can be turned into
        # all the same character by replacing at most k characters.

        # M — Match (Pattern)
        # Sliding Window with frequency count.
        # Window is valid if: window_size - max_frequency <= k

        count = {}     # frequency of characters in current window
        res = 0        # stores the longest valid window found
        l = 0          # left pointer of sliding window
        maxf = 0       # maximum frequency of any single character in the window

        # P — Plan
        # Expand window using right pointer.
        # Track char frequencies and max frequency.
        # If window becomes invalid, shrink from the left.
        # Update result with the largest valid window length.

        for r in range(len(s)):
            # I — Implement (expand window)
            count[s[r]] = 1 + count.get(s[r], 0)
            maxf = max(maxf, count[s[r]])

            # If window invalid, shrink it
            while (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1

            # After fixing validity, update result
            res = max(res, r - l + 1)

        # R — Review
        # We examined every possible valid window once.
        # maxf may be stale, but it never breaks correctness.

        # E — Evaluate
        # Time: O(n)
        # Space: O(1) — at most 26 characters in count
        return res
