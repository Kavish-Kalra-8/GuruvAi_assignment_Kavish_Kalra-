class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None


class LRUCache:
  
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
