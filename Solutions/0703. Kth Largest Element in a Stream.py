import heapq

class KthLargest:
    """
    U — UNDERSTAND
        Numbers arrive one at a time. After each add(val), return the kth
        largest number seen so far (k counts from the top, 1-indexed).
        The constructor gets k and some starting numbers.
        Q: duplicates? Yes, they count separately. [3, 3, 3] has a 3rd
           largest of 3. (A set would get this wrong.)
        Q: fewer than k starting numbers? Allowed. LeetCode guarantees there
           are at least k numbers by the time add() returns.
        Q: add(3) means a new number 3 arrives -- not arithmetic.
        Q: size? Up to 10^4 starting numbers and 10^4 add() calls.

    M — MATCH
        Attempt 1: store everything, sort on every add -> O(n log n) per
            call, and the list grows forever.
        Attempt 2: keep a sorted list, insert in place -> finding the spot
            is fast, but inserting shifts later items: O(n) per call.
        Notice: only the top k numbers ever matter. Anything below kth place
            can never become the kth largest later, since numbers only get
            added, never removed.
        And the answer is the SMALLEST of those top k (bronze on a 3-person
            podium = 3rd place).
        Need: peek smallest, remove smallest, add -> a MIN-heap of size k.
            heap[0] is always the smallest; push and pop are O(log k).
        Why min-heap for kth LARGEST: the heap guards the border of the top
            k. Its weakest member sits in front, ready to be compared
            against and kicked out.

    P — PLAN
        __init__:
            1. self.k = k, self.heap = nums
            2. heapify (smallest to the front)
            3. pop while there are more than k numbers
        add(val):
            1. push val
            2. if the heap now has k + 1 numbers, pop the smallest
               (if val was the smallest, it's the one popped: it didn't
               make the top k)
            3. return heap[0]
        self.k and self.heap are instance attributes: created once in
            __init__, shared by every add() call on this object.

    I — IMPLEMENT
        (below)

    R — REVIEW
        k = 3, nums = [4, 5, 8, 2]
        __init__: heapify [2, 4, 8, 5], pop 2       -> heap holds 4, 5, 8
        add(3):   push [3, 4, 8, 5], pop 3 (newcomer) -> 4, 5, 8   return 4
        add(5):   push [4, 5, 8, 5], pop 4            -> 5, 5, 8   return 5
        add(10):  push [5, 5, 8, 10], pop 5           -> [5, 10, 8] return 5
                  (not sorted -- only heap[0] is guaranteed)
        add(9):   push [5, 9, 8, 10], pop 5           -> 8, 9, 10  return 8
        add(4):   push [4, 8, 10, 9], pop 4 (newcomer) -> 8, 9, 10 return 8
        output [4, 5, 5, 8, 8]  matches expected

        k = 3, nums = [1, 2, 3, 3], adds 3, 5, 6, 7, 8
        -> [3, 3, 3, 5, 6]: four 3s, and each bigger arrival pushes out
           only one at a time, so the answer stays 3 for three calls.

        pop mechanics: [4, 5, 8, 5] -> remove 4, move LAST item (5) to the
            front, sink it -> [5, 5, 8]. No left-shift (that's O(n) and can
            break the heap).

    E — EVALUATE
        __init__: O(n) heapify + up to n - k pops at O(log n) each
            -> O(n log n) worst case.
        add:      one push + at most one pop on k + 1 items -> O(log k).
        Space:    O(k). The heap never exceeds k + 1 numbers, no matter how
            many arrive.
        Follow-ups:
            Skip the wasted push/pop when the newcomer won't make it?
                Once full: if val > heap[0], heapq.heapreplace(heap, val)
                (pop + push in one step); otherwise do nothing.
            Kth SMALLEST? Max-heap of size k. Python only has min-heaps,
                so store -x and negate when reading.
            Caller still needs their original list? self.heap = list(nums),
                since heapify rearranges it in place.
        Same "keep the top k in a heap of size k" pattern: LC 215, 347,
            973, 1046.
    """

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)               # smallest goes to the front
        while len(self.heap) > k:              # keep only the top k
            heapq.heappop(self.heap)           # drop the smallest

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)         # new number joins
        if len(self.heap) > self.k:            # one too many?
            heapq.heappop(self.heap)           # kick out the smallest
        return self.heap[0]                    # smallest of top k = kth largest