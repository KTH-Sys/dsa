import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        U — UNDERSTAND
            Given an array and k, return the kth largest element in sorted
            order (k is 1-indexed from the top), NOT the kth distinct one.
            [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4 -> ranked 6, 5, 5, 4 -> 4
            Q: duplicates? Count separately. A set would give the wrong answer.
            Q: k range? 1 <= k <= len(nums), so an answer always exists.
            Q: may I modify nums? Ask. This version doesn't.
            Q: size? Up to 10^5 numbers.
            Difference from LC 703 (stream): the whole array arrives at once
                and you answer ONCE, so no class and no saved state.

        M — MATCH
            Attempt 1: sorted(nums)[-k] -> O(n log n). Correct and a fine
                first answer, but sorts everything to find one number.
            Notice: only the top k numbers matter, and the answer is the
                SMALLEST of those top k (bronze = 3rd place on the podium).
            Tool: a min-heap of size k. heap[0] is always the smallest;
                push and pop are O(log k). Same idea as LC 703's add(),
                run once per number.
            Why MIN-heap for kth LARGEST: the heap guards the border of the
                top k. Its weakest member sits in front, ready to be kicked
                out when something bigger arrives.

        P — PLAN
            1. heap = []  (empty list is already a valid heap, so no heapify)
            2. For each number: push it. If the heap now holds k + 1
               numbers, pop the smallest.
            3. Return heap[0].
            heapq.heapify(x) returns None (it rearranges in place). Never
               write heap = heapq.heapify(nums).

        I — IMPLEMENT
            (below)

        R — REVIEW
            nums = [3, 2, 1, 5, 6, 4], k = 2
            push 3 -> [3]
            push 2 -> [2, 3]
            push 1 -> [1, 3, 2]  size 3 > 2, pop 1 -> [2, 3]
            push 5 -> [2, 3, 5]  pop 2 -> [3, 5]
            push 6 -> [3, 5, 6]  pop 3 -> [5, 6]
            push 4 -> [4, 6, 5]  pop 4 (newcomer, didn't make top 2) -> [5, 6]
            return heap[0] = 5
            [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4 -> heap ends 4, 5, 5, 6 -> 4
                (both 5s kept: duplicates count)
            [7], k = 1 -> 7
            k = len(nums) -> nothing is ever popped -> the overall minimum

        E — EVALUATE
            Time  O(n log k): n pushes, up to n pops, each on <= k + 1 items.
            Space O(k): the heap never exceeds k + 1 numbers.
            Alternatives:
                sorted(nums)[-k]                      O(n log n), O(n) space
                heapq.nlargest(k, nums)[-1]           O(n log k); list is
                    largest-first, so [-1] is the kth largest
                heapify(nums), pop n - k times, nums[0]
                    O(n + (n - k) log n), no extra space, but DESTROYS the
                    input (nums ends with only k numbers)
                Quickselect: pick a random pivot, partition into bigger /
                    smaller, recurse only into the side holding position k.
                    O(n) average, O(n^2) worst; LC 215's tests include many
                    duplicates, so use a three-way partition.
            Follow-up: numbers arrive over time -> LC 703, same heap kept in
                self.heap across add() calls.
            Same "top k in a size-k heap" pattern: LC 347, 973, 703.
        """
        heap = []
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:                # one too many
                heapq.heappop(heap)          # drop the smallest
        return heap[0]                       # smallest of top k = kth largest