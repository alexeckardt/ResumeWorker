
import heapq

#
#   Max Heap
#

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    # Push
    def push(self, item, score):
        # Using a negative score to turn heapq into a max-heap
        heapq.heappush(self._queue, (-score, self._index, item))
        self._index += 1

    # Pop
    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]
        raise IndexError("pop from an empty priority queue")

    # Convert to List of just items
    def to_list(self):
        # Convert the priority queue to a sorted list
        return [item for score, index, item in sorted(self._queue)]

    # Merge Together
    def merge(self, other):
        # Combine two priority queues
        for score, index, item in other._queue:
            heapq.heappush(self._queue, (score, self._index, item))
            self._index += 1

    # Get Length
    def __len__(self):
        return len(self._queue)
