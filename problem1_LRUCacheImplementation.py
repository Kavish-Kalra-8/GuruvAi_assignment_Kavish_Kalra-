'''
It is difficult because there are two conflicting requirements at the same time - the quick
lookup and the ability to track usage order so we know which element to evict.
Therefore, we need to have both data structures implemented. HashMap stores all the keys in
constant time and gives access to them. Any key in the cache immediately corresponds to a node 
in memory and can be found in O(1). Doubly linked list represents an order of elements (recently 
used). At any moment, the head will be pointing to the most recently used, and the tail - the least 
recently used item (will be evicted if necessary). It has to be a doubly linked list specifically
because the operation of putting an element in use involves moving the element to the top (most 
recently used position). To remove a middle element from a singly linked list, it is necessary to 
traverse it first and change the next node of the element just preceding to the deleted one (it is
O(n)). But with doubly linked list, we already know the previous element and can instantly remove
it in O(1). The HashMap and the list should always be consistent with each other - the items 
should correspond to each other and be stored in their right places. get(key) - find the key in the
HashMap and move the node to the head in the list. Return the value associated with it. Else, 
return -1. put(key, value) In case there was already such a key, we simply overwrite the value in
the existing node and move it to the head of the list (indicating that it is now most recently 
used). No new node is created and no eviction is needed since we updated the current node.
In case there is no such key and the cache is full, we evict the least recently used item by removing
the element immediately prior to the tail and deleting it from HashMap, after that we insert a new
item at the head of the list.
Two additional sentinel nodes (dummy nodes) were used - a head and a tail. They were never actually storing data but made the algorithm free of all checks whether the tail or the head were null before removing something from them. It helped to write cleaner and less complicated code. This way, both operations become truly O(1) regardless of the cache fill percentage.
'''



class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None


class LRUCache:
    """
    HashMap + Doubly Linked List approach.

    The idea is simple - HashMap gives O(1) access to any node,
    and the DLL lets us reorder/remove in O(1) since we always
    have a direct pointer to the node (no traversal needed).

    Most recent items sit near the head, LRU sits near the tail.
    Dummy head/tail just makes the insert/remove logic cleaner.
    """

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key -> Node

        self.head = Node(0, 0)  # dummy
        self.tail = Node(0, 0)  # dummy
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key].val = value
            self._remove(self.cache[key])
            self._push_front(self.cache[key])
            return

        if len(self.cache) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

        node = Node(key, value)
        self.cache[key] = node
        self._push_front(node)


'''
Data Structure Choice
The problem has two conflicting requirements at the same time — fast lookup and ordered eviction
— and no single data structure solves both. That's why I used two together.
A HashMap handles the lookup part. Every key maps directly to its corresponding node in the linked 
list, so any cache entry can be found or updated in O(1) regardless of cache size.
A Doubly Linked List handles the ordering part. The head always points to the most recently used 
item, the tail to the least recently used. When the cache is full and eviction is needed, I just 
remove the node right before the tail — no searching, no comparisons, straight O(1).
The reason it specifically needs to be a doubly linked list comes down to deletion. When a key is 
accessed, its node needs to move to the front. Removing a node from the middle of a singly linked 
list requires traversing from the head to find its predecessor, which is O(n). Since each node in 
a doubly linked list already knows its previous neighbor, removal is instant.
The HashMap and the list are always kept in sync — every entry in one exists in the other. The 
HashMap gives us the pointer, the linked list gives us the order. Neither works without the other.
I also used two dummy sentinel nodes at the head and tail that never store real data. This removes
the need for null checks when inserting or removing at the boundaries, keeping the logic clean and
uniform for every operation.
As a result, both get() and put() run in O(1) time because they only require a fixed number of 
HashMap accesses and linked list operations regardless of how full the cache is.

'''