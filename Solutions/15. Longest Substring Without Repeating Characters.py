from typing import Set

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        U — Understand
        ----------------
        Given a string s, find the length of the longest substring
        that contains no repeating characters.
        The substring must be contiguous.

        M — Match
        ----------------
        Pattern: Sliding Window (variable size)
        Reason:
        - We need a contiguous window
        - Window expands with a right pointer
        - When a duplicate appears, shrink from the left
        - Track the maximum valid window length

        P — Plan
        ----------------
        1) Use a set to track characters currently in the window
        2) Initialize two pointers:
           - left: start of the window
           - right: end of the window (loop variable)
        3) Expand the window by moving right
        4) If s[right] is already in the set:
           - Shrink the window from the left until duplicate is removed
        5) After each valid window, update the maximum length
        6) Return the maximum length found

        I — Implement
        ----------------
        """

        # Set to store unique characters in the current window
        charSet: Set[str] = set()

        # Left pointer of the sliding window
        left = 0

        # Result to track maximum window size
        res = 0

        # Right pointer expands the window
        for right in range(len(s)):
            # If current character causes a duplicate,
            # shrink the window from the left
            while s[right] in charSet:
                charSet.remove(s[left])
                left += 1

            # Add the current character to the window
            charSet.add(s[right])

            # Update maximum length (both pointers inclusive)
            res = max(res, right - left + 1)

        # E — Evaluate
        # ----------------
        # Time Complexity: O(n)
        #   - Each character is added to and removed from the set at most once
        # Space Complexity: O(m)
        #   - m = number of unique characters in the string

        # R — Review
        # ----------------
        # The sliding window always maintains a valid substring
        # with no duplicates. By only moving pointers forward,
        # we achieve linear time complexity.

        return res
