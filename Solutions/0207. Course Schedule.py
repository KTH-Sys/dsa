from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        U — UNDERSTAND
            Courses are numbered 0 to numCourses - 1.
            Each pair [a, b] means: to take a, you must FIRST take b.
            So the arrow goes b -> a (prerequisite -> course it unlocks).
            Return True if every course can be taken, False otherwise.
            Q: when is it impossible? Only when courses wait on each other
               in a loop (A needs B, B needs A), so none can go first.
            Q: no prerequisites at all? Every course is free -> True.
            Q: a course requiring itself, [0, 0]? A one-course loop -> False.
            Q: size? Up to 2,000 courses and 5,000 pairs.

        M — MATCH
            Attempt 1: look for reversed pairs ([a,b] and [b,a]) -> misses
                longer loops like 0 -> 1 -> 2 -> 0, where no pair is reversed.
            Attempt 2: try every ordering of courses -> n! orderings.
                10 courses is already 3.6 million.
            Fix: do what a student would. Keep taking any course whose
                prerequisites are all done. Finishing a course frees up the
                courses that needed it. (Kahn's algorithm / topological sort.)
            Two records:
                unlocks[x] = courses waiting on x (who to update when x is done)
                locks[x]   = how many of x's prerequisites aren't done yet
                             (the standard name is "indegree")
            Plus a queue of courses that are ready (0 locks) but not taken.
            Why this catches loops: a course in a loop always has a lock held
                by another course in the same loop, so it never reaches 0,
                never enters the queue, and is never counted.

        P — PLAN
            1. Build unlocks and locks from the pairs:
               for [course, prereq]: unlocks[prereq] gets course,
               locks[course] += 1
            2. Queue every course with 0 locks.
            3. While the queue isn't empty:
                 take the front course, taken += 1
                 for each course it unlocks: locks -= 1
                 if that course just reached 0 locks, queue it
            4. Return taken == numCourses.
            locks is a COUNT, not yes/no: a course with two prerequisites
               must wait for both before it's ready.

        I — IMPLEMENT
            (below)

        R — REVIEW
            numCourses = 4, [[1,0], [2,0], [3,1], [3,2]]
                  +-> 1 -+
                0-+      +-> 3
                  +-> 2 -+
            build:  unlocks = {0: [1, 2], 1: [3], 2: [3]}
                    locks   = [0, 1, 1, 2]
            start:  queue = [0]
            take 0: locks [0, 0, 0, 2]   1 and 2 ready   queue [1, 2]
            take 1: locks [0, 0, 0, 1]   3 still needs 2 queue [2]
            take 2: locks [0, 0, 0, 0]   3 ready         queue [3]
            take 3: nothing waits on 3                   queue []
            taken = 4 == 4 -> True

            numCourses = 4, [[1,0], [2,1], [3,2], [1,3]]   (1 -> 2 -> 3 -> 1)
            locks = [0, 2, 1, 1], queue = [0]
            take 0: locks [0, 1, 1, 1]   1 still needs 3 queue []
            taken = 1 != 4 -> False (1, 2, 3 stuck in a loop)

            [[1,0], [0,1]] -> locks [1, 1], queue starts empty -> 0 != 2 -> False
            [] -> every course free -> True
            [[0,0]] -> locks [1], never freed -> False

        E — EVALUATE
            Time  O(V + E), V = courses, E = pairs: each pair is read once
                to build, each course is queued at most once, and each
                unlocks entry is processed once.
            Space O(V + E): unlocks holds E entries; locks and the queue
                hold up to V.
            Follow-ups:
                Return a valid order (LC 210) -> append cur to a list each
                    time it's taken; return it if its length is
                    numCourses, otherwise [].
                DFS instead? Mark each course unvisited / in progress /
                    done; reaching an "in progress" course means a loop.
                    Same complexity; Kahn's gives the order for free.
            Same pattern: LC 210, 269 Alien Dictionary, 310, 1136.
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

        taken = 0
        while queue:
            cur = queue.popleft()
            taken += 1
            for nxt in unlocks[cur]:
                locks[nxt] -= 1              # one prerequisite of nxt is done
                if locks[nxt] == 0:          # its last lock just came off
                    queue.append(nxt)

        return taken == numCourses           # anything not taken was stuck in a loop