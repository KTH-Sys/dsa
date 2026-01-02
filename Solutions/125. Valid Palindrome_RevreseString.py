class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        U — Understand
        ----------------
        We need to determine if a string is a palindrome AFTER:
        1) removing all non-alphanumeric characters, and
        2) converting letters to lowercase.
        Then check if it reads the same forward and backward.

        M — Match
        ----------------
        Pattern: Two Pointers / String Processing
        Simple approach: Build a cleaned string, then compare it to its reverse.

        P — Plan
        ----------------
        1) Create an empty string newStr.
        2) Scan each character c in s:
           - if c is alphanumeric, append lowercase(c) to newStr.
        3) Compare newStr with its reversed version.
           - If equal => palindrome => True
           - Else => False

        I — Implement
        ----------------
        """

        newStr = ""  # cleaned version of s (only lowercase letters/digits)

        # Build the cleaned string
        for c in s:
            if c.isalnum():              # keep only letters + digits
                newStr += c.lower()      # normalize to lowercase and append

        # Compare cleaned string to its reverse
        return newStr == newStr[::-1]

        # E — Evaluate
        # ----------------
        # Let n = len(s)
        # Time Complexity: O(n)
        #   - We scan the string once, and reversing the cleaned string is linear.
        # Note: In Python, repeated string concatenation (newStr += ...) can be
        #       inefficient in worst-case; using a list and ''.join(...) is safer.
        #
        # Space Complexity: O(n)
        #   - newStr stores up to n characters in the worst case.

        # R — Review
        # ----------------
        # This solution is straightforward and correct.
        # Optimization (if needed): build characters in a list, then ''.join(...)
        # to avoid repeated string concatenation overhead.
