class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        U — Understand
        ----------------
        Check if s is a palindrome after:
        - removing non-alphanumeric characters
        - converting letters to lowercase

        M — Match
        ----------------
        Pattern: Two Pointers

        P — Plan
        ----------------
        Use left and right pointers.
        - Move left/right inward skipping non-alphanumeric characters.
        - Compare lowercase characters.
        - If mismatch -> False, else continue.
        - If pointers cross -> True.

        I — Implement
        ----------------
        """
        l, r = 0, len(s) - 1

        while l < r:
            # skip non-alphanumeric on the left
            while l < r and not s[l].isalnum():
                l += 1
            # skip non-alphanumeric on the right
            while l < r and not s[r].isalnum():
                r -= 1

            # compare normalized characters
            if s[l].lower() != s[r].lower():
                return False

            l += 1
            r -= 1
        return True

        # E — Evaluate
        # ----------------
        # Time: O(n) (each pointer moves at most n steps total)
        # Space: O(1) (no extra string built)

        # R — Review
        # ----------------
        # This avoids building a cleaned string and avoids repeated concatenation.

       
