from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        U — Understand
        ----------------
        Group strings that are anagrams of each other.
        Anagrams have the same characters with the same frequencies (order doesn't matter).

        M — Match
        ----------------
        Pattern: Hashing / Hash Map grouping
        Key idea: Use a "signature" for each word so all anagrams share the same key.
        Since strings are lowercase a-z, the signature can be a 26-length frequency array.

        P — Plan
        ----------------
        1) Create a hash map: key -> list of words
           - key = tuple of 26 counts (a..z)
           - value = all words with that exact frequency pattern
        2) For each word:
           - build its frequency array in O(len(word))
           - convert to tuple (hashable) and use it as the key
           - append the word into its group
        3) Return all groups (hash map values).

        I — Implement
        ----------------
        """

        # res maps: (26-count signature) -> list of anagram words
        res = defaultdict(list)

        # Process each string once
        for s in strs:
            # Build character frequency array for s (26 letters)
            count = [0] * 26

            # Count occurrences of each character in s
            for ch in s:
                # Convert character to index: 'a'->0, 'b'->1, ..., 'z'->25
                i = ord(ch) - ord('a')
                count[i] += 1

            # Convert list to tuple so it can be used as a dictionary key (immutable + hashable)
            key = tuple(count)

            # Group the original string under its signature
            res[key].append(s)

        # E — Evaluate
        # ----------------
        # Let m = number of strings, n = length of the longest string
        # Time:  O(m * n)
        #   - For each string, we scan its characters once to build counts.
        # Space (aux): O(m)
        #   - Up to m unique keys in the hash map (each key is a fixed 26-length tuple).
        # Total space including output: O(m * n)
        #   - Because we must store all strings in the grouped output.

        # R — Review
        # ----------------
        # Correctness: Two strings are anagrams iff their 26-letter frequency signatures match.
        # Using the signature as the hash key guarantees all anagrams are grouped together.

        return list(res.values())
