class MinHeap:
    def __init__(self):
        """Initialize an empty heap."""
        self.heap = []

    def parent(self, i):
        """Return the index of the parent node."""
        return (i - 1) // 2

    def left_child(self, i):
        """Return the index of the left child."""
        return 2 * i + 1

    def right_child(self, i):
        """Return the index of the right child."""
        return 2 * i + 2

    def insert(self, key):
        """Insert a new key into the heap."""
        self.heap.append(key)  # Add new key at the end
        self._heapify_up(len(self.heap) - 1)  # Restore heap property

    def extract_min(self):
        """Remove and return the smallest element (root of the heap)."""
        if not self.heap:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()  # Only one element in heap
        
        min_value = self.heap[0]  # Root element (smallest)
        self.heap[0] = self.heap.pop()  # Move last element to root
        self._heapify_down(0)  # Restore heap property
        return min_value

    def _heapify_up(self, i):
        """Move element up to maintain heap property."""
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)  # Move up to parent

    def _heapify_down(self, i):
        """Move element down to maintain heap property."""
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)  # Recursively heapify the affected subtree

    def is_empty(self):
        """Return True if heap is empty."""
        return len(self.heap) == 0

    def __str__(self):
        """Return string representation of the heap."""
        return str(self.heap)