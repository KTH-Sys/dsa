class Solution:
    def isValid(self, s: str) -> bool:

        # U — Understand
        # Input: a string containing only the bracket characters:
        #        '(', ')', '{', '}', '[' and ']'
        # Output: True if the parentheses are valid, otherwise False
        #
        # Valid means:
        # 1. Every opening bracket has a matching closing bracket
        # 2. Brackets close in the correct order
        #
        # Example:
        # s = "{[]}"  -> True
        # s = "([)]"  -> False


        # M — Match Pattern
        # This is a Stack problem.
        # Why?
        # Because the most recent opening bracket must be matched first.
        # That is exactly LIFO:
        # Last In, First Out.


        # P — Plan
        # 1. Create an empty stack
        # 2. Create a mapping from closing bracket -> matching opening bracket
        # 3. Traverse the string one character at a time
        # 4. If the character is a closing bracket:
        #       - check whether the stack is empty
        #       - check whether the top of stack matches its opening bracket
        #       - if not, return False
        #       - otherwise pop the stack
        # 5. If the character is an opening bracket:
        #       - push it onto the stack
        # 6. At the end, the stack must be empty for the string to be valid


        # I — Implement

        stack = []

        # closing bracket -> expected opening bracket
        mapping = {
            ")": "(",
            "}": "{",
            "]": "["
        }

        for char in s:

            # if current char is a closing bracket
            if char in mapping:

                # invalid if:
                # 1. stack is empty, so nothing to match with
                # 2. top of stack is not the expected opening bracket
                if not stack or stack[-1] != mapping[char]:
                    return False

                # valid match, remove opening bracket from stack
                stack.pop()

            else:
                # opening bracket, push onto stack
                stack.append(char)


        # R — Review
        # If stack is empty, every opening bracket found a valid match.
        # If stack is not empty, some opening brackets were never closed.


        # E — Evaluate
        # Time Complexity: O(n)
        #   We traverse the string once.
        #
        # Space Complexity: O(n)
        #   In the worst case, all characters are opening brackets
        #   and all get stored in the stack.

        return len(stack) == 0