import heapq
class Heap(object):
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """

    def __init__(self):
        """ create a new min-heap. """
        self._heap = []

    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        assert priority >= 0
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap)[1] # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        """ Get all elements ordered by asc. priority. """
        return self

    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration


h = Heap()
# add some nonsense:
h.push(10, "I'm a large one")
h.push(20, "Actually I'm larger")
h.push(5, "size is not everything")
h.push(0, "which size?")

# get it out in a cool way:
for item in h:
   print item

while len(h):
	data = h.pop()
	print(data)

# prints:
# which size?
# size is not everything
# I'm a large one
# Actually I'm larger

print h
