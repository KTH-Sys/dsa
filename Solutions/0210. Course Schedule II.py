from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        U — UNDERSTAND
            Courses are numbered 0 to numCourses - 1.
            Each pair [a, b] means: to take a, you must FIRST take b.
            So the arrow goes b -> a (prerequisite -> course it unlocks).
            Return ANY order that takes every course after its
            prerequisites. If that's impossible, return [].
            Q: when is it impossible? Only when courses wait on each other
               in a loop, so none of them can go first.
            Q: more than one valid order? Often. LeetCode accepts any.
               [0, 1, 2, 3] and [0, 2, 1, 3] are both valid when 1 and 2
               don't depend on each other.
            Q: no prerequisites? Any order works -> [0, 1, ..., n-1].

        M — MATCH
            This is Course Schedule I (LC 207) plus a list.
            LC 207 already takes courses in a valid order: a course is only
                taken once all its prerequisites are done. It just counted
                them (taken += 1) instead of writing them down.
            Change: order.append(cur) instead of taken += 1.
                len(order) plays the role of taken.
            Same two records as LC 207:
                unlocks[x] = courses waiting on x
                locks[x]   = how many of x's prerequisites aren't done yet
                             (standard name: "indegree")
            Plus a queue of courses that are ready but not yet taken.
            This order is a topological sort: everything appears after
                the things it depends on.

        P — PLAN
            1. Build unlocks and locks from the pairs:
               for [course, prereq]: unlocks[prereq] gets course,
               locks[course] += 1
            2. Queue every course with 0 locks.
            3. While the queue isn't empty:
                 take the front course, append it to order
                 for each course it unlocks: locks -= 1
                 if that course just reached 0 locks, queue it
            4. If order has every course, return it. Otherwise return [].
            Why the order is valid: a course enters the queue only when
               its locks hit 0, i.e. after every prerequisite was already
               appended to order.
            Why not just return order: with a loop, order is a PARTIAL
               schedule (e.g. [0]). The problem wants [] in that case.

        I — IMPLEMENT
            (below)

        R — REVIEW
            numCourses = 4, [[1,0], [2,0], [3,1], [3,2]]
                  +-> 1 -+
                0-+      +-> 3
                  +-> 2 -+
            build:  unlocks = {0: [1, 2], 1: [3], 2: [3]}
                    locks   = [0, 1, 1, 2]
            start:  queue = [0], order = []
            take 0: order [0]           locks [0, 0, 0, 2]   queue [1, 2]
            take 1: order [0, 1]        locks [0, 0, 0, 1]   queue [2]
            take 2: order [0, 1, 2]     locks [0, 0, 0, 0]   queue [3]
            take 3: order [0, 1, 2, 3]                       queue []
            len 4 == 4 -> return [0, 1, 2, 3]
            Check: 0 before 1 and 2; 1 and 2 before 3. Valid.

            numCourses = 4, [[1,0], [2,1], [3,2], [1,3]]   (1 -> 2 -> 3 -> 1)
            locks = [0, 2, 1, 1], queue = [0]
            take 0: order [0]           locks [0, 1, 1, 1]   queue []
            len 1 != 4 -> return []   (NOT the partial [0])

            [[1,0], [0,1]] -> queue starts empty, order [] -> []
            numCourses = 3, [] -> [0, 1, 2]
            numCourses = 1, [] -> [0]

        E — EVALUATE
            Time  O(V + E), V = courses, E = pairs: each pair read once,
                each course queued and appended at most once, each unlocks
                entry processed once.
            Space O(V + E): unlocks holds E entries; locks, queue, and
                order hold up to V.
            Follow-ups:
                Just True/False? That's LC 207: return
                    len(order) == numCourses.
                DFS instead? Visit a course's dependents fully, then add
                    the course; reverse the finished list at the end.
                    Track "in progress" to detect loops. Same complexity.
                Smallest-numbered course first when there's a choice?
                    Replace the deque with a min-heap (heapq).
            Same pattern: LC 207, 269 Alien Dictionary, 310, 1136.
        """
        unlocks = defaultdict(list)          # prereq -> courses waiting on it
        locks = [0] * numCourses             # unfinished prereqs per course

        for course, prereq in prerequisites: # [a, b]: b comes first
            unlocks[prereq].append(course)
            locks[course] += 1

        queue = deque()                      # courses ready to take
        for c in range(numCourses):
            if locks[c] == 0:
                queue.append(c)

        order = []                           # the schedule, built as we go
        while queue:
            cur = queue.popleft()
            order.append(cur)                # all of cur's prereqs are already in order
            for nxt in unlocks[cur]:
                locks[nxt] -= 1              # one prerequisite of nxt is done
                if locks[nxt] == 0:          # its last lock just came off
                    queue.append(nxt)

        if len(order) == numCourses:         # every course was taken
            return order
        return []                            # some courses stuck in a loop