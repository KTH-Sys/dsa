class Solution:
    def maxChunksToSorted(self, arr: List[int]) -> int:
        """
        U — UNDERSTAND
            Cut arr into chunks, sort each chunk, concatenate -> must equal
            sorted(arr). Return the max number of chunks.
            LC 769 guarantees arr is a permutation of 0..n-1, but this solution
            does NOT use that guarantee -- see M.
            Q: empty input? No, 1 <= n. n=1 returns 1 (one chunk, the whole array).
            Q: duplicates? Not in 769; this code handles them anyway.

        M — MATCH
            Seam invariant, same as LC 915 and the Split-and-Sort OA problem:
                a cut after index i is legal  iff  max(arr[0:i+1]) <= min(arr[i+1:])
            Prefix-aggregate / suffix-aggregate sweep. This is the GENERAL form.
            The permutation-only shortcut (prefix_max == i, O(1) space) is faster
            but dies the moment duplicates appear; this version survives that,
            so it solves LC 768 unchanged.

        P — PLAN
            1. rightMin[i] = min(arr[i:]), built right-to-left in one pass.
            2. Sweep left-to-right carrying leftMax = max(arr[0:i+1]).
            3. Count every i in [0, n-2] where leftMax <= rightMin[i+1].
            4. Start chunks at 1: those n-1 positions are the OPTIONAL internal
               cuts; the boundary at the end of the array is mandatory and is
               never visited by the loop. This is exactly why the chunk count
               equals the Split-and-Sort boundary count plus one.

        I — IMPLEMENT
            (below)

        R — REVIEW
            [1,0,2,3,4] -> rightMin = [0,0,2,3,4]
                i=0 leftMax=1, rightMin[1]=0  1<=0 no
                i=1 leftMax=1, rightMin[2]=2  1<=2 YES -> 2
                i=2 leftMax=2, rightMin[3]=3  YES -> 3
                i=3 leftMax=3, rightMin[4]=4  YES -> 4   => [1,0][2][3][4]
            [4,3,2,1,0] -> leftMax=4 always, rightMin[i+1] always < 4 -> 1.
            [0] -> both loops empty, returns 1.
            Trap: checking only arr[i] <= arr[i+1] is wrong -- [3,1,2,5] at i=1
            passes adjacency (1<=2) but max(left)=3 > min(right)=2.

        E — EVALUATE
            Time  O(n): two independent linear passes.
            Space O(n): the rightMin array.
            Trade-off vs the permutation shortcut: that one is O(1) space but
            only valid when values are exactly {0..n-1}. This one costs O(n)
            space and buys generality -- paste it into LC 768 and it passes.
        """
        n = len(arr)
        rightMin = [0] * n
        rightMin[-1] = arr[-1]

        for i in range(n - 2, -1, -1):
            rightMin[i] = min(arr[i], rightMin[i + 1])

        chunks = 1              # the mandatory boundary at the end of the array
        leftMax = arr[0]

        for i in range(n - 1):  # i = each optional internal cut point
            leftMax = max(leftMax, arr[i])

            if leftMax <= rightMin[i + 1]:
                chunks += 1

        return chunks