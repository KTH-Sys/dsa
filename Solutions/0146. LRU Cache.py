class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    """
    U — Understand
    ----------------
    Design a fixed-capacity key-value cache with O(1) get and put. On
    put, if capacity is exceeded, evict the LEAST RECENTLY USED key
    (the one that hasn't been touched by get/put for the longest time).

    M — Match
    ----------------
    Pattern: Hashmap + Doubly Linked List. Hashmap gives O(1) lookup of
    WHERE a key's node lives; doubly linked list gives O(1) removal and
    re-insertion of that node anywhere, using DIRECT references instead
    of scanning. Two dummy sentinel nodes (left=LRU end, right=MRU end)
    eliminate edge-case handling for empty lists or boundary nodes.

    P — Plan
    ----------------
    1) Maintain: a dict (key -> Node), and a doubly linked list bounded
       by two dummy sentinels — left (just before the LRU end) and
       right (just after the MRU end). List order: LRU ... MRU,
       left-to-right.
    2) remove(node): unlink node from wherever it currently sits, O(1)
       given a direct reference.
    3) insert(node): always insert immediately before `right` (the MRU
       end) — the most-recently-touched position.
    4) get(key): if key exists, remove+reinsert its node (refreshing it
       to MRU), return its value. Else return -1.
    5) put(key, value): if key exists, remove its old node first. Create
       a new node, insert it (at MRU). If over capacity, evict the node
       at left.next (the true LRU end) and delete it from the dict too.
    """
    # I — Implement
    # ---------------
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}   # the dictionary: key -> its box

        # The two fake "bookend" boxes
        self.left, self.right = Node(0, 0), Node(0, 0)
        # Start with them pointing at each other (empty chain between them)
        self.left.next = self.right
        self.right.prev = self.left

    def remove(self, node):
        # Yank a box out: make its two neighbors point at each other
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def insert(self, node):
        # Add a box right before `right` (the most-recently-used end)
        prev, nxt = self.right.prev, self.right
        prev.next = node
        nxt.prev = node
        node.prev = prev
        node.next = nxt

    def get(self, key: int) -> int:
        if key in self.cache:
            # It exists! Move it to the "just used" end, then return its value
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1   # not found

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Already there — remove the old box so we can replace it
            self.remove(self.cache[key])
        # Make a fresh box and add it at the "just used" end
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        if len(self.cache) > self.cap:
            # Too full! Kick out the least recently used (right next to `left`)
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

    # R — Review
    # ----------------
    # Correctness reasoning:
    # - The list is always ordered LRU (near left) -> MRU (near right),
    #   because EVERY touch (get or put) removes-then-reinserts a node
    #   at the MRU end, and eviction always targets left.next — the
    #   node furthest from any recent touch.
    # - The hashmap always mirrors exactly what's in the linked list,
    #   since every insert/remove of a node is paired with a
    #   cache[key]=... or del cache[key] at the same moment.
    # - Dummy sentinels mean remove/insert never need to check "is this
    #   the first/last real node" — there's always a real Node object
    #   (even if a dummy) on both sides to rewire against.

    # E — Evaluate
    # ----------------
    # Time:  O(1) for get and put — hashmap lookup is O(1), and
    #        linked-list remove/insert are O(1) given a direct node
    #        reference (no scanning required)
    # Space: O(capacity) — one node and one hashmap entry per cached key