class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        """
        U — Understand
        ----------------
        For each index i, compute the product of every element in nums
        EXCEPT nums[i] itself. Return these as a new array.
        Constraint: must run in O(n) time, and CANNOT use division
        (otherwise dividing the total product by nums[i] would be trivial,
        but breaks if any element is 0).

        M — Match
        ----------------
        Pattern: Prefix / Suffix products (Arrays & Hashing-adjacent technique).
        Key insight: result[i] = (product of everything to the LEFT of i)
                                * (product of everything to the RIGHT of i)
        Tool: Two passes over the array — one accumulating a running prefix
        product left-to-right, one accumulating a running suffix product
        right-to-left — combined into a single output array.

        P — Plan
        ----------------
        1) Create result array of same length as nums, initialized to 1s.
        2) First pass (left to right): for each i, store the running
           product of all elements BEFORE i into result[i]. Update the
           running prefix product as you go.
        3) Second pass (right to left): for each i, multiply result[i]
           by the running product of all elements AFTER i. Update the
           running suffix product as you go.
        4) Return result — no division ever needed.
        """
        # I — Implement
        # ----------------
        n = len(nums)
        result = [1] * n

        # Pass 1: left-to-right prefix products
        # ----------------
        prefix = 1
        for i in range(n):
            # Before overwriting, result[i] gets everything multiplied so far
            # (i.e., product of nums[0..i-1])
            result[i] = prefix
            # Update running prefix to include nums[i] for the NEXT iteration
            prefix *= nums[i]

        # Pass 2: right-to-left suffix products
        # ----------------
        suffix = 1
        for i in range(n - 1, -1, -1):
            # Multiply in everything to the right of i
            # (i.e., product of nums[i+1..n-1])
            result[i] *= suffix
            # Update running suffix to include nums[i] for the NEXT iteration
            suffix *= nums[i]

        return result

        # R — Review
        # ----------------
        # Correctness reasoning:
        # - After pass 1, result[i] = nums[0] * nums[1] * ... * nums[i-1]
        #   (everything strictly to the left of i). result[0] stays 1 since
        #   there's nothing to its left — correct base case.
        # - After pass 2, result[i] gets multiplied by
        #   nums[i+1] * nums[i+2] * ... * nums[n-1] (everything strictly to
        #   the right). result[n-1] stays unchanged by this pass's multiply
        #   since there's nothing to its right — correct base case.
        # - Combined: result[i] = (left product) * (right product), which is
        #   exactly "product of all elements except nums[i]" — nums[i] itself
        #   is never included in either pass.
        # - No division used anywhere, so zeros in nums are handled safely
        #   (division would fail or give wrong results if nums[i] == 0).

        # E — Evaluate
        # ----------------
        # Time:  O(n)  — two single passes over nums, each O(n)
        # Space: O(1)  extra space — only prefix and suffix are scalars;
        #        result itself is the required output, not counted as
        #        "extra" auxiliary space.