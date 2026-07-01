class Solution:
    def encode(self, strs: list[str]) -> str:
        """
        U — Understand
        ----------------
        Combine a list of strings into one string such that decode() can
        perfectly recover the original list — even if individual strings
        contain commas, spaces, colons, or any other character.
        The tricky part: any delimiter we pick (",", "#", etc.) might also
        appear INSIDE one of the strings, so a naive split() would corrupt data.

        M — Match
        ----------------
        Pattern: String encoding via length-prefixing (like HTTP chunked
        transfer or network protocols). Instead of using a delimiter character
        that could collide with string content, prefix each string with its
        own length, plus a delimiter that only separates the length from the
        string body — never appears inside the length itself (digits only).

        P — Plan
        ----------------
        1) For each string, compute its length.
        2) Write it as "{length}#{string}" — the '#' marks where the length
           number ends and the actual string content begins.
        3) Concatenate all these chunks back to back with no extra separator
           needed between chunks, since each chunk is self-describing.
        """
        # I — Implement
        # ----------------
        encoded = []
        for s in strs:
            # length + delimiter + raw string, e.g. "5#hello"
            encoded.append(str(len(s)) + "#" + s)
        return "".join(encoded)

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - The delimiter '#' could theoretically appear inside a string too,
        #   but that's fine: decode() doesn't search for '#' to find the end
        #   of the string body — it only uses '#' to mark where the LENGTH
        #   ends. Once decode() knows the length, it reads exactly that many
        #   characters, regardless of what's inside them (including more '#'s).
        # - This is why length-prefixing is collision-proof: the delimiter
        #   only needs to be unambiguous against DIGIT characters, not against
        #   the string body itself.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  where n = total characters across all strings
        # Space: O(n)  for the resulting encoded string


    def decode(self, s: str) -> list[str]:
        """
        U — Understand
        ----------------
        Reverse the encode() process: given the single combined string,
        recover the original list of strings in order.

        M — Match
        ----------------
        Pattern: Two-pointer scanning. Walk through s, reading a length
        prefix up to '#', then jump forward exactly that many characters
        to extract the next string, then repeat from there.

        P — Plan
        ----------------
        1) Use a pointer i starting at 0 to track our read position in s.
        2) From i, scan forward until '#' to read the length prefix.
        3) Convert that length substring to an int.
        4) The actual string starts right after '#' and runs for `length`
           characters — slice it out.
        5) Move i past this entire chunk (length prefix + '#' + string body)
           to start reading the next chunk.
        6) Repeat until i reaches the end of s.
        """
        # I — Implement
        # ----------------
        res = []
        i = 0

        while i < len(s):
            # Step 1: find where the length prefix ends ('#')
            j = i
            while s[j] != "#":
                j += 1

            # Step 2: parse the length number, e.g. "5" -> 5
            length = int(s[i:j])

            # Step 3: the string body starts right after '#'
            start = j + 1
            end = start + length

            # Step 4: extract exactly `length` characters
            res.append(s[start:end])

            # Step 5: move i to the start of the next chunk
            i = end

        return res

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - We never guess where a string ends by searching for a delimiter
        #   inside the body — we KNOW exactly how many characters to read,
        #   because the length was given to us up front. This is what makes
        #   it safe for strings to contain '#', digits, or anything else.
        # - i always advances past a fully-consumed chunk, so the loop
        #   terminates and never re-reads the same chunk twice.

        # E — Evaluate
        # ----------------
        # Time:  O(n)  single pass through s, n = len(s)
        # Space: O(n)  for the result list and extracted substrings