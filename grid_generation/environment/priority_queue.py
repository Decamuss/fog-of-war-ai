from utils.min_heap import MinHeap  # Import your custom MinHeap

class PriorityQueue:
    def __init__(self, favor_larger_g=False):
        """Priority Queue for A* with tie-breaking options using MinHeap"""
        self.heap = MinHeap()  # Use your MinHeap
        self.favor_larger_g = favor_larger_g  # Determines tie-breaking rule
        self.c = 100000  # Large constant for breaking ties

    def put(self, state, f_value, g_value):
        """Insert a state with tie-breaking based on g-value."""
        tie_breaker = -g_value if self.favor_larger_g else g_value
        priority = self.c * f_value + tie_breaker  # Custom priority calculation
        self.heap.insert((priority, state))  # Store (priority, state) in MinHeap

    def get(self):
        """Extract the state with the lowest f-value."""
        return self.heap.extract_min()[1]  # Return only the state, not priority

    def empty(self):
        """Check if the queue is empty."""
        return self.heap.is_empty()